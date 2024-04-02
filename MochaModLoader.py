# MochaMod Loader 
# This application is meant to help install mod folders to the users existing mod folder in their Minecraft directory (assuming they didn't move the folder from default location)

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext,PhotoImage
import getpass
import platform
import webbrowser

# MochaMod Loader Version number global variable
SOFTWARE_VERSION = "1.5.2"

def replace_mod_folder():
    source_folder = filedialog.askdirectory(title="Select Your Mod Folder")
    username = getpass.getuser()

    # This checks for all systems that I have added (because theres going to be someone who is using a macOS machine and cannot find their mod folder..)
    if platform.system() == "Windows":
        target_folder = f"C:/Users/{username}/AppData/Roaming/.minecraft/mods"
    elif platform.system() == "Darwin":  # macOS
        target_folder = f"/Users/{username}/Library/Application Support/minecraft/mods"
    elif platform.system() == "Linux":
        target_folder = f"/home/{username}/.minecraft/mods"
    else:
        messagebox.showerror("Unsupported OS", "This operating system is not supported.")
        return

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

# Opens the mod folder that the system found or that the user has preselected.
def open_mod_folder():
    username = getpass.getuser()

    if platform.system() == "Windows":
        mod_folder = f"C:/Users/{username}/AppData/Roaming/.minecraft/mods"
    elif platform.system() == "Darwin":  # macOS
        mod_folder = f"/Users/{username}/Library/Application Support/minecraft/mods"
    elif platform.system() == "Linux":
        mod_folder = f"/home/{username}/.minecraft/mods"
    else:
        messagebox.showerror("Unsupported OS", "This operating system is not supported.")
        return

    os.startfile(mod_folder)

# Function to clear the mod folder that was selected (we made sure to let the user know because this shit cannot be reversed..)    
def clear_mod_folder():
    username = getpass.getuser()

    if platform.system() == "Windows":
        mod_folder = f"C:/Users/{username}/AppData/Roaming/.minecraft/mods"
    elif platform.system() == "Darwin":  # macOS
        mod_folder = f"/Users/{username}/Library/Application Support/minecraft/mods"
    elif platform.system() == "Linux":
        mod_folder = f"/home/{username}/.minecraft/mods"
    else:
        messagebox.showerror("Unsupported OS", "This operating system is not supported.")
        return

    confirmed = messagebox.askokcancel("Clear Mod Folder", "Are you sure you want to clear the mod folder? This action cannot be undone.")

    if confirmed:
        try:
            # Delete the contents of the mod folder
            for item in os.listdir(mod_folder):
                item_path = os.path.join(mod_folder, item)
                if os.path.isfile(item_path):
                    os.unlink(item_path)
                else:
                    shutil.rmtree(item_path)
            messagebox.showinfo("Success", "Mod folder cleared successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")    
    
# Function to refresh the users folder under the list box we added in the GUI
def refresh_contents_list():
    username = getpass.getuser()

    if platform.system() == "Windows":
        mod_folder = f"C:/Users/{username}/AppData/Roaming/.minecraft/mods"
    elif platform.system() == "Darwin":  # macOS
        mod_folder = f"/Users/{username}/Library/Application Support/minecraft/mods"
    elif platform.system() == "Linux":
        mod_folder = f"/home/{username}/.minecraft/mods"
    else:
        messagebox.showerror("Unsupported OS", "This operating system is not supported.")
        return

    update_contents_list(mod_folder)

# Function for the about window
def show_about():
    about_text = f"MochaMod Loader\n\nVersion {SOFTWARE_VERSION}\n\nCreated by Xanadu Systems (Developer: ShiroNet)\n\nAllows mod folders to be replaced easily with a GUI"
                
    # Load the logo image using PhotoImage
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
            logo_image = tk.PhotoImage(file=logo_path)
    else:
            logo_image = None

    # Toplevel window for the about message box
    about_window = tk.Toplevel(root.master)
    about_window.title("About Software")
    # Set the size of the about window
    about_window.geometry("400x300") 
    about_window.resizable(False,False)

    # Make the about window set frozen
    about_window.grab_set()

    # Display the logo image if available
    if logo_image:
        logo_label = tk.Label(about_window, image=logo_image)
        logo_label.image = logo_image  # Keep a reference to prevent garbage collection
        logo_label.pack(pady=5)

    # Display the about text
    about_label = tk.Label(about_window, text=about_text)
    about_label.pack(pady=5)

    # Add a button to close the about window
    close_button = tk.Button(about_window, text="Close", command=lambda: close_about(about_window))
    close_button.pack(pady=5)

def close_about(about_window):
    about_window.grab_release()  # Release the grab so main window can be clicked
    about_window.destroy()

# OLD CODE 
#def show_about():
#messagebox.showinfo("About", f"MochaMod Loader\n\nVersion {SOFTWARE_VERSION}\n\nCreated by Xanadu Systems (ShiroNet)")

def show_usage():
    messagebox.showinfo("How to Use", "To use the software, follow these steps:\n\n1. Click the 'Replace Mod Folder' button to select your mod folder.\n2. Click the 'Open Mod Folder' button to open the current mod folder.\n3. Click the refresh button to verify that your mod folder has changed\n Enjoy using MochaMod Loader!")

def open_github():
    website_url = "https://github.com/Shiro-Net"
    webbrowser.open(website_url)
    
def show_log_notes():
    try:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to the log file
        log_file_path = os.path.join(script_dir, "log_notes.txt")

        # Open the .txt file containing the log notes
        with open(log_file_path, "r", encoding="utf-8") as file:
            log_notes_content = file.read()
            
        # Create a new window to display the log notes
        log_notes_window = tk.Toplevel(root)
        log_notes_window.title("ShrioNet's Log Notes")
        # Set the size of the about window
        log_notes_window.geometry("850x500") 
        log_notes_window.resizable(False,False)

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
        
        # Make the about window modal
        log_notes_window.grab_set()  

    except Exception as e:
        print("Exception occurred:", e)  # Print out the exception
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        #If this happens im not sure what the fuck happened to that log_notes ¯\_(ツ)_/¯ that shit gone for real, you can probably download it from the repo or some shit.

def close_log_note(log_notes_window):
    log_notes_window.grab_release()  # Release the grab so main window can be clicked
    log_notes_window.destroy()

# Update the list that contains the mods
def update_contents_list(folder):
    contents_list.delete(0, tk.END)
    if not os.path.exists(folder):
        messagebox.showerror("Error", f"Mod folder '{folder}' not found.")
        return
    
    try:
        for item in os.listdir(folder):
            contents_list.insert(tk.END, item)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("MochaMod Loader")
root.resizable(False, False)  # Prevent resizing

    # Set the icon
icon_path = os.path.join(os.path.dirname(__file__), "MochaModIcon.ico")
if os.path.exists(icon_path):
    root.iconbitmap(default=icon_path)
else:
    print("Error: Icon file not found.")


# Function to determine OS color
def get_os_color():
    system = platform.system()
    if system == "Windows":
        return "blue"
    elif system == "Darwin":  # macOS
        return "red"
    elif system == "Linux":
        return "orange"
    else:
        return "black"  # Default color 
    
# Create a menu strip
menu_strip = tk.Menu(root)
root.config(menu=menu_strip)

# Create a "Help" submenu
help_menu = tk.Menu(menu_strip, tearoff=0)
help_menu.add_command(label="About", command=show_about)
help_menu.add_command(label="How to Use the Software", command=show_usage)
menu_strip.add_cascade(label="Help", menu=help_menu)

# Create a "ShrioNet's Log Notes" submenu
log_notes_menu = tk.Menu(menu_strip, tearoff=0)
log_notes_menu.add_command(label="View Log Notes", command=show_log_notes)
menu_strip.add_cascade(label="ShrioNet's Log Notes", menu=log_notes_menu)

# Create a "ShiroNet's Github" submenu
github_menu = tk.Menu(menu_strip, tearoff=0)
github_menu.add_command(label="Open Github", command=open_github)
menu_strip.add_cascade(label="ShiroNet's Github", menu=github_menu)


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
username = getpass.getuser() # sick username bro
mod_folder_path = f"C:/Users/{username}/AppData/Roaming/.minecraft/mods"
current_mod_folder_label = tk.Label(root, text=f"Current Mod Folder: {mod_folder_path}")
current_mod_folder_label.pack(pady=5)

# Create and pack a title label
mod_folder_path_label = tk.Label(root, text="Current Mods in Folder", font=("Arial", 10))
mod_folder_path_label.pack(pady=2)

# Add a button to clear the mod folder
clear_button = tk.Button(root, text="Clear Mod Folder", command=clear_mod_folder)
clear_button.pack(pady=5)

# Create a refresh button to update the contents of the mod folder list
refresh_button = tk.Button(root, text="Refresh Mod List", command=refresh_contents_list)
refresh_button.pack(pady=2)

# Label for the list
list_label = tk.Label(root, text="Current Directory", font=("Arial", 8, "bold"))
list_label.pack(side=tk.TOP, anchor='w')  # Positioned below the creator label, aligned to the left'

# Create a listbox to display the contents of the mod folder
contents_list = tk.Listbox(root)
contents_list.pack(pady=5, expand=True, fill=tk.BOTH)

# Populate the listbox with the contents of the mod folder
update_contents_list(mod_folder_path)

# Detected operating system label
os_system_label = tk.Label(root, text=platform.system(), font=("Arial", 10, "bold"), fg=get_os_color())
os_system_label.pack(pady=3, side=tk.RIGHT)  # Positioned on the right

# Add OS label (For the people that dont know what OS they are using, which they should know but you know..theres people out there)
os_label = tk.Label(root, text="Current OS:", font=("Arial", 10, "bold"))
os_label.pack(pady=3, side=tk.RIGHT)  # Positioned on the right side of the screen

# Add creator label
creator_label = tk.Label(root, text="Application created by Xanadu Systems (ShiroNet)", fg="green")
creator_label.pack(side=tk.TOP, anchor='w')  # Positioned on the top of the menu screen, aligned to the left

# Add software version label
version_label = tk.Label(root, text="Version: " + SOFTWARE_VERSION, font=("Arial", 8, "bold"))
version_label.pack(side=tk.TOP, anchor='w')  # Positioned below the creator label, aligned to the left

# Run the Tkinter event loop
root.mainloop()
