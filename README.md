pyonedrive
==========

Onedrive REST api client

Installation
============
```
pip install pyonedrive
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
