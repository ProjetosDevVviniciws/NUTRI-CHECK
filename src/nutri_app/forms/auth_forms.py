from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Length, EqualTo, ValidationError
from src.nutri_app.database import engine
from sqlalchemy import text

class CadastroForm(FlaskForm):
    
    def validate_usuario(self, check_user):
        with engine.connect() as coon:
            user = coon.execute(text("SELECT * FROM usuarios WHERE usuario = :usuario"), {"usuario": check_user.data})
            if user.first():
                raise ValidationError("Usuário já existe! Cadastre outro nome de usuário.")
            
    def validate_email(self, check_email):
        with engine.connect() as coon:
            email = coon.execute(text("SELECT * FROM usuarios WHERE email = :email"), {"email": check_email.data})
            if email.first():
                raise ValidationError("E-mail já existe! Cadastre outro e-mail.")
            
    def validate_senha(self, check_senha):
        with engine.connect() as coon:
            senha = coon.execute(text("SELECT * FROM usuarios WHERE senha = :senha"), {"senha": check_senha.data})
            if senha.first():
                raise ValidationError("Senha já existe! Cadastre outra senha.")
    
    usuario = StringField(label='Usuario:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    senha1 = PasswordField(label='Senha:', validators=[Length(min=6), DataRequired()])
    senha2 = PasswordField(label='Confirmação da Senha:', validators=[EqualTo('senha1'), DataRequired()])
    submit = SubmitField(label='Cadastrar')
    
class LoginForm(FlaskForm):
    usuario = StringField(label='Usuário:', validators=[DataRequired()])
    senha = PasswordField(label='Senha:', validators=[DataRequired()])
    submit = SubmitField(label='Login')