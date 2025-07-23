from flask import Flask
from extensions import db,bcrypt
from models import Kullanici,Film
from auth.routes import auth_bp
from Film.routes import film_bp

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///filmler.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    app.config["SECRET_KEY"]="gizli_anahtar"

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp,url_prefix="/auth")
    app.register_blueprint(film_bp,url_prefix="/filmler")

    return app

if __name__=="__main__":
    app=create_app()
    app.run(debug=True,port=5001)