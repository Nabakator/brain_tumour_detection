import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import mysql.connector

# Function to retrieve patient profiles from MySQL database
def retrieve_profiles():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Telefon2001",
        database="myDB"
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM patient_profiles')
    profiles = cursor.fetchall()
    
    conn.close()

    return profiles

# Function to handle selecting a patient from the list
def on_selection(event):
    selected_index = profiles_listbox.curselection()
    if selected_index:
        selected_profile = profiles_list[selected_index[0]]
        update_profile_info(selected_profile)

# Function to update the patient information on the right side
def update_profile_info(profile):
    info_text.config(state=tk.NORMAL)
    info_text.delete("1.0", tk.END)
    info_text.insert(tk.END, profile["name"] + "\n")
    info_text.insert(tk.END, "Age: " + str(profile["age"]) + "\n")
    info_text.insert(tk.END, "Gender: " + profile["gender"] + "\n")
    info_text.config(state=tk.DISABLED)

# Function to perform a search based on the entered name
def search_by_name():
    search_query = search_entry.get().lower()
    matching_profiles = [profile for profile in profiles_list if search_query in profile["name"].lower()]

    profiles_listbox.delete(0, tk.END)  # Clear the listbox

    for profile in matching_profiles:
        profiles_listbox.insert(tk.END, profile["name"])

# Function to show a placeholder settings menu
def show_settings_menu():
    messagebox.showinfo("Settings", "Settings Menu Placeholder")

# Function to open and display an image
def open_image():
    file_path = '/Users/angelor/Downloads/brain-lateral.png'
    
    if file_path:
        try:
            image = Image.open(file_path)
            image = image.resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            # Update the image in the label widget
            image_label.config(image=photo)
            image_label.image = photo  # Keep a reference to avoid garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Error loading the image: {e}")

# Function to open the dialog for adding a new patient
def open_add_patient_dialog():
    global add_patient_dialog
    add_patient_dialog = tk.Toplevel(window)
    add_patient_dialog.title("Add New Patient")

    # Entry widgets for input
    entry_name_dialog = tk.Entry(add_patient_dialog, width=20)
    entry_name_dialog.pack(pady=5)
    entry_age_dialog = tk.Entry(add_patient_dialog, width=5)
    entry_age_dialog.pack(pady=5)
    entry_gender_dialog = tk.Entry(add_patient_dialog, width=10)
    entry_gender_dialog.pack(pady=5)

    # Button to submit the information
    submit_button = tk.Button(add_patient_dialog, text="Add Patient", command=add_patient_from_dialog)
    submit_button.pack(pady=10)

# Function to add patient from the dialog
def add_patient_from_dialog():
    name = entry_name_dialog.get()
    age = entry_age_dialog.get()
    gender = entry_gender_dialog.get()

    # Validate input
    if not name or not age or not gender:
        messagebox.showwarning("Input Error", "Please enter valid information.")
        return

    # Add the new patient to the list
    new_patient = {"name": name, "age": int(age), "gender": gender}
    profiles_list.append(new_patient)

    # Update the listbox with the new patient
    profiles_listbox.insert(tk.END, name)

    # Clear the input fields
    entry_name_dialog.delete(0, tk.END)
    entry_age_dialog.delete(0, tk.END)
    entry_gender_dialog.delete(0, tk.END)

    # Close the dialog
    add_patient_dialog.destroy()


# Create the main window
window = tk.Tk()
window.title("Patient Profiles")

# Set the window size
window.geometry("800x600")

# Patient profiles data retrieved from MySQL
profiles_list = retrieve_profiles()

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

# Populate the listbox with patient names
for profile in profiles_list:
    profiles_listbox.insert(tk.END, profile["name"])

profiles_listbox.bind("<<ListboxSelect>>", on_selection)

# Setting Menu
setting_button = tk.Button(search_frame, text="Settings", command=show_settings_menu)
setting_button.pack(side=tk.BOTTOM, anchor=tk.SW, pady=10)

image_button = tk.Button(search_frame, text="Open Image", command=open_image)
image_button.pack(side=tk.BOTTOM, pady=10)

# Right side - Patient Information
info_text = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED, height=5, width=20)
info_text.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

# Image Label
image_label = tk.Label(window)
image_label.pack()

# Initial selection
profiles_listbox.select_set(0)
initial_profile = profiles_list[0]
update_profile_info(initial_profile)

# Entry widgets for input
entry_name = tk.Entry(window, width=20)
entry_name.pack(side=tk.LEFT, padx=5)
entry_age = tk.Entry(window, width=5)
entry_age.pack(side=tk.LEFT, padx=5)
entry_gender = tk.Entry(window, width=10)
entry_gender.pack(side=tk.LEFT, padx=5)

# Add New Patient button

add_patient_button = tk.Button(window, text="Add New Patient", command=open_add_patient_dialog)
add_patient_button.pack(side=tk.LEFT, padx=5)

# Start the tkinter main loop
window.mainloop()
