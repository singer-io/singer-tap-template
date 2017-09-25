#!/usr/bin/env python3
import os
import singer
from singer import metrics, utils
import json
from .streams import all_streams, all_stream_ids
from .context import Context
from collections import namedtuple
from singer.catalog import Catalog

REQUIRED_CONFIG_KEYS = ["start_date"]
LOGGER = singer.get_logger()


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schema(tap_stream_id):
    path = "schemas/{}.json".format(tap_stream_id)
    schema = utils.load_json(get_abs_path(path))
    dependencies = schema.pop("tap_schema_dependencies", [])
    refs = {}
    for sub_stream_id in dependencies:
        refs[sub_stream_id] = load_schema(sub_stream_id)
    if refs:
        singer.resolve_schema_references(schema, refs)
    return schema


def discover():
    result = {"streams": []}
    for stream in all_streams:
        schema = load_schema(stream.tap_stream_id)
        schema["selected"] = True
        result["streams"].append(
            dict(stream=stream.tap_stream_id,
                 tap_stream_id=stream.tap_stream_id,
                 key_properties=stream.pk_fields,
                 schema=schema)
        )
    return Catalog.from_dict(result)


def output_schema(stream):
    schema = load_schema(stream.tap_stream_id)
    singer.write_schema(stream.tap_stream_id, schema, stream.pk_fields)


def sync(ctx):
    currently_syncing = ctx.state.get("currently_syncing")
    start_idx = all_stream_ids.index(currently_syncing) \
        if currently_syncing else 0
    streams = [s for s in all_streams[start_idx:]
               if s.tap_stream_id in
               [s.tap_stream_id for s in ctx.catalog.streams]]
    for stream in streams:
        output_schema(stream)
    for stream in streams:
        ctx.state["currently_syncing"] = stream.tap_stream_id
        ctx.write_state()
        stream.sync(ctx)
    ctx.state["currently_syncing"] = None
    ctx.write_state()


def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    if args.discover:
        discover().dump()
        print()
    else:
        catalog = Catalog.from_dict(args.properties) \
            if args.properties else discover()
        ctx = Context(args.config, args.state, catalog)
        sync(ctx)

if __name__ == "__main__":
    main()
