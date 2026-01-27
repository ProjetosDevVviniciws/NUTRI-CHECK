def gerar_grafico_progressao(datas, pesos):
    import os
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use("Agg")
    from flask import current_app

    datas = list(datas)
    pesos = [float(p) for p in pesos]
    
    plt.figure(figsize=(6, 3))
    plt.plot(datas, pesos, marker='o')
    plt.ylabel('Kg')
    plt.xlabel('Data')
    plt.grid(True)
    plt.tight_layout()
    
    caminho = os.path.join(
        current_app.root_path,
        'static',
        'images',
        'graficos'
    )  
    
    os.makedirs(caminho, exist_ok=True)
    
    plt.savefig(os.path.join(caminho, 'progresso_peso.png'))
    plt.close()