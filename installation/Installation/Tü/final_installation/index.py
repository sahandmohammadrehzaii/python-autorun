import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import socket
import threading
import platform
import subprocess
import time
from tkinter import PhotoImage

# İnternet bağlantısını kontrol etme fonksiyonu
def internet_baglanti_kontrol():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

# Çalışma sırasında 10 saniyelik internet bağlantı kontrolü
def interneti_izle():
    kopukluk_baslangic = None
    while True:
        if not internet_baglanti_kontrol():
            if kopukluk_baslangic is None:
                messagebox.showwarning("İnternet Kesintisi Uyarısı", "İnternet bağlantınız kesildi. Lütfen internetinizi kontrol edin.")
                kopukluk_baslangic = time.time()
            elif time.time() - kopukluk_baslangic >= 10:
                messagebox.showerror("İnternet Bağlantısı Koptu", "İnternet bağlantısı 10 saniyeden fazla kesik kaldı. Program kapanacaktır.")
                root.destroy()
                break
        else:
            kopukluk_baslangic = None
        time.sleep(1)

# Başka bir Python dosyasını çalıştırma fonksiyonu
def diger_python_dosyasini_calistir():
    try:
        # 'diger_script.py' yerine hedef dosya yolunu değiştirin
        subprocess.run(["python", "main.py"], check=True)
    except Exception as e:
        messagebox.showerror("Hata", f"Başka dosya çalıştırılırken hata oluştu:\n{e}")

# Son ekranı gösterme fonksiyonu
def son_ekrani_goster():
    son_pencere = tk.Toplevel(root)
    son_pencere.title("Son İşlemler")
    son_pencere.geometry("400x200")
    son_pencere.resizable(False, False)
    tk.Label(son_pencere, text="Tüm işlemler başarıyla tamamlandı.", fg="#2e8b57").pack(pady=20)
    tk.Button(son_pencere, text="Başka Dosya Çalıştır", command=diger_python_dosyasini_calistir, bg="#008cba", fg="white", relief="groove").pack(pady=10)

# İlk ilerleme çubuğunu güncelleme fonksiyonu
def ilerleme_guncelle_1():
    global ilerleme_1
    if ilerleme_1 < 100:
        ilerleme_1 += 100 / (2 * 60 * 10)  # 2 dakikada dolması için
        ilerleme_cubugu_1['value'] = ilerleme_1
        yuzde_etiketi_1.config(text=f"{int(ilerleme_1)}%")
        root.after(100, ilerleme_guncelle_1)
    else:
        yuzde_etiketi_1.config(text="100%")
        durum_etiketi_1.config(text="✔ Kurulum tamamlandı", fg="#2e8b57")
        tum_ilerlemeleri_kontrol_et()

# İkinci ilerleme çubuğunu güncelleme fonksiyonu
def ilerleme_guncelle_2():
    global ilerleme_2
    if ilerleme_2 < 100:
        ilerleme_2 += 100 / (60 * 10)  # 1 dakikada dolması için
        ilerleme_cubugu_2['value'] = ilerleme_2
        yuzde_etiketi_2.config(text=f"{int(ilerleme_2)}%")
        root.after(100, ilerleme_guncelle_2)
    else:
        yuzde_etiketi_2.config(text="100%")
        durum_etiketi_2.config(text="✔ Yükleme tamamlandı", fg="#2e8b57")
        tum_ilerlemeleri_kontrol_et()

# Üçüncü ilerleme çubuğunu güncelleme fonksiyonu (10 saniye)
def ilerleme_guncelle_3():
    global ilerleme_3
    if ilerleme_3 < 100:
        ilerleme_3 += 100 / (10 * 10)  # 10 saniyede dolması için
        ilerleme_cubugu_3['value'] = ilerleme_3
        yuzde_etiketi_3.config(text=f"{int(ilerleme_3)}%")
        root.after(100, ilerleme_guncelle_3)
    else:
        yuzde_etiketi_3.config(text="100%")
        durum_etiketi_3.config(text="✔ İşlem tamamlandı", fg="#2e8b57")
        tum_ilerlemeleri_kontrol_et()

# Tüm ilerleme çubuklarının tamamlanmasını kontrol et
def tum_ilerlemeleri_kontrol_et():
    if ilerleme_1 >= 100 and ilerleme_2 >= 100 and ilerleme_3 >= 100:
        son_ekrani_goster()

# İşletim sistemi kontrolü
if platform.system() != "Windows":
    def programi_kapat():
        os_ozel_root.destroy()
        exit()
    
    os_ozel_root = tk.Tk()
    os_ozel_root.title("Çalıştırılamaz")
    os_ozel_root.geometry("400x200")
    os_ozel_root.resizable(False, False)
    uyari_etiketi = tk.Label(os_ozel_root, text="Bu program sadece Windows işletim sistemi üzerinde çalıştırılabilir.")
    uyari_etiketi.pack(pady=20)
    cikis_butonu = tk.Button(os_ozel_root, text="Çıkış", command=programi_kapat)
    cikis_butonu.pack(pady=20)
    os_ozel_root.mainloop()

# Ana pencere oluşturma
root = tk.Tk()
root.title("İlerleme Çubuğu - tkinter ile proje")
root.geometry("500x650")
root.configure(bg="#f0f8ff")  # Arka plan rengi

# İlerleme çubuğu stili tanımı
stil = ttk.Style(root)
stil.theme_use('default')
stil.configure("Blue.Horizontal.TProgressbar", troughcolor='white', background='#008cba', thickness=20)

ilerleme_1 = 0
ilerleme_2 = 0
ilerleme_3 = 0

# İlk internet bağlantı kontrolü
if not internet_baglanti_kontrol():
    messagebox.showerror("İnternet Kesintisi", "Lütfen internet bağlantınızı kontrol edin. Program kapanacaktır.")
    exit()

# Alan 1
ilerleme_etiketi_1 = tk.Label(root, text="Sunucudan cihazınıza veri yükleniyor...", bg="#f0f8ff")
ilerleme_etiketi_1.pack(pady=5)
ilerleme_cubugu_1 = ttk.Progressbar(root, length=300, mode="determinate", style="Blue.Horizontal.TProgressbar")
ilerleme_cubugu_1.pack(pady=10)
yuzde_etiketi_1 = tk.Label(root, text="0%", bg="#f0f8ff")
yuzde_etiketi_1.pack()
durum_etiketi_1 = tk.Label(root, text="", bg="#f0f8ff") 
durum_etiketi_1.pack()

# Alan 2
ilerleme_etiketi_2 = tk.Label(root, text="Varsayılan veriler kopyalanıyor...", bg="#f0f8ff")
ilerleme_etiketi_2.pack(pady=20)
ilerleme_cubugu_2 = ttk.Progressbar(root, length=300, mode="determinate", style="Blue.Horizontal.TProgressbar")
ilerleme_cubugu_2.pack(pady=10)
yuzde_etiketi_2 = tk.Label(root, text="0%", bg="#f0f8ff")
yuzde_etiketi_2.pack()
durum_etiketi_2 = tk.Label(root, text="", bg="#f0f8ff") 
durum_etiketi_2.pack()

# Alan 3
ilerleme_etiketi_3 = tk.Label(root, text="İşletim sistemi ve bilgileri tanımlanıyor...", bg="#f0f8ff")
ilerleme_etiketi_3.pack(pady=20)
ilerleme_cubugu_3 = ttk.Progressbar(root, length=300, mode="determinate", style="Blue.Horizontal.TProgressbar")
ilerleme_cubugu_3.pack(pady=10)
yuzde_etiketi_3 = tk.Label(root, text="0%", bg="#f0f8ff")
yuzde_etiketi_3.pack()
durum_etiketi_3 = tk.Label(root, text="", bg="#f0f8ff") 
durum_etiketi_3.pack()

# İnternet bağlantısı izleme
internet_izleme_thread = threading.Thread(target=interneti_izle, daemon=True)
internet_izleme_thread.start()

# İlerleme çubuklarını başlat
ilerleme_guncelle_1()
ilerleme_guncelle_2()
ilerleme_guncelle_3()

root.mainloop()
