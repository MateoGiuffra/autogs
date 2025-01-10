document.addEventListener('DOMContentLoaded', () => {
    const actualizarButton = document.getElementById('actualizar');
    if (actualizarButton) {
        actualizarButton.addEventListener('click', async () => {
            const endpoint = '/resumenActual';
            const spinner = document.getElementById('spinner');
            
            if (!spinner) {
                console.error("No se encontró el elemento spinner");
                return;
            }

            try {
                spinner.style.display = 'inline-block';

                const response = await fetch(endpoint, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' }
                });

                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('total').textContent = data.total;
                    document.getElementById('last-report-date').textContent = data.last_report_date;
                    document.getElementById('dif').textContent = data.dif;

                    alert('Resumen actualizado con éxito.');
                } else {
                    console.error('Error:', response.status, response.statusText);
                    alert('Error al actualizar el resumen.');
                }
            } catch (error) {
                console.error('Error en la solicitud:', error);
                alert('Ocurrió un error al intentar actualizar.');
            } finally {
                spinner.style.display = 'none';
            }
        });
    } else {
        console.error("El botón con id 'actualizar' no existe.");
    }
});
