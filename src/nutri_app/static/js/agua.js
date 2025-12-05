document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("input-agua");
    const btn = document.getElementById("btnRegistrarAgua");
    const erro = document.getElementById("erro-agua");

    btn.addEventListener("click", () => {

        const valor = Number(input.value.trim());

        if (!valor) {
            mostrarErro("Informe a quantidade de água.");
            return;
        }

        if (valor < 50 || valor > 12000) {
            mostrarErro("Informe uma quantidade entre 50ml e 12000ml.");
            return;
        }

        erro.classList.add("d-none");

        fetch("/agua/registrar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ quantidade: valor })
        })
        .then(res => res.json())
        .then(data => {

            if (data.erro) {
                mostrarErro(data.erro);
                return;
            }

            const modal = bootstrap.Modal.getInstance(document.getElementById("modalRegistrarAgua"));
            modal.hide();

            alert(data.mensagem);

            input.value = "";
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
