import os
import espeakng
import re
import webbrowser
import requests
from github import Github
from gitlab import Gitlab
from datetime import datetime
import openai
import json
import shutil
import MySQLdb
# Set up the API keys and tokens
openai.api_key = os.environ["OPENAI_API_KEY"]
github_token = os.environ["GITHUB_TOKEN"]
gitlab_token = os.environ["GITLAB_TOKEN"]

# Set up espeak
voice = espeakng.Voice(language="es-mx", gender="female")  # Spanish (Mexico) female voice
speech = espeakng.Speaker(voice=voice, speed=120)  # Adjust speed to 120 words per minute

# Define the prompt to start the conversation
prompt = "Hola TheGhost, soy tu asistente virtual. ¿En qué puedo ayudarte hoy?"

# Set up the security measures
safe_folders = ["Documents", "Pictures", "Videos"]
dangerous_extensions = [".exe", ".bat", ".sh", ".com"]
safe_extensions = [".txt", ".pdf", ".py", ".java", ".cpp", ".js", ".html", ".css"]
logs_file = "security_logs.txt"

# Start the conversation
def start_conversation():
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the answer from the response
    answer = response.choices[0].text.strip()
    return answer

# If the answer is empty, perform a Google search to find an answer
def google_search(query):
    query = re.sub(r'[^\w\s]', '', query.lower())
    webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
    return "Lo siento, no tengo una respuesta para eso. He iniciado una búsqueda en Google para ayudarte."

def execute_code(code):
    try:
        exec(code)
        answer = "Código ejecutado correctamente."
    except Exception as e:
        answer = f"Hubo un error al ejecutar el código: {str(e)}"
    return answer

def generate_flutter_code():
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt="Genera un ejemplo de código de Flutter para una pantalla de inicio de sesión con correo electrónico y contraseña",
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    answer = response.choices[0].text.strip()
    return answer

def generate_code(language, code_prompt):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=code_prompt,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    answer = response.choices[0].text.strip()
    return answer

def get_repo_info(user_input):
    split_input = user_input.split()
    for i in range(len(split_input)):
        if split_input[i] == "en":
            language = split_input[i+1]
            break
    try:
        repo_name = split_input[-1]
        if "github" in split_input:
            g = Github(github_token)
            repo = g.get_repo(f"{language}/{
try:
repo_name = split_input[-1]
if "github" in split_input:
g = Github(github_token)
repo = g.get_repo(f"{language}/{repo_name}")
readme = repo.get_readme().decoded_content.decode("utf-8")
answer = f"El README del repositorio {repo_name} es: {readme}"
elif "gitlab" in split_input:
gl = Gitlab("https://gitlab.com", private_token=gitlab_token)
project = gl.projects.get(f"{language}/{repo_name}")
readme = project.files.get(file_path="README.md").decode().decode("utf-8")
answer = f"El README del repositorio {repo_name} es: {readme}"
else:
answer = "Lo siento, no puedo buscar información sobre ese repositorio."
except Exception as e:
answer = f"No se pudo encontrar el repositorio {repo_name}: {str(e)}"
return answer
def get_github_repo_info(language, github_token, input_text):
    split_input = input_text.split()
    if len(split_input) < 2:
        return "Please provide both a GitHub username and repository name"

    repo_name = split_input[-1]
    if "github" in split_input:
        g = Github(github_token)
        repo = g.get_repo(f"{language}/{repo_name}")
        return f"Repo name: {repo.name}\nDescription: {repo.description}\nStars: {repo.stargazers_count}\nLanguage: {repo.language}\nURL: {repo.html_url}"
    else:
        url = f"https://api.github.com/repos/{language}/{repo_name}"
        response = requests.get(url).json()
        return f"Repo name: {response['name']}\nDescription: {response['description']}\nStars: {response['stargazers_count']}\nLanguage: {response['language']}\nURL: {response['html_url']}"


def main():
    language = "python"
    github_token = os.environ.get("GITHUB_TOKEN")

    while True:
        input_text = input("What do you want to know about a GitHub repository? ")
        if input_text.lower() in ["quit", "exit", "stop"]:
            break

        print(get_github_repo_info(language, github_token, input_text))


if __name__ == "__main__":
    main()

def enviar_entrada_a_openai(usuario_input):
    response = openai.Completion.create(
        engine="davinci", prompt=usuario_input, max_tokens=100, n=1,stop=None,temperature=0.5,
    )
    return response.choices[0].text

# Función para buscar información en la base de datos
def buscar_en_db(usuario_input):
    # Conectarse a la base de datos
    db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="nombre_de_la_base_de_datos")
    cursor = db.cursor()

    # Ejecutar la consulta SQL
    cursor.execute("SELECT columna_a, columna_b FROM tabla WHERE columna_a LIKE %s", ['%' + usuario_input + '%'])
    results = cursor.fetchall()

    # Construir la respuesta del bot
    response = ""
    for row in results:
        response += row[0] + ": " + row[1] + "\n"
    response += "¿Hay algo más en lo que pueda ayudar?"

    # Cerrar la conexión a la base de datos y devolver la respuesta del bot
    cursor.close()
    db.close()
    return response

# Función para personalizar la respuesta del bot utilizando técnicas de aprendizaje automático
def personalizar_respuesta(usuario_input, historial):
    # Procesar y analizar el historial de conversaciones con el usuario
    modelo = sklearn.linear_model.LogisticRegression()
    X = procesar_historial(historial)
    y = procesar_respuestas(historial)
    modelo.fit(X, y)

    # Utilizar el modelo de aprendizaje automático para personalizar la respuesta
    X_nuevo = procesar_input(usuario_input)
    respuesta_personalizada = modelo.predict(X_nuevo)

    # Devolver la respuesta personalizada
    return respuesta_personalizada

# Función para recibir la entrada de voz del usuario
def recibir_entrada_voz():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Háblame...")
        audio = r.listen(source)
    try:
        entrada_voz = r.recognize_google(audio, language="es-MX")
        print("Usuario:", entrada_voz)
        return entrada_voz
    except:
        print("Lo siento, no pude entenderte...")
        return ""

# Función para enviar la respuesta del bot en forma de voz
def hablar(respuesta):
    motor_voz.say(respuesta)
    motor_voz.runAndWait()

# Función para manejar la conversación con el usuario
def manejar_conversacion():
    historial = []
    print("Hola, ¿en qué puedo ayudarte hoy?")
    while True:
        # Leer la entrada del usuario
        usuario_input = input("Usuario: ")
        historial.append(usuario_input)

        # Personalizar la respuesta del bot
        respuesta_personalizada = personalizar_respuesta(usuario_input, historial)

        # Enviar la entrada del usuario a OpenAI si no se encuentra una respuesta personalizada
        if not respuesta_personalizada:
            respuesta = enviar_entrada_a_openai(usuario_input)
        else:
            respuesta = respuesta_personalizada

