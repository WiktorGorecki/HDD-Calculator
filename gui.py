import tkinter as tk
from tkinter import messagebox
import os
from utils import run_plugin, load_plugins

# Create the main application window
window = tk.Tk()
window.title("HDD Calculator")
window.geometry("400x300")

# Create and configure widgets
label = tk.Label(window, text="HDD Calculator", font=("Arial", 16))
label.pack(pady=10)


def handle_plugins_menu():
    plugins = load_plugins()

    def handle_plugin_selection(plugin_path):
        result = run_plugin(plugin_path)

        # Display the drive and statistics
        if result:
            disk_space, word_width, number_of_blocks, address_width = result
            show_drive_info(disk_space, word_width, number_of_blocks, address_width)

    if not plugins:
        messagebox.showinfo("No Plugins", "No plugins found.")
        return

    plugin_window = tk.Toplevel(window)
    plugin_window.title("Plugins")

    label = tk.Label(plugin_window, text="Choose a plugin:")
    label.pack(pady=10)

    for index, plugin in enumerate(plugins, start=1):
        plugin_name = os.path.splitext(os.path.basename(plugin))[0]
        button = tk.Button(plugin_window, text=plugin_name, command=lambda path=plugin: handle_plugin_selection(path))
        button.pack()


def handle_exit():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        window.destroy()


def show_drive_info(disk_space, word_width, number_of_blocks, address_width):
    info_window = tk.Toplevel(window)
    info_window.title("Drive Information")

    label = tk.Label(info_window, text="Drive Information:")
    label.pack(pady=10)

    # Display drive details
    label = tk.Label(info_window, text=f"Disk Space: {disk_space}")
    label.pack()
    label = tk.Label(info_window, text=f"Word Width: {word_width}")
    label.pack()
    label = tk.Label(info_window, text=f"Number of Blocks: {number_of_blocks}")
    label.pack()
    label = tk.Label(info_window, text=f"Address Width: {address_width}")
    label.pack()

    # Calculate statistics
    blanks = disk_space - ((word_width * number_of_blocks) + (address_width * number_of_blocks))
    effective_capacity = number_of_blocks * word_width
    assigned_space = round(((disk_space - blanks) / disk_space) * 100)
    address_percentage = round(((address_width * number_of_blocks) / disk_space) * 100)
    word_percentage = round(((word_width * number_of_blocks / disk_space) * 100))
    unassigned_space = round((blanks / disk_space) * 100)

    label = tk.Label(info_window, text="Statistics:")
    label.pack(pady=10)

    # Display statistics
    label = tk.Label(info_window, text=f"Effective Capacity: {effective_capacity}b")
    label.pack()
    label = tk.Label(info_window, text=f"Assigned Space: {assigned_space}%")
    label.pack()
    label = tk.Label(info_window, text=f"   - Addresses: {address_percentage}%")
    label.pack()
    label = tk.Label(info_window, text=f"   - Words: {word_percentage}%")
    label.pack()
    label = tk.Label(info_window, text=f"Unassigned Space: {unassigned_space}%")
    label.pack()


# Create buttons
btn_plugins_menu = tk.Button(window, text="Plugins", command=handle_plugins_menu)
btn_plugins_menu.pack(pady=10)

btn_exit = tk.Button(window, text="Exit", command=handle_exit)
btn_exit.pack(pady=10)

# Start the main event loop
window.mainloop()
