document.addEventListener("DOMContentLoaded", () => {
    const nomeBuscaInput = document.querySelector('input[name="nome_busca"]');
    const porcaoInput = document.querySelector('input[name="porcao"]');
    const caloriasInput = document.getElementById('calorias');
    const proteinasInput = document.getElementById('proteinas');
    const carboidratosInput = document.getElementById('carboidratos');
    const gordurasInput = document.getElementById('gorduras');

    let originalMacros = {
        calorias: parseFloat(caloriasInput.value) || 0,
        proteinas: parseFloat(proteinasInput.value) || 0,
        carboidratos: parseFloat(carboidratosInput.value) || 0,
        gorduras: parseFloat(gordurasInput.value) || 0
    };

    function recalcularMacros(porcao) {
        if (!isNaN(porcao) && porcao > 0) {
            caloriasInput.value = ((porcao / 100) * originalMacros.calorias).toFixed(2);
            proteinasInput.value = ((porcao / 100) * originalMacros.proteinas).toFixed(2);
            carboidratosInput.value = ((porcao / 100) * originalMacros.carboidratos).toFixed(2);
            gordurasInput.value = ((porcao / 100) * originalMacros.gorduras).toFixed(2);
        } else {
            caloriasInput.value = proteinasInput.value = carboidratosInput.value = gordurasInput.value = '';
        }
    }

    porcaoInput.addEventListener('input', function () {
        const porcao = parseFloat(porcaoInput.value);
        recalcularMacros(porcao);
    });

    nomeBuscaInput.addEventListener("blur", async () => {
        const nome = nomeBuscaInput.value.trim();
        if (!nome) return;

        try {
            const response = await fetch(`/buscar_nome_api?nome=${encodeURIComponent(nome)}`);
            if (!response.ok) throw new Error("Erro na API");

            const data = await response.json();

            if (data.nome) {
                document.querySelector('input[name="nome"]').value = data.nome;
                caloriasInput.value = data.calorias;
                proteinasInput.value = data.proteinas;
                carboidratosInput.value = data.carboidratos;
                gordurasInput.value = data.gorduras;

                alert("Produto encontrado por nome! Preencha a porção para finalizar o cadastro.");

                atualizarMacrosOriginais();
            } else {
                alert("Produto não encontrado.");
            }
        } catch (error) {
            console.error("Erro ao buscar alimento:", error);
            alert("Erro ao buscar alimento.");
        }
    });

    window.atualizarMacrosOriginais = function () {
        originalMacros.calorias = parseFloat(caloriasInput.value) || 0;
        originalMacros.proteinas = parseFloat(proteinasInput.value) || 0;
        originalMacros.carboidratos = parseFloat(carboidratosInput.value) || 0;
        originalMacros.gorduras = parseFloat(gordurasInput.value) || 0;

        const evento = new Event('input');
        porcaoInput.dispatchEvent(evento);
    };
});
