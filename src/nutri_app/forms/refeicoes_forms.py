from wtforms import DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm

class RefeicaoForm(FlaskForm):
    produto_id = SelectField(label='Produto', coerce=int, validators=[DataRequired()])
    
    porcao = DecimalField(
        label='Porção (g)', 
        validators=[
            DataRequired(message="Informe a porção em gramas."),
            NumberRange(min=1, message="A quantidade deve ser maior que 0.")
        ]
    )
    
    tipo_refeicao = SelectField(
        label='Tipo de Refeição',
        choices=[
            ('cafe', 'Café da Manhã'),
            ('amolmoco', 'Almoço'),
            ('lanche', 'Lanche da Tarde'),
            ('jantar', 'Jantar')
        ],
        validators=[DataRequired(message="Selecione o tipo da refeição.")]
    )
    
    submit = SubmitField("Registrar Refeição")