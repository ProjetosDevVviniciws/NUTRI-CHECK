def gerar_grafico_progressao(peso_inicial, datas, pesos):
    import matplotlib.pyplot as plt
    
    datas_plot = ['Inicial'] + datas
    pesos_plot = [peso_inicial] + pesos if pesos else [peso_inicial]

    plt.figure(figsize=(6, 3))
    plt.plot(datas_plot, pesos_plot, marker='o')
    plt.title('Progresso de Peso')
    plt.ylabel('Kg')
    plt.xlabel('Data')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('static/images/graficos/progresso_peso.png')
    plt.close()