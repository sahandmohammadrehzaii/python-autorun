import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading
import platform
import subprocess
import time
from tkinter import PhotoImage

# تابع بررسی اتصال به اینترنت
def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

# تابع بررسی اتصال اینترنت در ده ثانیه (حین اجرا)
def monitor_internet():
    disconnected_start = None
    while True:
        if not check_internet():
            if disconnected_start is None:
                messagebox.showwarning("هشدار قطع اینترنت", "اتصال اینترنت شما قطع شده است. لطفاً اینترنت خود را بررسی کنید.")
                disconnected_start = time.time()
            elif time.time() - disconnected_start >= 10:
                messagebox.showerror("قطع اتصال اینترنت", "اتصال به اینترنت بیش از ۱۰ ثانیه قطع بود. برنامه بسته خواهد شد.")
                root.destroy()
                break
        else:
            disconnected_start = None
        time.sleep(1)

# تابع برای اجرای فایل پایتون دیگر
def execute_other_python_file():
    try:
        # جایگزین 'other_script.py' با مسیر فایل پایتون موردنظر
        subprocess.run(["python", "main.py"], check=True)
    except Exception as e:
        messagebox.showerror("خطا", f"خطا در اجرای فایل دیگر:\n{e}")

# تابع برای نمایش صفحه پایانی
def show_final_screen():
    final_window = tk.Toplevel(root)
    final_window.title("عملیات نهایی")
    final_window.geometry("400x200")
    final_window.resizable(False, False)
    tk.Label(final_window, text="تمام عملیات موفقیت‌آمیز به پایان رسید.", fg="#2e8b57").pack(pady=20)
    tk.Button(final_window, text="اجرای فایل دیگر", command=execute_other_python_file, bg="#008cba", fg="white", relief="groove").pack(pady=10)

# تابع برای به‌روزرسانی نوار پیشرفت اول
def update_progress_1():
    global progress_1
    if progress_1 < 100:
        progress_1 += 100 / (2 * 60 * 10)  # پر شدن در 2 دقیقه
        progress_bar_1['value'] = progress_1
        percent_label_1.config(text=f"{int(progress_1)}%")
        root.after(100, update_progress_1)
    else:
        percent_label_1.config(text="100%")
        status_label_1.config(text="✔ نصب کامل شد", fg="#2e8b57")
        check_all_progress_complete()

# تابع برای به‌روزرسانی نوار پیشرفت دوم
def update_progress_2():
    global progress_2
    if progress_2 < 100:
        progress_2 += 100 / (60 * 10)  # پر شدن در 1 دقیقه
        progress_bar_2['value'] = progress_2
        percent_label_2.config(text=f"{int(progress_2)}%")
        root.after(100, update_progress_2)
    else:
        percent_label_2.config(text="100%")
        status_label_2.config(text="✔ بارگیری کامل شد", fg="#2e8b57")
        check_all_progress_complete()

# تابع برای به‌روزرسانی نوار پیشرفت سوم (10 ثانیه)
def update_progress_3():
    global progress_3
    if progress_3 < 100:
        progress_3 += 100 / (10 * 10)  # پر شدن در 10 ثانیه
        progress_bar_3['value'] = progress_3
        percent_label_3.config(text=f"{int(progress_3)}%")
        root.after(100, update_progress_3)
    else:
        percent_label_3.config(text="100%")
        status_label_3.config(text="✔ عملیات انجام شد", fg="#2e8b57")
        check_all_progress_complete()

# تابع بررسی تکمیل تمامی نوارهای پیشرفت
def check_all_progress_complete():
    if progress_1 >= 100 and progress_2 >= 100 and progress_3 >= 100:
        show_final_screen()

# بررسی سیستم عامل
if platform.system() != "Windows":
    def exit_program():
        os_specific_root.destroy()
        exit()
    
    os_specific_root = tk.Tk()
    os_specific_root.title("غیرقابل اجرا")
    os_specific_root.geometry("400x200")
    os_specific_root.resizable(False, False)
    warning_label = tk.Label(os_specific_root, text="این برنامه فقط بر روی سیستم عامل ویندوز قابل اجرا است.")
    warning_label.pack(pady=20)
    exit_button = tk.Button(os_specific_root, text="خروج", command=exit_program)
    exit_button.pack(pady=20)
    os_specific_root.mainloop()

# ایجاد پنجره اصلی
root = tk.Tk()
root.title("Progress Bar - پروژه با tkinter")
root.geometry("500x650")
root.configure(bg="#f0f8ff")  # رنگ پس‌زمینه

# تعریف استایل نوار پیشرفت
style = ttk.Style(root)
style.theme_use('default')
style.configure("Blue.Horizontal.TProgressbar", troughcolor='white', background='#008cba', thickness=20)

progress_1 = 0
progress_2 = 0
progress_3 = 0

# بررسی اتصال اولیه به اینترنت
if not check_internet():
    messagebox.showerror("قطع اینترنت", "لطفاً اتصال اینترنت خود را بررسی کنید. برنامه بسته خواهد شد.")
    exit()

# فیلد 1
progress_label_1 = tk.Label(root, text="نصب اطلاعات از سرور بر روی دستگاه", bg="#f0f8ff")
progress_label_1.pack(pady=5)
progress_bar_1 = ttk.Progressbar(root, length=300, mode="determinate", style="Blue.Horizontal.TProgressbar")
progress_bar_1.pack(pady=10)
percent_label_1 = tk.Label(root, text="0%", bg="#f0f8ff")
percent_label_1.pack()
status_label_1 = tk.Label(root, text="", bg="#f0f8ff") 
status_label_1.pack()

# فیلد 2
progress_label_2 = tk.Label(root, text="کپي کردن داده هاي پيش فرض", bg="#f0f8ff")
progress_label_2.pack(pady=20)
progress_bar_2 = ttk.Progressbar(root, length=300, mode="determinate", style="Blue.Horizontal.TProgressbar")
progress_bar_2.pack(pady=10)
percent_label_2 = tk.Label(root, text="0%", bg="#f0f8ff")
percent_label_2.pack()
status_label_2 = tk.Label(root, text="", bg="#f0f8ff") 
status_label_2.pack()

# فیلد 3
progress_label_3 = tk.Label(root, text="شناسايي سيستم عامل و اطلاعات آن", bg="#f0f8ff")
progress_label_3.pack(pady=20)
progress_bar_3 = ttk.Progressbar(root, length=300, mode="determinate", style="Blue.Horizontal.TProgressbar")
progress_bar_3.pack(pady=10)
percent_label_3 = tk.Label(root, text="0%", bg="#f0f8ff")
percent_label_3.pack()
status_label_3 = tk.Label(root, text="", bg="#f0f8ff") 
status_label_3.pack()

# مانیتورینگ اینترنت
internet_thread = threading.Thread(target=monitor_internet, daemon=True)
internet_thread.start()

# شروع نوارهای پیشرفت
update_progress_1()
update_progress_2()
update_progress_3()

root.mainloop()
