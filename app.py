from flask import Flask,request,jsonify
from models import db,bcrypt,Kullanici,Film
from functools import wraps
import jwt
import datetime

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///filmler.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="gizli_anahtar"

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()

def token_gerekli(f):
    @wraps(f)
    def sarici(*args,**kwargs):
        token=request.headers.get("Authorization")
        if not token:
            return jsonify({"hata":"Token gerekli"}),401
        
        try:
            token=token.replace("Bearer","")
            data=jwt.decode(token,app.config["SECRET_KEY"],algorithms="HS256")
            kullanici_id=data["kullanici_id"]

        except jwt.ExpiredSignatureError:
            return jsonify({"hata":"Tokenin süresi bitmiş"}),401
        except jwt.InvalidTokenError:
            return jsonify({"hata":"Geçersiz token"}),401
        
        return f(kullanici_id,*args,**kwargs)
    return sarici

@app.route("/kayit",methods=["POST"])
def kayit():
    data=request.json
    kullanici_adi=data.get("kullanici_adi")
    sifre=data.get("sifre")

    if Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first():
        return jsonify({"hata":"Bu kullanici adi alinmiş"}),401
    
    sifre_hash=bcrypt.generate_password_hash(sifre).decode("utf-8")
    yeni_kisi=Kullanici(kullanici_adi=kullanici_adi,sifre_hash=sifre_hash)
    db.session.add(yeni_kisi)
    db.session.commit()

    return jsonify({"mesaj":"Kayit basarili"})

@app.route("/giris",methods=["POST"])
def giris():
    data=request.json
    kullanici_adi=data.get("kullanici_adi")
    sifre=data.get("sifre")

    kullanici=Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()
    if not kullanici or not kullanici.sifre_kontrol(sifre):
        return jsonify({"hata":"Geçersiz kullanici adi veya sifre"}),400
    
    token=jwt.encode(
        {
            "kullanici_id":kullanici.id,
            "exp":datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({"token":token})


@app.route("/filmler",methods=["POST"])
@token_gerekli
def film_ekle(kullanici_id):
    data=request.json
    isim=data.get("isim")
    yonetmen=data.get("yonetmen")
    yil=data.get("yil")

    if not isim or not yonetmen or not yil:
        return jsonify({"hata":"Eksik bilgi"}),400
    
    yeni_film=Film(isim=isim,yonetmen=yonetmen,yil=yil,kullanici_id=kullanici_id)
    db.session.add(yeni_film)
    db.session.commit()

    return jsonify({"mesaj":"Film eklendi"}),201

@app.route("/filmler",methods=["GET"])
def filmleri_getir():
    filmler=Film.query.all()
    return jsonify({"Filmler":[k.to_dict() for k in filmler ]})

@app.route("/filmler/<int:id>",methods=["GET"])
def filmi_getir(id):
    film=Film.query.get(id)
    if not film:
        return jsonify({"hata":"Film bulunamadi."}),404
    return jsonify(film.to_dict())

@app.route("/filmler/<int:id>",methods=["PUT"])
@token_gerekli
def film_guncelle(id,kullanici_id):
    film=Film.query.filter_by(id=id,kullanici_id=kullanici_id).first()
    if not film:
        return  jsonify({"hata":"Film bulunamadi"}),404
    
    data=request.json
    film.isim=data.get("isim",film.isim)
    film.yonetmen=data.get("yonetmen",film.yonetmen)
    film.yil=data.get("yil",film.yil)

    db.session.commit()

    return jsonify(film.to_dict())

@app.route("/filmler/<int:id>",methods=["DELETE"])
@token_gerekli
def film_sil(id,kullanici_id):
    film=Film.query.filter_by(id=id,kullanici_id=kullanici_id).first()
    if not film:
        return jsonify({"hata":"Film bulunamadi"}),404
    
    db.session.delete(film)
    db.session.commit()

    return jsonify({"mesaj":"Film silindi"})

if __name__=="__main__":
    app.run(debug=True,port=5001)
    
