from wtforms import StringField, FloatField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Optional, Length
from flask_wtf import FlaskForm

class AlimentoForm(FlaskForm):
    nome = StringField(label='Nome:' , validators=[DataRequired(), Length(min=2, max=100)])
    codigo_barras = StringField(label='Código de Barras:', validators=[Optional(), Length(max=50)])
    porcao = FloatField(label='Porção (g):', validators=[DataRequired()])
    calorias = DecimalField("Calorias", validators=[Optional()])
    proteinas = DecimalField("Proteínas", validators=[Optional()])
    carboidratos = DecimalField("Carboidratos", validators=[Optional()])
    gorduras = DecimalField("Gorduras", validators=[Optional()])
    submit = SubmitField(label='Cadastrar Alimento')