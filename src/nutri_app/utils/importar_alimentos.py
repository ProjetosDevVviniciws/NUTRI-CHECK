import requests
from sqlalchemy import text
from src.nutri_app.database import engine

def importar_alimentos_populares():
    url = "https://br.openfoodfacts.org/cgi/search.pl"
    
    total_paginas = 6
    
    with engine.begin() as conn:
        for pagina in range(1, total_paginas + 1):
            parametros = {
                "action": "process",
                "tagtype_0": "countries",
                "tag_contains_0": "contains",
                "tag_0": "brazil", 
                "sort_by": "unique_scans_n",  
                "page_size": 50,  
                "page": pagina,   
                "json": 1
            }
            
            reponse = requests.get(url, params=parametros)
            if reponse.status_code != 200:
                print("Erro ao acessar a API do OpenFoodFacts na página {pagina}.")
    
            data = reponse.json()
            produtos = data.get("products", [])
            
            for produto in produtos:
                nome = produto.get("product_name", "").strip()
                nutriments = produto.get("nutriments", {})
                calorias = nutriments.get("energy-kcal_100g")
                proteinas = nutriments.get("proteins_100g")
                gordura = nutriments.get("fat_100g")
                carboidrato = nutriments.get("carbohydrates_100g")
                
                if not nome or calorias is None:
                    continue
                
                existe = conn.execute(text("""
                    SELECT id FROM catalogo_alimentos WHERE nome = :nome
                    """), {"nome": nome}).fetchone()
                
                if existe:
                    print(f"Produto já existe: {nome}")
                    continue
                
                try:
                    porcao = produto.get("serving_size")
                    if porcao and "g" in str(porcao).lower():
                        try:
                            porcao = float(str(porcao).lower().replace("g", "").strip())
                        except:
                            porcao = 100
                    else:
                        porcao = 100
                    
                    conn.execute(text("""
                        INSERT INTO catalogo_alimentos (nome, porcao, calorias, proteinas, carboidratos, gorduras)
                        VALUES (:nome, :porcao, :calorias, :proteinas, :carboidratos, :gorduras)
                    """), {
                        "nome": nome[:100],
                        "porcao": porcao,
                        "calorias": calorias,
                        "proteinas": proteinas or 0,
                        "gorduras": gordura or 0,
                        "carboidratos": carboidrato or 0
                    })
                    print(f"Inserido: {nome}")
                except Exception as e:
                    print(f"Erro ao inserir {nome}: {e}")
                    raise
    
    print("\nImportação concluída.")
    
if __name__ == "__main__":
    importar_alimentos_populares()
                    