from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional, Length
from flask_wtf import FlaskForm

class ProdutoForm(FlaskForm):
    nome = StringField('Nome:' , validators=[DataRequired(), Length(min=2, max=100)])
    codigo_barras = StringField('Código de Barras:', validators=[Optional(), Length(max=50)])
    porcao = FloatField('Porção (g):', validators=[DataRequired()])
    calorias = FloatField('Calorias:', validators=[DataRequired()])
    proteinas = FloatField('Proteínas:', validators=[DataRequired()])
    carboidratos = FloatField('Carboidratos:', validators=[DataRequired()])
    gorduras = FloatField('Gorduras:', validators=[DataRequired()])
    submit = SubmitField('Adicionar Produto')