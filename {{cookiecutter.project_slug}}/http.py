import requests
from singer import metrics
import backoff

BASE_URL = ""  # FIXME


class RateLimitException(Exception):
    pass


class Client(object):
    def __init__(self, config):
        self.user_agent = config.get("user_agent")
        self.session = requests.Session()

    @backoff.on_exception(backoff.expo,
                          RateLimitException,
                          max_tries=10,
                          factor=2)
    def request(self, tap_stream_id, params={}, headers={}):
        with metrics.http_request_timer(tap_stream_id) as timer:
            url = None  # FIXME
            headers = headers.copy()
            if self.user_agent:
                headers["User-Agent"] = self.user_agent
            request = requests.Request("GET", url, headers=headers, params=params)
            response = self.session.send(request.prepare())
            timer.tags[metrics.Tag.http_status_code] = response.status_code
        # FIXME raise RateLimitException appropriately
        response.raise_for_status()
        return response.json()
