import mysql.connector

try:
    # Connect to the RDS database
    conn = mysql.connector.connect(
        host='kathameister.clsoq4mai7vi.ap-south-1.rds.amazonaws.com',
        user='admin',
        password='CroCro123',
        database='kathameister',
        
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Define the SQL query to create the table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL
    )
    """

    # Execute the SQL query
    cursor.execute(create_table_query)

    # Commit the changes
    conn.commit()

    print("Table 'users' created successfully.")

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
