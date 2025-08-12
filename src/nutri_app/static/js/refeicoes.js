document.addEventListener("DOMContentLoaded", function () {
    const tipoHidden = document.getElementById("tipo-refeicao-hidden");

    function carregarRefeicoes() {
        fetch("/refeicoes/listar")
            .then(res => res.json())
            .then(dados => {
                document.querySelectorAll(".refeicao-card").forEach(card => {
                    card.querySelector(".alimentos-list").innerHTML =
                        `<li class="list-group-item text-muted">Nenhum alimento adicionado</li>`;
                });

                for (const tipo in dados) {
                    const card = document.querySelector(`.refeicao-card[data-tipo="${tipo}"]`);
                    if (card) {
                        const lista = card.querySelector(".alimentos-list");
                        if (dados[tipo].length > 0) {
                            lista.innerHTML = dados[tipo].map(a => `
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    <span>${a.nome} — ${a.porcao}g</span>
                                    <span>${a.calorias} kcal</span>
                                </li>
                            `).join("");
                        }
                    }
                }
            })
            .catch(err => console.error("Erro ao carregar refeições:", err));
    }

    document.querySelectorAll(".adicionar-alimento-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            tipoHidden.value = btn.getAttribute("data-tipo");
            new bootstrap.Modal(document.getElementById("alimentoModal")).show();
        });
    });

    carregarRefeicoes();
});
