from flask import Blueprint, request, jsonify
from Film.services import film_ekle, film_getir, film_guncelle, film_sil
from Film.validators import eksik_alan_kontrol
from decorators import token_dogrula
from models import Film

film_bp = Blueprint("filmler", __name__)

@film_bp.route("/", methods=["POST"])
@token_dogrula
def film_ekle_route():
    veri = request.get_json()
    eksik = eksik_alan_kontrol(veri, ["isim", "yonetmen", "yil"])
    if eksik:
        return jsonify({"hata": f"{eksik} alani eksik"}), 400

    yeni_film = film_ekle(veri["isim"], veri["yonetmen"], veri["yil"], request.kullanici_id)
    return jsonify({"mesaj": "Film eklendi", "film_id": yeni_film.id}), 201

@film_bp.route("/", methods=["GET"])
@token_dogrula
def filmleri_getir():
    filmler = Film.query.filter_by(kullanici_id=request.kullanici_id).all()
    sonuc = [f.to_dict() for f in filmler]
    return jsonify(sonuc), 200

@film_bp.route("/<int:film_id>", methods=["GET"])
@token_dogrula
def film_getir_route(film_id):
    film = Film.query.filter_by(id=film_id, kullanici_id=request.kullanici_id).first_or_404()
    return jsonify(film.to_dict()), 200

@film_bp.route("/<int:film_id>", methods=["PUT"])
@token_dogrula
def film_guncelle_route(film_id):
    veri = request.get_json()
    film = Film.query.filter_by(id=film_id, kullanici_id=request.kullanici_id).first_or_404()
    film_guncelle(film, veri.get("isim"), veri.get("yonetmen"), veri.get("yil"))
    return jsonify({"mesaj": "Film güncellendi"}), 200

@film_bp.route("/<int:film_id>", methods=["DELETE"])
@token_dogrula
def film_sil_route(film_id):
    film = Film.query.filter_by(id=film_id, kullanici_id=request.kullanici_id).first_or_404()
    film_sil(film)
    return jsonify({"mesaj": "Film silindi"}), 200
