#!/usr/bin/env python3
import os
import json
import singer
from singer import utils, metadata
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema


DEFAULT_BATCH_SIZE = 1000
REQUIRED_CONFIG_KEYS = ["start_date", "username", "password"]
LOGGER = singer.get_logger()


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas():
    """ Load schemas from schemas folder """
    schemas = {}
    for filename in os.listdir(get_abs_path('schemas')):
        path = get_abs_path('schemas') + '/' + filename
        file_raw = filename.replace('.json', '')
        with open(path) as file:
            schemas[file_raw] = Schema.from_dict(json.load(file))
    return schemas


def discover():
    raw_schemas = load_schemas()
    streams = []
    for schema_name, schema in raw_schemas.items():
        # TODO: populate any metadata and stream's key properties here..
        stream_metadata = []
        key_properties = []
        streams.append(
            CatalogEntry(
                tap_stream_id=schema_name,
                stream=schema_name,
                schema=schema,
                key_properties=key_properties,
                metadata=stream_metadata,
                replication_key=None,
                is_view=None,
                database=None,
                table=None,
                row_count=None,
                stream_alias=None,
                replication_method=None,
            )
        )
    return Catalog(streams)


def read_all_data():
    """ Read all rows from upstream source and return data in proper json format """
    # TODO: Replace with real logic to retrieve data
    for dummy_value in range(10000):
        yield {"id": dummy_value, "name": str(dummy_value)}


def get_row_batches(batch_size=1):
    """ Return lists of data rows according to batch_size """
    queued = []
    queued_count = 0
    for item in read_all_data():
        queued.append(item)
        queued_count += 1
        if queued_count >= batch_size:
            yield queued
            queued = []
            queued_count = 0
    if queued:
        yield queued


def sync(config, state, catalog):
    """ Sync data from tap source """
    selected_stream_ids = catalog.get_selected_streams(state)
    # Loop over streams in catalog
    for stream in catalog.streams:
        stream_id = stream.tap_stream_id
        LOGGER.info("Syncing stream:" + stream_id)

        # TODO: initialize key and bookmark columns
        key_columns = ["id"]
        bookmark_column = "id"

        singer.write_schema(
            stream_name=stream_id, schema=stream.schema, key_properties=key_columns,
        )
        for rows in get_row_batches(DEFAULT_BATCH_SIZE):
            singer.write_records(stream_id, rows)
            if bookmark_column:
                singer.write_state({stream_id: row[bookmark_column]})
    return


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover()
        sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
