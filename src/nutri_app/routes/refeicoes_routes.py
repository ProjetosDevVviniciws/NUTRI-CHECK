from flask import Blueprint, render_template, redirect, url_for, flash
from src.nutri_app.forms.refeicoes_forms import RefeicaoForm
from src.nutri_app.database import engine
from sqlalchemy import text
from flask_login import login_required, current_user
from src.nutri_app.utils.macros import calcular_macros_totais
from datetime import date
import numpy as np

refeicoes_bp = Blueprint('refeicoes', __name__)

@refeicoes_bp.route('/refeicoes', methods=['GET', 'POST'])
@login_required
def registrar_refeicao():
    forms = RefeicaoForm()
    
    with engine.begin() as conn:
        produtos1 = conn.execute(
            text("SELECT id, nome FROM produtos WHERE usuario_id = :id"),
            {"id": current_user.id}
        ).fetchall()
        forms.produto_id.choices = [(p.id, p.nome) for p in produtos1]
     
        if forms.validate_on_submit():
            produto_id = forms.produto_id.data
            porcao = float(forms.porcao.data)
            tipo_refeicao = forms.tipo_refeicao.data
            
            produto = conn.execute(
                text("SELECT * FROM produtos WHERE id = :id"),
                {"id": produto_id}).fetchone()
                
            usuario = conn.execute(
                text("""
                    SELECT calorias_meta, proteinas_meta, carboidratos_meta, gorduras_meta,
                            calorias_consumidas, proteinas_consumidas, carboidratos_consumidos, gorduras_consumidas,
                            ultima_atualizacao
                    FROM usuario WHERE id = :id"""),
                {"id": current_user.id}
            ).fetchone()
            
            if not produto:
                flash("Produto não econtrado!", category="danger")
                return redirect(url_for('refeicoes.registrar_refeicao'))
            macros = calcular_macros_totais(produto, porcao)
                
            hoje = date.today()
            if usuario.ultima_atualizacao.date() != hoje:
                conn.execute(text("""
                    UPDATE usuario SET
                            calorias_consumidas = 0,
                            proteinas_consumidas = 0,
                            carboidratos_consumidos = 0,
                            gorduras_consumidas = 0,
                            ultima_atualizacao = :hoje
                    WHERE id = :id
            """), {"id": current_user.id, "hoje": hoje})
            
            query = text(""" 
                INSERT INTO refeicoes (usuario_id, produto_id, porcao, quantidade, calorias, proteinas, carboidratos, gorduras, tipo_refeicao)
                VALUES (:usuario_id, :produto_id, :porcao, :calorias, :proteinas, :carboidratos, :gorduras, :tipo_refeicao) 
            """)
            conn.execute(query, {
                "usuario_id": current_user.id,
                "produto_id": produto_id,
                "porcao": porcao,
                "calorias": macros[0],
                "proteinas": macros[1],
                "carboidratos": macros[2],
                "gorduras": macros[3],
                "tipo_refeicao": tipo_refeicao
            })
            
            conn.execute(text("""
                UPDATE usuario SET
                    calorias_consumidas = calorias_consumidas + :cal,
                    proteinas_consumidas = proteinas_consumidas + :prot,
                    carboidratos_consumidos = carboidratos_consumidos + :carb,
                    gorduras_consumidas = gorduras_consumidas + :gord
                WHERE id = :id
            """), {
                "id": current_user.id,
                "cal": macros[0],
                "prot": macros[1],
                "carb": macros[2],
                "gord": macros[3]
            })
            
            flash("Refeição registrada com sucesso!", category="success")
            return redirect(url_for('refeicoes.registrar_refeicao'))
            
        if forms.errors != {}:
            for err in forms.errors.values():
                flash(f"Erro ao registrar sua refeição: {err}", category="danger")

    return render_template("refeicoes.html", form=forms, produtos=produtos1)
            
    
