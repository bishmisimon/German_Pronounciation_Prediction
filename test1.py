import pytest
from test import is_valid_credentials

# Define test cases for valid and invalid credentials
@pytest.mark.parametrize("username, password, expected", [
    ("bish", "bish", True),  # Valid credentials
    ("user1", "wrongpassword", False),  # Invalid password
    ("nonexistentuser", "password1", False),  # Nonexistent username
])
def test_login(username, password, expected):
    assert is_valid_credentials(username, password) == expected
