
from flask import flash, redirect, request,session
from muroprivadito import app
from muroprivadito.models.model_mensaje import Mensaje

@app.route('/send_message',methods=["POST"])
def send_message():
    if "id" in session:
        data = {
            "contenido" : request.form["contenido"],
            "emisor_id" : session["id"],
            "receptor_id" : request.form["receptor_id"]
        }
        if(Mensaje.validateData(data)):
            resultado = Mensaje.sendMessage(data)
            if not resultado > 0:
                flash("Ocurrio un error al enviar el mensaje","mensaje")
        
        return redirect('/dashboard')
    else:
        return redirect('/')
