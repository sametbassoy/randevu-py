# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 17:12:39 2023

@author: excalibur
"""

# KÜTÜPHANELER
import sys
import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from veri import *  # Burada .ui dosyasından dönüştürülen dosya import ediliyor
import sqlite3
from PyQt5.QtCore import Qt

uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

# Veritabanı kısmı
baglanti = sqlite3.connect("kayıt.db")
islem = baglanti.cursor()

# Mevcut tabloya yeni sütun ekle
try:
    islem.execute("ALTER TABLE kayıt ADD COLUMN RastgeleSayi INTEGER DEFAULT NULL")
    baglanti.commit()
except sqlite3.OperationalError:
    # Sütun zaten varsa veya tablo boşsa hata alırız, bu yüzden bu hatayı göz ardı ediyoruz
    pass

def rez_ekle():
    Isim = ui.isimlne.text()
    SoyIsim = ui.soyismline.text()
    Telefon = int(ui.telline.text())
    Giris = ui.cmbgiris.currentText()
    Cıkıs = ui.cmbcikis.currentText()
    MasaNo = ui.comboBox.currentText()
    Tarih = ui.calendarWidget.selectedDate()
    RastgeleSayi = random.randint(1, 100)  # Sadece yeni eklenen satır için rastgele sayı ekleniyor
    
    try:
        ekle = "INSERT INTO kayıt (İsim, Soyisim, Telefon, Giriş, Çıkış, MasaNo, Tarih, RastgeleSayi) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        islem.execute(ekle, (Isim, SoyIsim, Telefon, Giris, Cıkıs, MasaNo, Tarih.toString(Qt.ISODate), RastgeleSayi))
        baglanti.commit()
        kayıt_gör()
        ui.statusbar.showMessage("Rezervasyon Eklenmiştir", 1000)
    except Exception as error:
        ui.statusbar.showMessage("Rezervasyon Eklenemedi Hata Oluştu ===" + str(error))

# FONKSİYONLAR
def kayıt_gör():
    ui.tblrez.clear()
    ui.tblrez.setColumnCount(8)
    ui.tblrez.setHorizontalHeaderLabels(("Müşteri Adı", "Müşteri Soyadı", "Müşteri Telefonu", "Giriş Saati", "Çıkış Saati", "MasaNo", "Tarih", "Müşteri Numarası"))
    sorgu = "SELECT * FROM kayıt"
    islem.execute(sorgu)
    
    # Tablo sadece bir kez temizlensin ve veriler eklendikçe yeni satırlar oluşturulsun
    satir_sayisi = 0
    for kayitNumarasi in islem:
        ui.tblrez.insertRow(satir_sayisi)
        for indexSutun, kayıtSutun in enumerate(kayitNumarasi):
            ui.tblrez.setItem(satir_sayisi, indexSutun, QTableWidgetItem(str(kayıtSutun)))
        satir_sayisi += 1

def arama_yap():
    arama_metni = ui.arama_line_edit.text()
    for row in range(ui.tblrez.rowCount()):
        for column in range(ui.tblrez.columnCount()):
            item = ui.tblrez.item(row, column)
            if item is not None and arama_metni in item.text():
                ui.tblrez.setCurrentCell(row, column)
    return

def kayıt_silme():
    sclnislem = ui.tblrez.selectedItems()
    if len(sclnislem) == 0:
        ui.statusbar.showMessage("Silinecek bir kayıt seçin.")
        return
    
    silme = QMessageBox.question(pencere, "Silmek İçin Onay", "Silme İşlemini Onaylıyor Musunuz?", QMessageBox.Yes | QMessageBox.No)
    if silme == QMessageBox.Yes:
        silinecekkayıt = sclnislem[0].text()
        sorgu = "DELETE FROM kayıt WHERE İsim = ?"
        try:
            islem.execute(sorgu, (silinecekkayıt,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt silindi.")
            kayıt_gör()
        except Exception as error:
            ui.statusbar.showMessage("Kayıt silinirken hata oluştu: " + str(error))
    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi.")







def kyt_güncelle():
    gnclmsj = QMessageBox.question(pencere, "Güncelleme Onay", "Güncellemek İstediğinizden Emin Misiniz?", QMessageBox.Yes | QMessageBox.No)
    if gnclmsj == QMessageBox.Yes:
        try:
            İsim = ui.isimlne.text()
            Soyisim = ui.soyismline.text()
            Telefon = ui.telline.text()
            Giriş = ui.cmbgiris.currentText()
            Çıkış = ui.cmbcikis.currentText()
            MasaNO = ui.comboBox.currentText()
            Tarih = ui.calendarWidget.selectedDate().toString(Qt.ISODate)

            if İsim == "" and Soyisim == "" and Telefon == "" and Giriş == "" and Çıkış == "" and MasaNO == "" and Tarih == "" :
                ui.statusbar.showMessage("Güncellenecek bir kayıt seçin.")
                return
            
            sorgu = "UPDATE kayıt SET "
            parametreler = []

            if İsim != "":
                sorgu += "İsim=?, "
                parametreler.append(İsim)

            if Soyisim != "":
                sorgu += "Soyisim=?, "
                parametreler.append(Soyisim)

            if Telefon != "":
                sorgu += "Telefon=?, "
                parametreler.append(Telefon)

            if Giriş != "":
                sorgu += "Giriş=?, "
                parametreler.append(Giriş)

            if Çıkış != "":
                sorgu += "Çıkış=?, "
                parametreler.append(Çıkış)

            if MasaNO != "":
                sorgu += "MasaNo=?, "
                parametreler.append(MasaNO)

            if Tarih != "":
                sorgu += "Tarih=?, "
                parametreler.append(Tarih)

            sorgu = sorgu.rstrip(", ")
            sorgu += " WHERE İsim=?"
            parametreler.append(İsim)

            islem.execute(sorgu, parametreler)
            baglanti.commit()

            kayıt_gör()
            ui.statusbar.showMessage("Kayıt başarıyla güncellendi.")
        except Exception as error:
            ui.statusbar.showMessage("Kayıt güncellenemedi. Hata Oluştu: " + str(error))
    else:
         ui.statusbar.showMessage("Güncelleme iptal edildi.")

# Butonlar
ui.eklebtn.clicked.connect(rez_ekle)
ui.kytgrntl.clicked.connect(kayıt_gör)
ui.arama_btn.clicked.connect(arama_yap)
ui.silbtn.clicked.connect(kayıt_silme)
ui.gncllebtn.clicked.connect(kyt_güncelle)

sys.exit(uygulama.exec_())
