document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("input-agua");
    const btn = document.getElementById("btnRegistrarAgua");
    const erro = document.getElementById("erro-agua");
    const totalAgua = document.getElementById("total-agua")
    const seletorData = document.getElementById("seletor-data");

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

    btn.addEventListener("click", () => {

        const valor = Number(input.value.trim());
        const dataSelecionada = window.dataSelecionada || new Date().toISOString().split("T")[0];

        if (!valor) return mostrarErro("Informe a quantidade de água.");
        if (valor < 50 || valor > 12000) return mostrarErro("Informe uma quantidade entre 50ml e 12000ml.");

        erro.classList.add("d-none");

        fetch("/agua/registrar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
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

    function mostrarErro(msg) {
        erro.textContent = msg;
        erro.classList.remove("d-none");
    }

});
