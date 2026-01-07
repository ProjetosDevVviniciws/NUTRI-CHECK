def gerar_grafico_progressao(peso_inicial, peso_atual):
    import matplotlib.pyplot as plt
    
    valores = [peso_inicial, peso_atual]
    labels = ['Inicial', 'Atual']

    plt.figure(figsize=(5, 3))
    plt.plot(labels, valores, marker='o')
    plt.title('Progresso de Peso')
    plt.ylabel('Kg')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('static/images/graficos/progresso_peso.png')
    plt.close()