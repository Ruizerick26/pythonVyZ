import speech_recognition as sr
import webbrowser as wb

reconocimiento = sr.Recognizer()

with sr.Microphone() as source:
    print("Hola que video deseas buscar")
    audio = reconocimiento.listen(source)

print("Acabas de decir: ")
frase = reconocimiento.recognize_google(audio, language="es-EC")
print(frase)

url="https://www.youtube.com/results?search_query="
buscar = url + frase
wb.open(buscar)