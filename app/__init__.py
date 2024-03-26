from flask import Flask
from .database import db

UPLOAD_FOLDER = 'uploads'


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metadata.db'

    import app.tfidfmodule.controllers as firstmodule

    app.register_blueprint(firstmodule.module)

    import app.swaggermodule.controllers as secondmodule

    app.register_blueprint(secondmodule.module)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app
