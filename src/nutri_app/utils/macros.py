import numpy as np

def calcular_macros_totais(produto, porcao_consumida):
    fator = porcao_consumida / produto.porcao
    return np.array([
        produto.calorias,
        produto.proteinas,
        produto.carboidratos,
        produto.gorduras
    ]) * fator
    
def calcular_tmb_macros(peso: float, altura: float, idade: int, sexo: str = "masculino") -> dict:
    if sexo.lower() == "femino":
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