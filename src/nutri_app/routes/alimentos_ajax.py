from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import text
from src.nutri_app.database import engine
import requests

alimentos_ajax_bp = Blueprint('alimentos_ajax', __name__)

def buscar_api_e_salvar(nome):
    url = f"https://world.openfoodfacts.org/api/v0/product/{nome}.json"
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
            INSERT INTO catalogo_alimentos (nome, porcao, calorias, proteinas, carboidratos, gorduras)
            VALUES (:nome, :porcao, :calorias, :proteinas, :carboidratos, :gorduras)
        """), {
            "nome": nome[:100],
            "porcao": porcao or 100,
            "calorias": calorias,
            "proteinas": proteinas,
            "carboidratos": carboidratos,
            "gorduras": gorduras
        })

    return {
        "nome": nome,
        "porcao": porcao or 100,
        "calorias": calorias,
        "proteinas": proteinas,
        "carboidratos": carboidratos,
        "gorduras": gorduras
    }

@alimentos_ajax_bp.route("/buscar_alimentos")
@login_required
def buscar_alimentos():
    termo = request.args.get('q', '').strip()
    if not termo:
        return jsonify([])

    with engine.connect() as conn:
        result_catalogo = conn.execute(text("""
            SELECT id, nome, calorias, proteinas, carboidratos, gorduras
            FROM catalogo_alimentos
            WHERE nome LIKE :termo
        """), {"termo": f"%{termo}%"}).mappings().all()

        result_usuario = conn.execute(text("""
            SELECT id, nome, calorias, proteinas, carboidratos, gorduras
            FROM alimentos
            WHERE nome LIKE :termo AND usuario_id = :usuario_id
        """), {
            "termo": f"%{termo}%",
            "usuario_id": current_user.id
        }).mappings().all()

    vistos = set()
    alimentos = []
    for row in result_usuario + result_catalogo:
        alimento_id = row.get("id")
        nome = row.get("nome") or ""
        if alimento_id not in vistos:
            vistos.add(alimento_id)
            alimentos.append({
                "id": alimento_id,
                "nome": nome,
                "origem": "usuario" if row in result_usuario else "catalogo",
                "calorias": float(row.get("calorias") or 0),
                "proteinas": float(row.get("proteinas") or 0),
                "carboidratos": float(row.get("carboidratos") or 0),
                "gorduras": float(row.get("gorduras") or 0)
            })

    return jsonify(alimentos)




