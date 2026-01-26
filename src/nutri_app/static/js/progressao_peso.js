document.addEventListener("DOMContentLoaded", () => {
    const modalElement = document.getElementById("modalRegistrarProgresso");
    const inputPeso = document.getElementById("input-peso");
    const inputData = document.getElementById("input-data");
    const erro = document.getElementById("erro-progressao");

    flatpickr("#input-data", {
        locale: "pt",
        dateFormat: "Y-m-d",   
        altInput: true,
        altFormat: "d/m/Y",    
        defaultDate: "today",
        allowInput: true
    });
    
    modalRegistrar.addEventListener("submit", async (e) => {
        e.preventDefault();

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
            window.location.reload(); 
        } else {
            alert(result.message);
        }
    });
});
