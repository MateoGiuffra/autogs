document.addEventListener("DOMContentLoaded", function () {
    const totalElement = document.getElementById("totalValue");

    // Función para formatear números
    function formatNumber(input) {
        const numberString = input.toString();
        const [integerPart, decimalPart] = numberString.split(".");
        const formattedInteger = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        return `${formattedInteger},${decimalPart || "00"}`;
    }
    
    // Obtener mensaje de porcentaje 
    const percentMessage = (lastTotal) => {
        const total = parseFloat(totalElement.getAttribute("data-total")); 
        const dif = total - lastTotal
        const percent = ((dif/total) * 100).toFixed(2)
        const moreOrLess =  dif > 0 ? "incremento " :  "disminución" 
        return `${moreOrLess} del ${Math.abs(percent)}%`;
    } 
    // Obtiene el input de los elementos dados y le aplica la funcion pasa por parametro
    const assignToFunction = (someElements, f) => {
        Array.from(someElements).forEach(element => {
            const value = parseFloat(element.textContent); // Convertir texto a número
            if (!isNaN(value)) {
                element.textContent = f(value); // Aplicar la funcion sobre el valor
            }
        });
    }

    const sub = (number) => {
        total = parseFloat(totalElement.getAttribute("data-total")); 
        dif = (total - number).toFixed(2)
        return formatNumber(Math.abs(dif))
    }

    // Formatear números en elementos con la clase "formatted-number"
    const elements = document.getElementsByClassName("formatted-number");
    assignToFunction(elements, formatNumber)
    // Obtener el mensaje del porcentaje de los elements con la clase "percent-message"
    const elementsPercentMessage = document.getElementsByClassName('percent-message');
    assignToFunction(elementsPercentMessage, percentMessage)
    const elementsToRestar = document.getElementsByClassName('difference');
    assignToFunction(elementsToRestar, sub)

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

                    totalElement.textContent = data.total;
                    document.getElementById('last-report-date').textContent = data.last_report_date;
                    document.getElementById("dif").textContent = sub(data.last_total);
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



});

