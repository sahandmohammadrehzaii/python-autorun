import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading
import platform
import subprocess
import time

# دالة التحقق من اتصال الإنترنت
def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

# دالة مراقبة اتصال الإنترنت خلال عشر ثوانٍ (أثناء التشغيل)
def monitor_internet():
    disconnected_start = None
    while True:
        if not check_internet():
            if disconnected_start is None:
                messagebox.showwarning("تحذير انقطاع الإنترنت", "تم فقدان اتصالك بالإنترنت. الرجاء التحقق من اتصالك.")
                disconnected_start = time.time()
            elif time.time() - disconnected_start >= 10:
                messagebox.showerror("انقطاع الإنترنت", "تم فقدان اتصال الإنترنت لأكثر من 10 ثوانٍ. سيتم إغلاق البرنامج.")
                root.destroy()
                break
        else:
            disconnected_start = None
        time.sleep(1)

# دالة تشغيل ملف بايثون آخر
def execute_other_python_file():
    try:
        # استبدل 'other_script.py' بمسار ملف البايثون المطلوب
        subprocess.run(["python", "main.py"], check=True)
    except Exception as e:
        messagebox.showerror("خطأ", f"خطأ أثناء تشغيل ملف آخر:\n{e}")

# دالة لعرض الشاشة النهائية
def show_final_screen():
    final_window = tk.Toplevel(root)
    final_window.title("العمليات النهائية")
    final_window.geometry("400x200")
    final_window.resizable(False, False)
    tk.Label(final_window, text="تم الانتهاء بنجاح من جميع العمليات.", fg="#2e8b57").pack(pady=20)
    tk.Button(final_window, text="تشغيل ملف آخر", command=execute_other_python_file, bg="#008cba", fg="white", relief="groove").pack(pady=10)

# دالة لتحديث شريط التقدم الأول
def update_progress_1():
    global progress_1
    if progress_1 < 100:
        progress_1 += 100 / (2 * 60 * 10)  # الاكتمال خلال دقيقتين
        progress_bar_1['value'] = progress_1
        percent_label_1.config(text=f"{int(progress_1)}%")
        root.after(100, update_progress_1)
    else:
        percent_label_1.config(text="100%")
        status_label_1.config(text="✔ تم التثبيت بنجاح", fg="#2e8b57")
        check_all_progress_complete()

# دالة لتحديث شريط التقدم الثاني
def update_progress_2():
    global progress_2
    if progress_2 < 100:
        progress_2 += 100 / (60 * 10)  # الاكتمال خلال دقيقة واحدة
        progress_bar_2['value'] = progress_2
        percent_label_2.config(text=f"{int(progress_2)}%")
        root.after(100, update_progress_2)
    else:
        percent_label_2.config(text="100%")
        status_label_2.config(text="✔ التحميل مكتمل", fg="#2e8b57")
        check_all_progress_complete()

# دالة لتحديث شريط التقدم الثالث (10 ثوانٍ)
def update_progress_3():
    global progress_3
    if progress_3 < 100:
        progress_3 += 100 / (10 * 10)  # الاكتمال خلال 10 ثوانٍ
        progress_bar_3['value'] = progress_3
        percent_label_3.config(text=f"{int(progress_3)}%")
        root.after(100, update_progress_3)
    else:
        percent_label_3.config(text="100%")
        status_label_3.config(text="✔ تم الانتهاء من العملية", fg="#2e8b57")
        check_all_progress_complete()

# دالة التحقق من اكتمال جميع أشرطة التقدم
def check_all_progress_complete():
    if progress_1 >= 100 and progress_2 >= 100 and progress_3 >= 100:
        show_final_screen()

# التحقق من نظام التشغيل
if platform.system() != "Windows":
    def exit_program():
        os_specific_root.destroy()
        exit()
    
    os_specific_root = tk.Tk()
    os_specific_root.title("غير قابل للتشغيل")
    os_specific_root.geometry("400x200")
    os_specific_root.resizable(False, False)
    warning_label = tk.Label(os_specific_root, text="هذا البرنامج يعمل فقط على نظام التشغيل Windows.")
    warning_label.pack(pady=20)
    exit_button = tk.Button(os_specific_root, text="خروج", command=exit_program)
    exit_button.pack(pady=20)
    os_specific_root.mainloop()

# إنشاء النافذة الرئيسية
root = tk.Tk()
root.title("Progress Bar - مشروع باستخدام tkinter")
root.geometry("500x650")
root.configure(bg="#f0f8ff")  # لون الخلفية

# تعريف نمط شريط التقدم
style = ttk.Style(root)
style.theme_use('default')
style.configure("Blue.Horizontal.TProgressbar", troughcolor='white', background='#008cba', thickness=20)

progress_1 = 0
progress_2 = 0
progress_3 = 0

# التحقق من الاتصال الأولي بالإنترنت
if not check_internet():
    messagebox.showerror("انقطاع الإنترنت", "الرجاء التحقق من اتصال الإنترنت الخاص بك. سيتم إغلاق البرنامج.")
    exit()

# الحقل 1
progress_label_1 = tk.Label(root, text="تثبيت البيانات من الخادم على الجهاز", bg="#f0f8ff")
progress_label_1.pack(pady=5)
progress_bar_1 = ttk.Progressbar(root, length=300, mode="determinate", style="Blue.Horizontal.TProgressbar")
progress_bar_1.pack(pady=10)
percent_label_1 = tk.Label(root, text="0%", bg="#f0f8ff")
percent_label_1.pack()
status_label_1 = tk.Label(root, text="", bg="#f0f8ff") 
status_label_1.pack()

# الحقل 2
progress_label_2 = tk.Label(root, text="نسخ البيانات الافتراضية", bg="#f0f8ff")
progress_label_2.pack(pady=20)
progress_bar_2 = ttk.Progressbar(root, length=300, mode="determinate", style="Blue.Horizontal.TProgressbar")
progress_bar_2.pack(pady=10)
percent_label_2 = tk.Label(root, text="0%", bg="#f0f8ff")
percent_label_2.pack()
status_label_2 = tk.Label(root, text="", bg="#f0f8ff") 
status_label_2.pack()

# الحقل 3
progress_label_3 = tk.Label(root, text="التعرف على نظام التشغيل ومعلوماته", bg="#f0f8ff")
progress_label_3.pack(pady=20)
progress_bar_3 = ttk.Progressbar(root, length=300, mode="determinate", style="Blue.Horizontal.TProgressbar")
progress_bar_3.pack(pady=10)
percent_label_3 = tk.Label(root, text="0%", bg="#f0f8ff")
percent_label_3.pack()
status_label_3 = tk.Label(root, text="", bg="#f0f8ff") 
status_label_3.pack()

# مراقبة الإنترنت
internet_thread = threading.Thread(target=monitor_internet, daemon=True)
internet_thread.start()

# بدء أشرطة التقدم
update_progress_1()
update_progress_2()
update_progress_3()

root.mainloop()
