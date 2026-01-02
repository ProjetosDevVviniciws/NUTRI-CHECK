from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import text
from src.nutri_app.database import engine
from datetime import datetime

progressao_bp = Blueprint('progressao', __name__)

@progressao_bp.route("/progressao", methods=['GET', 'POST'])
@login_required
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
    
