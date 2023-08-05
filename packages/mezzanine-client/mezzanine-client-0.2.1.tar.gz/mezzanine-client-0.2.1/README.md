# Mezzanine API Client

[![Download from PyPI](https://img.shields.io/pypi/v/mezzanine-client.svg)](https://pypi.python.org/pypi/mezzanine-client)
[![License](https://img.shields.io/pypi/l/mezzanine-client.svg)](https://pypi.python.org/pypi/mezzanine-client)
[![Join the chat](https://badges.gitter.im/gcushen/mezzanine-api.svg)](https://gitter.im/gcushen/mezzanine-api?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

A remote CLI and Python client SDK for [Mezzanine API](http://gcushen.github.io/mezzanine-api/).

It enables a user or service to remotely read or write to [Mezzanine CMS](http://mezzanine.jupo.org/) using Python or the command line. For example, you can write an article in Markdown on your laptop and type a simple command to automatically upload it and create a new blog post from it on your website.


# Installation

    $ pip install -U mezzanine-client

# Prerequisites

Install [Mezzanine API](http://gcushen.github.io/mezzanine-api/) either locally (for development) or remotely (for production), as we need an API to connect to.

Once Mezzanine API is installed,

1. Login to your Mezzanine CMS Admin Panel (e.g. [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/))
2. In the menu, click *OAuth* > *Applications*
3. Create a new application with the following details:

        App Name: Mezzanine Python Client
        App ID: id
        App Secret: secret
        Client Type: Confidential
        Grant Type: Code
        Redirect URI: https://httpbin.org/get

For development purposes, you can define the simple app ID and secret above, otherwise use the automatically generated ones.

# CLI Documentation

[CLI Documentation Website](http://gcushen.github.io/mezzanine-api/cli/)

## Configuration

Generally, you must set at least three configuration options: API URL, OAuth App ID, and OAuth App Secret. These settings correspond to the location of your Mezzanine API instance and your OAuth credentials to authenticate with it (as was discussed further in the above *Prerequisites* section).

```
$ mezzanine-cli config api_url http://127.0.0.1:8000/api
$ mezzanine-cli config client_id id
$ mezzanine-cli config client_secret secret
```

You can also see your current configuration and available options by issuing the `mezzanine-cli config` command without any arguments. Note that the `refresh_token` setting should not be altered.

## Getting started

Some examples:

```
# List all posts (most recent first).
$ mezzanine-cli posts list

# Get the post with the ID of 2.
$ mezzanine-cli posts get 2

# Create a post from a Markdown file.
$ mezzanine-cli posts create \
  --title='Test Post from API Client' \
  --content-file=~/Desktop/test.md \
  --categories='Test,Fun' \
  --markdown
```

Just add `--help` to any command in order to get help on the command line:

```
# General help.
$ mezzanine-cli

# View available options for creating posts.
$ mezzanine-cli posts create --help
```

Finally, if you wish to clear the credentials and reset CLI configuration, you can do so by running:

    $ mezzanine-cli logout

# SDK Documentation

[SDK Documentation Website](http://gcushen.github.io/mezzanine-api/client/)

Example code to display recent blog posts:

```python
from mezzanine_client import Mezzanine
api = Mezzanine( 'app_id', 'app_secret' )

# Recent posts
published_posts = api.get_posts(offset=0, limit=10)
for post in published_posts:
    print('{} (ID: {})'.format(post['title'], post['id']))
```

Further examples, such as for creating, listing, and retrieving blog posts, can be found in the [*examples*](https://github.com/gcushen/mezzanine-client-python/tree/master/examples) directory.

# Community

Join us in the [Mezzanine API chat room](https://gitter.im/gcushen/mezzanine-api?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge) or leave a message and we will try to get back to you.

Feel free to [star](https://github.com/gcushen/mezzanine-client-python/) Mezzanine Client on Github to show your support and monitor updates.

Please file a [ticket](https://github.com/gcushen/mezzanine-client-python/issues) or contribute a pull request on GitHub for bugs or feature requests.

# License

Licensed under the [ISC License](https://github.com/gcushen/mezzanine-client-python/blob/master/LICENSE).

Created by [George Cushen](https://twitter.com/GeorgeCushen).
