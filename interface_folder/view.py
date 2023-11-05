# view.py

import tkinter as tk
from tkinter import filedialog,Toplevel
from PIL import Image, ImageTk
import os

class ImageView:
    def __init__(self, root, controller):
        self.root = root
        self.root.title("Image Viewer")

        # Controller
        self.controller = controller

        # Canvas dimensions
        self.canvas_width = 1000
        self.canvas_height = 800

        # Create GUI components
        self.create_widgets()
        
        self.logs_listbox = tk.Listbox(self.canvas, selectmode=tk.SINGLE, width=8, height=23, bg='#D3D3D3', fg='black')
        self.canvas.create_window(155, 75, anchor="nw", window=self.logs_listbox)

        
                # Create an Text widget for comments
        self.comments_entry = tk.Text(self.canvas, width=30,height=28,)  # Adjust the width as needed
        self.canvas.create_window(715, 230, anchor="nw", window=self.comments_entry)



    def create_widgets(self):
        # Create a canvas to place elements
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Button for user to input picture
        self.upload_button = tk.Button(self.canvas, text="Upload Picture", command=self.controller.upload_picture)
        self.canvas.create_window(300, 170, anchor="nw", window=self.upload_button)

        # Display area for the image
        self.image_label = tk.Label(self.root, text="No Image")
        self.canvas.create_window(self.canvas_width/2 - 200, self.canvas_height/2 -200, anchor="nw", window=self.image_label)

        # Listbox for displaying names
        # self.names_listbox = tk.Listbox(self.canvas, selectmode=tk.SINGLE, width=4)
        # self.canvas.create_window(200, 0 , anchor="nw", window=self.names_listbox)

        # Button to update the names
        self.update_names_button = tk.Button(self.canvas, text="Update Names", command=self.controller.update_name_list)
        self.canvas.create_window(0, 0, anchor="nw", window=self.update_names_button)

        ## Bind ListboxSelect event to on_name_selected method
        #self.names_listbox.bind("<<ListboxSelect>>", self.on_name_selected)

        # Listbox for displaying names
        self.names_listbox = tk.Listbox(self.canvas, selectmode=tk.SINGLE, width=13,height = 23,bg ='#D3D3D3',fg='black')
        self.names_listbox.bind("<ButtonRelease-1>", lambda event=None: self.show_user_details())
        self.canvas.create_window(5, 75 , anchor="nw", window=self.names_listbox)

        # Label for displaying user details
        # self.user_details_label = tk.Label(self.canvas, text="User Details:")
        # self.canvas.create_window(0, self.canvas_height/3, anchor="nw", window=self.user_details_label)

        # Button to update the names
       # self.update_names_button = tk.Button(self.canvas, text="Update Names", command=self.controller.update_name_list)
       # self.canvas.create_window(0, 0, anchor="nw", window=self.update_names_button)

        
        self.names_listbox.bind("<<ListboxSelect>>", self.on_name_selected)

        
        
        self.add_log_button = tk.Button(self.canvas, text="Add Log", command=self.show_add_log_dialog)
        
        self.canvas.create_window(150, 0, anchor="nw", window=self.add_log_button)

        #button to check for logs8

        # Button to trigger the get_logs method
        self.check_logs_button = tk.Button(self.canvas, text="Check Logs", command=self.controller.check_logs_for_selected_patient)
        self.canvas.create_window(142, 40, anchor="nw", window=self.check_logs_button)
        
        
        
        #button to run uploaded picture through model
        
        self.model_picture = tk.Button(self.canvas,text="Brain Tumour Detector",command=self.controller.brain_tumour_detector)
        self.canvas.create_window(525, 170, anchor="nw", window=self.model_picture)
        
        
        # Label for adding comments
        self.add_comments_label = tk.Label(self.canvas, text="Add Comments:")
        self.canvas.create_window(715, 200, anchor="nw", window=self.add_comments_label)

        
        
    def add_comments_textbox(self):
        # Entry for comments
        comments_entry = tk.Entry(self.canvas, width=50)
        self.canvas.create_window(500, 200, anchor="nw", window=comments_entry)

        
 
        
    def update_image_label(self, image_path):
        # Open the image using PIL
        img = Image.open(image_path)
        
        # Resize the image if needed
        img = img.resize((400, 400), Image.LANCZOS)  # Use Image.LANCZOS for resizing

        # Convert the image to PhotoImage
        photo = ImageTk.PhotoImage(img)

        # Update the label with the new image
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def update_names(self, names):
        # Update the listbox with the new names
        self.names_listbox.delete(0, tk.END)  # Clear the listbox
        for name in names:
            self.names_listbox.insert(tk.END, name)

    def update_name_list(self, names):
        # Update the listbox with the new names
        self.names_listbox.delete(0, tk.END)  # Clear the listbox
        for name in names:
            self.names_listbox.insert(tk.END, name)
            
    def update_logs_list(self, logs, selected_patient_id):
    # Update the logs list in the view for the selected patient
        if hasattr(self, 'logs_listbox'):  # Check if logs_listbox attribute exists
            self.logs_listbox.delete(0, tk.END)  # Clear the listbox

        # Filter logs for the selected patient
            patient_logs = [log for log in logs if log["patient_id"] == selected_patient_id]
            

            for log in patient_logs:
                # Truncate the text to a certain length (e.g., 50 characters)
                truncated_text = log["text"][30:50] + "..." if len(log["text"]) > 50 else log["text"]
                self.logs_listbox.insert(tk.END, f"{log['date']}: {truncated_text}")



    def on_name_selected(self, event):
        # Get the selected name from the Listbox
        selected_index = self.names_listbox.curselection()
        if selected_index:
            selected_name = self.names_listbox.get(selected_index)

            # Get user details based on the selected name
            user_details = self.controller.get_user_details(selected_name)

            
            
            # Show user details in an info box
            self.show_user_details(user_details)

    def show_user_details(self, event=None):
        # Get the selected name from the listbox
        selected_index = self.names_listbox.curselection()
        if selected_index:
            selected_name = self.names_listbox.get(selected_index)
            print(selected_name)
            # Replace this with actual user details retrieval logic
            user_details = {"Name": selected_name, "Age": 25, "Gender": "Male"}
            
            # Retrieve the patient ID from the model using the selected name
            
            patient_id = self.controller.get_selected_patient_id(selected_name)
            # Get user details based on the selected patient ID
            user_details = self.controller.get_user_details(patient_id)

        # Show user details in an info box
            self.display_user_details(user_details, patient_id)
            
            
            # Clear any previous details in the canvas
            self.canvas.delete("user_details")
            
        
            # Display user details in canvas -------------- THIS IS THE CODE FOR DISPLAYING INFO OF PATIENT(NAME,GENDER,AGE)
            # y_position = 10
            # x_position = 200
            # for key, value in user_details.items():
            #     detail_text = f"{key}: {value}"
            #     self.canvas.create_text(x_position, y_position, text=detail_text, tags="user_details", anchor="center")
            #     y_position += 20
                
            # image_path = user_details.get("Image", "")
            # if image_path:
            #     self.display_user_image(image_path, x_position, y_position + 10)  # Adjust the y_position as needed
                
            # Update the logs list in the view for the selected patient
        

        

        
    
    def display_user_image(self, image_path, x_position, y_position):
        # Open the image using PIL
        img = Image.open(image_path)
        # Resize the image if needed
        img = img.resize((50, 50), Image.LANCZOS)  # Adjust the size as needed
        # Convert the image to PhotoImage
        photo = ImageTk.PhotoImage(img)
        # Display the image on the canvas
        self.canvas.create_image(x_position, y_position, anchor="nw", image=photo)
        self.canvas.image = photo  # Keep a reference to avoid garbage collection
        
        
    def show_add_log_dialog(self):
        # Create a Toplevel window for adding logs
        add_log_window = Toplevel(self.root)
        add_log_window.title("Add Log")
        # Entry for entering log text
        log_text_entry = tk.Entry(add_log_window, width=20)
        log_text_entry.pack(pady=15)
        # Button to select an image for the log
        select_image_button = tk.Button(add_log_window, text="Select Image", command=self.upload_image_for_log)
        select_image_button.pack(pady=10)
        # Button to add the log
        add_log_button = tk.Button(add_log_window, text="Add Log", command=lambda: self.add_log_to_patient(log_text_entry.get()))
        add_log_button.pack(pady=10)
   
    def upload_image_for_log(self):
         # Update the method to use the controller's method for uploading images
        self.controller.upload_image_for_log()

    
    
        # Similar to upload_picture method for selecting images
        # You can use self.controller.upload_picture as a reference
        
        
        
        
    def add_log_to_patient(self, log_text):
        
            # Get the selected patient's ID (you need to implement this method in your controller)
            
            patient_id = self.controller.get_selected_patient_id()

            # Get the image path (you need to implement this method in your controller)
            image_path = self.controller.get_uploaded_image_path()


            # Call the controller method to add the log
            self.controller.add_log(patient_id, log_text, image_path)
            
    def add_check_log_button_dialog(self):

            self.controller.get_logs()
    


            # Example: Display user details in a label
            # for key, value in user_details.items():
            #     detail_label = tk.Label(details_window, text=f"{key}: {value}")
            #     detail_label.pack()