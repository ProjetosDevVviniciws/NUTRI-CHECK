document.addEventListener("DOMContentLoaded", () => {
  const nomeBuscaInput = document.getElementById('buscaAlimento');
  const nomeInput = document.getElementById('nome');
  const codigoBarrasInput = document.getElementById('codigo_barras');
  const porcaoInput = document.querySelector('input[name="porcao"]');
  const caloriasInput = document.getElementById('calorias');
  const proteinasInput = document.getElementById('proteinas');
  const carboidratosInput = document.getElementById('carboidratos');
  const gordurasInput = document.getElementById('gorduras');

  let originalMacros = {
    calorias: 0,
    proteinas: 0,
    carboidratos: 0,
    gorduras: 0
  };

  function safeNumber(value) {
    let num = parseFloat(value)
    return isNaN(num) ? 0 : num;
  }

  function recalcularMacros(porcao) {
    porcao = safeNumber(porcao)
    if (porcao > 0) {
      caloriasInput.value = ((porcao / 100) * originalMacros.calorias).toFixed(2);
      proteinasInput.value = ((porcao / 100) * originalMacros.proteinas).toFixed(2);
      carboidratosInput.value = ((porcao / 100) * originalMacros.carboidratos).toFixed(2);
      gordurasInput.value = ((porcao / 100) * originalMacros.gorduras).toFixed(2);
    } else {
      caloriasInput.value = proteinasInput.value = carboidratosInput.value = gordurasInput.value = '';
    }
  }

  window.atualizarMacrosOriginais = function () {
    originalMacros.calorias = safeNumber(caloriasInput.value) || 0;
    originalMacros.proteinas = safeNumber(proteinasInput.value) || 0;
    originalMacros.carboidratos = safeNumber(carboidratosInput.value) || 0;
    originalMacros.gorduras = safeNumber(gordurasInput.value) || 0;
    recalcularMacros(parseFloat(porcaoInput.value));
  };

  porcaoInput.addEventListener('input', () => {
    recalcularMacros(parseFloat(porcaoInput.value));
  });

  new TomSelect(nomeBuscaInput, {
    valueField: "id",
    labelField: "nome",
    searchField: "nome",
    load: function (query, callback) {
      if (!query.length) return callback();
      fetch(`/buscar_alimentos?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(json => {
          callback(json.map(item => ({
            id: item.id || "",
            nome: item.text || ""
          })));
        })
        .catch(() => callback());
    },
    render: {
      option: function (item, escape) {
        return `<div>${escape(item.nome || "")}</div>`;
      }
    },
    onChange: function (value) {
      if (!value) return;
      fetch(`/buscar_codigo/${value}`)
        .then(res => res.json())
        .then(data => {
          if (data.erro) {
            alert(data.erro);
            return;
          }
          nomeInput.value = data.nome || '';
          codigoBarrasInput.value = data.codigo_barras || '';
          caloriasInput.value = safeNumber(data.calorias);
          proteinasInput.value = safeNumber(data.proteinas);
          carboidratosInput.value = safeNumber(data.carboidratos);
          gordurasInput.value = safeNumber(data.gorduras);
          atualizarMacrosOriginais();
        })
        .catch(err => {
          console.error("Erro ao buscar código do alimento:", err);
          alert("Erro ao buscar alimento.");
        });
    }
  });
});
