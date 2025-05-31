from flask import Flask
from .db import init_db

def create_app():
    app = Flask(__name__)
    
    #load config
    app.config.from_object("config.Config")
    
    # DB
    init_db(app)
    
    # Routes
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app

