# model.py

class ImageModel:
    def __init__(self):
        self.image_path = None

    def set_image_path(self, path):
        self.image_path = path

    def get_image_path(self):
        return self.image_path


# model.py

import mysql.connector

class PatientModel:
    def __init__(self):
        # Initialize the database connection parameters
        self.db_params = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "Telefon2001",
            "database": "myDB"
        }

    def get_user_details(self, patient_id):
        # Establish a connection to the database
        conn = mysql.connector.connect(**self.db_params)

        # Create a cursor to execute SQL queries
        cursor = conn.cursor(dictionary=True)

        # Use a parameterized query to avoid SQL injection
        query = 'SELECT name, age, gender FROM patient_profiles WHERE id = %s'
        cursor.execute(query, (patient_id,))

        # Fetch the user details
        user_details = cursor.fetchone()

        # Close the database connection
        conn.close()

        # Return the user details
        return user_details

    def get_names_from_database(self):
        # Establish a connection to the database
        conn = mysql.connector.connect(**self.db_params)

        # Create a cursor to execute SQL queries
        cursor = conn.cursor(dictionary=True)

        # Retrieve names from the patient_profiles table
        cursor.execute('SELECT name FROM patient_profiles')
        names = [row["name"] for row in cursor.fetchall()]

        # Close the database connection
        conn.close()

        # Return the names
        return names

    def get_images_paths_from_database(self):
        # Establish a connection to the database
        conn = mysql.connector.connect(**self.db_params)

        # Create a cursor to execute SQL queries
        cursor = conn.cursor(dictionary=True)

        # Retrieve image paths from the patient_profiles table
        cursor.execute('SELECT image_path FROM patient_profiles')
        image_paths = [row["image_path"] for row in cursor.fetchall()]

        # Close the database connection
        conn.close()

        # Return the image paths
        return image_paths