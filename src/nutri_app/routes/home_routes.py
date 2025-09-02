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
        usuario = conn.execute(text("""
            SELECT calorias_consumidas, proteinas_consumidas, carboidratos_consumidos, gorduras_consumidas, ultima_atualizacao
            FROM usuarios
            WHERE id = :usuario_id AND ultima_atualizacao = :ultima_atualizacao
        """), {"usuario_id": current_user.id, "ultima_atualizacao": hoje}).mappings().first()

        if not usuario or usuario["ultima_atualizacao"] != hoje:
            conn.execute(text("""
                UPDATE usuarios
                SET calorias_consumidas = 0,
                    proteinas_consumidas = 0,
                    carboidratos_consumidos = 0,
                    gorduras_consumidas = 0,
                    ultima_atualizacao = :hoje
                WHERE id = :usuario_id
            """), {"hoje": hoje, "usuario_id": current_user.id})

            totais_dia = {
                "calorias_consumidas": 0,
                "proteinas_consumidas": 0,
                "carboidratos_consumidos": 0,
                "gorduras_consumidas": 0,
                "ultima_atualizacao": hoje
            }
        else:
            totais_dia = usuario
        
    return render_template(
        "pages/home.html",
        totais_dia=totais_dia,
        current_date=hoje
    )
