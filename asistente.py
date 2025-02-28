import speech_recognition as sr
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import spacy
nlp = spacy.load('en_core_web_sm')
import time
time.clock = time.time
import entrenamiento
import pyttsx3

# inicializamos el bot
chatbot = ChatBot(
    'Amebot',
    logic_adapter=['chatterbot.logic.BestMatch'] 
)

trainer = ListTrainer(chatbot)

trainer.train(entrenamiento.conversaciones_saludos)
trainer.train(entrenamiento.conversaciones_despedidas)
trainer.train(entrenamiento.conversaciones_clima)
trainer.train(entrenamiento.conversaciones_info_personal)
trainer.train(entrenamiento.conversaciones_reservas)
trainer.train(entrenamiento.conversaciones_horarios)

reconocedor = sr.Recognizer()

motor = pyttsx3.init()
voces = motor.getProperty('voices') # Obtiene la lista de voces disponibles en tu sistema
motor.setProperty('voice',voces[1].id) # Voz femenina


while True:
    with sr.Microphone() as mic:
        print("Haga su consulta...")
        reconocedor.adjust_for_ambient_noise(mic,duration=0.4)
        audio = reconocedor.listen(mic)
        texto = reconocedor.recognize_google(audio)
        texto = texto.lower()
        print("ChacIA: ", texto)
    if texto.lower() in ["salir", "adios", "hasta luego", "chau", "nos vemos"]:
        print("Amebot: Adiós, hasta la próxima aventura verde 🌿")
        motor.say("Adiós, hasta la próxima aventura verde")
        motor.runAndWait()
        break
    respuesta = chatbot.get_response(texto)
    print(f"AmeBot: {respuesta}")
    motor.say(respuesta)
    motor.runAndWait()


