document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("perfil-form");

  fetch("/perfil/dados")
    .then(res => res.json())
    .then(data => {
      if (!data.error) {
        document.getElementById("nome").value = data.nome || "";
        document.getElementById("altura").value = data.altura || "";
        document.getElementById("peso").value = data.peso || "";
        document.getElementById("idade").value = data.idade || "";
        document.getElementById("sexo").value = data.sexo || "M";
      }
    });

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const payload = {
      nome: document.getElementById("nome").value,
      altura: document.getElementById("altura").value,
      peso: document.getElementById("peso").value,
      idade: document.getElementById("idade").value,
      sexo: document.getElementById("sexo").value,
      senha: document.getElementById("senha").value
    };

    fetch("/perfil/atualizar", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        form.reset();
        location.reload(); 
      })
      .catch(err => {
        console.error("Erro ao atualizar perfil:", err);
        alert("Erro ao atualizar perfil.");
      });
  });
});
