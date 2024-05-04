import unittest
from unittest.mock import MagicMock, patch
from katha import register

class TestRegister(unittest.TestCase):
    @patch('main.mysql.connector.connect')
    def test_register_success(self, mock_connect):
        # Mock cursor and execute method
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (0,)  # Simulate no existing username
        mock_cursor.execute.return_value = None
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Call register function
        result = register("test_user", "test@example.com", "Test", "User", "password")

        # Check if registration was successful
        self.assertTrue(result)

    @patch('main.mysql.connector.connect')
    def test_register_existing_username(self, mock_connect):
        # Mock cursor and execute method
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)  # Simulate existing username
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Call register function
        result = register("Caroline","caroline@gmail.com","caroline","Perera","caroline123")

        # Check if registration failed
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()


