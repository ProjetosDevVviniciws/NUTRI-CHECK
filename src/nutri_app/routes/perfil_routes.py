from flask import Blueprint, render_template, request, jsonify
from src.nutri_app.database import engine
from sqlalchemy import text
from flask_login import login_required, current_user
from src.nutri_app.utils.macros import calcular_tmb_macros
from src.nutri_app.utils.hash import gerar_hash
from datetime import date

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route("/perfil", methods=["GET"])
@login_required
def perfil_page():
    return render_template("includes/perfil.html")
            