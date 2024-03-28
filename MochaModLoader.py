# MochaMod Loader 
# This application is meant to help install mod folders to the users existing mod folder in their Minecraft directory (assuming they didnt move the folder from default location)

import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
import getpass

def replace_mod_folder():
    source_folder = filedialog.askdirectory(title="Select Your Mod Folder")
    username = getpass.getuser()
    target_folder = f"C:/Users/{username}/AppData/Roaming/.minecraft/mods"
    
    # Display a warning message
    confirmed = messagebox.askokcancel("MochaMod Loader Warning!", "Once you agree this cannot be undone! Please verify!")
    
    # If user cancels the operation, return to the main menu
    if not confirmed:
        messagebox.showwarning("Stopping Operating","Current Mod Folder will not be changed!")
        return

    try:
        # Check if the source folder exists
        if not os.path.exists(source_folder):
            messagebox.showerror("Error", f"Source folder '{source_folder}' not found.")
            return
        
        # Delete the contents of the target folder
        for item in os.listdir(target_folder):
            item_path = os.path.join(target_folder, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            else:
                shutil.rmtree(item_path)
        
        # Copy the contents of the source folder to the target folder
        for item in os.listdir(source_folder):
            source_item_path = os.path.join(source_folder, item)
            target_item_path = os.path.join(target_folder, item)
            if os.path.isfile(source_item_path):
                shutil.copy2(source_item_path, target_item_path)
            else:
                shutil.copytree(source_item_path, target_item_path)
        
        messagebox.showinfo("Success", "Mod folder replaced successfully.")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def open_mod_folder():
    username = getpass.getuser()
    mod_folder = f"C:/Users/{username}/AppData/Roaming/.minecraft/mods"
    os.startfile(mod_folder)
    
def refresh_contents_list():
    username = getpass.getuser()
    mod_folder = f"C:/Users/{username}/AppData/Roaming/.minecraft/mods"
    update_contents_list(mod_folder)    

def show_about():
    messagebox.showinfo("About", "MochaMod Loader\n\nVersion 1.4\n\nCreated by Xanadu Systems (ShiroNet)")

def show_usage():
    messagebox.showinfo("How to Use", "To use the software, follow these steps:\n\n1. Click the 'Replace Mod Folder' button to select your mod folder.\n2. Click the 'Open Mod Folder' button to open the current mod folder.\n3. Click the refresh button to verify that your mod folder has changed\n Enjoy using MochaMod Loader!")

def show_log_notes():
    try:
        # Open the .txt file containing the log notes
        with open("log_notes.txt", "r", encoding="utf-8") as file:
            log_notes_content = file.read()
            
        # Create a new window to display the log notes
        log_notes_window = tk.Toplevel(root)
        log_notes_window.title("ShrioNet's Log Notes")

        # Create a Text widget to display the log notes
        log_text = tk.Text(log_notes_window, wrap=tk.WORD)
        log_text.pack(expand=True, fill=tk.BOTH)

        # Populate the Text widget with the content of the log notes
        log_text.insert(tk.END, log_notes_content)
        log_text.config(state=tk.DISABLED)  # Disable text editing

        # Create a vertical scrollbar and associate it with the Text widget
        scrollbar = tk.Scrollbar(log_notes_window, command=log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        log_text.config(yscrollcommand=scrollbar.set)

    except FileNotFoundError:
        messagebox.showerror("Error", "Log notes file not found.")

# Update the list that contains the mods
def update_contents_list(folder):
    contents_list.delete(0, tk.END)
    for item in os.listdir(folder):
        contents_list.insert(tk.END, item)

# Create the main window
root = tk.Tk()
root.title("MochaMod Loader")
root.resizable(False, False)  # Prevent resizing

# Create a menu strip
menu_strip = tk.Menu(root)
root.config(menu=menu_strip)

# Create a submenu for "Help"
help_menu = tk.Menu(menu_strip, tearoff=0)
help_menu.add_command(label="About", command=show_about)
help_menu.add_command(label="How to Use the Software", command=show_usage)
menu_strip.add_cascade(label="Help", menu=help_menu)
menu_strip.add_cascade(label="ShrioNet's Log Notes", command=show_log_notes)

# Create a marquee label
marquee_text = "Please select the correct folder that contain your mods before uploading!                                        "  # Extra spaces added
marquee_label = tk.Label(root, text=marquee_text, font=("Arial", 10), fg="blue")
marquee_label.pack()

# Create a function to move the marquee text horizontally
def move_marquee():
    global marquee_text
    marquee_text = marquee_text[1:] + marquee_text[0]
    marquee_label.config(text=marquee_text)
    marquee_label.after(100, move_marquee)  # Update every 100 milliseconds

move_marquee()  # Start the marquee animation

# Create and pack a title label
title_label = tk.Label(root, text="MochaMod Loader", font=("Arial", 16))
title_label.pack(pady=10)

# Create and pack a button to replace the mod folder
replace_button = tk.Button(root, text="Replace Mod Folder", command=replace_mod_folder)
replace_button.pack(pady=10)

# Create and pack a button to open the current mod folder
open_button = tk.Button(root, text="Open Mod Folder", command=open_mod_folder)
open_button.pack(pady=5)

# Create a label to display the current mod folder
username = getpass.getuser()
mod_folder_path = f"C:/Users/{username}/AppData/Roaming/.minecraft/mods"
current_mod_folder_label = tk.Label(root, text=f"Current Mod Folder: {mod_folder_path}")
current_mod_folder_label.pack(pady=5)

# Create and pack a title label
mod_folder_path_label = tk.Label(root, text="Current Mods in Folder", font=("Arial", 10))
mod_folder_path_label.pack(pady=2)

# Create a refresh button to update the contents of the mod folder list
refresh_button = tk.Button(root, text="Refresh Mod List", command=refresh_contents_list)
refresh_button.pack(pady=2)

# Create a listbox to display the contents of the mod folder
contents_list = tk.Listbox(root)
contents_list.pack(pady=5, expand=True, fill=tk.BOTH)

# Populate the listbox with the contents of the mod folder
update_contents_list(mod_folder_path)

# Create a label for the application creator
creator_label = tk.Label(root, text="Application created by Xanadu Systems (ShiroNet)")
creator_label.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()

