# controller.py

from view import ImageView
from model import ImageModel, PatientModel
import tkinter as tk
from tkinter import filedialog
import os
import mysql.connector
from datetime import datetime

class ImageController:
    def __init__(self, root):
        """
        Initializes the ImageController.

        Parameters:
        - root (Tk): The Tkinter root window.
        """
        self.root = root

        # Model
        self.image_model = ImageModel()
        self.patient_model = PatientModel()

        # View
        self.view = ImageView(root, self)

        # Attributes
        self.selected_patient_id = None
        self.uploaded_image_path = None
        
        self.draw_rectangle()
        
        
        
    def draw_rectangle(self):
        # Get the canvas from the view
        
            canvas1 = self.view.canvas

        # Coordinates of the rectangle (x1, y1, x2, y2)
            rectangle_coords = 300, 200, 700, 600

        # Draw the rectangle on the canvas
            canvas1.create_rectangle(rectangle_coords, outline="black", width=2, fill="lightblue")    


    def get_comments(self):
        # Get comments from the Entry widget
        comments = self.view.comments_entry.get()
        return comments
    
    # Image Handling
    def upload_picture(self):
        """
        Handles the process of uploading a picture.

        Opens a file dialog to select a picture, checks if a file is selected,
        verifies if the file is of a supported type (PNG, JPG, or JPEG), and
        updates the image in the view.

        Note:
        - This method runs in an infinite loop until a valid file is selected.
        """
        while True:
            # Open file dialog to select a picture
            file_path = filedialog.askopenfilename(title="Select Picture")

            # Check if a file is selected
            if not file_path:
                print("No file selected. Exiting.")
                break

            # Check if the file is a supported type
            if self.is_supported_file(file_path):
                self.image_model.set_image_path(file_path)
                self.view.update_image_label(file_path)
                break
            else:
                print("Unsupported file type. Please select a PNG, JPG, or JPEG file.")
                
    def is_supported_file(self, file_path):
        """
        Checks if the given file is of a supported type.

        Parameters:
        - file_path (str): The path of the file to check.

        Returns:
        - bool: True if the file type is supported; False otherwise.
        """
        # Check if the file extension is supported
        file_name, file_extension = os.path.splitext(file_path.lower())
        return file_extension in {'.png', '.jpg', '.jpeg'}
    
    def application_supports_secure_restorable_state(self):
        """
        Addresses the warning about missing method.

        Returns:
        - bool: True indicating that the application supports secure restorable state.
        """
        return True

    # Names and User Details
    def update_name_list(self):
        # Connect to the model to get names
        names = self.patient_model.get_names_from_database()

        # Update the names in the view
        self.view.update_names(names)

    def get_user_details(self, patient_id):
        # Connect to the model to get user details
        user_details = self.patient_model.get_user_details(patient_id)

        # Update the details in the view
        self.view.show_user_details(user_details)
        
        self.selected_patient_id = patient_id

    # Retrieving and Displaying Patient Info in GUI
    def add_log(self, patient_id, text, image_path):
        # Get the current date and time
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Call the model method to insert a log
        self.patient_model.insert_patient_log(patient_id, date, text, image_path)
                
        # Update the view to reflect the changes
        logs = self.get_logs_for_selected_patient()

        self.view.update_logs_list(logs, self.get_selected_patient_id())


    

    # Image for Log Handling
    def upload_image_for_log(self):
        # Similar to upload_picture method for selecting images
        file_path = filedialog.askopenfilename(title="Select Image for Log")

        # Check if a file is selected
        if not file_path:
            print("No file selected. Exiting.")
            return

        # Check if the file is a supported type
        if self.is_supported_file(file_path):
            self.uploaded_image_path = file_path
            print("Image uploaded for log:", file_path)
        else:
            print("Unsupported file type. Please select a PNG, JPG, or JPEG file.")

    def add_log_to_patient(self, log_text):
        # Get the uploaded image path from the controller
        image_path = self.uploaded_image_path

        # Call the controller method to add a log with text and image
        self.add_log(self.selected_patient_id, log_text, image_path)

        # Clear the uploaded image path after adding the log
        self.uploaded_image_path = None

        # Update the logs list in the view
        self.update_logs_list()


    def update_logs_list(self):
        # Update the logs list in the view
        logs = self.get_logs_for_selected_patient()
        self.view.update_logs_list(logs)
        
        
    def get_selected_patient_id(self):
        # Get the selected index from the names listbox
        selected_index = self.view.names_listbox.curselection()

        if selected_index:
            # Get the selected patient's name
            selected_name = self.view.names_listbox.get(selected_index)

            # Retrieve the patient ID from the model using the selected name
            patient_id = self.patient_model.get_patient_id_by_name(selected_name)
            return patient_id

        return None
         
    def get_logs_for_selected_patient(self):
        
        patient_id = self.get_selected_patient_id()
        
        if patient_id:
            logs = self.patient_model.get_logs_for_patient(patient_id)
            return logs
        
        return logs
    
    def get_logs_for_patient(self,patient_id):
        # Establish a connection to the database
        conn = mysql.connector.connect(**self.db_params)

        # Create a cursor to execute SQL queries
        cursor = conn.cursor(dictionary=True)

        # Use a parameterized query to avoid SQL injection
        query = 'SELECT date, text, image_path FROM patient_logs WHERE patient_id = %s ORDER BY date DESC'
        cursor.execute(query, (patient_id,))

        # Fetch the logs for the patient
        logs = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Return the logs
        return logs

            
    def get_uploaded_image_path(self):
        return self.uploaded_image_path
    
    def check_logs_for_selected_patient(self):
        # Get the selected patient's ID
        patient_id = self.get_selected_patient_id()

        if patient_id:
            # Retrieve logs for the selected patient
            logs = self.patient_model.get_logs_for_patient(patient_id)

            # Process the logs (you can modify this based on your requirements)
            for log in logs:
                print(f"Date: {log['date']}, Text: {log['text']}, Image Path: {log['image_path']}")

            # Update the logs list in the view
            self.view.update_logs_list(logs, patient_id)
    
    def brain_tumour_detector(self):
        pass
        
    

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    image_controller = ImageController(root)
    root.mainloop()
