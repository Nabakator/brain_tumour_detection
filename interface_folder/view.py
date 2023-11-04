# view.py

import tkinter as tk
from tkinter import filedialog,Toplevel
from PIL import Image, ImageTk

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
        
        


    def create_widgets(self):
        # Create a canvas to place elements
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Button for user to input picture
        self.upload_button = tk.Button(self.canvas, text="Upload Picture", command=self.controller.upload_picture)
        self.canvas.create_window(800, 0, anchor="nw", window=self.upload_button)

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
        self.names_listbox.bind("<ButtonRelease-1>", self.show_user_details)  # Bind the event to show details
        self.canvas.create_window(5, 50 , anchor="nw", window=self.names_listbox)

        # Label for displaying user details
        # self.user_details_label = tk.Label(self.canvas, text="User Details:")
        # self.canvas.create_window(0, self.canvas_height/3, anchor="nw", window=self.user_details_label)

        # Button to update the names
       # self.update_names_button = tk.Button(self.canvas, text="Update Names", command=self.controller.update_name_list)
       # self.canvas.create_window(0, 0, anchor="nw", window=self.update_names_button)

        
        self.names_listbox.bind("<<ListboxSelect>>", self.on_name_selected)

        
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


    def on_name_selected(self, event):
        # Get the selected name from the Listbox
        selected_index = self.names_listbox.curselection()
        if selected_index:
            selected_name = self.names_listbox.get(selected_index)

            # Get user details based on the selected name
            user_details = self.controller.get_user_details(selected_name)

            # Show user details in an info box
            self.show_user_details(user_details)

    def show_user_details(self, event):
        # Get the selected name from the listbox
        selected_index = self.names_listbox.curselection()
        if selected_index:
            selected_name = self.names_listbox.get(selected_index)
            # Replace this with actual user details retrieval logic
            user_details = {"Name": selected_name, "Age": 25, "Gender": "Male"}
        
            # Clear any previous details in the canvas
            self.canvas.delete("user_details")
        
            # Display user details in canvas
            y_position = 60
            x_position = 200
            for key, value in user_details.items():
                detail_text = f"{key}: {value}"
                self.canvas.create_text(x_position, y_position, text=detail_text, tags="user_details", anchor="center")
                y_position += 20
                
            image_path = user_details.get("Image", "")
            if image_path:
                self.display_user_image(image_path, x_position, y_position + 10)  # Adjust the y_position as needed

        
        def show_user_details(self, event):
            # ... (existing code)
            
            # Display the image
            image_path = user_details.get("Image", "")
            if image_path:
                self.display_user_image(image_path, x_position, y_position + 10)  # Adjust the y_position as needed
            
        
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

        

        # Example: Display user details in a label
        # for key, value in user_details.items():
        #     detail_label = tk.Label(details_window, text=f"{key}: {value}")
        #     detail_label.pack()