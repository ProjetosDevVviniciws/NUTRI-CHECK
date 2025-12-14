document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("input-agua");
    const btn = document.getElementById("btnRegistrarAgua");
    const erro = document.getElementById("erro-agua");
    const totalAgua = document.getElementById("total-agua");
    const dataSpan = document.getElementById("data-selecionada");
    const seletorData = document.getElementById("seletor-data");
    const btnAnterior = document.getElementById("dia-anterior");
    const btnProximo = document.getElementById("proximo-dia");
    const btnCalendario = document.getElementById("abrir-calendario");

    function carregarTotalAgua(data) {
        fetch(`/agua/total?data=${data}`)
            .then(res => res.json())
            .then(data => {
                totalAgua.textContent = `${data.total} ml`;
            })
            .catch(() => {
                totalAgua.textContent = "0 ml";
            });
    }

    window.dataSelecionada = seletorData.value;
    carregarTotalAgua(window.dataSelecionada);

    btn.addEventListener("click", () => {

        const valor = Number(input.value.trim());
        const dataSelecionada = window.dataSelecionada;

        if (!valor) return mostrarErro("Informe a quantidade de água.");
        if (valor < 50 || valor > 12000) return mostrarErro("Informe uma quantidade entre 50ml e 12000ml.");

        erro.classList.add("d-none");

        fetch("/agua/registrar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ quantidade: valor, data: dataSelecionada })
        })
            .then(res => res.json())
            .then(data => {

                if (data.erro) {
                    mostrarErro(data.erro);
                    return;
                }

                const modal = bootstrap.Modal.getInstance(document.getElementById("modalRegistrarAgua"));
                modal.hide();

                totalAgua.textContent = `${data.total} ml`;
                input.value = "";

                alert(data.mensagem);

            })
            .catch(() => {
                mostrarErro("Erro ao registrar água. Tente novamente.");
            });
    });

    if (btnAnterior && btnProximo && seletorData) {
        btnAnterior.addEventListener("click", () => {
            dataAtual.setDate(dataAtual.getDate() - 1);
            atualizarDataDisplay();
            carregarTotalAgua();
        });

        btnProximo.addEventListener("click", () => {
            dataAtual.setDate(dataAtual.getDate() + 1);
            atualizarDataDisplay();
            carregarTotalAgua();
        });

        seletorData.addEventListener("change", e => {
            const [ano, mes, dia] = e.target.value.split("-").map(Number);
            dataAtual = new Date(ano, mes - 1, dia);
            atualizarDataDisplay();
            carregarTotalAgua();
        });

        btnCalendario?.addEventListener("click", () => {
            seletorData.showPicker();
        });
    }
        
    function mostrarErro(msg) {
        erro.textContent = msg;
        erro.classList.remove("d-none");
    }
});
