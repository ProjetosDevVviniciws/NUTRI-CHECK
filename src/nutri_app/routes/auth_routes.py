from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from src.nutri_app.forms.auth_forms import CadastroForm, LoginForm
from src.nutri_app.database import engine
from src.nutri_app.utils.hash import gerar_hash, verificar_senha
from src.nutri_app.utils.user_login import UserLogin
from sqlalchemy import text
from flask_login import login_user, login_required, logout_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    forms = CadastroForm()
    if forms.validate_on_submit():
        usuario = forms.usuario.data
        email = forms.email.data
        senha_hash = gerar_hash(forms.senha1.data)
        
        with engine.connect() as coon:
            query = text("INSERT INTO usuarios (usuario, email, senha) VALUES (:usuario, :email, :senha)")
            coon.execute(query, {"usuario": usuario, "email": email, "senha": senha_hash})   
            flash("Cadastro realizado com sucesso!", category="success")
            return redirect(url_for('auth.refeicoes'))
    if forms.errors != {}:
        for err in forms.errors.values():
            flash(f"Erro ao cadastrar: {err}", category="danger")
        return render_template("cadastro.html", form= forms)
    
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    forms = LoginForm()
    if forms.validate_on_submit():
        usuario = forms.usuario.data
        senha = forms.senha.data
        
        with engine.connect() as coon:
            query = (text("SELECT * FROM usuarios WHERE usuario = :usuario"))
            result = coon.execute(query, {"usuario": usuario}).fetchone()
            
        if result:
            if verificar_senha(result.senha, senha):
                user = UserLogin(result)
                login_user(user)
                flash(f"Sucesso! Bem-Vindo(a), {result.usuario}", category="success")
                return redirect(url_for('auth.refeicoes'))
            else:
                flash("Usuário ou senha estão incorretos! Tente novamente.", category="danger")
    return render_template("login.html", form=forms)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você fez o logout", category="info")
    return redirect(url_for('home'))
                    