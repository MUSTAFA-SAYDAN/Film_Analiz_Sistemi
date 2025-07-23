from flask import Blueprint,request,jsonify
from Film.services import film_ekle,film_getir,film_guncelle,film_sil
from Film.validators import eksik_alan_kontrol,tip_kontrol
from decorators import token_dogrula
from models import Film

film_bp=Blueprint("filmler",__name__)

@film_bp.route("/",methods=["POST"])
@token_dogrula
def film_ekle_route():
    veri=request.get_json()
    eksik=eksik_alan_kontrol(veri,["isim","yonetmen","yil"])
    if eksik:
        return jsonify({"hata":f"{eksik} alani eksik"}),400
    
    tip_hatasi=tip_kontrol(veri)
    if tip_hatasi:
        return jsonify({"hata":f"{tip_hatasi} alani yanlis tipte"}),400
    
    yeni_film=film_ekle(veri["isim"],veri["yonetmen"],veri["yil"],request.kullanici_id)
    return jsonify({"mesaj":"Film eklendi","film_id":yeni_film.id}),201

@film_bp.route("/",methods=["GET"])
def filmleri_listele():
    filmler=Film.query.all()
    sonuc=[u.to_dict() for u in filmler]
    return jsonify(sonuc),200

@film_bp.route("/<int:film_id>",methods=["GET"])
def film_getir_route(film_id):
    film=film_getir(film_id)
    return jsonify(film.to_dict()),200


@film_bp.route("/<int:film_id>",methods=["PUT"])
@token_dogrula
def urun_guncelle_route(film_id):
    veri=request.get_json()
    tip_hatasi=tip_kontrol(veri)
    if tip_hatasi:
        return jsonify({"hata":f"{tip_hatasi} alani yanlis tipte"}),400
    film=film_getir(film_id)
    film_guncelle(film,veri.get("isim"),veri.get("yonetmen"),veri.get("yil"))
    return jsonify({"mesaj":"Film guncellendi"}),200

@film_bp.route("/<int:film_id>",methods=["DELETE"])
@token_dogrula
def film_sil_route(film_id):
    film=film_getir(film_id)
    film_sil(film)
    return jsonify({"mesaj":"Film silindi"}),200    