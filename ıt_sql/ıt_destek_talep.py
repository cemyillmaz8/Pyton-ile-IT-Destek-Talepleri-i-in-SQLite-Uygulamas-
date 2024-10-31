import sqlite3

# Veritabanına bağlan (yoksa oluştur)
db = sqlite3.connect("it_destek.db")
yetki = db.cursor()

# Talepler tablosunu oluştur
yetki.execute('''
    CREATE TABLE IF NOT EXISTS talepler (
        talep_id INTEGER PRIMARY KEY,
        kullanici_adi TEXT,
        konu TEXT,
        aciklama TEXT,
        durum TEXT DEFAULT 'Açık'
    )
''')
db.commit()

# Yeni talep ekleme fonksiyonu
def yeni_talep_ekleme(talep_id, kullanici_adi, konu, aciklama):
    yetki.execute('''
        INSERT INTO talepler (talep_id, kullanici_adi, konu, aciklama) 
        VALUES (?, ?, ?, ?)
    ''', (talep_id, kullanici_adi, konu, aciklama))
    db.commit()
    print("Yeni talep eklendi.\n")

# Talepleri listeleme fonksiyonu
def talepleri_listele():
    yetki.execute("SELECT * FROM talepler")
    talepler = yetki.fetchall()  # Bütün talepleri al
    if talepler:
        print("*** Destek Talepleri ***")
        for talep in talepler:
            print(f"ID: {talep[0]}, Kullanıcı: {talep[1]}, Konu: {talep[2]}, Durum: {talep[4]}")
    else:
        print("\nHiç talep bulunmamaktadır.")
    print()

# Talep durumu güncelleme fonksiyonu
def talep_durumu_degistir(talep_id, yeni_durum):
    yetki.execute("SELECT * FROM talepler WHERE talep_id=?", (talep_id,))
    talep = yetki.fetchone()
    if talep:
        yetki.execute('UPDATE talepler SET durum=? WHERE talep_id=?', (yeni_durum, talep_id))
        db.commit()
        print(f"Talep ID: {talep_id} durumu '{yeni_durum}' olarak güncellendi.\n")
    else:
        print("Talep bulunamadı.\n")

# Kullanıcının önüne çıkan menü
def ana_menu():
    while True:
        print("=== IT Destek Talep Yönetim Sistemi ===")
        print("1. Yeni Talep Ekle")
        print("2. Talepleri Görüntüle")
        print("3. Talep Durumunu Güncelle")
        print("4. Çıkış")
        
        secim = input("Seçiminizi yapın (1-4): ")

        if secim == '1':
            try:
                talep_id = int(input("Talep ID'si: "))  # Talep ID kullanıcıdan alınıyor
                kullanici_adi = input("Kullanıcı Adı: ")
                konu = input("Konu: ")
                aciklama = input("Açıklama: ")
                yeni_talep_ekleme(talep_id, kullanici_adi, konu, aciklama)
            except ValueError:
                print("Geçersiz Talep ID. Lütfen sayısal bir değer girin.\n")

        elif secim == '2':
            talepleri_listele()

        elif secim == '3':
            try:
                talep_id = int(input("Durumunu güncellemek istediğiniz talebin ID'si: "))
                yeni_durum = input("Yeni durum (Açık, Kapalı, Beklemede): ")
                talep_durumu_degistir(talep_id, yeni_durum)
            except ValueError:
                print("Geçersiz Talep ID. Lütfen sayısal bir değer girin.\n")

        elif secim == '4':
            print("Çıkış yapılıyor...")
            break

        else:
            print("Geçersiz seçim, lütfen 1-4 arasında bir sayı girin.\n")

# Ana menüyü çalıştır
ana_menu()

# Veritabanı bağlantısını kapat
db.close()
