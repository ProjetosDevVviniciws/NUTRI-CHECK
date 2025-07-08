from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class AguaForm(FlaskForm):
    quantidade = IntegerField(
        label="Quantidade de água (ml)",
        validators=[
            DataRequired(message="Informe a quantidade de água."),
            NumberRange(min=50, max=12000, message="Informe entre 50ml e 12000ml.")
        ]
    )
    
    submit = SubmitField("Registrar Água")