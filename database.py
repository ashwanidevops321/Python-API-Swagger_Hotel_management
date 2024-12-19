import mysql.connector
from mysql.connector import Error
from typing import Optional


def get_connection() -> Optional[mysql.connector.MySQLConnection]:
    """
    Establishes a connection to the hotel management database.

    Returns:
        A MySQLConnection object if the connection is successful, None otherwise.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password@123',
            database='hotel_management_db'
        )
        print("Successfully connected to the database.")
        return connection
    except Error as error:
        print(f"Error connecting to database: {error}")
        return None


def initialize_db():
    """
    Initializes the database by creating necessary tables if they don't already exist.
    """
    connection = get_connection()
    if connection is None:
        print("Database connection failed. Exiting initialization.")
        return

    try:
        cursor = connection.cursor()

        # Create the 'rooms' table
        create_rooms_table = '''
            CREATE TABLE IF NOT EXISTS rooms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                room_number VARCHAR(50) UNIQUE NOT NULL,
                type VARCHAR(50) NOT NULL,
                price_per_night FLOAT NOT NULL,
                is_available TINYINT NOT NULL
            )
        '''
        cursor.execute(create_rooms_table)
        print("Created 'rooms' table successfully.")

        # Create the 'location' table
        create_location_table = '''
            CREATE TABLE IF NOT EXISTS location (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hotel_name VARCHAR(100) NOT NULL,
                address VARCHAR(255) NOT NULL,
                city VARCHAR(50) NOT NULL,
                state VARCHAR(50) NOT NULL,
                zip_code VARCHAR(20) NOT NULL,
                latitude DOUBLE,
                longitude DOUBLE
            )
        '''
        cursor.execute(create_location_table)
        print("Created 'location' table successfully.")

        # Commit the changes
        connection.commit()
        print("Database tables created and committed successfully.")

    except Error as error:
        print(f"Error during database initialization: {error}")
    finally:
        # Ensure resources are closed properly
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Database connection closed.")


# Entry point for the script
if __name__ == "__main__":
    initialize_db()