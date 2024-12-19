from flask import Flask, jsonify
from application.service.SummaryService import SummaryService
from decouple import config  
from dotenv import load_dotenv 
import os 

load_dotenv() # para cargar el .env en local

app = Flask(__name__)

from flask import Flask, request
from application.service.SummaryService import SummaryService

app = Flask(__name__)

@app.route("/resumen", methods=["POST"])
def recibir_mensaje():
    incoming_message = request.form.get("Body").strip().lower()  # Mensaje de WhatsApp
    
    if incoming_message == "resumen":
        try:
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


@app.route("/obtenerResumen", methods=["GET"])
def obtener_resumen():
    url = "https://game.systemmaster.com.ar/frmLogin.aspx"
    user = config("DB_USER")
    password = config("DB_PASSWORD")
    
    try:
        # Obtener el resumen usando el servicio
        total = SummaryService.get_summary(url, user, password)
        response_message = {"message": f"El total es: {total}"}
        return jsonify(response_message), 200

    except Exception as e:
        # Manejo de errores
        error_message = {"error": str(e)}
        return jsonify(error_message), 500
           


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render asigna el puerto como variable de entorno
    app.run(host="0.0.0.0", port=port, debug=True)