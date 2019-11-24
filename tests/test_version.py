import unittest

from runningbox_api_python import __version__


class VersionTest(unittest.TestCase):
    @staticmethod
    def test_version():
        assert __version__ == '0.0.0'
