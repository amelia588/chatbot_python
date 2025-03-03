from flask import Flask, render_template, request
import pyttsx3
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import entrenamiento
import asyncio

app = Flask(__name__)

chatbot = ChatBot("AmeBot")
trainer = ListTrainer(chatbot)

trainer.train(entrenamiento.conversaciones_saludos)
trainer.train(entrenamiento.conversaciones_despedidas)
trainer.train(entrenamiento.conversaciones_clima)

motor = pyttsx3.init()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_input = request.form["mensaje"]
    respuesta = chatbot.get_response(user_input)
    motor.say(str(respuesta))
    try:
        asyncio.run(motor.runAndWait())  # Ejecuta usando asyncio
    except RuntimeError:
        motor.runAndWait()  # Ejecuta normalmente si hay conflicto
    return str(respuesta)

if __name__ == "__main__":
    app.run(debug=True)


