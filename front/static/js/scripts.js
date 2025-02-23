document.addEventListener("DOMContentLoaded", function () {
    const totalElement = document.getElementById("totalValue");

    // Función para formatear números como "123.456,78"
    function formatNumber(number) {
        if (typeof number !== "number") {
            number = parseFloat(number);
        }
        if (isNaN(number)) return "";

        const parts = number.toFixed(2).split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        return parts.join(",");
    }

    // Aplicar formato a todos los elementos con la clase "formatted-number"
    function applyFormatting() {
        const formattedElements = document.getElementsByClassName("formatted-number");
        Array.from(formattedElements).forEach(function (element) {
            const value = parseFloat(element.textContent.replace(/[^\d.-]/g, ""));
            if (!isNaN(value)) {
                element.textContent = formatNumber(value);
            }
        });
    }

    // Función para calcular el mensaje de porcentaje
    function percentMessage(lastTotal) {
        const total = parseFloat(totalElement.getAttribute("data-total"));
        const dif = total - lastTotal;
        const percent = ((dif / lastTotal) * 100).toFixed(2);
        const moreOrLess = dif > 0 ? "un incremento" : "una disminución";
        return `${moreOrLess} del ${Math.abs(percent)}%`;
    }

    // Función para aplicar una función a varios elementos
    function applyFunctionTo(someElements, f) {
        Array.from(someElements).forEach(function (element) {
            const value = parseFloat(element.textContent);
            if (!isNaN(value)) {
                element.textContent = f(value);
            }
        });
    }

    // Función para calcular la diferencia
    function sub(number) {
        const total = (totalElement.getAttribute("data-total"));
        const floatNumber = typeof number === "string" ? parseFloat(number) : number;  
        const dif = (total - floatNumber).toFixed(2);
        return Math.abs(dif).toString();
    }

    // Aplicar formato inicial a los números
    applyFormatting();

    // Aplicar mensajes de porcentaje y diferencias
    const elementsPercentMessage = document.getElementsByClassName("percent-message");
    applyFunctionTo(elementsPercentMessage, percentMessage);

    const elementsToSub = document.getElementsByClassName("difference");
    applyFunctionTo(elementsToSub, sub);

    // Manejar el botón de actualización
    const actualizarButton = document.getElementById("actualizar-hoy");
    if (actualizarButton) {
        const spinner = document.getElementById("spinner");
        actualizarButton.addEventListener("click", async function () {
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

                    document.getElementById("total").textContent = formatNumber(data.total);
                    document.getElementById("last-report-date").textContent = data.last_report_date;
                    document.getElementById("dif").textContent = sub(data.last_total);

                    spinner.style.display = "none";
                    alert("Resumen de HOY actualizado con éxito.");
                } else {
                    console.error("Error:", response.status, response.statusText);
                    alert("Error al actualizar el resumen. Actualiza la página para refrescar los cambios");
                }
            } catch (error) {
                console.error("Error en la solicitud:", error);
                alert("Ocurrió un error al intentar actualizar.");
            } finally {
                spinner.style.display = "none";
            }
        });
    }
});