from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class PerfilForm(FlaskForm):
    nome = StringField(
        label="Nome",
        validators=[
            DataRequired(message="Informe seu nome."),
            Length(min=2, max=60, message="Nome deve ser entre 2 e 50 caracteres.")
        ]
    )
    
    altura = DecimalField(
        label="Altura (cm)",
        validators=[
            DataRequired(message="Informe sua altura em cm."),
            NumberRange(min=50, max=250, message="Altura deve estar entre 50 e 250cm.")
        ]
    )
    
    peso = DecimalField(
        label="Peso (kg)",
        validators=[
            DataRequired(message="Informe seu peso em kg."),
            NumberRange(min=20, max=300, message="Peso deve estar entre 20 e 300 kg.")
        ]
    )
    
    idade = IntegerField(
        label="Idade",
        validators=[
            DataRequired(message="Informe sua idade."),
            NumberRange(min=10, max=120, message="Idade deve estar entre 10 e 120 anos.")
        ]
    )
    
    senha = PasswordField(
        label="Nova Senha (opcional)",
        validators=[
            Optional(),
            Length(min=6, message="A senha deve ter no mínimo 6 caracteres.")
        ]
    )
    
    submit = SubmitField(label="Salvar Alterações")