function formatNumber(input) {
    const numberString = input.toString();
    const [integerPart, decimalPart] = numberString.split(".");
    const formattedInteger = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return `${formattedInteger},${decimalPart || "00"}`;
}

document.addEventListener("DOMContentLoaded", function () {
    // Obtener los valores desde el DOM
    const total = parseFloat(document.getElementById("totalValue").getAttribute("data-total"));
    const lastTotal = parseFloat(document.getElementById("lastTotalValue").getAttribute("data-last-total"));

    // Actualizar elementos con el formato deseado
    document.getElementById("total").textContent = formatNumber(total);
    document.getElementById("last_months_total").textContent = formatNumber(parseFloat('{{data1["last_months_total"]}}'));
    document.getElementById("last_months_total_today").textContent = formatNumber(parseFloat('{{data1["last_months_total_today"]}}'));

    // Calcular la diferencia y formatearla
    const dif = total - lastTotal;
    document.getElementById("dif").textContent = formatNumber(dif);
});
46109827.06