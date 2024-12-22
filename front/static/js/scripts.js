// scripts.js
async function obtenerResumen() {
    try {
        const response = await fetch("/obtenerResumen", {
            method: "GET",
        });
        const text = await response.text();
        document.getElementById("response").innerHTML = text;
    } catch (error) {
        document.getElementById("response").innerHTML = "Error: " + error;
    }
}
