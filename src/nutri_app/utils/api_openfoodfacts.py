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

def buscar_por_nome(nome_alimento):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={nome_alimento}&search_simple=1&action=process&json=1&page_size=10&fields=product_name,nutriments"

    response = requests.get(url)

    if response.status_code == 200:
        produtos = response.json().get("products", [])
        for produto in produtos:
            nutr = produto.get("nutriments", {})
            if all(nutr.get(k) is not None for k in ["energy-kcal_100g", "proteins_100g", "carbohydrates_100g", "fat_100g"]):
                return {
                    "nome": produto.get("product_name", ""),
                    "calorias": nutr["energy-kcal_100g"],
                    "proteinas": nutr["proteins_100g"],
                    "carboidratos": nutr["carbohydrates_100g"],
                    "gorduras": nutr["fat_100g"]
                }
    return None




