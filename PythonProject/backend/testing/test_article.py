import requests
import unittest

class TestUser(unittest.TestCase):
    url = 'http://localhost:8000/'
    api = {
        'articles': 'api/articles',
    }
    def test_get_articles(self):
        url = self.url + self.api.get('articles')
        response = requests.get(url=url)
        status_code = response.status_code
        self.assertEqual(status_code, 200)