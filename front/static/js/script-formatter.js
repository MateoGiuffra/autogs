document.addEventListener("DOMContentLoaded", function() {
    const total = parseFloat(document.getElementById('totalValue').getAttribute('data-total'));
    
    const dif = total - lastTotal;

    document.getElementById('dif').textContent = dif;
});