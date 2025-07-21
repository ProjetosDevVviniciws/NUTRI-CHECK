from flask import Blueprint, render_template, redirect, url_for, flash
from src.nutri_app.forms.progressao_forms import ProgressaoForm
from flask_login import login_required, current_user
from sqlalchemy import text
from src.nutri_app.database import engine
from src.nutri_app.utils.progressao_peso import gerar_graficos_progressao

progressao_bp = Blueprint('progressao', __name__)

@progressao_bp.route('/progressao', methods=['GET', 'POST'])
@login_required
def registrar_progressao_peso():
    forms = ProgressaoForm()
    grafico_base64 = None
    historico_progressao = []
    
    with engine.begin() as conn:
        if forms.validate_on_submit():
            peso = float(forms.peso.data)
            data = forms.data.data
            
            conn.execute(text("""
                INSERT INTO progressao_peso (usuario_id, peso, data)
                VALUES (:usuario_id, :peso, :data)
            """), {"usuario_id": current_user.id, "peso": peso, "data": data})
            
            flash("Progresso registrado com sucesso!", category="success")
            return redirect(url_for('progressao.registrar_progressao_peso'))
        
        resultados = conn.execute(text("""
            SELECT peso, data
            FROM progressao_peso
            WHERE usuario_id = :id
            ORDER BY data ASC
        """), {"id": current_user.id}).fetchall()
        
        if resultados:
            pesos = [float(r.peso) for r in resultados]
            datas = [r.data.strftime('%d/%m') for r in resultados]
            historico_progressao = resultados
            
            grafico_base64 = gerar_graficos_progressao(datas, pesos)
        else:
            flash("Você ainda não registrou nenhum progresso para gerar o gráfico.", category="danger")
            return redirect(url_for('progressao.registrar_progressao_peso'))
    
    return render_template("includes/progressao.html", form=forms, grafico=grafico_base64, historico=historico_progressao)