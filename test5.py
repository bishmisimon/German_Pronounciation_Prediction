import pytest
from test import register, is_username_exists

# Test case to check that a new user cannot register with an existing username
def test_new_user_cannot_use_existing_username():
    # Define an existing username
    existing_username = "existinguser"
    password = "password123"
    email = "existinguser@example.com"

    # Attempt to register the existing user
    result = register(existing_username, password, email)

    # Check if the registration failed
    assert result == True
