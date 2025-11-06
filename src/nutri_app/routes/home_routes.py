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
        usuario_meta = conn.execute(text("""
            SELECT 
                calorias_meta, proteinas_meta, carboidratos_meta, gorduras_meta,
                ultima_atualizacao
            FROM usuarios
            WHERE id = :usuario_id 
        """), {"usuario_id": current_user.id}).mappings().first()

        totais_refeicoes = conn.execute(text("""
            SELECT
                COALESCE(SUM(calorias), 0) AS calorias_consumidas,
                COALESCE(SUM(proteinas), 0) AS proteinas_consumidas,
                COALESCE(SUM(carboidratos), 0) AS carboidratos_consumidos,
                COALESCE(SUM(gorduras), 0) AS gorduras_consumidas
            FROM refeicoes
            WHERE usuario_id = :usuario_id AND DATE(data) = :data_refeicao
        """), {"usuario_id": current_user.id, "data_refeicao": str(hoje)}).mappings().first()
        
        if not usuario_meta:
            metas_dia = {
                "calorias_meta": 0,
                "proteinas_meta": 0,
                "carboidratos_meta": 0,
                "gorduras_meta": 0
            }
        else:
            metas_dia = {
                "calorias_meta": usuario_meta["calorias_meta"] or 0,
                "proteinas_meta": usuario_meta["proteinas_meta"] or 0,
                "carboidratos_meta": usuario_meta["carboidratos_meta"] or 0,
                "gorduras_meta": usuario_meta["gorduras_meta"] or 0
            }
            
            totais_dia = {
                "calorias_consumidas": float(totais_refeicoes["calorias_consumidas"] or 0),
                "proteinas_consumidas": float(totais_refeicoes["proteinas_consumidas"] or 0),
                "carboidratos_consumidos": float(totais_refeicoes["carboidratos_consumidos"] or 0),
                "gorduras_consumidas": float(totais_refeicoes["gorduras_consumidas"] or 0),
                "ultima_atualizacao": usuario_meta["ultima_atualizacao"] if usuario_meta else hoje
            }
            
            restantes_dia = {
                "calorias_restantes": round(metas_dia["calorias_meta"] - totais_dia["calorias_consumidas"], 2),
                "proteinas_restantes": round(metas_dia["proteinas_meta"] - totais_dia["proteinas_consumidas"], 2),
                "carboidratos_restantes": round(metas_dia["carboidratos_meta"] - totais_dia["carboidratos_consumidos"], 2),
                "gorduras_restantes": round(metas_dia["gorduras_meta"] - totais_dia["gorduras_consumidas"], 2)
            }
        
    return render_template(
        "pages/home.html",
        totais_dia=totais_dia,
        metas_dia=metas_dia,
        restantes_dia=restantes_dia,
        current_date=hoje
    )
