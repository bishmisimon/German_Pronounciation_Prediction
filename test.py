import streamlit as st
import os
import welcome 

# Function to register a new user
# Function to register a new user
def register(username, password, email):
    if is_username_exists(username):
        print(f"Username '{username}' already exists. Registration failed.")
        return False
    try:
        with open("KathaMeisterdb.txt", "a") as file:
            file.write(f"{username},{password},{email}\n")
        print(f"User '{username}' registered successfully.")
        return True  # Return True upon successful registration
    except Exception as e:
        print(f"Error registering user: {e}")
        return False  # Return False if registration fails



# Function to check if a username already exists
def is_username_exists(username):
    with open("KathaMeisterdb.txt", "r") as file:
        for line in file:
            if line.split(",")[0] == username:
                return True
    return False




# Function to check if the provided credentials are valid
def is_valid_credentials(username, password):
    with open("KathaMeisterdb.txt", "r") as file:
        for line in file:
            stored_username, stored_password, _ = line.strip().split(",")
            if stored_username == username and stored_password == password:
                return True
    return False

# Function to display the registration form
def registration_form():
    st.title("User Registration")
    username = st.text_input("Username", key="username_input_reg")
    password = st.text_input("Password", type="password", key="password_input_reg")
    email = st.text_input("Email Address", key="email_input_reg")
    if st.button("Register", key="register_btn"):
        if not is_username_exists(username):
            register(username, password, email)
            st.success("Registration successful! Please proceed to login.")
        else:
            st.error("Username already exists. Please choose a different username.")

# Function to display the login form
def login_form():
    st.title("User Login")
    username = st.text_input("Username", key="username_input_login")
    password = st.text_input("Password", type="password", key="password_input_login")
    if st.button("Login", key="login_btn"):
        if is_valid_credentials(username, password):
            st.success(f"Welcome, {username}!")
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password.")

def main():
    if st.session_state.get("logged_in"):
        st.success("Logged in successfully to the Dashboard!")
        st.write("Redirecting to welcome page...")
        welcome.main()  # Display the welcome page
    
    else:
        st.title("User Authentication")
        st.write("Please login or register to access the application.")
        st.write("---")
        login_form()
        st.write("or")
        registration_form()

if __name__ == "__main__":
    main()
