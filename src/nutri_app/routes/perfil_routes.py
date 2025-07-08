from flask import Blueprint, render_template, redirect, request, url_for, flash
from src.nutri_app.forms.perfil_forms import PerfilForm
from src.nutri_app.database import engine
from sqlalchemy import text
from flask_login import login_required, current_user
from src.nutri_app.utils.macros import calcular_tmb_macros
from datetime import date

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route('/perfil' ,methods=['GET', 'POST'])
@login_required
def perfil_usuario():
    forms = PerfilForm()
    
    with engine.connect() as conn:
        usuario = conn.execute(
            text("SELECT * FROM usuario WHERE id = :id"),
            {"id": current_user.id}
        ).fetchone()
    
    if request.method == 'GET':
        if usuario:
            forms.nome.data = usuario.nome
            forms.altura.data = usuario.altura
            forms.peso.data = usuario.peso
            forms.idade.data = usuario.idade
            forms.sexo.data = usuario.sexo
        else:
            flash("Usuário não encontrado!", category="danger")
            return redirect(url_for('perfil.perfil_usuario'))

    if forms.validate_on_submit():
        nome = forms.nome.data
        altura = float(forms.altura.data)
        peso = float(forms.peso.data)
        idade = int(forms.idade.data)
        nova_senha = forms.senha.data
        sexo = forms.sexo.data
        
        macros = calcular_tmb_macros(peso=peso, altura=altura, idade=idade, sexo=sexo)
        
        with engine.begin() as conn:
            query = text("""
                UPDATE usuario SET 
                    nome = :nome,
                    altura = :altura,
                    peso = :peso,
                    idade = :idade,
                    senha = COALESCE(:senha, senha),
                    calorias_meta = :calorias,
                    proteinas_meta = :proteinas,
                    carboidratos_meta = :carboidratos,
                    gorduras_meta = :gorduras,
                    ultima_atualizacao = :hoje
                WHERE id = :id
            """)
            conn.execute(query, {
                "id": current_user.id,
                "nome": nome,
                "altura": altura,
                "peso": peso,
                "idade": idade,
                "senha": nova_senha if nova_senha else None,
                "calorias": macros["calorias"],
                "proteinas": macros["proteinas"],
                "carboidratos": macros["carboidratos"],
                "gorduras": macros["gorduras"],
                "hoje": date.today()
            })
            
        flash("Perfil atualizado com sucesso!", category="success")
        return redirect(url_for('perfil.perfil_usuario'))
    
    return render_template("perfil.html", form=forms)
            