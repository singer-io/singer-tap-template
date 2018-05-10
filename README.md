# singer-tap-template

A [cookiecutter](https://github.com/audreyr/cookiecutter) template for creating
[Singer](https://github.com/singer-io) taps.

## Usage

The best way to demonstrate creating your tap structure is with an example.
Below I will initialize the "tap-foobar" project:

Start by installing cookiecutter:
```bash
$ pip install cookiecutter
```

The next command will ask for some input.  Enter the name of your tap:
```bash
$ cookiecutter https://github.com/singer-io/singer-tap-template.git
project_name [e.g. 'tap-facebook']: tap-foobar
```

For the package_name, I just hit enter since tap_foobar is what I wanted:
```bash
package_name [tap_foobar]:
```

Now that the project exists, make a virtual environment:
```bash
$ cd tap-foobar
$ python3 -m venv ~/.virtualenvs/tap-foobar
$ source ~/.virtualenvs/tap-foobar/bin/activate
```
Install the package:
```bash
$ pip install -e .
```

And invoke the tap in discovery mode to get the catalog:
```bash
$ tap-foobar -c sample_config.json --discover
```
The output should be a catalog with the single sample stream (from the schemas folder):
```bash
{
  "streams": [
    {
      "metadata": [],
      "schema": {
        "additionalProperties": false,
        "properties": {
          "string_field": {
            "type": [
              "null",
              "string"
            ]
          },
          "datetime_field": {
            "type": [
              "null",
              "string"
            ],
            "format": "date-time"
          },
          "double_field": {
            "type": [
              "null",
              "number"
            ]
          },
          "integer_field": {
            "type": [
              "null",
              "integer"
            ]
          }
        },
        "type": [
          "null",
          "object"
        ]
      },
      "stream": "sample_stream",
      "key_properties": [],
      "tap_stream_id": "sample_stream"
    }
  ]
}
```
If this catalog is saved to a `catalog.json` file, it can be passed back into the tap in sync mode:
```
tap-foobar -c sample_config.json --properties catalog.json
```

Now you build the tap!


Copyright &copy; 2018 Stitch
