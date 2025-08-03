from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.nutri_app.forms.refeicoes_forms import RefeicaoForm
from src.nutri_app.utils.decorators import perfil_completo_required
from src.nutri_app.database import engine
from sqlalchemy import text
from flask_login import login_required, current_user
from src.nutri_app.utils.macros import calcular_macros_totais
from src.nutri_app.utils.api_openfoodfacts import buscar_por_codigo_barras
from datetime import date

refeicoes_bp = Blueprint('refeicoes', __name__)

@refeicoes_bp.route('/refeicoes', methods=['GET', 'POST'])
@login_required
def registrar_refeicao():
    form = RefeicaoForm()
    alimento_api = None
    
    with engine.begin() as conn:
        alimentos_db = conn.execute(
            text("SELECT id, nome, usuario_id FROM alimentos WHERE usuario_id = :id OR usuario_id IS NULL"),
            {"id": current_user.id}
        ).fetchall()
        
        choices = [(p.id, f"{p.nome}") if p.usuario_id is None else (p.id, p.nome) for p in alimentos_db]
        
        codigo_barras = request.args.get("codigo_barras")
        if codigo_barras:
            alimento_api = buscar_por_codigo_barras(codigo_barras)
            if alimento_api:
                choices.insert(0, (-1, f"{alimento_api['nome']} (via OpenFoodFacts)"))
            else:
                flash("Produto não encontrado via OpenFoodFacts.", category="warning")
        if not choices:
            flash("Nenhum alimento cadastrado. Você pode buscar por código de barras.", category="info")
                
        form.alimento_id.choices = choices
     
        if form.validate_on_submit():
            alimento_id = form.alimento.data
            porcao = float(form.porcao.data)
            tipo_refeicao = form.tipo_refeicao.data
            
            if alimento_id == -1:
                if not alimento_api:
                    flash("Não foi possível registrar o alimento da API.", category="danger")
                    return redirect(url_for('refeicoes.registrar_refeicao'))
                
                macros = calcular_macros_totais(alimento_api, porcao)
            else:
                alimento = conn.execute(
                    text("""SELECT * FROM alimentos WHERE id = :id"""),{"id": alimento_id}).fetchone()
                
                if not alimento:
                    flash("Alimento não encontrado!", category="danger")
                    return redirect(url_for('refeicoes.registrar_refeicao'))
                
                macros = calcular_macros_totais(alimento, porcao)
                
            usuario = conn.execute(
                text("""
                    SELECT calorias_meta, proteinas_meta, carboidratos_meta, gorduras_meta,
                            calorias_consumidas, proteinas_consumidas, carboidratos_consumidos, gorduras_consumidas,
                            ultima_atualizacao
                    FROM usuarios WHERE id = :id"""),
                {"id": current_user.id}
            ).fetchone()
                
            hoje = date.today()
            if usuario.ultima_atualizacao.date() != hoje:
                conn.execute(text("""
                    UPDATE usuarios SET
                            calorias_consumidas = 0,
                            proteinas_consumidas = 0,
                            carboidratos_consumidos = 0,
                            gorduras_consumidas = 0,
                            ultima_atualizacao = :hoje
                    WHERE id = :id
            """), {"id": current_user.id, "hoje": hoje})
            
            query = text(""" 
                INSERT INTO refeicoes (usuario_id, alimento_id, porcao, calorias, proteinas, carboidratos, gorduras, tipo_refeicao)
                VALUES (:usuario_id, :alimento_id, :porcao, :calorias, :proteinas, :carboidratos, :gorduras, :tipo_refeicao) 
            """)
            conn.execute(query, {
                "usuario_id": current_user.id,
                "alimento_id": None if alimento_id == -1 else alimento_id,
                "porcao": porcao,
                "calorias": macros[0],
                "proteinas": macros[1],
                "carboidratos": macros[2],
                "gorduras": macros[3],
                "tipo_refeicao": tipo_refeicao
            })
            
            conn.execute(text("""
                UPDATE usuarios SET
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
            
        if form.errors != {}:
            for err in form.errors.values():
                flash(f"Erro ao registrar sua refeição: {err}", category="danger")

    return render_template("includes/refeicoes.html", form=form)
            
    
