#Carlos Andres Riveramelo Del Toro
#Chatbot

#ChatBot inteligente con WhatsApp en Python
from flask import Flask, jsonify, request
app = Flask(__name__)
#Recibe peticiones en esta ruta
@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    #Datos recibidos via GET
    if request.method == "GET":
        #Verifica el token
        if request.args.get('hub.verify_token') == "papasito":
            #Valor recibido por face
            return request.args.get('hub.challenge')
        else:
            #mandamos el mensaje de error
          return "Error en la pagina."
    #Recibimos los datos via JSON
    data=request.get_json()
    #Tomamos el numero y mensaje del cliente
    telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    #Tomamos el telefono del cliente
    mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    #Tomamos el ID del telefono del cliente
    idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
    #Verificamos y tomamos la hora en la que se envio el mensaje
    timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
    #Escribimos el numero de mensaje y texto si hay un mensaje
    if mensaje is not None:
      from rivescript import RiveScript
      #Inicializamos RiveScript y cargamos la conversacion
      bot = RiveScript()
      bot.load_file('barberia.rive')
      bot.sort_replies()
      #Obtenemos la respuesta
      respuesta = bot.reply("localuser",mensaje)
      respuesta = respuesta.replace("\\n","\\\n")
      respuesta = respuesta.replace("\\","")
      #Nos conectamos a la base de datos
      import mysql.connector
      mydb = mysql.connector.connect(
          host = "mysql-sharlo.alwaysdata.net",
          user = "sharlo",
          password = "Charlie131092",
          database='sharlo_chat'
          )
      mycursor = mydb.cursor()
      query="SELECT count(id) AS cantidad FROM registro WHERE id_wa='" + idWA + "';"
      mycursor.execute("SELECT count(id) AS cantidad FROM registro WHERE id_wa='" + idWA + "';")
      
      cantidad, = mycursor.fetchone()
      cantidad=str(cantidad)
      cantidad=int(cantidad)
      if cantidad==0 :
          sql = ("INSERT INTO registro"+ 
                 "(mensaje_recibido,mensaje_enviado,id_wa      ,timestamp_wa   ,telefono_wa) VALUES "+
                 "('"+mensaje+"'   ,'"+respuesta+"','"+idWA+"' ,'"+timestamp+"','"+telefonoCliente+"');")
          mycursor.execute(sql)
          mydb.commit()
          
    enviar(telefonoCliente,respuesta)
      #Retornamos el estatus en un JSON
    return jsonify({"status": "success"}, 200)
      
def enviar(telefonoRecibe,respuesta):
          from heyoo import WhatsApp
          #TOKEN DE ACCESO DE FACEBOOK
          token='EAAK4nif8GqQBADacSq0rltrAcERwnZCUcVwZC3weDnEqQoouaDfYDxwk91YAllZA3FI3dypipuNykEmbiPZAJ69biCr0sEoeDb8bcWCeGDfdMUeTxoOchgaiCAorXlmWKTIJ7M8LJLNJuIaZCFRQmyJh3hGBTd1gTfSLR84JGtdTMaK5d4UlKgE4h2E7sY9L56EBGOqnRVA4cgVpmNdqm'
          #IDENTIFICADOR DE NÚMERO DE TELÉFONO
          idNumeroTeléfono='117058714754082'
          #INICIALIZAMOS ENVIO DE MENSAJES
          mensajeWa=WhatsApp(token,idNumeroTeléfono)
          telefonoRecibe=telefonoRecibe.replace("521","52")
          #ENVIAMOS UN MENSAJE DE TEXTO
          mensajeWa.send_message(respuesta,telefonoRecibe)
  
#Iniciamos FLASK
if __name__ == "__main__":
  app.run(debug=True)