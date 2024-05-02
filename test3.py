import pytest
from test import register, is_username_exists

# Test case for registering an existing user
def test_register_existing_user():
    # Define existing user credentials
    existing_username = "bish"
    existing_password = "bish"
    existing_email = "bishmisimon@gmail.com"

    # Attempt to register the existing user
    result = register(existing_username, existing_password, existing_email)

    # Check if the registration was unsuccessful
    assert result == False

    # Check if the existing user already exists in the database
    assert is_username_exists(existing_username) == True
