document.addEventListener("DOMContentLoaded", function () {
    const totalElement = document.getElementById("totalValue");
    if (!totalElement) {
        console.error("No se encontró el elemento con ID 'totalValue'");
        return;
    }

    const add3Hours = () =>{
        let lastReportDate = document.getElementById('last-report-date').getAttribute('datetime');
        
        // Convertir a objeto Date en JavaScript
        let date = new Date(lastReportDate);
        
        // Sumar 3 horas
        date.setHours(date.getHours() + 3);
        
        // Actualizar el atributo datetime con la nueva fecha
        document.getElementById('last-report-date').setAttribute('datetime', date.toISOString());
    };
    // add3Hours();


    function formatNumber(number) {
        if (typeof number !== "number") {
            number = parseFloat(number);
        }
        if (isNaN(number)) return "";
        
        const parts = number.toFixed(2).split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        return parts.join(",");
    }

    function applyFormatting(className) {
        const formattedElements = document.getElementsByClassName(className);
        Array.from(formattedElements).forEach(function (element) {
            const value = parseFloat(element.textContent.replace(/[^\d.-]/g, ""));
            if (!isNaN(value)) {
                element.textContent = formatNumber(value);
            }
        });
    }

    function percentMessage(lastTotal) {
        const total = parseFloat(totalElement.getAttribute("data-total"));
        if (isNaN(total) || isNaN(lastTotal) || lastTotal === 0) {
            return "No hay cambio porcentual disponible";
        }
        const dif = total - lastTotal;
        const percent = ((dif / lastTotal) * 100).toFixed(2);
        const moreOrLess = dif > 0 ? "un incremento" : "una disminución";
        return `${moreOrLess} del ${Math.abs(percent)}%`;
    }

    function applyFunctionTo(someElements, f) {
        Array.from(someElements).forEach(function (element) {
            const value = parseFloat(element.textContent.replace(/[^\d.-]/g, ""));
            if (!isNaN(value)) {
                element.textContent = f(value);
            }
        });
    }

    function sub(number) {
        const total = parseFloat(totalElement.getAttribute("data-total"));
        if (isNaN(total) || isNaN(number)) {
            console.error("Valores no válidos para la resta");
            return "0";
        }
        const dif = (total - number).toFixed(2);
        return Math.abs(dif).toString();
    }

    applyFormatting("formatted-number");

    const elementsPercentMessage = document.getElementsByClassName("percent-message");
    applyFunctionTo(elementsPercentMessage, percentMessage);

    const elementsToSub = document.getElementsByClassName("difference");
    applyFunctionTo(elementsToSub, sub);
    applyFunctionTo(elementsToSub, formatNumber);

    const spinner = document.getElementById("spinner");

    const handleButton = (button, operation, path) => {
        if (!button) return;
        
        button.addEventListener("click", async function(event) {
            event.preventDefault();
            if (!spinner) {
                console.error("No se encontró el elemento spinner");
                return;
            }
            
            try {
                spinner.style.display = "inline-block";
                const response = await fetch(path, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                });
                
                if (response.ok) {
                    const data = await response.json();
                    operation(data);
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
    };

    const updateTodayButton = (data) => {
        document.getElementById("total").textContent = formatNumber(data.total);
        document.getElementById("last-report-date").textContent = data.last_report_date;
        document.getElementById("dif").textContent = sub(data.last_total);
    };

    const updateLastMonthTotalButton = (data) => {
        document.getElementById("last_months_total").textContent = formatNumber(data.last_months_total);
        document.getElementById("last_months_total_span").textContent = formatNumber(data.last_months_total);
        document.getElementById("last_months_total_dif").textContent = formatNumber(sub(data.last_months_total));
    };

    const updateLastMonthTodayButton = (data) => {
        document.getElementById("last_months_total_today").textContent = formatNumber(data.last_months_total_today);
        document.getElementById("last_months_total_today_span").textContent = formatNumber(data.last_months_total_today);
        document.getElementById("last_months_total_today_dif").textContent = formatNumber(sub(data.last_months_total_today));
    };

    handleButton(document.getElementById("actualizar-hoy"), updateTodayButton, "/resumenActual"); 
    handleButton(document.getElementById("actualizar-total"), updateLastMonthTotalButton, "/resumenDelMesPasado"); 
    handleButton(document.getElementById("actualizar-parcial"), updateLastMonthTodayButton, "/resumenDeUnMesAtras"); 
});
