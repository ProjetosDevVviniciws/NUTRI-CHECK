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
            SELECT 
                calorias_meta, proteinas_meta, carboidratos_meta, gorduras_meta,
                calorias_consumidas, proteinas_consumidas, carboidratos_consumidos, gorduras_consumidas,
                calorias_restantes, proteinas_restantes, carboidratos_restantes, gorduras_restantes,
                ultima_atualizacao
            FROM usuarios
            WHERE id = :usuario_id 
        """), {"usuario_id": current_user.id}).mappings().first()

        if not usuario:
            totais_dia = {
                "calorias_consumidas": 0,
                "proteinas_consumidas": 0,
                "carboidratos_consumidos": 0,
                "gorduras_consumidas": 0,
                "ultima_atualizacao": hoje
            }
            metas_dia = {
                "calorias_meta": 0,
                "proteinas_meta": 0,
                "carboidratos_meta": 0,
                "gorduras_meta": 0
            }
            restantes_dia = {
                "calorias_restantes": 0,
                "proteinas_restantes": 0,
                "carboidratos_restantes": 0,
                "gorduras_restantes": 0
            }
        
        elif usuario["ultima_atualizacao"] != hoje:
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
            metas_dia = {
                "calorias_meta": usuario["calorias_meta"],
                "proteinas_meta": usuario["proteinas_meta"],
                "carboidratos_meta": usuario["carboidratos_meta"],
                "gorduras_meta": usuario["gorduras_meta"]
            }
            restantes_dia = {
                "calorias_restantes": usuario["calorias_restantes"],
                "proteinas_restantes": usuario["proteinas_restantes"],
                "carboidratos_restantes": usuario["carboidratos_restantes"],
                "gorduras_restantes": usuario["gorduras_restantes"]
            }
        
        else:
            totais_dia = {
                "calorias_consumidas": usuario["calorias_consumidas"],
                "proteinas_consumidas": usuario["proteinas_consumidas"],
                "carboidratos_consumidos": usuario["carboidratos_consumidos"],
                "gorduras_consumidas": usuario["gorduras_consumidas"],
                "ultima_atualizacao": usuario["ultima_atualizacao"]
            }
            metas_dia = {
                "calorias_meta": usuario["calorias_meta"],
                "proteinas_meta": usuario["proteinas_meta"],
                "carboidratos_meta": usuario["carboidratos_meta"],
                "gorduras_meta": usuario["gorduras_meta"]
            }
            restantes_dia = {
                "calorias_restantes": usuario["calorias_restantes"],
                "proteinas_restantes": usuario["proteinas_restantes"],
                "carboidratos_restantes": usuario["carboidratos_restantes"],
                "gorduras_restantes": usuario["gorduras_restantes"]
            }
        
    return render_template(
        "pages/home.html",
        totais_dia=totais_dia,
        metas_dia=metas_dia,
        restantes_dia=restantes_dia,
        current_date=hoje
    )
