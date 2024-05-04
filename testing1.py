import unittest
from katha import is_valid_credentials
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class TestLogin(unittest.TestCase):
    def test_valid_credentials(self):
        # Test case for valid credentials
        username = "bishisimo"
        password = "CroCro123@"
        result = is_valid_credentials(username, password)
        self.assertTrue(result)

    def test_invalid_username(self):
        # Test case for invalid username
        username = "invalid_user"
        password = "test_password"
        result = is_valid_credentials(username, password)
        self.assertFalse(result)

   

if __name__ == "__main__":
    unittest.main()
