import speech_recognition as sr

reconocimiento = sr.Recognizer()

archivo = sr.AudioFile('Grabación.wav')

with archivo as source:
    audio = reconocimiento.record(source)

print("Acabas de decir: ")
frase = reconocimiento.recognize_google(audio, language="es-EC")
print(frase)