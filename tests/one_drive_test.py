""" Testing onedrive client

"""

import json
import unittest
from mock import Mock, patch, call
from pyonedrive import OneDrive
import requests


class OneDriveTestCase(unittest.TestCase):
    def setUp(self):
        self.client = OneDrive('token', 'r_token', 'id', 'secret')

    def test_refresh_token(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            self.client.refresh_callback = Mock()

            res1 = requests.Response()
            res2 = requests.Response()
            res1.status_code = 401
            res2.status_code = 200
            api_results = [res1, res2]

            tokens = requests.Response()
            tokens.status_code = 200
            tokens._content = json.dumps(
                {
                    'access_token': 'tok',
                    'refresh_token': 'refresh'
                }
            )
            mock_requests.request.side_effect = api_results
            mock_requests.post.return_value = tokens
            r = self.client.get_user_metadata()
            mock_requests.post.assert_called_once_with(
                'https://login.live.com/oauth20_token.srf',
                data={
                    'client_secret': 'secret',
                    'client_id': 'id',
                    'grant_type': 'refresh_token',
                    'refresh_token': 'r_token'
                }
            )
            self.client.refresh_callback.assert_called_once_with(
                'tok', 'refresh')
            self.assertEquals(self.client.token, 'tok')
            self.assertEquals(self.client.refresh_token, 'refresh')
            self.assertEquals(r.status_code, 200)

    def test_user_metadata(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'metadata': 'OK'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_user_metadata()
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/me',
                params={'access_token': 'token'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'metadata': 'OK'})

    def test_user_picture(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'picture': 'OK'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_user_picture()
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/me/picture',
                params={'access_token': 'token'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'picture': 'OK'})

    def test_user_root_folder(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'root_folder': 'OK'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_root_folder()
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/me/skydrive',
                params={'access_token': 'token'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'root_folder': 'OK'})

    def test_user_albums(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'albums': 'OK'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_albums()
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/me/albums',
                params={'access_token': 'token'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'albums': 'OK'})

    def test_user_shared_albums(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'shared_albums': 'OK'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_shared_albums()
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/me/skydrive/shared/albums',
                params={'access_token': 'token'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'shared_albums': 'OK'})

    def test_folder_content_generator(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res1 = requests.Response()
            res1.status_code = 200
            res1._content = json.dumps(
                {'data': 'ok',
                 'paging': {'next': 'next_url'}}
            )
            res2 = requests.Response()
            res2.status_code = 200
            res2._content = json.dumps(
                {'data': 'ok',
                 'paging': {}}
            )

            mock_requests.request.side_effect = [res1, res2]

            for data in self.client.get_folder_content_generator(1):
                self.assertEquals(data, 'ok')
            self.assertEquals(mock_requests.request.call_count, 2)
            mock_requests.request.assert_has_calls(
                [
                    call(
                        'get',
                        'https://apis.live.net/v5.0/1/files',
                        params={'access_token': 'token',
                                'limit': 20},
                        data=None,
                        headers=None
                    ),
                    call(
                        'get',
                        'https://apis.live.net/v5.0/next_url',
                        params={'access_token': 'token',
                                'limit': 20},
                        data=None,
                        headers=None
                    )
                ])

    def test_filtered_folder_content_generator(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'data': 'ok',
                 'paging': {}}
            )

            mock_requests.request.return_value = res

            for data in self.client.get_folder_content_generator(1,
                                                                 'audio'):
                self.assertEquals(data, 'ok')
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/1/files',
                params={'access_token': 'token',
                        'limit': 20,
                        'filter': 'audio'},
                data=None,
                headers=None
            )

    def test_folder_content(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'folder_content': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_folder_content(1)
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/1/files',
                params={'access_token': 'token',
                        'limit': 20,
                        'offset': 0},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'folder_content': 'ok'})

    def test_filtered_folder_content(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'filtered_content': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_folder_content(1, content_filter='audio')
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/1/files',
                params={'access_token': 'token',
                        'limit': 20,
                        'offset': 0,
                        'filter': 'audio'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'filtered_content': 'ok'})

    def test_user_shared_objects(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'shared_objects': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_shared_objects()
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/me/skydrive/shared',
                params={'access_token': 'token',
                        'limit': 20,
                        'offset': 0},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'shared_objects': 'ok'})

    def test_user_filtered_shared_objects(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'filtered_shared_objects': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_shared_objects(content_filter='audio')
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/me/skydrive/shared',
                params={'access_token': 'token',
                        'limit': 20,
                        'offset': 0,
                        'filter': 'audio'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'filtered_shared_objects': 'ok'})

    def test_user_shared_folders(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'shared_folders': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_shared_folders()
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/me/skydrive/shared',
                params={'access_token': 'token',
                        'limit': 20,
                        'offset': 0,
                        'filter': 'folders'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'shared_folders': 'ok'})

    def test_user_most_recent(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'most_recent': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_most_recent()
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/me/skydrive/recent_docs',
                params={'access_token': 'token'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'most_recent': 'ok'})

    def test_user_quota(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'quota': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_usage_quota()
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/me/skydrive/quota',
                params={'access_token': 'token'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'quota': 'ok'})

    def test_shared_read_link(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'read_link': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_shared_read_link(1)
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/1/shared_read_link',
                params={'access_token': 'token'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'read_link': 'ok'})

    def test_shared_edit_link(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'edit_link': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_shared_edit_link(1)
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/1/shared_edit_link',
                params={'access_token': 'token'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'edit_link': 'ok'})

    def test_embed_link(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'embed_link': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_embed_link(1)
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/1/embed',
                params={'access_token': 'token'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'embed_link': 'ok'})

    def test_preview(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res1 = requests.Response()
            res1.status_code = 200
            res1._content = json.dumps(
                {'link': 'item_link'}
            )
            res2 = requests.Response()
            res2.status_code = 200
            res2._content = json.dumps(
                {'preview': 'ok'}
            )

            mock_requests.request.side_effect = [res1, res2]

            r = self.client.get_preview(1)
            self.assertEquals(mock_requests.request.call_count, 2)
            mock_requests.request.assert_has_calls(
                [
                    call(
                        'get',
                        'https://apis.live.net/v5.0/1/shared_read_link',
                        params={'access_token': 'token'},
                        data=None,
                        headers=None
                    ),
                    call(
                        'get',
                        'https://apis.live.net/v5.0/skydrive/get_item_preview',
                        params={'type': 'thumbnail',
                                'url': 'item_link'}
                    )
                ])
            self.assertEquals(r.json(), {'preview': 'ok'})

    def test_comments(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'comments': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_comments(1)
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/1/comments',
                params={'access_token': 'token',
                        'limit': 20,
                        'offset': 0},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'comments': 'ok'})

    def test_comments_generator(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res1 = requests.Response()
            res1.status_code = 200
            res1._content = json.dumps(
                {'data': 'ok',
                 'paging': {'next': 'next_url'}}
            )
            res2 = requests.Response()
            res2.status_code = 200
            res2._content = json.dumps(
                {'data': 'ok',
                 'paging': {}}
            )

            mock_requests.request.side_effect = [res1, res2]

            for data in self.client.get_comments_generator(1):
                self.assertEquals(data, 'ok')
            self.assertEquals(mock_requests.request.call_count, 2)
            mock_requests.request.assert_has_calls(
                [
                    call(
                        'get',
                        'https://apis.live.net/v5.0/1/comments',
                        params={'access_token': 'token',
                                'limit': 20},
                        data=None,
                        headers=None
                    ),
                    call(
                        'get',
                        'https://apis.live.net/v5.0/next_url',
                        params={'access_token': 'token',
                                'limit': 20},
                        data=None,
                        headers=None
                    )
                ])

    def test_tags(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'tags': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.get_tags(1)
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/1/tags',
                params={'access_token': 'token',
                        'limit': 20,
                        'offset': 0},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'tags': 'ok'})

    def test_tags_generator(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res1 = requests.Response()
            res1.status_code = 200
            res1._content = json.dumps(
                {'data': 'ok',
                 'paging': {'next': 'next_url'}}
            )
            res2 = requests.Response()
            res2.status_code = 200
            res2._content = json.dumps(
                {'data': 'ok',
                 'paging': {}}
            )

            mock_requests.request.side_effect = [res1, res2]

            for data in self.client.get_tags_generator(1):
                self.assertEquals(data, 'ok')
            self.assertEquals(mock_requests.request.call_count, 2)
            mock_requests.request.assert_has_calls(
                [
                    call(
                        'get',
                        'https://apis.live.net/v5.0/1/tags',
                        params={'access_token': 'token',
                                'limit': 20},
                        data=None,
                        headers=None
                    ),
                    call(
                        'get',
                        'https://apis.live.net/v5.0/next_url',
                        params={'access_token': 'token',
                                'limit': 20},
                        data=None,
                        headers=None
                    )
                ])

    def test_delete(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'delete': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.delete_item(1)
            mock_requests.request.assert_called_once_with(
                'delete',
                'https://apis.live.net/v5.0/1',
                params={'access_token': 'token'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'delete': 'ok'})

    def test_download(self):
        with patch('pyonedrive.py_onedrive.requests') as mock_requests:
            res = requests.Response()
            res.status_code = 200
            res._content = json.dumps(
                {'download': 'ok'}
            )

            mock_requests.request.return_value = res

            r = self.client.download_file(1)
            mock_requests.request.assert_called_once_with(
                'get',
                'https://apis.live.net/v5.0/1/content',
                params={'access_token': 'token'},
                data=None,
                headers=None
            )
            self.assertEquals(r.json(), {'download': 'ok'})
