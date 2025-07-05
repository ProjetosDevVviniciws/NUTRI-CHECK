from flask import Blueprint, render_template, redirect, url_for, flash
from src.nutri_app.forms.refeicoes_forms import RefeicaoForm
from src.nutri_app.database import engine
from sqlalchemy import text
from flask_login import login_required
import numpy as np

refeicoes_bp = Blueprint('refeicoes', __name__)

@refeicoes_bp.route('/refeicoes', methods=['GET', 'POST'])
@login_required
def registrar_refeicao():
    forms = RefeicaoForm()
    
    with engine.connect() as conn:
        produtos1 = conn.execute(text("SELECT id, nome FROM produtos")).fetchall()
    
    forms.produto_id.choices = [(p.id, p.nome) for p in produtos1]
     
    if forms.validate_on_submit():
        produto_id = forms.produto_id.data
        porcao = float(forms.porcao.data)
        tipo_refeicao = forms.tipo_refeicao.data
        
        with engine.connect() as conn:
            produto = conn.execute(
                text("SELECT * FROM produtos WHERE id = :id"),
                {"id": produto_id}).fetchone()
            
            if produto:
                fator = porcao / produto.porcao
                macros = np.array([
                    produto.calorias,
                    produto.proteinas,
                    produto.carboidratos,
                    produto.gorduras
                ]) * fator
                
                query = text(""" 
                    INSERT INTO refeicoes (produto_id, porcao, quantidade, calorias, proteinas, carboidratos, gorduras, tipo_refeicao)
                    VALUES (:produto_id, :porcao, :calorias, :proteinas, :carboidratos, :gorduras, :tipo_refeicao) 
                """)
                conn.execute(query, {
                    "produto_id": produto_id,
                    "porcao": porcao,
                    "calorias": macros[0],
                    "proteinas": macros[1],
                    "carboidratos": macros[2],
                    "gorduras": macros[3],
                    "tipo_refeicao": tipo_refeicao
                })
                
                flash("Refeição registrada com sucesso!", category="success")
                return redirect(url_for('refeicoes.registrar_refeicao'))
            else:
                flash("Produto não econtrado!", category="danger")
                return redirect(url_for('refeicoes.registrar_refeicao'))
    if forms.errors != {}:
        for err in forms.errors.values():
            flash(f"Erro ao registrar sua refeição: {err}", category="danger")
            
    return render_template("refeicoes.html", form=forms, produtos=produtos1)
                
    
