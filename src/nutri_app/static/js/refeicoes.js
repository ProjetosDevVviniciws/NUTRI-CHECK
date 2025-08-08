document.addEventListener("DOMContentLoaded", () => {
  const alimentoSelect = document.getElementById("alimento-select");
  const porcaoInput = document.getElementById("porcao");
  const adicionarBtn = document.getElementById("btn-adicionar-refeicao");
  const listarBtn = document.getElementById("btn-listar-refeicoes");
  const refeicoesList = document.getElementById("lista-refeicoes");

  let originalMacros = { calorias: 0, proteinas: 0, carboidratos: 0, gorduras: 0 };

  // Inicializa Tom Select para autocomplete com busca AJAX
  const ts = new TomSelect(alimentoSelect, {
    valueField: "id",
    labelField: "nome",
    searchField: "nome",
    load: function(query, callback) {
      if (!query.length) return callback();
      fetch(`/refeicoes/buscar_alimentos?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(json => {
          // Ajusta label para mostrar origem (catálogo ou usuário)
          json.forEach(item => {
            item.nome = item.nome + (item.origem === "catalogo" ? " (Catálogo)" : " (Meu)");
          });
          callback(json);
        })
        .catch(() => callback());
    },
    render: {
      option: function(item, escape) {
        return `<div>${escape(item.nome)}</div>`;
      }
    }
  });

  // Quando seleciona alimento, busca detalhes para preencher macros base
  alimentoSelect.addEventListener("change", async () => {
    const alimentoId = ts.getValue();
    if (!alimentoId) return;

    try {
      // Buscar detalhes do alimento da API (ajuste para origem se precisar)
      // Exemplo: pode ser adaptado para considerar origem, aqui assumindo 'usuario'
      const response = await fetch(`/alimentos/detalhes_alimento/${alimentoId}`);
      if (!response.ok) throw new Error("Não encontrado");

      const data = await response.json();

      originalMacros = {
        calorias: parseFloat(data.calorias) || 0,
        proteinas: parseFloat(data.proteinas) || 0,
        carboidratos: parseFloat(data.carboidratos) || 0,
        gorduras: parseFloat(data.gorduras) || 0
      };

      recalcularMacros(parseFloat(porcaoInput.value));
    } catch (err) {
      console.error("Erro ao buscar detalhes do alimento", err);
    }
  });

  // Recalcula macros conforme a porção
  function recalcularMacros(porcao) {
    if (!porcao || isNaN(porcao) || porcao <= 0) {
      atualizarCamposMacros(0, 0, 0, 0);
      return;
    }
    atualizarCamposMacros(
      ((porcao / 100) * originalMacros.calorias).toFixed(2),
      ((porcao / 100) * originalMacros.proteinas).toFixed(2),
      ((porcao / 100) * originalMacros.carboidratos).toFixed(2),
      ((porcao / 100) * originalMacros.gorduras).toFixed(2)
    );
  }

  function atualizarCamposMacros(cals, prots, carbs, gord) {
    document.getElementById("calorias").value = cals;
    document.getElementById("proteinas").value = prots;
    document.getElementById("carboidratos").value = carbs;
    document.getElementById("gorduras").value = gord;
  }

  porcaoInput.addEventListener("input", () => {
    const porcao = parseFloat(porcaoInput.value);
    recalcularMacros(porcao);
  });

  // Função para enviar nova refeição para o backend
  adicionarBtn.addEventListener("click", async () => {
    const alimentoId = ts.getValue();
    const porcao = parseFloat(porcaoInput.value);

    if (!alimentoId || !porcao || porcao <= 0) {
      alert("Selecione um alimento válido e informe a porção.");
      return;
    }

    try {
      const response = await fetch("/refeicoes/criar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ alimento_id: alimentoId, porcao })
      });
      const data = await response.json();

      if (response.ok) {
        alert(data.mensagem);
        listarRefeicoes(); // atualizar lista após adicionar
      } else {
        alert(data.erro || "Erro ao registrar refeição.");
      }
    } catch (err) {
      alert("Erro ao conectar com o servidor.");
      console.error(err);
    }
  });

  // Função para listar refeições do dia
  async function listarRefeicoes() {
    try {
      const response = await fetch("/refeicoes/listar");
      if (!response.ok) throw new Error("Erro ao listar");
      const dados = await response.json();

      refeicoesList.innerHTML = "";
      dados.forEach(r => {
        const li = document.createElement("li");
        li.textContent = `${r.alimento} — ${r.porcao} g — ${r.calorias} kcal`;
        refeicoesList.appendChild(li);
      });
    } catch (err) {
      refeicoesList.innerHTML = "<li>Erro ao carregar refeições</li>";
      console.error(err);
    }
  }

  listarBtn.addEventListener("click", listarRefeicoes);

  // Carregar lista ao abrir a página
  listarRefeicoes();
});
