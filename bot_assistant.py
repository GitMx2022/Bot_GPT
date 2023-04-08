import openai
import os
import espeakng
impirt re
import webbrowser
import requests
from github import Github
from gitlab import Gitlab

# Set up the API keys and tokens
openai.api_key = os.environ["OPENAI_API_KEY"]
github_token = os.environ["GITHUB_TOKEN"]
gitlab_token = os.environ["GITLAB_TOKEN"]

# Set up espeak
voice = espeakng.Voice(language="es-mx", gender="female")  # Spanish (Mexico) female voice
speech = espeakng.Speaker(voice=voice, speed=120)  # Adjust speed to 120 words per minute

# Define the prompt to start the conversation
prompt = "Hola TheGhost, soy tu asistente virtual. ¿En qué puedo ayudarte hoy?"

# Start the conversation
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

# If the answer is empty, perform a Google search to find an answer
if not answer:
    query = re.sub(r'[^\w\s]', '', prompt.lower())
    webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
    answer = "Lo siento, no tengo una respuesta para eso. He iniciado una búsqueda en Google para ayudarte."
else:
    # Check if the answer contains code and execute it
    if '```' in answer:
        code = re.search('```(.*)```', answer, re.DOTALL).group(1).strip()
        try:
            exec(code)
            answer = "Código ejecutado correctamente."
        except Exception as e:
            answer = f"Hubo un error al ejecutar el código: {str(e)}"
    # Check if the answer contains a Flutter code prompt and generate Flutter code
    elif "genera código de Flutter" in answer.lower():
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
    # Check if the answer contains a code prompt and generate code in the given language
    elif "genera código" in answer.lower():
        language = re.search(r'(en|para)\s+(\w+)', answer, re.IGNORECASE).group(2).strip()
        code_prompt = re.search(r'(```)(\s*\w+)?\n([^`]+)(```)', answer, re.IGNORECASE | re.DOTALL)
        if code_prompt:
            code_prompt = code_prompt.group(3).strip()
        else:
            code_prompt = f"Escribe un programa en {language} para..."
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=code_prompt,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response.choices[0].text.strip
 # Check if the answer contains a text prompt and generate text
elif "genera texto" in answer.lower():
text_prompt = re.search(r'(escribe|genera) un (párrafo|texto) sobre (.+)', answer, re.IGNORECASE)
if text_prompt:
text_prompt = text_prompt.group(3).strip()
else:
text_prompt = "Escribe un párrafo sobre..."
response = openai.Completion.create(
engine="davinci",
prompt=text_prompt,
temperature=0.7,
max_tokens=1024,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)
answer = response.choices[0].text.strip()
Speak the answer

speech.say(answer)
Ask the user if they want to save the answer

response = openai.Completion.create(
engine="davinci-codex",
prompt="¿Quieres guardar esta información?",
temperature=0.5,
max_tokens=1024,
top_p=1,
frequency_penalty=0,
presence_penalty=0,
choice="Yes\nNo"
)
Extract the user's response

save_answer = response.choices[0].text.strip()
If the user wants to save the answer, prompt them for a filename and save the answer to a file

if save_answer == "Yes":
response = openai.Completion.create(
engine="davinci-codex",
prompt="Ingresa un nombre para el archivo:",
temperature=0.5,
max_tokens=1024,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)
filename = response.choices[0].text.strip()

with open(f"{filename}.txt", "w") as file:
    file.write(answer)
    answer = f"La respuesta ha sido guardada en el archivo {filename}.txt."

else:
answer = "Entendido, la respuesta no ha sido guardada."
Speak the answer againaa

speech.say(answer)
