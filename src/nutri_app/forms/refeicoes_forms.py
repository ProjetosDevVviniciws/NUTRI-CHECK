from wtforms import DecimalField, SelectField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm

class RefeicaoForm(FlaskForm):
    alimento_id = SelectField(label='Alimento', coerce=int, validators=[DataRequired()])
    
    porcao = DecimalField(label='Porção (g)', validators=[
            DataRequired(message="Informe a porção em gramas."),
            NumberRange(min=1, message="A quantidade deve ser maior que 0.")])
    
    tipo_refeicao = SelectField(label='Tipo de Refeição',
        choices=[
            ('cafe', 'Café da Manhã'),
            ('almoco', 'Almoço'),
            ('lanche', 'Lanche da Tarde'),
            ('jantar', 'Jantar')
        ], validators=[DataRequired(message="Selecione o tipo da refeição.")])
    
    submit = SubmitField("Registrar Refeição")

class EditarRefeicaoForm(FlaskForm):
    alimento = SelectField(label="Alimento", coerce=int, validators=[DataRequired()])
    
    porcao = FloatField(label="Porção (g)", validators=[DataRequired(), NumberRange(min=1)])
    
    tipo_refeicao = SelectField(label="Tipo de Refeição", 
        choices=[
            ('cafe_da_manha', 'Café da Manhã'),
            ('almoco', 'Almoço'),
            ('jantar', 'Jantar'),
            ('lanches', 'Lanches'),
        ], validators=[DataRequired()])
    
    submit = SubmitField("Salvar")