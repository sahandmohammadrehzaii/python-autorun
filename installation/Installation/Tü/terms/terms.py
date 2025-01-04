import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import sqlite3
import os

# SQLite veritabanına bağlanma veya mevcut değilse oluşturma
def setup_database():
    conn = sqlite3.connect('database/user_installation_data/user_data.db')  # Veritabanı dosyasına bağlanma veya oluşturma
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

# Kullanıcının mutabakatını veritabanında kaydetme
def log_user_agreement(user_name="Anonymous"):
    conn = sqlite3.connect('database/user_installation_data/user_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_agreement (username) VALUES (?)', (user_name,))
    conn.commit()
    conn.close()

# Son dosyayı açmak için bir fonksiyon
def open_python_file(file_name):
    try:
        # Dosyanın mutlak yolunu bulma
        absolute_path = os.path.abspath(file_name)
        
        # Dosyanın varlığını kontrol etme
        if not os.path.exists(absolute_path):
            raise FileNotFoundError(f"İstenilen dosya bulunamadı: {absolute_path}")
        
        # Kullanıcının mutabakatını veritabanında kaydetme
        log_user_agreement()
        
        # Dosyayı Python ile çalıştırma
        subprocess.Popen([sys.executable, absolute_path])
        
        # Kullanıcı arayüzünü kapatma
        root.destroy()
    
    except FileNotFoundError as fnf_error:
        messagebox.showerror("Hata", f"Hata: {str(fnf_error)}")
    except Exception as e:
        messagebox.showerror("Hata", f"Dosyayı çalıştırırken bir hata meydana geldi:\n\n{str(e)}")

# Veritabanını ayarlama
setup_database()

# Programın ana penceresi
root = tk.Tk()
root.title("Yazılım Kurulumu")
root.geometry("1000x600")
root.configure(bg="#f0f8ff")

terms_text = """\
Şartlar ve Koşullar

Ghadaam-Famer'a hoş geldiniz. Bu yazılımı kurmadan önce, lütfen aşağıdaki şartlar ve koşulları dikkatlice okuyun. "Kabul ediyorum" butonuna tıklayarak veya programı kurup kullanarak, bu şartları okuduğunuzu, anladığınızı ve kabul ettiğinizi onaylıyorsunuz.
"""

license_text = """\
1. Lisans Sözleşmesi

Bu yazılım lisanslıdır, satılmamıştır. Ghadaam ekibi, bu yazılımı burada belirlenen şartlara uygun olarak kişisel veya ticari amaçlarla kullanmanız için size sınırlı, gayri-menkul ve devredilemez bir lisans vermektedir.
"""

privacy_text = """\
2. Gizlilik

Bu yazılımı kullanarak, gizlilik politikasına da onay vermiş olursunuz. Kurulum veya kullanım sırasında toplanan veriler, ancak bunlarla sınırlı olmamak üzere şunları içerebilir:

    Cihaz bilgileri
    Kullanıcı tercihleri
    Hata raporları

Verileriniz, gizlilik politikamız uyarınca güvenli bir şekilde yönetilecektir.
"""

restrictions_text = """\
3. Kısıtlamalar

Şunları kabul edersiniz:

    Yazılımı kopyalamaz, değiştirmeyecek, uyarlamayacak veya dağıtmayacaksınız.
    Yazılımın herhangi bir bölümünün tersine mühendislik, decompiling veya ayrıştırma işlemlerini yapmayacaksınız.
    Yazılımı herhangi bir yasadışı veya zararlı faaliyet için kullanmayacaksınız.
"""

disclaimer_text = """\
4. Feragatname

Yazılım "olduğu gibi" sağlanmakta olup, hiçbir türde, açık ya da örtük herhangi bir garanti verilmemektedir. Ghadaam-Prime, yazılımın hatalardan, kusurlardan veya kesintilerden arındırılmış olacağını garanti etmemektedir.
"""

termination_text = """\
5. Fesih

Ghadaam-Prime, herhangi bir bildirimde bulunmaksızın, herhangi bir sebep göstermeksizin, bu şartları ihlal etmeniz durumunda yazılıma erişiminizi sona erdirme hakkına sahiptir.
"""

liability_text = """\
6. Sorumluluk

Ghadaam-Prime, yazılımı kullanmanız veya kullanamamanızdan kaynaklanan doğrudan, dolaylı, tesadüfi veya özel zararlar için hiçbir koşulda sorumlu değildir.
"""

governing_text = """\
7. Geçerli Hukuk

Bu şartlar ve koşullar, Türkiye Cumhuriyeti yasalarına tabidir. Herhangi bir uyuşmazlık, yalnızca bu yargı yetkisine tabi mahkemelerde çözülecektir.
"""

contact_text = """\
8. İletişim

Herhangi bir soru veya destek talebi için lütfen bizimle iletişime geçin:

    Email: mohammadrezaiisahand.com
    Telefon: 09148407326
"""

agree_text = """\
9. "Kabul ediyorum" butonuna tıklamak veya kurulumun devam etmesi, bu şartlar ve koşulları kabul ettiğinizi ve onayladığınızı gösterir.
"""

# Farklı metinleri tek bir metin haline getirme
combined_text = f"{terms_text}\n\n{'_'*100}\n\n{license_text}\n\n{'_'*100}\n\n{privacy_text}\n\n{'_'*100}\n\n{restrictions_text}\n\n{'_'*100}\n\n{disclaimer_text}\n\n{'_'*100}\n\n{termination_text}\n\n{'_'*100}\n\n{liability_text}\n\n{'_'*100}\n\n{governing_text}\n\n{'_'*100}\n\n{contact_text}\n\n{'_'*100}\n\n{agree_text}"

# Uzun metinler için Scrollbar kullanma
frame = tk.Frame(root, bg="#f0f8ff")
frame.pack(padx=10, pady=10, expand=True, fill="both")

text_widget = tk.Text(frame, wrap="word", font=("Arial", 12), bg="#f0f8ff", fg="#333", height=15, relief="flat")
text_widget.insert("1.0", combined_text)
text_widget.config(state="disabled")  # Metin düzenleme özelliğini devre dışı bırak
text_widget.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
scrollbar.pack(side="right", fill="y")
text_widget.config(yscrollcommand=scrollbar.set)

# Onay kutusu oluşturma
agree_var = tk.BooleanVar()

def toggle_install_button():
    """Onay kutusunun durumuna göre kurulum butonunu aktifleştirme veya devre dışı bırakma"""
    if agree_var.get():
        install_button.config(state="normal")
    else:
        install_button.config(state="disabled")

agree_checkbox = tk.Checkbutton(root, text="Şartlar ve koşulları kabul ediyorum", variable=agree_var, onvalue=True,
                                offvalue=False, command=toggle_install_button, font=("Arial", 12), bg="#f0f8ff")
agree_checkbox.pack(pady=10)

# Kurulum butonunu tanımlama
install_button = tk.Button(root, text="Programı Kur",
                           command=lambda: open_python_file("Installation/Tü/final_installation/index.py"),
                           font=("Arial", 12), bg="#17a2b8", fg="white", width=20, height=2)
install_button.pack(pady=10)

install_button.config(state="disabled")

def open_additional_file():
    additional_file = "start.py"
    open_python_file(additional_file)

additional_button = tk.Button(root, text="önceki", 
                              command=open_additional_file,
                              font=("Arial", 9), bg="#28a745", fg="white", width=6, height=1)
additional_button.pack(side="left", anchor="se", padx=10, pady=10)

root.mainloop()