# cookiecutter-singer-tap

A [cookiecutter](https://github.com/audreyr/cookiecutter) template for creating
[Singer](https://github.com/singer-io) taps.

## Usage

The best way to demonstrate creating your tap structure is with an example.
Below I will initialize the "tap-foobar" project:

```bash
$ pip install cookiecutter
```
The next command will ask for some input.  Enter the name of your tap:
```bash
$ cookiecutter https://github.com/singer-io/singer-tap-template.git
project_name [e.g. 'tap-facebook']: tap-foobar
```
For the package_name, I just hit enter since tap_foobar is what I wanted
```bash
package_name [tap_foobar]:
```
Now that the project exists, you can make a virtualenv and invoke the tap:
```bash
$ cd tap-foobar
$ python3 -m venv ~/.virtualenvs/tap-foobar
$ source ~/.virtualenvs/tap-foobar/bin/activate
...
$ pip install -e .
...
$ tap-foobar
usage: tap-foobar [-h] -c CONFIG [-s STATE] [-p PROPERTIES]
                  [--catalog CATALOG] [-d]
tap-foobar: error: the following arguments are required: -c/--config
```

Now you build the tap!

## Example Taps

These taps were built using this template:

- [tap-zendesk-chat](https://github.com/singer-io/tap-zendesk-chat)
- [tap-jira](https://github.com/singer-io/tap-jira)
