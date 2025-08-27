import requests
from sqlalchemy import text
from src.nutri_app.database import engine

LIMIT = 1000  

def carregar_catalogo_inicial():
    url = f"https://br.openfoodfacts.org/cgi/search.pl?action=process&sort_by=unique_scans_n&page_size={LIMIT}&json=true&fields=product_name,serving_size_gram,energy-kcal_100g,proteins_100g,carbohydrates_100g,fat_100g"
    r = requests.get(url)
    data = r.json()

    produtos = data.get("products", [])
    inseridos = 0

    with engine.begin() as conn:
        for p in produtos:
            nome = p.get("product_name")
            porcao = None
            if p.get("serving_size_gram"):
                try:
                    porcao = float(p["serving_size_gram"].replace("g", "").strip())
                except:
                    porcao = None

            calorias = p.get("energy-kcal_100g")
            proteinas = p.get("proteins_100g")
            carboidratos = p.get("carbohydrates_100g")
            gorduras = p.get("fat_100g")

            if not nome or not calorias:
                continue 

            existe = conn.execute(
                text("SELECT id FROM catalogo_alimentos WHERE nome = :nome"),
                {"nome": nome}
            ).fetchone()

            if not existe:
                conn.execute(text("""
                    INSERT INTO catalogo_alimentos (nome, porcao, calorias, proteinas, carboidratos, gorduras)
                    VALUES (:nome,:porcao, :calorias, :proteinas, :carboidratos, :gorduras)
                """), {
                    "nome": nome[:100],
                    "porcao": porcao or 100,
                    "calorias": calorias,
                    "proteinas": proteinas,
                    "carboidratos": carboidratos,
                    "gorduras": gorduras
                })
                inseridos += 1

    print(f"✅ Catálogo carregado com {inseridos} novos alimentos.")

if __name__ == "__main__":
    carregar_catalogo_inicial()
