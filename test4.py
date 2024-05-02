import pytest
from test import is_username_exists

# Test case for checking if an existing user exists
def test_check_existing_user_exists():
    # Define an existing username
    existing_username = "existinguser"

    # Check if the existing user exists in the database
    result = is_username_exists(existing_username)

    # Assert that the existing user exists
    assert result == True
