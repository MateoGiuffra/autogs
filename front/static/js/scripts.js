// scripts.js
document.addEventListener("DOMContentLoaded", () => {
    const btnObtenerResumen = document.getElementById("btn-obtener-resumen");
    const btnDiferenciaResumenes = document.getElementById("btn-diferencia-resumenes");
    const responseMessage = document.getElementById("response-message");

    btnObtenerResumen.addEventListener("click", () => {
        fetch("/obtenerResumen")
            .then(response => {
                if (!response.ok) {
                    throw new Error("Error al obtener resumen");
                }
                return response.json();
            })
            .then(data => {
                responseMessage.textContent = data;
                btnDiferenciaResumenes.disabled = false;
            })
            .catch(error => {
                responseMessage.textContent = `Error: ${error.message}`;
            });
    });

    btnDiferenciaResumenes.addEventListener("click", () => {
        fetch("/diferenciaResumenes")
            .then(response => {
                if (!response.ok) {
                    throw new Error("Error al calcular diferencia entre resúmenes");
                }
                return response.json();
            })
            .then(data => {
                responseMessage.textContent = data;
            })
            .catch(error => {
                responseMessage.textContent = `Ocurrio algo inesperado: ${error.message}`;
            });
    });
});
