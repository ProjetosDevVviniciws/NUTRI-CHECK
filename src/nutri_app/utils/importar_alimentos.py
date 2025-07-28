import csv
from sqlalchemy import text
from src.nutri_app.database import engine
import os

def importar_alimentos_csv():
    csv.field_size_limit(1_000_000)
    caminho_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'alimentos_openfoodfacts.csv')
    
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT COUNT(*) FROM alimentos WHERE usuario_id IS NULL"))
        if resultado.scalar() > 0:
            return
        
        with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            alimentos_inseridos = 0
            for row in reader:
                try:
                    nome = row.get('product_name', '').strip()
                    if not nome:
                        continue
                    
                    calorias = float(row.get('energy-kcal_100g') or 0)
                    proteinas = float(row.get('proteins_100g') or 0)
                    carboidratos = float(row.get('carbohydrates_100g') or 0)
                    gorduras = float(row.get('fat_100g') or 0)
                    porcao = 100.0
                    
                    query = text("""
                        INSERT INTO alimentos (usuario_id, nome, porcao, calorias, proteinas, carboidratos, gorduras)
                        VALUES (NULL, :nome, :porcao, :calorias, :proteinas, :carboidratos, :gorduras)
                    """)
                    conn.execute(query, {
                       "nome": nome,
                       "porcao": porcao,
                       "calorias": calorias,
                       "proteinas": proteinas,
                       "carboidratos": carboidratos,
                       "gorduras": gorduras 
                    })
                    alimentos_inseridos +=1
                    
                    if alimentos_inseridos >= 500:
                        break
                except Exception:
                    continue