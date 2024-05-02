# Update your Streamlit app configuration to connect to the RDS instance
import mysql.connector

# Connect to the RDS database
conn = mysql.connector.connect(
    host=endpoint,
    user='admin',
    password='mypassword',
    database='mydatabase'
)

# Use this connection to interact with the database from your Streamlit app
