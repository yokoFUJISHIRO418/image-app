from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from apps.config import config
from flask_login import LoginManager

db = SQLAlchemy()

csrf = CSRFProtect()


login_manager = LoginManager()
login_manager.login_view = "auth.signup"
login_manager.login_mesage = ""

def create_app(config_key):
    app=Flask(__name__)
    app.config.from_object(config[config_key])
    # app.config.from_mapping(
    #     SECRET_KEY="dlkafjadkljlkfad",
    #     SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent/ 'local.sqlite'}",
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False,
    #     SQLALCHEMY_ECHO=True,
    #     WTF_CSRF_SECRETKEY="lkjlkglfkgs",
    # )    

    csrf.init_app(app)
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)
    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    from apps.detector import views as dt_views
    app.register_blueprint(dt_views.dt)
    return app