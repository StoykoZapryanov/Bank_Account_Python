import unittest
from app import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_estimate_traffic(self):
        # Test the estimate_traffic endpoint
        response = self.app.get('/estimate_traffic?total_request_count=1000000')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('estimated_traffic', data)

if __name__ == '__main__':
    unittest.main()
