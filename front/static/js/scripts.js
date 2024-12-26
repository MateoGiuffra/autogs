document.addEventListener("DOMContentLoaded", () => {
    const btnObtenerResumen = document.getElementById("btn-obtener-resumen");
    const btnDiferenciaResumenes = document.getElementById("btn-diferencia-resumenes");
    const btnDiferenciaHoy = document.getElementById("btn-diferencia-hoy");
    const responseMessage = document.getElementById("response-message");
    const loadingIndicator = document.getElementById("loading-indicator");
    const summaryContainer = document.getElementById("summary-container");
    const summaryNumber = document.getElementById("summary-number");
    const summaryText = document.getElementById("summary-text");
    const btnCopyNumber = document.getElementById("btn-copy-number");
    
    btnDiferenciaResumenes.disabled = true;
    btnDiferenciaHoy.disabled = true;
    
    const showLoadingIndicator = () => {
        loadingIndicator.style.display = "block";
    };

    const hideLoadingIndicator = () => {
        loadingIndicator.style.display = "none";
    };

    const resetResponseMessage = () => {
        responseMessage.textContent = "Procesando...";
    };

    const copyToClipboard = (text, buttonElement) => {
        navigator.clipboard.writeText(text)
            .then(() => {
                const originalText = buttonElement.textContent;
                buttonElement.textContent = "¡Copiado!";
                setTimeout(() => {
                    buttonElement.textContent = originalText;
                }, 2000); // Cambia el texto por 2 segundos
            })
            .catch(() => {
                console.error("Error al copiar el texto.");
            });
    };

    btnCopyNumber.addEventListener("click", () => {
        copyToClipboard(summaryNumber.textContent, btnCopyNumber);
    });

    const handleRequest = (endpoint, onSuccess) => {
        showLoadingIndicator(); 
        resetResponseMessage(); 

        fetch(endpoint)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error en la solicitud a ${endpoint}`);
                }
                return response.json();
            })
            .then(data => {
                onSuccess(data);        
            })
            .catch(error => {
                responseMessage.textContent = `Ocurrio algo inesperado: ${error.message}`;
            })
            .finally(() => {
                hideLoadingIndicator();
            });
    };

    btnObtenerResumen.addEventListener("click", () => {
        handleRequest("/obtenerResumen", data => {
            summaryNumber.textContent = `${data.total}`;      
            summaryText.textContent = `${data.message}`;      // Actualiza el número y el mensaje

            summaryContainer.style.display = "block";         // Muestra el contenedor con el resumen y el botón de copiar
            btnCopyNumber.style.display = "inline-block";     

            btnDiferenciaResumenes.disabled = false;          // Habilita los botones "Mensual" y "De Hoy"
            btnDiferenciaHoy.disabled = false;                
        });
    });

    btnDiferenciaResumenes.addEventListener("click", () => {
        handleRequest("/diferenciaResumenes", data => {
            responseMessage.textContent = data.error ? data.error : data.message;
        });
    });

    btnDiferenciaHoy.addEventListener("click", () => {
        handleRequest("/diferenciaResumenesHoy", data => {
            responseMessage.textContent = data.error ? data.error : data.message;
        });
    });
});
