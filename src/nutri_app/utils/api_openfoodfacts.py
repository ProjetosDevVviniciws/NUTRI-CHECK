import requests

def buscar_por_codigo_barras(codigo_barras):
    url = f"https://world.openfoodfacts.org/api/v0/product/{codigo_barras}.json"
    resposta = requests.get(url)

    if resposta.status_code != 200:
        return None

    dados = resposta.json()
    produto = dados.get("product", {})

    if not produto or not produto.get("product_name"):
        return None

    nome = produto.get("product_name", "Desconhecido")
    nutriments = produto.get("nutriments", {})

    return {
        "nome": nome,
        "porcao_padrao": nutriments.get("serving_size", 100),
        "calorias": nutriments.get("energy-kcal_100g", 0),
        "proteinas": nutriments.get("proteins_100g", 0),
        "carboidratos": nutriments.get("carbohydrates_100g", 0),
        "gorduras": nutriments.get("fat_100g", 0),
    }
