# controller.py

from view import ImageView
from model import ImageModel,PatientModel
import tkinter as tk
from tkinter import filedialog
import os
import mysql.connector



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



    def application_supports_secure_restorable_state(self):
        return True

##############  LIST OF NAME FROM SQL TABLES #################################

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
        

   
    
    
######## RETRIEVING AND DISPLAYING PATIENT INFO IN GUI##############

    # def get_user_details(self,patient_id):
        
    #     conn = mysql.connector.connect(
    #         host="127.0.0.1",
    #         user="root",
    #         password="Telefon2001",
    #         database="myDB"
    #     )

    #     cursor = conn.cursor(dictionary=True)
    
    #     # Use a parameterized query to avoid SQL injection
    #     query = 'SELECT name, age, gender FROM patient_profiles WHERE id = %s'
    #     cursor.execute(query, (patient_id,))
        
    #     # Fetch the user details
    #     user_details = cursor.fetchone()

    #     # Close the connection
    #     conn.close()

    #     # Return the user details
    #     return user_details
        
        
    
    
# Main program
if __name__ == "__main__":
    root = tk.Tk()
    image_controller = ImageController(root)
    root.mainloop()
