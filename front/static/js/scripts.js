document.addEventListener("DOMContentLoaded", () => {
    const btnObtenerResumen = document.getElementById("btn-obtener-resumen");
    const btnDiferenciaResumenes = document.getElementById("btn-diferencia-resumenes");
    const responseMessage = document.getElementById("response-message");
    const loadingIndicator = document.getElementById("loading-indicator");
    const summaryContainer = document.getElementById("summary-container");
    const summaryNumber = document.getElementById("summary-number");
    const summaryText = document.getElementById("summary-text");
    const btnCopyNumber = document.getElementById("btn-copy-number");

    // Función para mostrar el indicador de carga
    const showLoadingIndicator = () => {
        loadingIndicator.style.display = "block";
    };

    // Función para ocultar el indicador de carga
    const hideLoadingIndicator = () => {
        loadingIndicator.style.display = "none";
    };

    // Función para copiar el número al portapapeles
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

    // Hacer que el botón de copiar funcione
    btnCopyNumber.addEventListener("click", () => {
        copyToClipboard(summaryNumber.textContent);
    });

    btnObtenerResumen.addEventListener("click", () => {
        showLoadingIndicator();  // Mostrar el spinner al hacer la solicitud

        fetch("/obtenerResumen")
            .then(response => {
                if (!response.ok) {
                    throw new Error("Error al obtener resumen");
                }
                return response.json();
            })
            .then(data => {
                // Mostrar el resumen y habilitar el botón para copiar
                summaryNumber.textContent = `${data.total}`;  // Suponiendo que el número viene en `data.number`
                summaryText.textContent = `${data.message}`;  // Suponiendo que el texto viene en `data.text`

                summaryContainer.style.display = "block";  // Mostrar el contenedor con el resumen
                btnCopyNumber.style.display = "inline-block";  // Mostrar el botón de copiar

                btnDiferenciaResumenes.disabled = false;  // Habilitar el botón de diferencia
                hideLoadingIndicator();  // Ocultar el spinner cuando se reciba la respuesta
            })
            .catch(error => {
                responseMessage.textContent = `Ocurrio algo inesperado: ${error.message}`;
                hideLoadingIndicator();  // Ocultar el spinner en caso de error
            });
    });

    btnDiferenciaResumenes.addEventListener("click", () => {
        showLoadingIndicator(); // Mostrar el spinner al hacer la solicitud
    
        fetch("/diferenciaResumenes")
            .then(response => {
                if (!response.ok) {
                    throw new Error("Error al calcular diferencia entre resúmenes");
                }
                return response.json(); // Parsear la respuesta JSON
            })
            .then(data => {
                if (data.error) {
                    responseMessage.textContent = data.error; // Mostrar el mensaje de error si existe
                } else {
                    responseMessage.textContent = data.message; // Mostrar el mensaje principal
                }
                hideLoadingIndicator(); // Ocultar el spinner cuando se reciba la respuesta
            })
            .catch(error => {
                responseMessage.textContent = `Error: ${error.message}`;
                hideLoadingIndicator(); // Ocultar el spinner en caso de error
            });
    });
});
