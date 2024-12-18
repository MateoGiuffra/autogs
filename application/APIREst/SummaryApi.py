from flask import Flask, jsonify
from application.service.SummaryService import SummaryService
from decouple import config  

app = Flask(__name__)

from flask import Flask, request
from application.service.SummaryService import SummaryService

app = Flask(__name__)

@app.route("/resumen", methods=["POST"])
def recibir_mensaje():
    incoming_message = request.form.get("Body").strip().lower()  # Mensaje de WhatsApp
    sender = request.form.get("From")  # Número del remitente

    if incoming_message == "resumen":
        try:
            # Llama a tu lógica
            url = "https://game.systemmaster.com.ar/frmLogin.aspx"
            user = config("DB_USER")
            password = config("DB_PASSWORD")
            
            total = SummaryService.get_summary(url, user, password)
            response_message = f"El total es: {total}"
        except Exception as e:
            response_message = f"Error: {str(e)}"
    else:
        response_message = "Mensaje no reconocido. Envía 'resumen' para obtener el total."

    # Respuesta al remitente
    response = f"""<Response>
                      <Message>{response_message}</Message>
                   </Response>"""
    return response, 200, {'Content-Type': 'application/xml'}

if __name__ == "__main__":
    app.run(port=5000, debug=True)
