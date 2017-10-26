import singer
from singer import metrics
from singer.transform import transform as tform

LOGGER = singer.get_logger()


class Stream(object):
    """Information about and functions for syncing streams.

    Important class properties:

    :var tap_stream_id:
    :var pk_fields: A list of primary key fields"""
    def __init__(self, tap_stream_id, pk_fields):
        self.tap_stream_id = tap_stream_id
        self.pk_fields = pk_fields

    def metrics(self, records):
        with metrics.record_counter(self.tap_stream_id) as counter:
            counter.increment(len(records))

    def write_records(self, records):
        singer.write_records(self.tap_stream_id, records)
        self.metrics(records)

    def transform(self, ctx, records):
        ret = []
        for record in records:
            ret.append(tform(record, ctx.schema_dicts[self.tap_stream_id]))
        return ret


all_streams = [
]
all_stream_ids = [s.tap_stream_id for s in all_streams]
