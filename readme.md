# 🎬 Flask JWT Film API

Bu proje, Python Flask kullanılarak geliştirilmiş bir Film API'sidir.  
Kullanıcılar kayıt olabilir, giriş yapabilir, JWT token alarak film ekleyebilir, listeleyebilir, güncelleyebilir ve silebilir.

---

## 🚀 Özellikler

- Kullanıcı Kaydı ve Giriş
- JWT Token ile Kimlik Doğrulama
- Her kullanıcının sadece kendi filmleri üzerinde işlem yapabilmesi
- Film CRUD (Create, Read, Update, Delete)
- Flask, SQLAlchemy, Bcrypt, JWT kullanımı

---

## 🛠️ Kullanılan Teknolojiler

- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- PyJWT
- SQLite (geliştirme ortamı için)

---

## 📦 Kurulum

### 1. Sanal Ortam Oluştur
```bash
python -m venv venv
venv\Scripts\activate  # Windows için
# source venv/bin/activate  # Linux/macOS için
2. Gereksinimleri Yükle
bash
Kopyala
Düzenle
pip install flask flask_sqlalchemy flask_bcrypt pyjwt
3. Uygulamayı Başlat
bash
Kopyala
Düzenle
python app.py
Uygulama http://localhost:5001 adresinde çalışır.

🔐 Kimlik Doğrulama Akışı
✅ Kullanıcı Kaydı
http
Kopyala
Düzenle
POST /kayit
Content-Type: application/json

{
  "kullanici_adi": "mustafa",
  "sifre": "1234"
}
🔑 Giriş ve Token Alma
h
Kopyala
Düzenle
POST /giris
Content-Type: application/json

{
  "kullanici_adi": "mustafa",
  "sifre": "1234"
}
Yanıt:

json
Kopyala
Düzenle
{
  "token": "eyJ0eXAiOiJKV1QiLCJh..."
}
🎥 Film İşlemleri
🔒 Film Ekle (JWT Gerekli)
http
Kopyala
Düzenle
POST /filmler
Authorization: Bearer <TOKEN>
Content-Type: application/json

{
  "isim": "Interstellar",
  "yonetmen": "Christopher Nolan",
  "yil": 2014
}
📃 Tüm Filmleri Listele (Herkese Açık)
http
Kopyala
Düzenle
GET /filmler
🔍 Tek Film Getir
http
Kopyala
Düzenle
GET /filmler/1
✏️ Film Güncelle (JWT Gerekli)
http
Kopyala
Düzenle
PUT /filmler/1
Authorization: Bearer <TOKEN>
Content-Type: application/json

{
  "isim": "Inception",
  "yil": 2010
}
❌ Film Sil (JWT Gerekli)
http
Kopyala
Düzenle
DELETE /filmler/1
Authorization: Bearer <TOKEN>
📁 Proje Yapısı
pgsql
Kopyala
Düzenle
film-api/
│
├── app.py              # Ana uygulama dosyası
├── models.py           # Veritabanı modelleri
├── README.md           # Açıklamalar
└── requirements.txt    # (İsteğe bağlı: pip freeze > requirements.txt)