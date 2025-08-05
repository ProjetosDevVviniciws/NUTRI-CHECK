from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional, Length
from flask_wtf import FlaskForm

class AlimentoForm(FlaskForm):
    nome = StringField(label='Nome:' , validators=[DataRequired(), Length(min=2, max=100)])
    codigo_barras = StringField(label='Código de Barras:', validators=[Optional(), Length(max=50)])
    nome_busca = StringField(label='Buscar por Nome:', validators=[Optional()])
    porcao = FloatField(label='Porção (g):', validators=[DataRequired()], render_kw={"id": "porcao"})
    calorias = FloatField("Calorias:", render_kw={"readonly": True, "id": "calorias"})
    proteinas = FloatField("Proteínas", render_kw={"readonly": True, "id": "proteinas"})
    carboidratos = FloatField("Carboidratos", render_kw={"readonly": True, "id": "carboidratos"})
    gorduras = FloatField("Gorduras", render_kw={"readonly": True, "id": "gorduras"})
    submit = SubmitField(label='Cadastrar Alimento')