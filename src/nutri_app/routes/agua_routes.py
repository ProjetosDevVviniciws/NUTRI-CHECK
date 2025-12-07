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
    return render_template("modals/registrar_agua_modal")

@agua_bp.route("/agua/registrar", methods=['POST'])
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
    
    if quantidade < 50 or quantidade > 12000:
        return jsonify({"erro": "Informe uma quantidade entre 50ml e 12000ml."}), 400
    
    hoje = date.today()
    
    with engine.begin() as conn:
        usuario = conn.execute(text("""
            SELECT agua_consumida, ultima_atualizacao
            FROM usuarios WHERE id = :id
        """), {"id": current_user.id}).fetchone()
        
        if usuario.ultima_atualizacao != hoje:
            conn.execute(text("""
                UPDATE usuarios SET
                    agua_consumida = 0,
                    ultima_atualizacao = :hoje
                WHERE id = :id
            """), {"id": current_user.id, "hoje": hoje})
            
        conn.execute(text("""
                UPDATE usuarios SET
                    agua_consumida = agua_consumida + :qtd
                WHERE id = :id
            """), {"id": current_user.id, "qtd": quantidade})
        
    return jsonify({
    "mensagem": f"{quantidade}ml registrados com sucesso!",
    "quantidade": quantidade
    })

            
