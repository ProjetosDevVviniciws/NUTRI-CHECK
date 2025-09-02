from flask import render_template, Blueprint
from flask_login import login_required, current_user
from datetime import date
from src.nutri_app.database import engine
from sqlalchemy import text

home_bp = Blueprint('home', __name__)

@home_bp.route("/")
@login_required
def home():
    hoje = date.today()
    
    with engine.begin() as conn:
        totais_dia = conn.execute(text("""
            SELECT calorias_consumidas, proteinas_consumidas, carboidratos_consumidos, gorduras_consumidas, ultima_atualizacao
            FROM usuarios
            WHERE id = :usuario_id AND ultima_atualizacao = :ultima_atualizacao
        """), {"usuario_id": current_user.id, "ultima_atualizacao": hoje}).mappings().first()

    return render_template(
        "pages/home.html",
        totais_dia=totais_dia,
        current_date=hoje
    )
