Slack Bulk File Delete
======================

For free tier memberships, Slack has a limit of 5gb for file uploads, this
program wipes out old files.

Installation
------------

    pip3 install slack-bulkdelete

will create a new command `slack-bulkdelete`

Configuration
-------------

Create a configuration file with the Slack API token for a personal
account that has administrative privileges. (Bot accounts will not work.)

Acquire a WEB API token for the Group Manager account.
``https://api.slack.com/docs/oauth-test-tokens``

The API token is of the form `xoxp-nnnnnnnnnn-nnnnnnn-nnnnnnnnn-aaaaaa`.

Put the token, in quotes, in `$HOME/.slack_api_token` or the configuration
file you specify on the command line.  This file is a json format file, but
only has the one entry.

Use
---

Before letting it run for real, try using `--dry-run` to see what files
will be deleted and saved.

::

    usage: __init__.py [-h] [-C CONFIG_PATH] [-n] [-u USERS] [-a MAX_AGE]
                       [-s MIN_SIZE] [-p]

    optional arguments:
      -h, --help            show this help message and exit
      -C CONFIG_PATH, --config-path CONFIG_PATH
                            configuration info (default: ~/.slack_api_token)
      -n, --dry-run         just simulate the deletes
      -u USERS, --user USERS
                            limit delete to user
      -a MAX_AGE, --max-age MAX_AGE
                            maximum age in days (default: 30)
      -s MIN_SIZE, --min-size MIN_SIZE
                            minimum size (in kb) of file to delete (default: 200)
      -p, --pinned          include pinned files (you don't want this!)


Notes
-----

Python 3 has some issues with Unicode encoding if the ``LANG``
environment variable is not set properly before the interepreter
executes code. Make sure that ``LANG`` is set to a utf-8 encoding such
as ``C.utf-8`` or ``EN_us.utf-8``.
