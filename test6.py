import pytest
from main import register, is_valid_credentials




# Test case to check that a new user can register with a unique username
def test_new_user_can_register():
    # Define a new username
    new_username = "Terro"
    password = "terrol123@"
    email = "caremal@example.com"

    # Ensure the new username is not already registered
    assert not is_valid_credentials(new_username, password)

    # Attempt to register the new user
    result = register(new_username, email, "", "", password)

    # Check if the registration was successful
    assert result == True

    # Check if the new user is now registered
    assert is_valid_credentials(new_username, password)

# Assuming `is_valid_credentials` function checks both username and password
# and returns True if they exist in the database, and False otherwise
