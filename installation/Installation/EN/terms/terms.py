import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import sqlite3
import os

# Connect to SQLite database or create it if it doesn't exist
def setup_database():
    conn = sqlite3.connect('database/user_installation_data/user_data.db')  # Create or connect to the database file
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_agreement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            agreed_on DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Log user agreement in the database
def log_user_agreement(user_name="Anonymous"):
    conn = sqlite3.connect('database/user_installation_data/user_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_agreement (username) VALUES (?)', (user_name,))
    conn.commit()
    conn.close()

# Function to open the final file
def open_python_file(file_name):
    try:
        # Find the absolute path of the file
        absolute_path = os.path.abspath(file_name)
        
        # Verify the file exists
        if not os.path.exists(absolute_path):
            raise FileNotFoundError(f"The requested file is not found: {absolute_path}")
        
        # Log user agreement in the database
        log_user_agreement()
        
        # Run the file with Python
        subprocess.Popen([sys.executable, absolute_path])
        
        # Close the user interface
        root.destroy()
    
    except FileNotFoundError as fnf_error:
        messagebox.showerror("Error", f"Error: {str(fnf_error)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while running the file:\n\n{str(e)}")

# Setup the database
setup_database()

# Main application window
root = tk.Tk()
root.title("Software Installation")
root.geometry("1000x600")
root.configure(bg="#f0f8ff")

terms_text = """\
Terms and Conditions

Welcome to Ghadaam-Famer. Before proceeding with the installation of this software, please read the following terms and conditions carefully. By clicking "Agree" or installing/using the program, you acknowledge that you have read, understood, and agreed to abide by these terms.
"""

license_text = """\
1. License Agreement

This software is licensed, not sold. The Ghadaam team grants you a limited, non-exclusive, non-transferable license to use this software for personal or commercial purposes in accordance with the terms set forth herein.
"""

privacy_text = """\
2. Privacy

By using this software, you agree to our privacy policy. The data collected during installation or usage may include, but is not limited to:

    Device information
    User preferences
    Crash reports

Your data will be handled securely and in accordance with our privacy guidelines.
"""

restrictions_text = """\
3. Restrictions

You agree not to:

    Copy, modify, adapt, or distribute the software.
    Reverse engineer, decompile, or disassemble any part of this software.
    Use the software for any illegal or malicious activities.
"""

disclaimer_text = """\
4. Disclaimer

The software is provided "as is" without any warranty of any kind, either express or implied. Ghadaam-Prime does not guarantee that the software will be free from defects, errors, or interruptions.
"""

termination_text = """\
5. Termination

Ghadaam-Prime reserves the right to terminate your access to the software at any time, without notice, for any reason, including a violation of these terms.
"""

liability_text = """\
6. Liability

Under no circumstances shall Ghadaam-Prime be liable for any direct, indirect, incidental, or consequential damages arising from the use or inability to use the software.
"""

governing_text = """\
7. Governing Laws

These terms and conditions are governed by the laws of Iran. Any disputes shall be exclusively resolved by the courts of this jurisdiction.
"""

contact_text = """\
8. Contact

For any inquiries or support, please contact us at:

    Email: mohammadrezaiisahand.com
    Phone: 09148407326
"""

agree_text = """\
9. By clicking "Agree" or proceeding with the installation, you confirm your acceptance of these terms and conditions and agree to abide by them.
"""

# Combine different texts into one
combined_text = f"{terms_text}\n\n{'_'*100}\n\n{license_text}\n\n{'_'*100}\n\n{privacy_text}\n\n{'_'*100}\n\n{restrictions_text}\n\n{'_'*100}\n\n{disclaimer_text}\n\n{'_'*100}\n\n{termination_text}\n\n{'_'*100}\n\n{liability_text}\n\n{'_'*100}\n\n{governing_text}\n\n{'_'*100}\n\n{contact_text}\n\n{'_'*100}\n\n{agree_text}"

# Use Scrollbar for long texts
frame = tk.Frame(root, bg="#f0f8ff")
frame.pack(padx=10, pady=10, expand=True, fill="both")

text_widget = tk.Text(frame, wrap="word", font=("Arial", 12), bg="#f0f8ff", fg="#333", height=15, relief="flat")
text_widget.insert("1.0", combined_text)
text_widget.config(state="disabled")  # Disabling text editing
text_widget.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
scrollbar.pack(side="right", fill="y")
text_widget.config(yscrollcommand=scrollbar.set)

# Create checkbox for agreement
agree_var = tk.BooleanVar()

def toggle_install_button():
    """Enable or disable the install button based on the checkbox state"""
    if agree_var.get():
        install_button.config(state="normal")
    else:
        install_button.config(state="disabled")

agree_checkbox = tk.Checkbutton(root, text="I agree to the terms and conditions", variable=agree_var, onvalue=True,
                                offvalue=False, command=toggle_install_button, font=("Arial", 12), bg="#f0f8ff")
agree_checkbox.pack(pady=10)

# Define install button
install_button = tk.Button(root, text="Install Application",
                           command=lambda: open_python_file("Installation/EN/final_installation/index.py"),
                           font=("Arial", 12), bg="#17a2b8", fg="white", width=20, height=2)
install_button.pack(pady=10)

# Disable the install button by default
install_button.config(state="disabled")

def open_additional_file():
    additional_file = "start.py"  # مسیر فایل پایتونی جدید را در اینجا قرار دهید
    open_python_file(additional_file)

# دکمه‌ای برای اجرای فایل پایتونی جدید (در گوشه پایین سمت راست)
additional_button = tk.Button(root, text="Previous", 
                              command=open_additional_file,
                              font=("Arial", 9), bg="#28a745", fg="white", width=6, height=1)
additional_button.pack(side="left", padx=10, pady=10)

# Run the application
root.mainloop()