from flask import Blueprint, render_template, request, jsonify
from src.nutri_app.utils.decorators import perfil_completo_required
from src.nutri_app.database import engine
from sqlalchemy import text
from flask_login import login_required, current_user
from datetime import date

agua_bp = Blueprint('agua', __name__)

@agua_bp.route("/agua", methods=['GET'])
@login_required
@perfil_completo_required
def pagina_agua():
    return render_template("includes/agua.html")

@agua_bp.route("/agua_registrar", methods=['POST'])
@login_required
@perfil_completo_required
def registrar_agua():
    data = request.get_json()
    
    if not data or "quantidade" not in data:
        return jsonify({"erro": "Quantidade não enviada."}), 400

    try:
        quantidade = int(data["quantidade"])
    except ValueError:
        return jsonify({"erro": "Quantidade inválida."}), 400
    
    with engine.begin() as conn:
        usuario = conn.execute(text("""
            SELECT agua_consumida, ultima_atualizacao
            FROM usuarios WHERE id = :id
        """), {"id": current_user.id}).fetchone()
    
        hoje = date.today()
        
        if usuario.ultima_atualizacao.date() != hoje:
            conn.execute(text("""
                UPDATE usuarios SET
                    agua_consumida = 0,
                    ultima_atualizacao = :hoje
                WHERE id = :id
            """), {"id": current_user.id, "hoje": hoje})
            
        if forms.validate_on_submit():
            quantidade = forms.quantidade.data
            
            conn.execute(text("""
                UPDATE usuarios SET
                    agua_consumida = agua_consumida + :qtd
                WHERE id = :id
            """), {"id": current_user.id, "qtd": quantidade})

            flash(f"{quantidade}ml de água registrados com sucesso!", category="success")
            return redirect(url_for('agua.registrar_agua'))
            
    return render_template('includes/agua.html', form=forms)