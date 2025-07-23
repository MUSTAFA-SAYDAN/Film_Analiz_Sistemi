from models import Film
from extensions import db

def film_ekle(isim,yonetmen,yil,kullanici_id):
    yeni_film=Film(isim=isim,yonetmen=yonetmen,yil=yil,kullanici_id=kullanici_id)
    db.session.add(yeni_film)
    db.session.commit()
    return yeni_film

def film_getir(film_id):
    return Film.query.get_or_404(film_id)

def film_guncelle(film,isim=None,yonetmen=None,yil=None):
    if isim is not None:
        film.isim=isim
    if yonetmen is not None:
        film.yonetmen=yonetmen
    if yil is not None:
        film.yil=yil
    db.session.commit()
    return film

def film_sil(film):
    db.session.delete(film)
    db.session.commit()
    
