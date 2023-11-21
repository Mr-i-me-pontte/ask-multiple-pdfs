import unittest


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.app = app.test_client()

    def test_process_pdf(self):
        # Send a test POST request
        response = self.app.post('/process', json={'question': 'list transactions'})
        # Check the status code and response data
        self.assertEqual(response.status_code, 200)
        self.assertIn('chat_history', response.json)

if __name__ == '__main__':
    # Run the tests
    unittest.main()