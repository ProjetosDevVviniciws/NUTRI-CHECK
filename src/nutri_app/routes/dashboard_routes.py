from flask import Blueprint, render_template
from src.nutri_app.database import engine
from sqlalchemy import text
from flask_login import login_required, current_user
from datetime import date

alimentos_bp = Blueprint('resumo_diario', __name__)

@alimentos_bp.route("/resumo_diario")
@login_required
def resumo_diario():
    hoje = date.today()

    with engine.connect() as conn:
        query = text("""
            SELECT
                refeicao,
                SUM(calorias) as calorias,
                SUM(proteinas) as proteinas,
                SUM(carboidratos) as carboidratos,
                SUM(gorduras) as gorduras
            FROM alimentos
            WHERE usuario_id = :usuario_id AND DATE(data_cadastro) = :hoje
            GROUP BY refeicao
        """)
        resultados = conn.execute(query, {"usuario_id": current_user.id, "hoje": hoje}).fetchall()

    return render_template("includes/resumo_diario.html", resultados=resultados)
