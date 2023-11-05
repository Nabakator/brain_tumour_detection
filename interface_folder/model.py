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
        query = 'SELECT name, age, gender FROM patient_profiles WHERE id_patients = %s'
        cursor.execute(query, (patient_id,))

        # Fetch the user details
        user_details = cursor.fetchone()

        # Close the database connection
        conn.close()

        # Return the user details
        return user_details

    def add_log_to_patient(self, patient_id, log_text, image_path):
        # Establish a connection to the database
        conn = mysql.connector.connect(**self.db_params)

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Use a parameterized query to avoid SQL injection
        query = 'UPDATE patient_profiles SET log_text = %s, image_path = %s WHERE id_patients = %s'
        cursor.execute(query, (log_text, image_path, patient_id))

        # Commit the changes
        conn.commit()

        # Close the database connection
        conn.close()
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
    
    def insert_patient_log(self, patient_id, date, text, image_path):
        conn = mysql.connector.connect(**self.db_params)
        cursor = conn.cursor()

        query = """
        INSERT INTO patient_logs (patient_id, date, text, image_path)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (patient_id, date, text, image_path))
        conn.commit()

        conn.close()
        
    def get_patient_id_by_name(self, patient_name):
        # Establish a connection to the database
        conn = mysql.connector.connect(**self.db_params)

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Use a parameterized query to avoid SQL injection
        query = 'SELECT id_patients FROM patient_profiles WHERE name = %s'
        cursor.execute(query, (patient_name,))

        # Fetch the patient ID
        patient_id = cursor.fetchone()

        # Close the database connection
        conn.close()

        return patient_id[0] if patient_id else None

    def get_logs_for_patient(self, patient_id):
        # Establish a connection to the database
        conn = mysql.connector.connect(**self.db_params)

        # Create a cursor to execute SQL queries
        cursor = conn.cursor(dictionary=True)

        # Use a parameterized query to avoid SQL injection
        query = 'SELECT date, text, image_path FROM patient_logs WHERE patient_id = %s ORDER BY date DESC'
        cursor.execute(query, (patient_id,))

        # Fetch the logs for the patient
        logs = cursor.fetchall()

        # Add the patient_id to each log
        for log in logs:
            log["patient_id"] = patient_id

        # Close the database connection
        conn.close()

        # Return the logs
        return logs
    
    

    