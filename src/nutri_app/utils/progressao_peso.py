import matplotlib.pyplot as plt
import io
import base64

def gerar_graficos_progressao(datas, pesos):
    if not datas or not pesos:
        return None
    
    img = io.BytesIO()
    
    plt.figure(figsize=(8, 4))
    plt.plot(datas, pesos, marker='o', color='blue')
    plt.title("Progresso de Peso")
    plt.xlabel("Data")
    plt.tight_layout()
    plt.grid()
    plt.savefig(img, format='png')
    
    img.seek(0)
    return base64.b64decode(img.getvalue()).decode('utf-8')