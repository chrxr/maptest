import os
import maptest
import unittest
import six
import json

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = maptest.app.test_client()

    def test_data_is_returned(self):
        with self.app.test_request_context('/runmap/clear'):
            assert flask.request.path == '/runmap/'

        # rv = self.app.get('/runmap/')
        # six.print_(rv.g)
        # assert rv.data

if __name__ == '__main__':
    unittest.main()
