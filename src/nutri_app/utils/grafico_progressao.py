def gerar_grafico_progressao(datas, pesos):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(6, 3))
    plt.plot(datas, pesos, marker='o')
    plt.title('Progresso de Peso')
    plt.ylabel('Kg')
    
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('static/images/graficos/progresso_peso.png')
    plt.close()