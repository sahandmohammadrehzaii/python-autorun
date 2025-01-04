import tkinter as tk
import subprocess
import sys

def open_python_file(file_name):
    try:
        subprocess.Popen([sys.executable, file_name])
        
        root.destroy()
    except Exception as e:
        print(f"خطا در باز کردن فایل {file_name}: {e}")

root = tk.Tk()
root.title("File Installation")
root.geometry("400x500")

root.configure(bg="#f0f8ff")

label = tk.Label(root, text="Select a file to execute", font=("Arial", 14), bg="#f0f8ff", fg="#333")
label.pack(pady=20)

files = [("English", "Installation/EN/terms/terms.py"),
         ("Arabic", "Installation/AR/terms/terms.py"),
         ("Farsi", "Installation/Fa/terms/terms.py"),
         ("Türkçe", "Installation/Tü/terms/terms.py")]

for file in files:
    button = tk.Button(root, text=file[0], 
                       command=lambda file_name=file[1]: open_python_file(file_name),
                       font=("Arial", 12), bg="#17a2b8", fg="white", width=20, height=2)
    button.pack(pady=10)

root.mainloop()