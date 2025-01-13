document.addEventListener("DOMContentLoaded", function () {
    // Función para restar números
    const totalElement = document.getElementById("totalValue");
    const lastTotalElement = document.getElementById("lastTotalValue");

    if (totalElement && lastTotalElement) {
        const total = parseFloat(totalElement.getAttribute("data-total"));
        const lastTotal = parseFloat(lastTotalElement.getAttribute("data-last-total"));
        const dif = total - lastTotal;

        document.getElementById("dif").textContent = dif;
    }


    // Función para el botón de actualizar resumen
    const actualizarButton = document.getElementById("actualizar");
    if (actualizarButton) {
        const spinner = document.getElementById("spinner");

        actualizarButton.addEventListener("click", async () => {
            if (!spinner) {
                console.error("No se encontró el elemento spinner");
                return;
            }

            try {
                spinner.style.display = "inline-block";

                const response = await fetch("/resumenActual", {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                });

                if (response.ok) {
                    const data = await response.json();
                    const resta = data.total - data.last_total;

                    totalElement.textContent = data.total;
                    document.getElementById('last-report-date').textContent = data.last_report_date;
                    document.getElementById("dif").textContent = resta;
                    spinner.style.display = "none";
                    alert("Resumen actualizado con éxito.");
                } else {
                    console.error("Error:", response.status, response.statusText);
                    alert("Error al actualizar el resumen.");
                }
            } catch (error) {
                console.error("Error en la solicitud:", error);
                alert("Ocurrió un error al intentar actualizar.");
            } finally {
                spinner.style.display = "none";
            }
        });
    } else {
        console.error("El botón con id 'actualizar' no existe.");
    }

    // Función para formatear números
    function formatNumber(input) {
        const numberString = input.toString();
        const [integerPart, decimalPart] = numberString.split(".");
        const formattedInteger = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        return `${formattedInteger},${decimalPart || "00"}`;
    }

    // Formatear números en elementos con la clase "formatted-number"
    const elements = document.getElementsByClassName("formatted-number");

    Array.from(elements).forEach(element => {
        const value = parseFloat(element.textContent); // Convertir texto a número
        if (!isNaN(value)) {
            element.textContent = formatNumber(value); // Formatear y actualizar
        }
    });
});

