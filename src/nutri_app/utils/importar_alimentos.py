import requests
from sqlalchemy import text
from src.nutri_app.database import engine

def importar_alimentos_polulares():
    url = "https://br.openfoodfacts.org/cgi/search.pl"
    
    total_paginas = 6
    
    with engine.connect() as conn:
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
                print("Erro ao acessar a API do OpenFoodFacts.")
    
            data = reponse.json()
            produtos = data.get("products", [])
            
            for produto in produtos:
                nome = produto.get("product_name", "").strip()
                codigo_barras = produto.get("code", "").strip()
                
                nutriments = produto.get("nutriments", {})
                calorias = nutriments.get("energy-kcal_100g")
                proteinas = nutriments.get("proteins_100g")
                gordura = nutriments.get("fat_100g")
                carboidrato = nutriments.get("carbohydrates_100g")
                
                if not nome or calorias is None or not codigo_barras:
                    continue
                
                existe = conn.execute(text("""
                    SELECT id FROM alimentos WHERE codigo_barras = :codigo_barras
                    """), {"codigo_barras": codigo_barras}).fetchone()
                
                if existe:
                    print(f"Produto já existe: {nome}")
                    
                try:
                    conn.execute(text("""
                        INSERT INTO alimentos (
                            nome, codigo_barras, porcao, calorias, proteinas, gorduras, carboidratos, usuario_id 
                        ) VALUES (
                            :nome, codigo_barras, porcao, calorias, proteinas, gorduras, carboidratos, NULL
                        )
                    """), {
                        "nome": nome,
                        "codigo_barras": codigo_barras,
                        "porcao": 100,
                        "calorias": calorias,
                        "proteinas": proteinas or 0,
                        "gorduras": gordura or 0,
                        "carboidratos": carboidrato or 0
                    })
                    print(f"Inserido: {nome}")
                except Exception as e:
                    print(f"Erro ao inserir {nome}: {e}")
    
    print("\nImportação concluída.")
    
if __name__ == "__main__":
    importar_alimentos_polulares()
                    