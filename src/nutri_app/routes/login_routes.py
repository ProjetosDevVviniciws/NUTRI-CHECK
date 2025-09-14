from flask import Blueprint, render_template, redirect, url_for, flash
from src.nutri_app.database import engine
from src.nutri_app.utils.hash import verificar_senha
from src.nutri_app.utils.user_login import UserLogin
from src.nutri_app.forms.auth_forms import LoginForm
from sqlalchemy import text
from flask_login import login_user

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=['GET', 'POST'])
def login():
    forms = LoginForm()
    if forms.validate_on_submit():
        usuario = forms.usuario.data
        senha = forms.senha.data
        
        with engine.connect() as conn:
            query = (text("SELECT * FROM usuarios WHERE usuario = :usuario"))
            result = conn.execute(query, {"usuario": usuario}).fetchone()
            
        if result:
            if verificar_senha(result.senha, senha):
                user = UserLogin(result)
                login_user(user)
                flash(f"Sucesso! Bem-Vindo(a), {result.usuario}", category="success")
                return redirect(url_for('home.home'))
            else:
                flash("Usuário ou senha estão incorretos! Tente novamente.", category="danger")
    return render_template("includes/login.html", form=forms)