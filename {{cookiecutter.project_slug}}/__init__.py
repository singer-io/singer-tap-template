#!/usr/bin/env python3
import os
import singer
from singer import metrics, utils
import json
from .streams import STREAMS

REQUIRED_CONFIG_KEYS = ["start_date"]


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schema(tap_stream_id):
    path = "schemas/{}.json".format(tap_stream_id)
    schema = utils.load_json(get_abs_path(path))
    if "definitions" not in schema:
        schema["definitions"] = {}
    for sub_stream_id in list(schema["definitions"].keys()):
        sub_schema = load_schema(sub_stream_id)
        schema["definitions"][sub_stream_id] = sub_schema
        if "definitions" in sub_schema:
            schema["definitions"].update(sub_schema.pop("definitions"))
    return schema


def discover():
    result = {"streams": []}
    for stream in STREAMS:
        result["streams"].append(
            dict(stream=stream.tap_stream_id,
                 tap_stream_id=stream.tap_stream_id,
                 key_properties=stream.pk_fields,
                 schema=load_schema(stream.tap_stream_id))
        )
    return result


def run_stream(config, state, stream):
    state["currently_syncing"] = stream.tap_stream_id
    schema = load_schema(stream.tap_stream_id)
    singer.write_schema(stream.tap_stream_id, schema, stream.pk_fields)
    puller = stream.puller.prepare(config, state, stream.tap_stream_id)
    with metrics.record_counter(stream.tap_stream_id) as counter:
        for page in puller.yield_pages():
            counter.increment(len(page))
            page = stream.format_page(page)
            singer.write_records(stream.tap_stream_id, page)
            singer.write_state(state)
    singer.write_state(state)


def sync(config, state, catalog):
    currently_syncing = state.get("currently_syncing")
    start_idx = [e.tap_stream_id for e in STREAMS].index(currently_syncing) \
        if currently_syncing \
        else 0
    stream_ids_to_sync = [c["tap_stream_id"] for c in catalog["streams"]]
    for stream in STREAMS[start_idx:]:
        if stream.tap_stream_id not in stream_ids_to_sync:
            continue
        run_stream(config, state, stream)
    state["currently_syncing"] = None
    singer.write_state(state)


def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    if args.discover:
        print(json.dumps(discover(), indent=4))
    else:
        catalog = args.properties if args.properties else discover()
        sync(args.config, args.state, catalog)

if __name__ == "__main__":
    main()
