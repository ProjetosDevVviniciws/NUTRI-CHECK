from flask import Flask
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

load_dotenv()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    
    bcrypt.init_app(app)
    
    from .routes.home_routes import home_bp
    from .routes.auth_routes import auth_bp
    from .routes.perfil_routes import perfil_bp
    from .routes.refeicoes_routes import refeicoes_bp
    from .routes.produtos_routes import produtos_bp
    from .routes.agua_routes import agua_bp
    from .routes.progressao_routes import progressao_bp
    
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(perfil_bp)
    app.register_blueprint(refeicoes_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(agua_bp)
    app.register_blueprint(progressao_bp)
    
    return app