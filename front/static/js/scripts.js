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
        const percent = ((dif/lastTotal) * 100).toFixed(2)
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

    // Función para el botón de actualizar el resumen de hoy
    const actualizarButton = document.getElementById("actualizar-hoy");
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

                    document.getElementById('total').textContent = data.total;
                    document.getElementById('last-report-date').textContent = data.last_report_date;
                    document.getElementById("dif").textContent = sub(data.last_total);
                    spinner.style.display = "none";
                    alert("Resumen de HOY actualizado con éxito.");
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
        console.error("El botón con id 'actualizar-hoy' no existe.");
    }

    const actualizarTotalDelMesAnterior = document.getElementById("actualizar-total");
    if (actualizarTotalDelMesAnterior) {
        const spinner = document.getElementById("spinner");

        actualizarTotalDelMesAnterior.addEventListener("click", async () => {
            if (!spinner) {
                console.error("No se encontró el elemento spinner");
                return;
            } 

            try {
                spinner.style.display = "inline-block";

                const response = await fetch("/resumenDelMesPasado", {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                });

                if (response.ok) {
                    const data = await response.json();

                    document.getElementById("last_months_total").textContent = data.last_months_total;
                    spinner.style.display = "none";
                    alert("Resumen TOTAL actualizado con éxito.");
                } else {
                    console.error("Error:", response.status, response.statusText);
                    alert("Error al actualizar el resumen total del mes anterior.");
                }
            } catch (error) {
                console.error("Error en la solicitud:", error);
                alert("Ocurrió un error al intentar actualizar.");
            } finally {
                spinner.style.display = "none";
            }
        });
    } else {
        console.error("El botón con id 'actualizar-total' no existe.");
    }

    const actualizarParcialDeUnMesAtras = document.getElementById("actualizar-parcial");
    if (actualizarParcialDeUnMesAtras) {
        const spinner = document.getElementById("spinner");

        actualizarParcialDeUnMesAtras.addEventListener("click", async () => {
            if (!spinner) {
                console.error("No se encontró el elemento spinner");
                return;
            } 

            try {
                spinner.style.display = "inline-block";

                const response = await fetch("/resumenDeUnMesAtras", {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                });

                if (response.ok) {
                    const data = await response.json();

                    document.getElementById("last_months_total_today").textContent = data.last_months_total_today;
                    spinner.style.display = "none";
                    alert("Resumen PARCIAL actualizado con éxito.");
                } else {
                    console.error("Error:", response.status, response.statusText);
                    alert("Error al actualizar el resumen total del mes anterior.");
                }
            } catch (error) {
                console.error("Error en la solicitud:", error);
                alert("Ocurrió un error al intentar actualizar.");
            } finally {
                spinner.style.display = "none";
            }
        });
    } else {
        console.error("El botón con id 'actualizar-parcial' no existe.");
    }



});

