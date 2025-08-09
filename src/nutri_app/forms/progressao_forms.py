from flask_wtf import FlaskForm
from wtforms import DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from datetime import date

class ProgressaoForm(FlaskForm):
    peso = DecimalField(label='Peso (kg)',
        validators=[DataRequired("Informe seu peso."), NumberRange(min=0)],
        render_kw={"placeholder": "Ex: 85.5"})
    
    data = DateField(label='Data',default=date.today,
        validators=[DataRequired(message="Informe a data.")])
    
    submit = SubmitField('Registrar')