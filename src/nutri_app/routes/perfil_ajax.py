from flask import Blueprint, render_template, request, jsonify
from src.nutri_app.database import engine
from sqlalchemy import text
from flask_login import login_required, current_user
from src.nutri_app.utils.macros import calcular_tmb_macros
from src.nutri_app.utils.hash import gerar_hash
from datetime import date

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route("/perfil")
@login_required
def perfil_page():
    return render_template("includes/perfil.html")


@perfil_bp.route("/perfil/dados")
@login_required
def perfil_dados():
    with engine.connect() as conn:
        usuario = conn.execute(text("""
            SELECT nome, altura, peso, idade, sexo,
                calorias_meta, proteinas_meta, carboidratos_meta, gorduras_meta
            FROM usuarios
            WHERE id = :id
        """), {"id": current_user.id}).mappings().first()
    
    if usuario:
        return jsonify(dict(usuario)), 200
    else:
        return jsonify({
            "nome": "",
            "altura": "",
            "peso": "",
            "idade": "",
            "sexo": "M",
            "calorias_meta": "",
            "proteinas_meta": "",
            "carboidratos_meta": "",
            "gorduras_meta": ""
        }), 200


@perfil_bp.route("/perfil/atualizar", methods=["PUT"])
@login_required
def perfil_atualizar():
    data = request.json
    nome = data.get("nome")
    altura = float(data.get("altura"))
    peso = float(data.get("peso"))
    idade = int(data.get("idade"))
    sexo = data.get("sexo")
    nova_senha = data.get("senha")

    macros = calcular_tmb_macros(peso=peso, altura=altura, idade=idade, sexo=sexo)
    senha_hash = gerar_hash(nova_senha) if nova_senha else None

    with engine.begin() as conn:
        query = text("""
            UPDATE usuarios SET 
                nome = :nome,
                altura = :altura,
                peso = :peso,
                idade = :idade,
                sexo = :sexo,
                senha = COALESCE(:senha, senha),
                calorias_meta = :calorias,
                proteinas_meta = :proteinas,
                carboidratos_meta = :carboidratos,
                gorduras_meta = :gorduras,
                ultima_atualizacao = :hoje
            WHERE id = :id
        """)
        conn.execute(query, {
            "id": current_user.id,
            "nome": nome,
            "altura": altura,
            "peso": peso,
            "idade": idade,
            "sexo": sexo,
            "senha": senha_hash,
            "calorias": macros["calorias"],
            "proteinas": macros["proteinas"],
            "carboidratos": macros["carboidratos"],
            "gorduras": macros["gorduras"],
            "hoje": date.today()
        })

    return jsonify({"message": "Perfil atualizado com sucesso!"}), 200            