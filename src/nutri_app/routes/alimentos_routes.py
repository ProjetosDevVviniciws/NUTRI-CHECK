from flask import Blueprint, render_template, redirect, url_for, flash, request
from nutri_app.forms.alimentos_forms import AlimentoForm
from src.nutri_app.utils.macros import calcular_macros_por_porcao
from nutri_app.utils.api_openfoodfacts import buscar_por_codigo_barras, buscar_por_nome
from src.nutri_app.utils.decorators import perfil_completo_required
from src.nutri_app.database import engine
from sqlalchemy import text
from flask_login import login_required, current_user

alimentos_bp = Blueprint('alimentos', __name__)

@alimentos_bp.route('/alimentos', methods=['GET', 'POST'])
@login_required
def cadastrar_alimento():
    form = AlimentoForm()

    if request.method == 'POST':
        if form.codigo_barras.data and not form.calorias.data:
            dados = buscar_por_codigo_barras(form.codigo_barras.data)
            if dados:
                form.nome.data = dados["nome"]
                form.calorias.data = dados["calorias"]
                form.proteinas.data = dados["proteinas"]
                form.carboidratos.data = dados["carboidratos"]
                form.gorduras.data = dados["gorduras"]
                flash("Produto encontrado! Preencha a porção para finalizar o cadastro.", category="info")
            else:
                flash("Produto não encontrado. Por favor, preencha os dados manualmente.", category="warning")
            return render_template("includes/alimentos.html", form=form)

        elif form.nome_busca.data and not form.calorias.data:
            dados = buscar_por_nome(form.nome_busca.data)
            if dados:
                form.nome.data = dados["nome"]
                form.calorias.data = dados["calorias"]
                form.proteinas.data = dados["proteinas"]
                form.carboidratos.data = dados["carboidratos"]
                form.gorduras.data = dados["gorduras"]
                flash("Produto encontrado por nome! Preencha a porção para finalizar o cadastro.", category="info")
            else:
                flash("Produto não encontrado por nome. Preencha os dados manualmente.", category="warning")
            return render_template("includes/alimentos.html", form=form)
        
    if form.validate_on_submit():
        nome = form.nome.data
        codigo_barras = form.codigo_barras.data or None
        porcao = float(form.porcao.data)

        macros = calcular_macros_por_porcao(porcao, {
            "calorias": float(form.calorias.data),
            "proteinas": float(form.proteinas.data),
            "carboidratos": float(form.carboidratos.data),
            "gorduras": float(form.gorduras.data)
        })

        with engine.begin() as conn:
            query = text("""
                INSERT INTO alimentos (usuario_id, nome, codigo_barras, porcao, calorias, proteinas, carboidratos, gorduras)
                VALUES (:usuario_id, :nome, :codigo_barras, :porcao, :calorias, :proteinas, :carboidratos, :gorduras)
            """)
            conn.execute(query, {
                "usuario_id": current_user.id,
                "nome": nome,
                "codigo_barras": codigo_barras,
                "porcao": porcao,
                **macros
            })

        flash("Alimento adicionado com sucesso!", category="success")
        return redirect(url_for('refeicoes.registrar_refeicao'))

    if form.errors:
        for err in form.errors.values():
            flash(f"Erro ao cadastrar alimento: {err}", category="danger")

    return render_template("includes/alimentos.html", form=form)
