import attr
from .http import Client


class Puller(object):
    def prepare(self, config, state, tap_stream_id, client=None):
        self.config = config
        self.state = state
        self.tap_stream_id = tap_stream_id
        self.client = client or Client(config)
        return self

    @property
    def _bookmark(self):
        if "bookmarks" not in self.state:
            self.state["bookmarks"] = {}
        if self.tap_stream_id not in self.state["bookmarks"]:
            self.state["bookmarks"][self.tap_stream_id] = {}
        return self.state["bookmarks"][self.tap_stream_id]

    def _set_last_updated(self, key, updated_at):
        if isinstance(updated_at, datetime):
            updated_at = updated_at.isoformat()
        self._bookmark[key] = updated_at

    def _update_start_state(self, key):
        if not self._bookmark.get(key):
            self._set_last_updated(key, self.config["start_date"])
        return self._bookmark[key]


class Everything(Puller):
    def yield_pages(self):
        page = self.client.request(self.tap_stream_id)
        if page:
            yield page if type(page) == list else [page]


@attr.s
class Stream(object):
    tap_stream_id = attr.ib()
    pk_fields = attr.ib()
    puller = attr.ib()
    formatter = attr.ib(default=None)
    def format_page(self, page):
        if self.formatter:
            return self.formatter(page)
        return page


STREAMS = [
]
