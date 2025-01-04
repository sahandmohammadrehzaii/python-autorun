import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import sqlite3
import os

# الاتصال بقاعدة بيانات SQLite أو إنشائها إذا لم تكن موجودة
def setup_database():
    conn = sqlite3.connect('database/user_installation_data/user_data.db')  # إنشاء أو الاتصال بملف قاعدة البيانات
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

# تسجيل موافقة المستخدم في قاعدة البيانات
def log_user_agreement(user_name="Anonymous"):
    conn = sqlite3.connect('database/user_installation_data/user_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_agreement (username) VALUES (?)', (user_name,))
    conn.commit()
    conn.close()

# وظيفة لفتح الملف النهائي
def open_python_file(file_name):
    try:
        # العثور على المسار المطلق للملف
        absolute_path = os.path.abspath(file_name)
        
        # التحقق من وجود الملف
        if not os.path.exists(absolute_path):
            raise FileNotFoundError(f"الملف المطلوب غير موجود: {absolute_path}")
        
        # تسجيل موافقة المستخدم في قاعدة البيانات
        log_user_agreement()
        
        # تشغيل الملف بلغة بايثون
        subprocess.Popen([sys.executable, absolute_path])
        
        # إغلاق واجهة المستخدم
        root.destroy()
    
    except FileNotFoundError as fnf_error:
        messagebox.showerror("خطأ", f"خطأ: {str(fnf_error)}")
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء تشغيل الملف:\n\n{str(e)}")

# إعداد قاعدة البيانات
setup_database()

# نافذة التطبيق الرئيسية
root = tk.Tk()
root.title("تثبيت البرنامج")
root.geometry("1000x600")
root.configure(bg="#f0f8ff")

terms_text = """\
الشروط والأحكام

مرحباً بكم في Ghadaam-Famer. قبل المضي قدمًا في تثبيت هذا البرنامج، يُرجى قراءة الشروط والأحكام التالية بعناية. من خلال الضغط على "موافق" أو تثبيت/استخدام البرنامج، فإنك تقر بأنك قرأت وفهمت ووافقت على الالتزام بهذه الشروط.
"""

license_text = """\
1. اتفاقية الترخيص

هذا البرنامج مُرخص، وليس مباعًا. يمنحك فريق Ghadaam ترخيصًا محدودًا وغير حصري وغير قابل للتحويل لاستخدام هذا البرنامج للأغراض الشخصية أو العملية وفقًا للشروط الواردة هنا.
"""

privacy_text = """\
2. الخصوصية

باستخدام هذا البرنامج، فإنك توافق على سياسة الخصوصية الخاصة بنا. قد تتضمن البيانات التي يتم جمعها أثناء التثبيت أو الاستخدام، على سبيل المثال لا الحصر:

    معلومات الجهاز
    تفضيلات المستخدم
    تقارير الأعطال

سيتم التعامل مع بياناتك بأمان ووفقًا لإرشادات الخصوصية الخاصة بنا.
"""

restrictions_text = """\
3. القيود

أنت توافق على عدم:

    نسخ، تعديل، تكييف، أو توزيع البرنامج.
    إجراء الهندسة العكسية أو فك التشفير أو تفكيك أي جزء من هذا البرنامج.
    استخدام البرنامج لأي أنشطة غير قانونية أو خبيثة.
"""

disclaimer_text = """\
4. إخلاء المسؤولية

يتم تقديم البرنامج "كما هو" دون أي ضمان من أي نوع، صريحًا كان أم ضمنيًا. لا تضمن Ghadaam-Prime أن البرنامج سيكون خالياً من العيوب أو الأخطاء أو الانقطاعات.
"""

termination_text = """\
5. الإنهاء

تحتفظ Ghadaam-Prime بالحق في إنهاء وصولك إلى البرنامج في أي وقت، دون إشعار، لأي سبب، بما في ذلك انتهاك هذه الشروط.
"""

liability_text = """\
6. المسؤولية

لن تكون Ghadaam-Prime مسؤولة بأي حال من الأحوال عن أي أضرار مباشرة أو غير مباشرة أو عرضية أو تبعية تنشأ عن استخدام أو عدم القدرة على استخدام البرنامج.
"""

governing_text = """\
7. القوانين المطبقة

تخضع هذه الشروط والأحكام لقوانين إيران. سيتم حل أي نزاعات بشكل حصري من خلال محاكم هذا الاختصاص القضائي.
"""

contact_text = """\
8. الاتصال

لأي استفسارات أو دعم، يُرجى الاتصال بنا على:

    البريد الإلكتروني: mohammadrezaiisahand.com
    الهاتف: 09148407326
"""

agree_text = """\
9. بالضغط على "موافق" أو المضي قدمًا في التثبيت، فإنك تؤكد قبولك لهذه الشروط والأحكام وتوافق على الالتزام بها.
"""

# دمج النصوص المختلفة في نص واحد
combined_text = f"{terms_text}\n\n{'_'*100}\n\n{license_text}\n\n{'_'*100}\n\n{privacy_text}\n\n{'_'*100}\n\n{restrictions_text}\n\n{'_'*100}\n\n{disclaimer_text}\n\n{'_'*100}\n\n{termination_text}\n\n{'_'*100}\n\n{liability_text}\n\n{'_'*100}\n\n{governing_text}\n\n{'_'*100}\n\n{contact_text}\n\n{'_'*100}\n\n{agree_text}"

# استخدام Scrollbar للنصوص الطويلة
frame = tk.Frame(root, bg="#f0f8ff")
frame.pack(padx=10, pady=10, expand=True, fill="both")

text_widget = tk.Text(frame, wrap="word", font=("Arial", 12), bg="#f0f8ff", fg="#333", height=15, relief="flat")
text_widget.insert("1.0", combined_text)
text_widget.config(state="disabled")  # تعطيل تحرير النص
text_widget.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
scrollbar.pack(side="right", fill="y")
text_widget.config(yscrollcommand=scrollbar.set)

# إنشاء مربع التحديد
agree_var = tk.BooleanVar()

def toggle_install_button():
    """تفعيل أو تعطيل زر التثبيت بناءً على حالة مربع التحديد"""
    if agree_var.get():
        install_button.config(state="normal")
    else:
        install_button.config(state="disabled")

agree_checkbox = tk.Checkbutton(root, text="أوافق على الشروط والأحكام", variable=agree_var, onvalue=True,
                                offvalue=False, command=toggle_install_button, font=("Arial", 12), bg="#f0f8ff")
agree_checkbox.pack(pady=10)

# تعريف زر التثبيت
install_button = tk.Button(root, text="تثبيت التطبيق",
                           command=lambda: open_python_file("Installation/AR/final_installation/index.py"),
                           font=("Arial", 12), bg="#17a2b8", fg="white", width=20, height=2)
install_button.pack(pady=10)

# تعطيل زر التثبيت كإعداد افتراضي
install_button.config(state="disabled")

def open_additional_file():
    additional_file = "start.py"  # مسیر فایل پایتونی جدید را در اینجا قرار دهید
    open_python_file(additional_file)

# دکمه‌ای برای اجرای فایل پایتونی جدید (در گوشه پایین سمت راست)
additional_button = tk.Button(root, text="سابق", 
                              command=open_additional_file,
                              font=("Arial", 9), bg="#28a745", fg="white", width=6, height=1)
additional_button.pack(side="left", anchor="se", padx=10, pady=10)

# تشغيل التطبيق
root.mainloop()