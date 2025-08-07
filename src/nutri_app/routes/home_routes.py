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
        result = conn.execute(text("""
            SELECT r.id, r.tipo_refeicao, r.porcao, r.calorias, r.proteinas, r.carboidratos, r.gorduras, a.nome
            FROM refeicoes r
            JOIN alimentos a ON r.alimento_id = a.id
            WHERE r.usuario_id = :usuario_id AND r.data = :data
            ORDER BY r.tipo_refeicao, r.id DESC
        """), {"usuario_id": current_user.id, "data": hoje}).fetchall()

    refeicoes_por_tipo = {}
    totais_dia = {"calorias": 0, "proteinas": 0, "carboidratos": 0, "gorduras": 0}

    for r in result:
        tipo = r.tipo_refeicao
        refeicoes_por_tipo.setdefault(tipo, []).append(r)

        totais_dia["calorias"] += r.calorias
        totais_dia["proteinas"] += r.proteinas
        totais_dia["carboidratos"] += r.carboidratos
        totais_dia["gorduras"] += r.gorduras

    return render_template(
        "home.html",
        totais_dia=totais_dia,
        refeicoes_por_tipo=refeicoes_por_tipo,
        current_date=hoje
    )
