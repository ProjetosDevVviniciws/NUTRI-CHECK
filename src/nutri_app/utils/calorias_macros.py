from sqlalchemy import text

def calcular_totais_conn(conn, usuario_id, data_refeicao):
    q = text("""
        SELECT
            COALESCE(SUM(calorias), 0) AS calorias_consumidas,
            COALESCE(SUM(proteinas), 0) AS proteinas_consumidas,
            COALESCE(SUM(carboidratos), 0) AS carboidratos_consumidos,
            COALESCE(SUM(gorduras), 0) AS gorduras_consumidas
        FROM refeicoes
        WHERE usuario_id = :usuario_id AND DATE(data) = :data_refeicao
    """)
    r = conn.execute(q, {"usuario_id": usuario_id, "data_refeicao": str(data_refeicao)}).mappings().first()
    return {
        "calorias_consumidas": float(r["calorias_consumidas"] or 0),
        "proteinas_consumidas": float(r["proteinas_consumidas"] or 0),
        "carboidratos_consumidos": float(r["carboidratos_consumidos"] or 0),
        "gorduras_consumidas": float(r["gorduras_consumidas"] or 0),
    }