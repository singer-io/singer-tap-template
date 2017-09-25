from .http import Client
import singer
from datetime import datetime


class Context(object):
    def __init__(self, config, state, catalog):
        self.config = config
        self.state = state
        self.catalog = catalog
        self.client = Client(config)

    @property
    def bookmarks(self):
        if "bookmarks" not in self.state:
            self.state["bookmarks"] = {}
        return self.state["bookmarks"]

    def bookmark(self, path):
        bookmark = self.bookmarks
        for p in path:
            if p not in bookmark:
                bookmark[p] = {}
            bookmark = bookmark[p]
        return bookmark

    def set_bookmark(self, path, val):
        if isinstance(val, datetime):
            val = val.isoformat()
        self.bookmark(path[:-1])[path[-1]] = val

    def update_start_date_bookmark(self, path):
        val = self.bookmark(path)
        if not val:
            val = self.config["start_date"]
            self.set_bookmark(path, val)
        return val

    def write_state(self):
        singer.write_state(self.state)
