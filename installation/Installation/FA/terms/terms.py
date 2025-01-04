import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import sqlite3
import os

# اتصال به پایگاه داده SQLite یا ایجاد آن در صورت عدم وجود
def setup_database():
    conn = sqlite3.connect('database/user_installation_data/user_data.db')  # ایجاد یا اتصال به فایل پایگاه داده
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

# ثبت موافقت کاربر در پایگاه داده
def log_user_agreement(user_name="Anonymous"):
    conn = sqlite3.connect('database/user_installation_data/user_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_agreement (username) VALUES (?)', (user_name,))
    conn.commit()
    conn.close()

# تابعی برای باز کردن فایل نهایی
def open_python_file(file_name):
    try:
        # پیدا کردن مسیر مطلق فایل
        absolute_path = os.path.abspath(file_name)
        
        # تأیید وجود فایل
        if not os.path.exists(absolute_path):
            raise FileNotFoundError(f"فایل درخواست شده یافت نشد: {absolute_path}")
        
        # ثبت موافقت کاربر در پایگاه داده
        log_user_agreement()
        
        # اجرای فایل با پایتون
        subprocess.Popen([sys.executable, absolute_path])
        
        # بستن رابط کاربری
        root.destroy()
    
    except FileNotFoundError as fnf_error:
        messagebox.showerror("خطا", f"خطا: {str(fnf_error)}")
    except Exception as e:
        messagebox.showerror("خطا", f"یک خطا در حین اجرای فایل رخ داده است:\n\n{str(e)}")

# راه‌اندازی پایگاه داده
setup_database()

# پنجره اصلی برنامه
root = tk.Tk()
root.title("نصب نرم‌افزار")
root.geometry("1000x600")
root.configure(bg="#f0f8ff")

terms_text = """\
شرایط و ضوابط

به Ghadaam-Famer خوش آمدید. قبل از ادامه نصب این نرم‌افزار، لطفاً شرایط و ضوابط زیر را به دقت بخوانید. با کلیک بر روی "موافقم" یا نصب/استفاده از برنامه، تأیید می‌کنید که این شرایط را خوانده‌اید، فهمیده‌اید و با آن‌ها موافقید.
"""

license_text = """\
1. توافق نامه مجوز

این نرم‌افزار مجوز داده شده است، نه فروخته شده. تیم Ghadaam به شما مجوز محدود، غیر انحصاری و غیر قابل انتقال برای استفاده از این نرم‌افزار به منظورهای شخصی یا تجاری مطابق با شرایط ذکر شده در اینجا را می‌دهد.
"""

privacy_text = """\
2. حریم خصوصی

با استفاده از این نرم‌افزار، شما با سیاست حریم خصوصی ما موافقت می‌کنید. داده‌های جمع‌آوری شده در حین نصب یا استفاده ممکن است شامل، اما نه محدود به:

    اطلاعات دستگاه
    ترجیحات کاربر
    گزارش‌های خطا

داده‌های شما به طور ایمن و مطابق با دستورالعمل‌های حریم خصوصی ما مدیریت خواهد شد.
"""

restrictions_text = """\
3. محدودیت‌ها

شما موافقت می‌کنید که:

    نرم‌افزار را کپی، تغییر، سازگار، یا توزیع نکنید.
    مهندسی معکوس، دی‌کامپایل یا جدا کردن هر بخشی از این نرم‌افزار انجام ندهید.
    از نرم‌افزار برای هرگونه فعالیت غیرقانونی یا مخرب استفاده نکنید.
"""

disclaimer_text = """\
4. اخطار

نرم‌افزار به صورت "همان‌طور که هست" ارائه می‌شود و هیچگونه ضمانتی از هر نوع، صریح یا ضمنی، ندارد. Ghadaam-Prime تضمینی نمی‌دهد که نرم‌افزار عاری از نقص، خطا یا وقفه خواهد بود.
"""

termination_text = """\
5. خاتمه

Ghadaam-Prime حق دارد در هر زمان، بدون اطلاع، دسترسی شما به نرم‌افزار را برای هر دلیلی، از جمله نقض این شرایط، خاتمه دهد.
"""

liability_text = """\
6. مسئولیت

در هیچ شرایطی، Ghadaam-Prime مسئول هیچگونه خسارت مستقیم، غیرمستقیم، تصادفی یا تبعی ناشی از استفاده از یا عدم توانایی در استفاده از نرم‌افزار نخواهد بود.
"""

governing_text = """\
7. قوانین حاکم

این شرایط و ضوابط تابع قوانین ایران است. هرگونه اختلاف به طور انحصاری توسط دادگاه‌های این حوزه قضایی حل و فصل خواهد شد.
"""

contact_text = """\
8. تماس

برای هرگونه پرسش یا پشتیبانی، لطفاً با ما تماس بگیرید در:

    ایمیل: mohammadrezaiisahand.com
    تلفن: 09148407326
"""

agree_text = """\
9. با کلیک بر روی "موافقم" یا پیش رفتن در نصب، شما تأیید می‌کنید که این شرایط و ضوابط را قبول کرده‌اید و با آن‌ها موافقید.
"""

# ادغام متون مختلف به یک متن واحد
combined_text = f"{terms_text}\n\n{'_'*100}\n\n{license_text}\n\n{'_'*100}\n\n{privacy_text}\n\n{'_'*100}\n\n{restrictions_text}\n\n{'_'*100}\n\n{disclaimer_text}\n\n{'_'*100}\n\n{termination_text}\n\n{'_'*100}\n\n{liability_text}\n\n{'_'*100}\n\n{governing_text}\n\n{'_'*100}\n\n{contact_text}\n\n{'_'*100}\n\n{agree_text}"

# استفاده از Scrollbar برای متون طولانی
frame = tk.Frame(root, bg="#f0f8ff")
frame.pack(padx=10, pady=10, expand=True, fill="both")

text_widget = tk.Text(frame, wrap="word", font=("Arial", 12), bg="#f0f8ff", fg="#333", height=15, relief="flat")
text_widget.insert("1.0", combined_text)
text_widget.config(state="disabled")  # غیرفعال کردن ویرایش متن
text_widget.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
scrollbar.pack(side="right", fill="y")
text_widget.config(yscrollcommand=scrollbar.set)

# ایجاد چک باکس برای موافقت
agree_var = tk.BooleanVar()

def toggle_install_button():
    """فعال یا غیرفعال کردن دکمه نصب بر اساس وضعیت چک باکس"""
    if agree_var.get():
        install_button.config(state="normal")
    else:
        install_button.config(state="disabled")

agree_checkbox = tk.Checkbutton(root, text="من با شرایط و ضوابط موافقم", variable=agree_var, onvalue=True,
                                offvalue=False, command=toggle_install_button, font=("Arial", 12), bg="#f0f8ff")
agree_checkbox.pack(pady=10)

# تعریف دکمه نصب
install_button = tk.Button(root, text="نصب برنامه",
                           command=lambda: open_python_file("Installation/FA/final_installation/index.py"),
                           font=("Arial", 12), bg="#17a2b8", fg="white", width=20, height=2)
install_button.pack(pady=10)

# غیرفعال کردن دکمه نصب به طور پیش‌فرض
install_button.config(state="disabled")

def open_additional_file():
    additional_file = "start.py"  # مسیر فایل پایتونی جدید را در اینجا قرار دهید
    open_python_file(additional_file)

# دکمه‌ای برای اجرای فایل پایتونی جدید (در گوشه پایین سمت راست)
additional_button = tk.Button(root, text="قبلی", 
                              command=open_additional_file,
                              font=("Arial", 9), bg="#28a745", fg="white", width=6, height=1)
additional_button.pack(side="left", anchor="se", padx=10, pady=10)

# اجرای برنامه
root.mainloop()