def gerar_grafico_progressao(peso_inicial, datas, pesos):
    import matplotlib.pyplot as plt
    
    labels = ['Inicial'] + datas
    valores = [peso_inicial] + pesos if pesos else [peso_inicial]

    plt.figure(figsize=(5, 3))
    plt.plot(labels, valores, marker='o')
    plt.title('Progresso de Peso')
    plt.ylabel('Kg')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('static/images/graficos/progresso_peso.png')
    plt.close()