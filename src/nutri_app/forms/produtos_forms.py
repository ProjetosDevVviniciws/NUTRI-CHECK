from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional, Length
from flask_wtf import FlaskForm

class ProdutoForm(FlaskForm):
    nome = StringField(label='Nome:' , validators=[DataRequired(), Length(min=2, max=100)])
    codigo_barras = StringField(label='Código de Barras:', validators=[Optional(), Length(max=50)])
    porcao = FloatField(label='Porção (g):', validators=[DataRequired()])
    calorias = FloatField(label='Calorias:', validators=[DataRequired()])
    proteinas = FloatField(label='Proteínas:', validators=[DataRequired()])
    carboidratos = FloatField(label='Carboidratos:', validators=[DataRequired()])
    gorduras = FloatField(label='Gorduras:', validators=[DataRequired()])
    submit = SubmitField(label='Adicionar Produto')