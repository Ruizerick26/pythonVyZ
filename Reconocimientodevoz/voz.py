import speech_recognition as sr
import webbrowser as wb

reconocimiento = sr.Recognizer()

with sr.Microphone() as source:
    print("Hola en que puedo ayudarte")
    audio = reconocimiento.listen(source)

print("Acabas de decir: ")
frase = reconocimiento.recognize_google(audio, language="es-EC")
print(frase)

url="https://www.google.com/search?q="
buscar = url + frase
wb.open(buscar)