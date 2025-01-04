import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading
import platform
import subprocess
import time
from tkinter import PhotoImage

# Function to check internet connectivity
def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

# Function to monitor internet connection (during execution)
def monitor_internet():
    disconnected_start = None
    while True:
        if not check_internet():
            if disconnected_start is None:
                messagebox.showwarning("Internet Connection Warning", "Your internet connection is lost. Please check your internet.")
                disconnected_start = time.time()
            elif time.time() - disconnected_start >= 10:
                messagebox.showerror("Internet Disconnection", "Internet connection has been lost for more than 10 seconds. The program will close.")
                root.destroy()
                break
        else:
            disconnected_start = None
        time.sleep(1)

# Function to execute another Python file
def execute_other_python_file():
    try:
        # Replace 'other_script.py' with the path of the desired Python file
        subprocess.run(["python", "main.py"], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Error in executing another file:\n{e}")

# Function to display the final screen
def show_final_screen():
    final_window = tk.Toplevel(root)
    final_window.title("Final Operations")
    final_window.geometry("400x200")
    final_window.resizable(False, False)
    tk.Label(final_window, text="All operations have been successfully completed.", fg="#2e8b57").pack(pady=20)
    tk.Button(final_window, text="Execute Another File", command=execute_other_python_file, bg="#008cba", fg="white", relief="groove").pack(pady=10)

# Function to update the first progress bar
def update_progress_1():
    global progress_1
    if progress_1 < 100:
        progress_1 += 100 / (2 * 60 * 10)  # Complete in 2 minutes
        progress_bar_1['value'] = progress_1
        percent_label_1.config(text=f"{int(progress_1)}%")
        root.after(100, update_progress_1)
    else:
        percent_label_1.config(text="100%")
        status_label_1.config(text="✔ Installation Completed", fg="#2e8b57")
        check_all_progress_complete()

# Function to update the second progress bar
def update_progress_2():
    global progress_2
    if progress_2 < 100:
        progress_2 += 100 / (60 * 10)  # Complete in 1 minute
        progress_bar_2['value'] = progress_2
        percent_label_2.config(text=f"{int(progress_2)}%")
        root.after(100, update_progress_2)
    else:
        percent_label_2.config(text="100%")
        status_label_2.config(text="✔ Loading Completed", fg="#2e8b57")
        check_all_progress_complete()

# Function to update the third progress bar (10 seconds)
def update_progress_3():
    global progress_3
    if progress_3 < 100:
        progress_3 += 100 / (10 * 10)  # Complete in 10 seconds
        progress_bar_3['value'] = progress_3
        percent_label_3.config(text=f"{int(progress_3)}%")
        root.after(100, update_progress_3)
    else:
        percent_label_3.config(text="100%")
        status_label_3.config(text="✔ Operation Completed", fg="#2e8b57")
        check_all_progress_complete()

# Function to check whether all progress bars are completed
def check_all_progress_complete():
    if progress_1 >= 100 and progress_2 >= 100 and progress_3 >= 100:
        show_final_screen()

# Verify operating system
if platform.system() != "Windows":
    def exit_program():
        os_specific_root.destroy()
        exit()
    
    os_specific_root = tk.Tk()
    os_specific_root.title("Unsupported OS")
    os_specific_root.geometry("400x200")
    os_specific_root.resizable(False, False)
    warning_label = tk.Label(os_specific_root, text="This program can only be executed on Windows.")
    warning_label.pack(pady=20)
    exit_button = tk.Button(os_specific_root, text="Exit", command=exit_program)
    exit_button.pack(pady=20)
    os_specific_root.mainloop()

# Create main window
root = tk.Tk()
root.title("Progress Bar - Tkinter Project")
root.geometry("500x650")
root.configure(bg="#f0f8ff")  # Background color

# Define progress bar style
style = ttk.Style(root)
style.theme_use('default')
style.configure("Blue.Horizontal.TProgressbar", troughcolor='white', background='#008cba', thickness=20)

progress_1 = 0
progress_2 = 0
progress_3 = 0

# Check initial internet connection
if not check_internet():
    messagebox.showerror("Internet Disconnection", "Please check your internet connection. The program will close.")
    exit()

# Field 1
progress_label_1 = tk.Label(root, text="Installing data from server onto device", bg="#f0f8ff")
progress_label_1.pack(pady=5)
progress_bar_1 = ttk.Progressbar(root, length=300, mode="determinate", style="Blue.Horizontal.TProgressbar")
progress_bar_1.pack(pady=10)
percent_label_1 = tk.Label(root, text="0%", bg="#f0f8ff")
percent_label_1.pack()
status_label_1 = tk.Label(root, text="", bg="#f0f8ff") 
status_label_1.pack()

# Field 2
progress_label_2 = tk.Label(root, text="Copying default data", bg="#f0f8ff")
progress_label_2.pack(pady=20)
progress_bar_2 = ttk.Progressbar(root, length=300, mode="determinate", style="Blue.Horizontal.TProgressbar")
progress_bar_2.pack(pady=10)
percent_label_2 = tk.Label(root, text="0%", bg="#f0f8ff")
percent_label_2.pack()
status_label_2 = tk.Label(root, text="", bg="#f0f8ff") 
status_label_2.pack()

# Field 3
progress_label_3 = tk.Label(root, text="Identifying OS and its details", bg="#f0f8ff")
progress_label_3.pack(pady=20)
progress_bar_3 = ttk.Progressbar(root, length=300, mode="determinate", style="Blue.Horizontal.TProgressbar")
progress_bar_3.pack(pady=10)
percent_label_3 = tk.Label(root, text="0%", bg="#f0f8ff")
percent_label_3.pack()
status_label_3 = tk.Label(root, text="", bg="#f0f8ff") 
status_label_3.pack()

# Launch internet monitoring thread
internet_thread = threading.Thread(target=monitor_internet, daemon=True)
internet_thread.start()

# Start progress bars
update_progress_1()
update_progress_2()
update_progress_3()

root.mainloop()
