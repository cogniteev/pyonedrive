pyonedrive
==========

Onedrive REST api client

Installation
============
```
pip install pyonedrive
```

Testing pyonedrive
==================
Some tests are provided and can be run using the following command :

``` bash
[pyonedrive/tests]$ nosetests --with-coverage --cover-package=pyonedrive
--cover-html --cover-html-dir=../coverage_report --cover-branches
```

This will run a unit test suite and generate an html coverage report under
pyonedrive/coverage_report

OAuth authentication
====================

To help you going trough OAuth authentication, you can use the LiveAuth class
the following way :

``` python
from pyonedrive import LiveAuth

auth = LiveAuth({client_id}, {client_secret}, {scope}, {redirect_uri})

## For implicit grant flow redirect the user to
auth.generate_oauth_initiation_url('token')

## For authorization code flow redirect the user to
auth.generate_oauth_initiation_url('code')
```

If you choose the implicit grant flow, Live APIs will then be redirected to the
redirect_uri along with the 'token' as a url parameter.

For authorization code flow, Live APIs hits the redirect_uri with a code as an
url parameter. This code is to be exchanged for an access_token (aswell as a
refresh token if the wl.offline_access scope is asked) as follow:

``` python
response = auth.exchange_oauth_code_for_token({code})

if response.status_code == 200 or response.status_code == 201:
    ## extract tokens from response
    tokens = response.json()
    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']
```

Usage
=====

In order to use the OneDrive client, you'll need to authenticate via Oauth first
 and supply it the obtained credentials :

``` python
from pyonedrive import OneDrive

client = OneDrive(token, refresh_token, client_id, client_secret,
                  refresh_callback=handle_refresh)
```

OneDrive's API use tokens that can expires and provide a refresh process, this
 is handled automatically by this API. the optional refresh_callback parameter
 will allow you to register a function to be called upon token refresh.
Such a registered function will receive two parameters :

- the newly acquired token
- the newly acquired refresh_token

Features
========

GET :

- user's metadata
- user's profile picture
- root folder
- albums
- shared items
- folder content
- folder content (with generator)
- most recent
- usage quota
- share links (read only, read-write, embeddable)
- previews
- comments
- comments (with generator)
- tags
- tags (with generator)
- downloads

DELETE :

- delete an item by its ID
