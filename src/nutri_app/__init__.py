from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from dotenv import load_dotenv
 
from nutri_app.forms.progressao_forms import ProgressaoForm

load_dotenv()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'
    login_manager.login_message = 'Por favor, realize o login'
    login_manager.login_message_category = 'info'

    from .routes.login_routes import login_bp
    from .routes.auth_routes import auth_bp
    from .routes.home_routes import home_bp
    from .routes.perfil_ajax import perfil_bp
    from .routes.refeicoes_ajax import refeicoes_ajax_bp
    from .routes.alimentos_ajax import alimentos_ajax_bp
    from .routes.agua_routes import agua_bp
    from .routes.progressao_routes import progressao_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(perfil_bp)
    app.register_blueprint(refeicoes_ajax_bp)
    app.register_blueprint(alimentos_ajax_bp)
    app.register_blueprint(agua_bp)
    app.register_blueprint(progressao_bp)

    @app.context_processor
    def inject_forms():
        return {
            'form_agua': AguaForm(),
            'form_peso': ProgressaoForm()
        }

    return app
