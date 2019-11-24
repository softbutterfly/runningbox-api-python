import unittest

from runningbox_api_python import __version__
from runningbox_api_python.client import Client


class ClientTest(unittest.TestCase):
    api_key = 'sample_api_key'
    broker_tax_id = 'sample_broker_tax_id'
    version = __version__

    def test_client_headers(self):
        client = Client(
            api_key=self.api_key,
            broker_tax_id=self.broker_tax_id
        )

        headers = {
            'User-Agent': f'Runningbox-API-Python/{self.version}',
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        assert headers['User-Agent'] == client.session.headers['User-Agent']
        assert headers['Content-type'] == client.session.headers['Content-type']
        assert headers['Accept'] == client.session.headers['Accept']


if __name__ == '__main__':
    unittest.main()
