document.addEventListener("DOMContentLoaded", () => {
    const toggleSenha = document.getElementById("toggle-senha");
    const senhaInput = document.getElementById("senha-input");
    const iconeSenha = document.getElementById("icone-senha");

    if (!toggleSenha || !senhaInput || !iconeSenha) return;

    toggleSenha.addEventListener("click", () => {
        const isPassword = senhaInput.type === "password";

        senhaInput.type = isPassword ? "text" : "password";
        iconeSenha.classList.toggle("fa-eye");
        iconeSenha.classList.toggle("fa-eye-slash");
    });
});
