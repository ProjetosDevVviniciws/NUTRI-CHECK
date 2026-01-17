from flask import Blueprint, render_template, request, jsonify
from src.nutri_app.utils.decorators import perfil_completo_required
from flask_login import login_required, current_user
from sqlalchemy import text
from src.nutri_app.database import engine
from datetime import datetime

progressao_bp = Blueprint('progressao', __name__)

@progressao_bp.route("/progressao/registrar", methods=['GET', 'POST'])
@login_required
@perfil_completo_required
def registrar_progressao_peso():

    datas, pesos = [], []
    
    if request.method == 'POST':
        data_json = request.get_json()

        peso = data_json.get('peso')
        data = data_json.get('data')
        
        if not peso or not data:
            return jsonify({"success": False, "message": "Dados inválidos."}), 400

        try:
            peso = float(peso)
            data = datetime.strptime(data, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"success": False, "message": "Formato inválido."}), 400
        
        with engine.begin() as conn: 
            conn.execute(text("""
                INSERT INTO progressao_peso (usuario_id, peso, data)
                VALUES (:usuario_id, :peso, :data)
            """), {"usuario_id": current_user.id, "peso": peso, "data": data})
                
            return jsonify({"success": True, "message": "Progresso registrado com sucesso!"})

    with engine.begin() as conn:    
        resultados = conn.execute(text("""
            SELECT peso, data
            FROM progressao_peso
            WHERE usuario_id = :id
            ORDER BY data ASC
        """), {"id": current_user.id}).fetchall()
        
        if resultados:
            pesos = [float(r.peso) for r in resultados]
            datas = [r.data.strftime('%d/%m') for r in resultados]
            
    return render_template(
        "pages/progressao.html",
        datas=datas,
        pesos=pesos
    )
    
@progressao_bp.route("/progressao/listar")
@login_required
@perfil_completo_required
def listar_progressao_peso():
    with engine.begin() as conn:
        resultados = conn.execute(text("""
            SELECT peso, data
            FROM progressao_peso
            WHERE usuario_id = :usuario_id
            ORDER BY data ASC
        """), {"usuario_id": current_user.id}).fetchall()

    progressoes = [
        {
            "peso": float(r.peso),
            "data": r.data.strftime("%Y-%m-%d"),
            "data_formatada": r.data.strftime("%d/%m/%Y")
        }
        for r in resultados
    ]

    return jsonify({"success": True, "progressoes": progressoes})

@progressao_bp.route("/progressao/editar", methods=["PUT"])
@login_required
@perfil_completo_required
def editar_progressao_peso():
    data_json = request.get_json()

    peso = data_json.get("peso")
    data = data_json.get("data")

    if not peso or not data:
        return jsonify({"success": False, "message": "Dados inválidos."}), 400

    try:
        peso = float(peso)
        data = datetime.strptime(data, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"success": False, "message": "Formato inválido."}), 400

    with engine.begin() as conn:
        resultado = conn.execute(text("""
            UPDATE progressao_peso
            SET peso = :peso
            WHERE usuario_id = :usuario_id
              AND data = :data
        """), {
            "peso": peso,
            "usuario_id": current_user.id,
            "data": data
        })

        if resultado.rowcount == 0:
            return jsonify({"success": False, "message": "Registro não encontrado."}), 404

    return jsonify({"success": True, "message": "Progresso atualizado com sucesso!"})

@progressao_bp.route("/progressao/excluir", methods=["DELETE"])
@login_required
@perfil_completo_required
def excluir_progressao_peso():
    data_json = request.get_json()
    data = data_json.get("data")

    if not data:
        return jsonify({"success": False, "message": "Data não informada."}), 400

    try:
        data = datetime.strptime(data, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"success": False, "message": "Formato inválido."}), 400

    with engine.begin() as conn:
        resultado = conn.execute(text("""
            DELETE FROM progressao_peso
            WHERE usuario_id = :usuario_id
              AND data = :data
        """), {
            "usuario_id": current_user.id,
            "data": data
        })

        if resultado.rowcount == 0:
            return jsonify({"success": False, "message": "Registro não encontrado."}), 404

    return jsonify({"success": True, "message": "Progresso removido com sucesso!"})


    
