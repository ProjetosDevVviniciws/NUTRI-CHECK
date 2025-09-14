from flask import Blueprint, render_template, redirect, url_for, flash
from src.nutri_app.forms.agua_forms import AguaForm
from src.nutri_app.utils.decorators import perfil_completo_required
from src.nutri_app.database import engine
from sqlalchemy import text
from flask_login import login_required, current_user
from datetime import date

agua_bp = Blueprint('agua', __name__)

@agua_bp.route("/agua", methods=['GET', 'POST'])
@login_required
@perfil_completo_required
def registrar_agua():
    forms = AguaForm()
    
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