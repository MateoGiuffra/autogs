from flask import Flask, jsonify, request
from application.service.SummaryService import SummaryService
from decouple import config  
from dotenv import load_dotenv 
import os 

load_dotenv()  # para cargar el .env en local

app = Flask(__name__)

@app.route("/resumen", methods=["POST"])
def recibir_mensaje():
    # Obtener el mensaje del cuerpo de la solicitud
    incoming_message = request.form.get("Body").strip().lower()  # Mensaje de WhatsApp
    print("Mensaje recibido:", incoming_message)  # Ver lo que llega
    
    if incoming_message == "resumen":
        print("Entrando en el bloque de resumen")  # Ver si entra aquí
        try:
            url = "https://game.systemmaster.com.ar/frmLogin.aspx"
            user = config("DB_USER")
            password = config("DB_PASSWORD")
            
            # Llamada al servicio para obtener el resumen
            total = SummaryService.get_summary(url, user, password)
            response_message = f"El total es: {total}"
        except Exception as e:
            response_message = f"Error: {str(e)}"
            print("Error al obtener el resumen:", e)  # Ver el error si ocurre
    else:
        print("Mensaje no reconocido:", incoming_message)  # Ver el mensaje no reconocido
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
