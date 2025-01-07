document.addEventListener("DOMContentLoaded", () => {
    const btnActualizar = document.getElementById("actualizar-button");

    btnActualizar.addEventListener("click", () => {
        handleRequest("/actualizar_resumen", data => {        
        });
    });
}); 