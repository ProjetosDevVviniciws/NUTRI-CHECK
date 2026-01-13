from flask import Blueprint, request, jsonify
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
    
@agua_bp.route("/agua/total")
@login_required
def total_agua_por_data():
    data_str = request.args.get("data")
    
    if not data_str:
        return jsonify({"erro": "Data não enviada"}), 400

    try:
        data = datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"erro": "Formato de data inválido"}), 400

    with engine.begin() as conn:
        total = conn.execute(text("""
            SELECT quantidade_ml 
            FROM agua_registros
            WHERE usuario_id = :id AND data = :data
        """), {"id": current_user.id, "data": data}).scalar()

    return jsonify({"total": total or 0})

@agua_bp.route("/agua/editar", methods=["PUT"])
@login_required
@perfil_completo_required
def editar_agua():
    data = request.get_json()

    if not data or "quantidade" not in data or "data" not in data:
        return jsonify({"erro": "Dados incompletos."}), 400

    try:
        nova_quantidade = int(data["quantidade"])
        data_registro = datetime.strptime(data["data"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"erro": "Dados inválidos."}), 400

    if nova_quantidade < 0 or nova_quantidade > 12000:
        return jsonify({"erro": "Quantidade deve estar entre 0 e 12000ml."}), 400

    with engine.begin() as conn:
        resultado = conn.execute(text("""
            UPDATE agua_registros
            SET quantidade_ml = :qtd
            WHERE usuario_id = :id AND data = :data
        """), {
            "qtd": nova_quantidade,
            "id": current_user.id,
            "data": data_registro
        })

        if resultado.rowcount == 0:
            return jsonify({"erro": "Registro de água não encontrado."}), 404

    return jsonify({
        "mensagem": "Quantidade de água atualizada com sucesso.",
        "total": nova_quantidade
    })
    
@agua_bp.route("/agua/remover", methods=["DELETE"])
@login_required
@perfil_completo_required
def remover_agua():
    data = request.get_json()

    if not data or "data" not in data:
        return jsonify({"erro": "Dados incompletos."}), 400

    try:
        data_registro = datetime.strptime(data["data"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"erro": "Dados inválidos."}), 400

    with engine.begin() as conn:
        resultado = conn.execute(text("""
            DELETE FROM agua_registros
            WHERE usuario_id = :id AND data = :data
        """), {
            "id": current_user.id,
            "data": data_registro
        })

        if resultado.rowcount == 0:
            return jsonify({"erro": "Registro de água não encontrado."}), 404

    return jsonify({
        "mensagem": "Consumo de água do dia removido com sucesso.",
        "total": 0
    })



            
