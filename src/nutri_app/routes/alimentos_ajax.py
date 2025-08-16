from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import text
from src.nutri_app.database import engine
import requests

alimentos_ajax_bp = Blueprint('alimentos_ajax', __name__)

def buscar_api_e_salvar(codigo):
    url = f"https://world.openfoodfacts.org/api/v0/product/{codigo}.json"
    r = requests.get(url).json()

    if r.get("status") != 1:
        return None

    produto = r["product"]
    nome = produto.get("product_name")
    porcao = produto.get("serving_size")
    if porcao and "g" in porcao.lower():
        try:
            porcao = float(porcao.lower().replace("g", "").strip())
        except:
            porcao = None

    calorias = produto.get("nutriments", {}).get("energy-kcal_100g")
    proteinas = produto.get("nutriments", {}).get("proteins_100g")
    carboidratos = produto.get("nutriments", {}).get("carbohydrates_100g")
    gorduras = produto.get("nutriments", {}).get("fat_100g")

    if not nome or calorias is None:
        return None

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO catalogo_alimentos (nome, codigo_barras, porcao, calorias, proteinas, carboidratos, gorduras)
            VALUES (:nome, :codigo, :porcao, :calorias, :proteinas, :carboidratos, :gorduras)
        """), {
            "nome": nome[:100],
            "codigo": codigo,
            "porcao": porcao or 100,
            "calorias": calorias,
            "proteinas": proteinas,
            "carboidratos": carboidratos,
            "gorduras": gorduras
        })

    return {
        "nome": nome,
        "codigo_barras": codigo,
        "porcao": porcao or 100,
        "calorias": calorias,
        "proteinas": proteinas,
        "carboidratos": carboidratos,
        "gorduras": gorduras
    }

@alimentos_ajax_bp.route('/buscar_alimentos', methods=['GET'])
@login_required
def buscar_alimentos():
    termo = request.args.get('q', '').strip()
    if not termo:
        return jsonify([])

    with engine.connect() as conn:
        result_catalogo = conn.execute(text("""
            SELECT codigo_barras, nome
            FROM catalogo_alimentos
            WHERE nome LIKE :termo
            LIMIT 10
        """), {"termo": f"%{termo}%"}).mappings().all()

        result_usuario = conn.execute(text("""
            SELECT codigo_barras, nome
            FROM alimentos
            WHERE nome LIKE :termo AND usuario_id = :usuario_id
            LIMIT 10
        """), {
            "termo": f"%{termo}%",
            "usuario_id": current_user.id
        }).mappings().all()

    vistos = set()
    alimentos = []
    for row in result_usuario + result_catalogo:
        codigo = row.get("codigo_barras") or ""
        nome = row.get("nome") or ""
        if codigo and codigo not in vistos:
            vistos.add(codigo)
            alimentos.append({
                "id": codigo,
                "text": nome
            })

    return jsonify(alimentos)

@alimentos_ajax_bp.route('/buscar_codigo/<codigo>', methods=['GET'])
@login_required
def buscar_codigo(codigo):
    with engine.connect() as conn:
        alimento = conn.execute(text("""
            SELECT * FROM catalogo_alimentos
            WHERE codigo_barras = :codigo
        """), {"codigo": codigo}).mappings().first()

        if not alimento:
            alimento = conn.execute(text("""
                SELECT * FROM alimentos
                WHERE codigo_barras = :codigo AND usuario_id = :usuario_id
            """), {
                "codigo": codigo,
                "usuario_id": current_user.id
            }).mappings().first()

    if alimento:
        return jsonify({k: v if v is not None else "" for k, v in dict(alimento).items()})

    novo_alimento = buscar_api_e_salvar(codigo)
    if novo_alimento:
        return jsonify({k: v if v is not None else "" for k, v in novo_alimento.items()})

    return jsonify({"erro": "Alimento não encontrado"}), 404


