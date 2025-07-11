from flask import Blueprint, render_template, redirect, url_for, flash
from src.nutri_app.forms.produtos_forms import ProdutoForm
from src.nutri_app.database import engine
from sqlalchemy import text
from flask_login import login_required, current_user

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/produtos', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    forms = ProdutoForm()
    if forms.validate_on_submit():
        nome = forms.nome.data
        codigo_barras = forms.codigo_barras.data
        porcao = float(forms.porcao.data)
        calorias = float(forms.calorias.data)
        proteinas = float(forms.proteinas.data)
        carboidratos = float(forms.carboidratos.data)
        gorduras = float(forms.gorduras.data)
        
        with engine.connect() as conn:
            query = text("""
                INSERT INTO produtos (usuario_id, nome, codigo_barras, porcao, calorias, proteinas, carboidratos, gorduras)
                VALUES (:usuario_id, :nome, :codigo_barras, :porcao, :calorias, :proteinas, :carboidratos, :gorduras)
            """)
            conn.execute(query, {
                "usuario_id": current_user.id, 
                "nome": nome,
                "codigo_barras": codigo_barras,
                "porcao": porcao,
                "calorias": calorias,
                "proteinas": proteinas,
                "carboidratos": carboidratos,
                "gorduras": gorduras
            })
            flash("Produto adicionado com sucesso!", category="success")
            return redirect(url_for('refeicoes.registrar_refeicao'))
    if forms.errors != {}:
        for err in forms.errors.values(): 
            flash(f"Erro ao cadastrar produto: {err}", category="danger")
        
    return render_template("produtos.html", form=forms)
       