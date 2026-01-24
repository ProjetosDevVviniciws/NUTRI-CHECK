document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-progressao");
    const modalRegistrar = new bootstrap.Modal(document.getElementById("modalRegistrarProgresso"));
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
    
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const peso = inputPeso.value;
        const data = inputData.value;

        if (!peso || peso <= 0) {
            alert("Informe um peso válido.");
            return;
        }

        if (!data) {
            alert("Informe a data.");
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
