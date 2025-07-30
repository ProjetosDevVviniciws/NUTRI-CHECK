import numpy as np

def calcular_macros_totais(alimento, porcao_consumida):
    fator = porcao_consumida / alimento.porcao
    return np.array([
        alimento.calorias,
        alimento.proteinas,
        alimento.carboidratos,
        alimento.gorduras
    ]) * fator

def calcular_macros_por_porcao(porcao, macros_100g):
    fator = porcao / 100.00
    return {
        'calorias': round(macros_100g.get('calorias', 0) * fator, 2),
        'proteinas': round(macros_100g.get('proteinas', 0) * fator, 2),
        'carboidratos': round(macros_100g.get('carboidratos', 0) * fator, 2),
        'gorduras': round(macros_100g.get('gorduras', 0) * fator, 2)
    }

def calcular_tmb_macros(peso: float, altura: float, idade: int, sexo: str = "masculino") -> dict:
    if sexo.lower() == "feminino":
        tmb = 10 * peso + 6.25 * altura - 5 * idade - 161
    else:
        tmb = 10 * peso + 6.25 * altura - 5 * idade + 5
        
    calorias = tmb * 1.55 
    proteinas = peso * 2.2
    gorduras = peso * 1.0
    carboidratos = (calorias - (proteinas * 4 + gorduras * 9)) / 4
    
    return {
        "calorias": round(calorias, 2),
        "proteinas": round(proteinas, 2),
        "gorduras": round(gorduras, 2),
        "carboidratos": round(carboidratos, 2)
    }