document.addEventListener("DOMContentLoaded", function () {

    const tipoHidden = document.getElementById("tipo-refeicao-hidden");
    const modalEditar = new bootstrap.Modal(document.getElementById("modalEditarRefeicao"));
    const dataSpan = document.getElementById("data-selecionada");
    const seletorData = document.getElementById("seletor-data");
    const btnAnterior = document.getElementById("dia-anterior");
    const btnProximo = document.getElementById("proximo-dia");
    const btnCalendario = document.getElementById("abrir-calendario");
    const hoje = new Date();
    
    const fp = flatpickr(seletorData, {
        locale: "pt",
        dateFormat: "Y-m-d",     
        altInput: false, 
        clickOpens: false,         
        defaultDate: hoje,
        allowInput: true,

        onChange: function (selectedDates) {
            if (selectedDates.length) {
                dataAtual = selectedDates[0];
                atualizarDataDisplay();
                carregarRefeicoes();
            }
        }
    });

    let dataAtual = new Date(seletorData?.value || hoje);
    let alimentoSelecionado = null;

    const atualizarDataDisplay = () => {
        if (dataSpan) {
            dataSpan.textContent = dataAtual.toLocaleDateString("pt-BR");
        }

        window.dataSelecionada = dataAtual.toISOString().split("T")[0];

        fp.setDate(dataAtual, false);
    };

    function atualizarTotais(totais) {
        if (!totais) return;
        document.querySelector("#totais-calorias").textContent = `${totais.calorias_consumidas} kcal`;
        document.querySelector("#totais-proteinas").textContent = `${totais.proteinas_consumidas} g`;
        document.querySelector("#totais-carboidratos").textContent = `${totais.carboidratos_consumidos} g`;
        document.querySelector("#totais-gorduras").textContent = `${totais.gorduras_consumidas} g`;
    }

    function atualizarRestantes(restantes) {
        if (!restantes) return;
        document.querySelector("#restantes-calorias").textContent = `${restantes.calorias_restantes} kcal`;
        document.querySelector("#restantes-proteinas").textContent = `${restantes.proteinas_restantes} g`;
        document.querySelector("#restantes-carboidratos").textContent = `${restantes.carboidratos_restantes} g`;
        document.querySelector("#restantes-gorduras").textContent = `${restantes.gorduras_restantes} g`;
    }

    function carregarRefeicoes() {
        const dataFormatada = dataAtual.toISOString().split("T")[0];
        
        fetch(`/refeicoes/listar?data=${dataFormatada}`)
            .then(res => res.json())
            .then(dados => {
                const refeicoes = dados.refeicoes || {};
                const totais = dados.totais || {};
                const restantes = dados.restantes || {};

                document.querySelectorAll(".refeicao-card").forEach(card => {
                    card.querySelector(".alimentos-list").innerHTML =
                        `<li class="list-group-item text-muted">Nenhum alimento adicionado</li>`;
                });

                for (const tipo in refeicoes) {
                    const card = document.querySelector(`.refeicao-card[data-tipo="${tipo}"]`);
                    if (card) {
                        const lista = card.querySelector(".alimentos-list");
                        if (refeicoes[tipo].length > 0) {
                            lista.innerHTML = refeicoes[tipo].map(a => `
                                <li class="list-group-item d-flex justify-content-between align-items-center refeicao-item"
                                    data-id="${a.id}"
                                    data-nome="${a.alimento}"
                                    data-porcao="${a.porcao}"
                                    data-calorias="${a.calorias}"
                                    data-proteinas="${a.proteinas}"
                                    data-carboidratos="${a.carboidratos}"
                                    data-gorduras="${a.gorduras}"
                                    data-tipo="${tipo}">
                                    <span>${a.alimento} — ${a.porcao}g</span>
                                    <span>${a.calorias} kcal</span>
                                </li>
                            `).join("");

                            inicializarEventosEdicao(lista);
                        }
                    }
                }

                atualizarTotais(totais);
                atualizarRestantes(restantes);
            })
            .catch(err => console.error("Erro ao carregar refeições:", err));
    }

    function inicializarEventosEdicao(lista) {
        lista.querySelectorAll(".refeicao-item").forEach(item => {
            item.addEventListener("click", () => {
                document.getElementById("refeicaoId").value = item.dataset.id;
                document.getElementById("nomeEditar").value = item.dataset.nome;
                document.getElementById("porcaoEditar").value = item.dataset.porcao;
                document.getElementById("caloriasEditar").value = item.dataset.calorias;
                document.getElementById("proteinasEditar").value = item.dataset.proteinas;
                document.getElementById("carboidratosEditar").value = item.dataset.carboidratos;
                document.getElementById("gordurasEditar").value = item.dataset.gorduras;

                modalEditar.show();
            });
        });
    }

    document.getElementById("btnSalvarRefeicao").addEventListener("click", () => {
        const id = document.getElementById("refeicaoId").value;
        const porcao = document.getElementById("porcaoEditar").value;
        const tipo_refeicao = document.querySelector(`.refeicao-card .refeicao-item[data-id="${id}"]`)?.dataset.tipo;

        fetch(`/refeicoes/editar/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                porcao: porcao,
                tipo_refeicao: tipo_refeicao
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.erro) {
                alert(data.erro);
            } else {
                modalEditar.hide();
                carregarRefeicoes();
                atualizarTotais(data.totais);
                atualizarRestantes(data.restantes);
            }
        })
        .catch(err => console.error("Erro ao editar refeição:", err));
    });

    document.getElementById("btnRemoverRefeicao").addEventListener("click", () => {
        const id = document.getElementById("refeicaoId").value;

        if (!confirm("Tem certeza que deseja remover esta refeição?")) return;

        fetch(`/refeicoes/excluir/${id}`, {
            method: "DELETE"
        })
        .then(res => res.json())
        .then(data => {
            if (data.erro) {
                alert(data.erro);
            } else {
                modalEditar.hide();
                carregarRefeicoes();
                atualizarTotais(data.totais);
                atualizarRestantes(data.restantes);
            }
        })
        .catch(err => console.error("Erro ao remover refeição:", err));
    });

    document.querySelectorAll(".adicionar-alimento-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            tipoHidden.value = btn.getAttribute("data-tipo");
            new bootstrap.Modal(document.getElementById("modalAdicionarAlimento")).show();
        });
    });

    document.getElementById("btnAdicionarAlimento").addEventListener("click", () => {
        const porcao = document.getElementById("porcao").value;
        const tipo_refeicao = tipoHidden.value;
        const dataSelecionada = window.dataSelecionada || new Date().toISOString().split("T")[0];

        if (!alimentoSelecionado) {
            alert("Selecione um alimento antes de adicionar.");
            return;
        }

        fetch("/refeicoes/registrar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                alimento_id: alimentoSelecionado.id,
                porcao: porcao,
                tipo_refeicao: tipo_refeicao,
                data_refeicao: dataSelecionada
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.erro) {
                alert(data.erro);
            } else {
                bootstrap.Modal.getInstance(document.getElementById("modalAdicionarAlimento")).hide();
                carregarRefeicoes();
                atualizarTotais(data.totais);
                atualizarRestantes(data.restantes);
            }
        })
        .catch(err => console.error("Erro ao adicionar refeição:", err));
    });

    if (btnAnterior && btnProximo && seletorData) {
        btnAnterior.addEventListener("click", () => {
            dataAtual.setDate(dataAtual.getDate() - 1);
            atualizarDataDisplay();
            carregarRefeicoes();
        });

        btnProximo.addEventListener("click", () => {
            dataAtual.setDate(dataAtual.getDate() + 1);
            atualizarDataDisplay();
            carregarRefeicoes();
        });

        seletorData.addEventListener("change", (e) => {
            const [ano, mes, dia] = e.target.value.split("-").map(Number);
            dataAtual = new Date(ano, mes - 1, dia);
            atualizarDataDisplay();
            carregarRefeicoes();
        });

        btnCalendario?.addEventListener("click", () => {
            fp.open();
        });

    }

    atualizarDataDisplay();
    carregarRefeicoes();

    window.setAlimentoSelecionado = (item) => {
        alimentoSelecionado = item;
    };
});