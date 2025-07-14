from flask import Blueprint, render_template, redirect, url_for, flash
from src.nutri_app.forms.auth_forms import CadastroForm
from src.nutri_app.database import engine
from src.nutri_app.utils.hash import gerar_hash
from sqlalchemy import text
from flask_login import  login_required, logout_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    forms = CadastroForm()
    if forms.validate_on_submit():
        usuario = forms.usuario.data
        email = forms.email.data
        senha_hash = gerar_hash(forms.senha1.data)
        
        with engine.connect() as conn:
            query = text("INSERT INTO usuarios (usuario, email, senha) VALUES (:usuario, :email, :senha)")
            conn.execute(query, {"usuario": usuario, "email": email, "senha": senha_hash})   
            flash("Cadastro realizado com sucesso!", category="success")
            return redirect(url_for('refeicoes.registrar_refeicao'))
    if forms.errors != {}:
        for err in forms.errors.values():
            flash(f"Erro ao cadastrar: {err}", category="danger")
        return render_template("cadastro.html", form= forms)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você fez o logout", category="info")
    return redirect(url_for('/.home'))
                    