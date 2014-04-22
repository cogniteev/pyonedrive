""" Authentication tests

"""

import unittest
import mock
from pyonedrive import LiveAuth
import requests


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.auth = LiveAuth('id', 'secret', 'scope', 'redirect')

    def test_generate_code_url(self):
        url = self.auth.generate_oauth_initiation_url('code')
        self.assertIsInstance(url, str)
        self.assertEquals(
            url,
            'https://login.live.com/oauth20_authorize.srf?client_id='
            'id&scope=scope&response_type=code&redirect_uri=redirect')

    def test_generate_token_url(self):
        url = self.auth.generate_oauth_initiation_url('token')
        self.assertIsInstance(url, str)
        self.assertEquals(
            url,
            'https://login.live.com/oauth20_authorize.srf?client_id='
            'id&scope=scope&response_type=token&redirect_uri=redirect')

    def test_generate_invalid_url(self):
        with self.assertRaises(ValueError) as val:
            self.auth.generate_oauth_initiation_url('invalid')
        self.assertIsNotNone(val)

    def test_exchange_code(self):
        res = requests.Response()
        res.status_code = 200
        with mock.patch('pyonedrive.live_auth.requests') as mock_requests:
            mock_requests.post.return_value = res
            r = self.auth.exchange_oauth_code_for_token('my_code')
            mock_requests.post.assert_called_once_with(
                'https://login.live.com/oauth20_token.srf',
                data={
                    'code': 'my_code',
                    'client_secret': 'secret',
                    'redirect_uri': 'redirect',
                    'client_id': 'id',
                    'grant_type': 'authorization_code'
                }
            )
            self.assertEquals(r.status_code, 200)