import unittest
from katha import register, is_valid_credentials
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class TestRegistration(unittest.TestCase):
    def test_registration_success(self):
        # Test case for successful registration
        username = "Caroline"
        email = "caroline@gmail.com"
        f_name = "caroline"
        l_name = "Perera"
        password = "caroline123"
        result = register(username, email, f_name, l_name, password)
        self.assertTrue(result)

    def test_registration_existing_username(self):
        # Test case for registration with existing username
        username = "Lukas"
        email = "lukas@gmail.com"
        f_name = "Lukas"
        l_name = "Simon"
        password = "Lukas123"
        result = register(username, email, f_name, l_name, password)
        self.assertFalse(result)

    def test_registration_invalid_email(self):
        # Test case for registration with invalid email
        username = "new_user"
        email = "bish.com"
        f_name = "Test"
        l_name = "User"
        password = "test_password"
        result = register(username, email, f_name, l_name, password)
        self.assertFalse(result)

    def test_registration_invalid_password(self):
        # Test case for registration with invalid password
        username = "new_user"
        email = "user@gmail.com"
        f_name = "Test"
        l_name = "User"
        password = "s"
        result = register(username, email, f_name, l_name, password)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
