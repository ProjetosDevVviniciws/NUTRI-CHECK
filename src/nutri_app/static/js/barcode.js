document.addEventListener("DOMContentLoaded", () => {
  const btnLerCodigo = document.getElementById("btnLerCodigo");
  const scannerContainer = document.getElementById("scanner-container");
  const readerElement = document.getElementById("reader");

  let html5QrCode = null;

  btnLerCodigo.addEventListener("click", () => {
    scannerContainer.style.display = "block";

    if (!html5QrCode) {
      html5QrCode = new Html5Qrcode("reader");
    }

    // Lista as câmeras disponíveis
    Html5Qrcode.getCameras().then(devices => {
      if (devices && devices.length) {
        // Tenta achar uma câmera USB (se não achar, usa a primeira)
        let cameraId = devices[0].id;
        const usbCamera = devices.find(d => d.label.toLowerCase().includes("usb"));
        if (usbCamera) {
          cameraId = usbCamera.id;
        }

        html5QrCode.start(
          cameraId,
          {
            fps: 10,
            qrbox: function (viewfinderWidth, viewfinderHeight) {
              let minEdgeSize = Math.min(viewfinderWidth, viewfinderHeight);
              return { 
                width: minEdgeSize * 0.8, 
                height: minEdgeSize * 0.4 
              };
            },
            formatsToSupport: [
              Html5QrcodeSupportedFormats.EAN_13,
              Html5QrcodeSupportedFormats.UPC_A,
              Html5QrcodeSupportedFormats.UPC_E,
              Html5QrcodeSupportedFormats.CODE_128
            ]
          },
          (decodedText, decodedResult) => {
            console.log("Código de barras detectado:", decodedText);

            // Para após detectar
            html5QrCode.stop().then(() => {
              scannerContainer.style.display = "none";
              html5QrCode = null; // 🔑 libera o objeto p/ reiniciar depois
            });

            // Buscar alimento no backend
            fetch(`/alimentos/buscar_codigo/${decodedText}`)
              .then(res => res.json())
              .then(data => {
                if (data.nome) {
                  document.getElementById("nome").value = data.nome;
                  document.getElementById("calorias").value = data.calorias;
                  document.getElementById("proteinas").value = data.proteinas;
                  document.getElementById("carboidratos").value = data.carboidratos;
                  document.getElementById("gorduras").value = data.gorduras;
                } else {
                  alert("Alimento não encontrado.");
                }
              })
              .catch(err => {
                console.error("Erro ao buscar alimento:", err);
                alert("Erro ao buscar alimento.");
              });
          },
          errorMessage => {
            console.warn("Erro na leitura:", errorMessage);
          }
        ).catch(err => {
          console.error("Erro ao iniciar câmera:", err);
          alert("Erro ao acessar câmera. Verifique permissões ou use HTTPS/localhost");
        });
      } else {
        alert("Nenhuma câmera encontrada.");
      }
    }).catch(err => {
      console.error("Erro ao listar câmeras:", err);
      alert("Erro ao listar câmeras.");
    });
  });
});
