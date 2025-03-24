#Suppose you have a function fetch_data_from_api(url) that fetches data from an API. Write a unit test using unittest.mock to simulate the API response.
from unittest.mock import patch
import requests

#function to e tested

def fetch_data_from_api(url):
    import requests
    response = requests.get(url)
    return response.json()

#unittest

import unittest
class TestFetchData(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_data_from_api(self, mock_get):
        mock_get.return_value.json.return_value = {'key': 'value'}
        result = fetch_data_from_api('http://fakeurl.com')
        self.assertEqual(result, {'key': 'value'})

if __name__ == '__main__':
    unittest.main()
