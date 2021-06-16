import unittest
import main
class TestMain(unittest.TestCase):
    def test_response_status_code(self):
        self.assertEqual(main.getResponseStatus(), 200)


if __name__ == '__main__':
    unittest.main()