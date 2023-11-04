import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

def on_selection(event):
    selected_index = profiles_listbox.curselection()
    if selected_index:
        selected_profile = profiles_list[selected_index[0]]
        update_profile_info(selected_profile)

def update_profile_info(profile):
    info_text.config(state=tk.NORMAL)
    info_text.delete("1.0", tk.END)
    info_text.insert(tk.END, profile["name"] + "\n")
    info_text.insert(tk.END, "Age: " + str(profile["age"]) + "\n")
    info_text.insert(tk.END, "Gender: " + profile["gender"] + "\n")
    info_text.config(state=tk.DISABLED)
    


def search_by_name():
    search_query = search_entry.get().lower()
    matching_profiles = [profile for profile in profiles_list if search_query in profile["name"].lower()]

    profiles_listbox.delete(0, tk.END)  # Clear the listbox

    for profile in matching_profiles:
        profiles_listbox.insert(tk.END, profile["name"])
        
def show_settings_menu():
    messagebox.showinfo("Settings", "Settings Menu Placeholder")
    
    
def open_image():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

    if file_path:
        image = Image.open(file_path)
        image = image.resize((100, 100), Image.ANTIALIAS)  # Resize the image if needed
        photo = ImageTk.PhotoImage(image)

        # Update the image in the info_text Text widget
        info_text.image_create(tk.END, image=photo)
        info_text.image = photo  # Keep a reference to avoid garbage collection


# Create the main window
window = tk.Tk()
window.title("Patient Profiles")

# Set the window size
window.geometry("800x600")

# Patient profiles data (replace this with your actual data)
profiles_list = [
    {"name": "John Doe", "age": 30, "gender": "Male"},
    {"name": "Jane Smith", "age": 25, "gender": "Female"},
    {"name": "Alice Johnson", "age": 35, "gender": "Female"},
    {"name": "Bob Brown", "age": 28, "gender": "Male"},
    # Add more profiles as needed
]

# Left side - Search and Patient Profiles List
search_frame = tk.Frame(window)
search_frame.pack(side=tk.TOP, fill=tk.X)

search_label = tk.Label(search_frame, text="Search by Name:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(search_frame, text="Search", command=search_by_name)
search_button.pack(side=tk.LEFT, padx=5)



profiles_listbox = tk.Listbox(window, selectmode=tk.SINGLE, width=20)  # Reduced width
profiles_listbox.pack(side=tk.LEFT, fill=tk.Y)
profiles_listbox.bind("<<ListboxSelect>>", on_selection)

#Setting Menu
setting_button = tk.Button(search_frame, text="Settings",command=show_settings_menu)
setting_button.pack(side=tk.BOTTOM, anchor=tk.SW, pady=10)

image_button = tk.Button(search_frame, text="Open Image", command=open_image)
image_button.pack(side=tk.BOTTOM, anchor=tk.SW, pady=10)

# Populate the listbox with patient names
for profile in profiles_list:
    profiles_listbox.insert(tk.END, profile["name"])

# Right side - Patient Information
info_text = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED, height=5, width=20)
info_text.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

# Initial selection
profiles_listbox.select_set(0)
initial_profile = profiles_list[0]
update_profile_info(initial_profile)

# Start the tkinter main loop
window.mainloop()
