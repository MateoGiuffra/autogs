document.getElementById('actualizar').addEventListener('click', async () => {
    const endpoint = '/resumenActual';
    const spinner = document.getElementById('spinner');

    try {
        // Mostrar el spinner
        spinner.style.display = 'inline-block';

        const response = await fetch(endpoint, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            // Actualizar dinámicamente el contenido de la página
            document.getElementById('total').textContent = data.total;
            document.getElementById('last-report-date').textContent = data.last_report_date;
            document.getElementById('dif').textContent = data.dif;

            alert('Resumen actualizado con éxito.');
        } else {
            alert('Error al actualizar el resumen.');
            console.error('Error:', response.status, response.statusText);
        }
    } catch (error) {
        console.error('Error en la solicitud:', error);
        alert('Ocurrió un error al intentar actualizar.');
    } finally {
        // Ocultar el spinner
        spinner.style.display = 'none';
    }
});
