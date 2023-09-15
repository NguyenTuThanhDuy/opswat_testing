import requests
import unittest

class TestUser(unittest.TestCase):
    url = 'http://localhost:8000/'
    api = {
        'users': 'api/users',
        'login': 'api/login'
    }
    def test_get_users(self):
        url = self.url + self.api.get('users')
        response = requests.get(url=url)
        status_code = response.status_code
        self.assertEqual(status_code, 200)