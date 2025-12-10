from flask import Blueprint, render_template, request, jsonify
from src.nutri_app.utils.decorators import perfil_completo_required
from src.nutri_app.database import engine
from sqlalchemy import text
from flask_login import login_required, current_user
from datetime import date, datetime

agua_bp = Blueprint('agua', __name__)

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
    
    data_registro = data.get("data")
    if data_registro:
        try:
            data_registro = datetime.strptime(data_registro, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"erro": "Formato de data inválido"}), 400
    else:
        data_registro = date.today()
    
    with engine.begin() as conn:
        registro_agua = conn.execute(text("""
            SELECT quantidade_ml 
            FROM agua_registros
            WHERE usuario_id = :id AND data = :data
        """), {"id": current_user.id, "data": data_registro}).fetchone()
        
        if registro_agua:
            conn.execute(text("""
                UPDATE agua_registros 
                SET quantidade_ml = quantidade_ml + :qtd
                WHERE usuario_id = :id AND data = :data
            """), {"qtd": quantidade,"id": current_user.id, "data": data_registro})
        else:
            conn.execute(text("""
                INSERT INTO agua_registros (usuario_id, data, quantidade_ml)
                VALUES (:id, :data, :qtd)
            """), {"id": current_user.id, "data": data_registro, "qtd": quantidade})
        
        total = conn.execute(text("""
            SELECT quantidade_ml 
            FROM agua_registros 
            WHERE usuario_id = :id AND data = :data
        """), {"id": current_user.id, "data": data_registro}).scalar()
        
    return jsonify({
    "mensagem": f"{quantidade}ml registrados com sucesso!",
    "total": total,
    "data": data_registro.strftime("%d/%m/%Y")
    })

            
