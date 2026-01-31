document.addEventListener("DOMContentLoaded", () => {
    const modalElement = document.getElementById("modalRegistrarProgresso");
    const modalRegistrar = new bootstrap.Modal(modalElement);
    const inputPeso = document.getElementById("input-peso");
    const inputData = document.getElementById("input-data");
    const btnRegistrar = document.getElementById("btnRegistrarProgresso");
    const erro = document.getElementById("erro-progressao");

    flatpickr("#input-data", {
        locale: "pt",
        dateFormat: "Y-m-d",   
        altInput: true,
        altFormat: "d/m/Y",    
        defaultDate: "today",
        allowInput: true
    });
    
    modalElement.addEventListener("shown.bs.modal", () => {
        erro.classList.add("d-none");
        erro.textContent = "";
    });
    
    btnRegistrar.addEventListener("click", async (e) => {
        erro.classList.add("d-none");
        erro.textContent = "";

        const peso = inputPeso.value;
        const data = inputData.value;

        if (!peso || peso <= 0) {
            erro.textContent = "Informe um peso válido.";
            erro.classList.remove("d-none");
            return;
        }

        if (!data) {
            erro.textContent = "Informe a data.";
            erro.classList.remove("d-none");
            return;
        }

        const response = await fetch("/progressao/registrar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ peso, data })
        });

        const result = await response.json();

        if (result.success) {
            alert(result.message);
            modalRegistrar.hide()
            window.location.reload(); 
        } else {
            alert(result.message);
        }
    });

    if (window.graficoPesoData) {
        const ctx = document.getElementById("graficoPeso");

        new Chart(ctx, {
            type: "line",
            data: {
                labels: window.graficoPesoData.labels,
                datasets: [{
                    label: "Peso (kg)",
                    data: window.graficoPesoData.values,
                    borderWidth: 2,
                    tension: 0.3,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: "Kg"
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: "Data"
                        }
                    }
                }
            }
        });
    }

    const listaRegistros = document.getElementById("lista-registros-peso");

    async function carregarRegistrosPeso() {
        if (!listaRegistros) return;

        const response = await fetch("/progressao/listar");
        const result = await response.json();

        listaRegistros.innerHTML = "";

        if (!result.success || result.progressoes.length === 0) {
            listaRegistros.innerHTML = `
                <li class="list-group-item text-muted text-center">
                    Nenhum registro ainda
                </li>
            `;
            return;
        }

        result.progressoes.forEach(registro => {
            const li = document.createElement("li");
            li.classList.add(
                "list-group-item",
                "d-flex",
                "justify-content-between",
                "align-items-center",
                "registro-peso"
            );

            li.dataset.data = registro.data; 
            li.dataset.peso = registro.peso;

            li.innerHTML = `
                <span>${registro.data_formatada}</span>
                <strong>${registro.peso.toFixed(1)} kg</strong>
            `;

            li.addEventListener("click", () => abrirModalEditar(li));

            listaRegistros.appendChild(li);
        });
    }

    carregarRegistrosPeso();

    const modalEditarEl = document.getElementById("modalEditarProgresso");
    const modalEditar = new bootstrap.Modal(modalEditarEl);

    const inputEditarPeso = modalEditarEl.querySelector("#input-peso");
    const inputEditarData = modalEditarEl.querySelector("#input-data");
    const erroEditar = modalEditarEl.querySelector("#erro-progressao");

    let dataRegistroSelecionado = null;

    function abrirModalEditar(elemento) {
        erroEditar.classList.add("d-none");
        erroEditar.textContent = "";

        const peso = elemento.dataset.peso;
        const data = elemento.dataset.data;

        dataRegistroSelecionado = data;

        inputEditarPeso.value = peso;
        inputEditarData.value = data;

        modalEditar.show();
    }

    document.getElementById("btnSalvarProgresso").addEventListener("click", async () => {
        erroEditar.classList.add("d-none");
        erroEditar.textContent = "";

        const peso = inputEditarPeso.value;
        const data = inputEditarData.value;

        if (!peso || peso <= 0) {
            erroEditar.textContent = "Informe um peso válido.";
            erroEditar.classList.remove("d-none");
            return;
        }

        const response = await fetch("/progressao/editar", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ peso, data })
        });

        const result = await response.json();

        if (result.success) {
            alert(result.message);
            modalEditar.hide();
            window.location.reload();
        } else {
            erroEditar.textContent = result.message;
            erroEditar.classList.remove("d-none");
        }
    });

});
