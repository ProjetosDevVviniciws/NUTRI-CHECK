from flask import Blueprint, render_template, redirect, url_for, flash
from src.nutri_app.database import engine
from src.nutri_app.utils.hash import verificar_senha
from src.nutri_app.utils.user_login import UserLogin
from src.nutri_app.forms.auth_forms import LoginForm
from src.nutri_app.forms.auth_forms import EsqueciSenhaForm, RedefinirSenhaForm
from src.nutri_app.utils.token import gerar_token, validar_token
from src.nutri_app.utils.email_service import enviar_email_reset
from src.nutri_app.utils.hash import gerar_hash
from sqlalchemy import text
from flask_login import login_user

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=['GET', 'POST'])
def login():
    forms = LoginForm()
    if forms.validate_on_submit():
        nome = forms.nome.data
        senha = forms.senha.data
        
        with engine.connect() as conn:
            query = (text("SELECT * FROM usuarios WHERE nome = :nome"))
            result = conn.execute(query, {"nome": nome}).fetchone()
            
        if result:
            if verificar_senha(result.senha, senha):
                user = UserLogin(result)
                login_user(user)
                flash(f"Sucesso! Bem-Vindo(a), {result.nome}", category="info")
                return redirect(url_for('home.home'))
            else:
                flash("Nome ou senha estão incorretos! Tente novamente", category="danger")
    return render_template("pages/login.html", form=forms)

@login_bp.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    form = EsqueciSenhaForm()
    if form.validate_on_submit():
        email = form.email.data

        with engine.connect() as conn:
            user = conn.execute(text("""
                SELECT * FROM usuarios WHERE email = :email
            """), {"email": email}).mappings().first()

        if user:
            token = gerar_token(email)
            link = url_for("login.resetar_senha", token=token, _external=True)

            enviar_email_reset(user["email"], link, user["nome"])

        flash("Se o email existir, um link de recuperação foi enviado.", "info")
        return redirect(url_for("login.login"))

    return render_template("pages/esqueci_senha.html", form=form)

@login_bp.route("/redefinir-senha/<token>", methods=["GET", "POST"])
def redefinir_senha(token):
    form = RedefinirSenhaForm()
    email = validar_token(token)

    if not email:
        flash("Token inválido ou expirado.", "danger")
        return redirect(url_for("login.login"))

    if form.validate_on_submit():
        nova_senha = form.senha.data
        senha_hash = gerar_hash(nova_senha)

        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE usuarios
                SET senha = :senha
                WHERE email = :email
            """), {
                "senha": senha_hash,
                "email": email
            })

        flash("Senha atualizada com sucesso!", "info")
        return redirect(url_for("login.login"))

    return render_template("pages/redefinir_senha.html", form=form)
