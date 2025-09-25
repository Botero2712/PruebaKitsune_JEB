import re
import requests
from transformers import pipeline

API_BASE = "http://127.0.0.1:8000"  # tu API local

# Clasificador zero-shot de intenciones
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Intenciones posibles
CANDIDATE_LABELS = ["listar", "buscar", "detalle"]


def call_api(endpoint: str):
    """Hace la llamada a la API y devuelve JSON."""
    url = f"{API_BASE}{endpoint}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def interpret_query(query: str):
    """Clasifica la intención de la consulta."""
    result = classifier(query, CANDIDATE_LABELS)
    intent = result["labels"][0]  # best score always
    return intent


def agent_query(user_input: str):
    """Agente que interpreta y responde."""
    intent = interpret_query(user_input)

    if intent == "listar":
        data = call_api("/articles?limit=5")
        return "Aquí tienes algunos artículos:\n" + \
               "\n".join([f"- {r['id']}: {r['title']}" for r in data])

    elif intent == "buscar":
        #last word as keyword
        keyword = user_input.split()[-1]
        data = call_api(f"/search?q={keyword}")
        results = data
        if not results:
            return f"No encontré artículos con la palabra clave '{keyword}'."
        return f"Encontré {len(data)} artículos con '{keyword}':\n" + \
               "\n".join([f"- {r['id']}: {r['title']}" for r in results])

    elif intent == "detalle":
        # eextract number from query
        match = re.search(r"\d+", user_input)
        if match:
            article_id = match.group()
            data = call_api(f"/articles/{article_id}")
            return f"Artículo {data['id']} — {data['title']}\nResumen: {data['summary']}"
        else:
            return "No entendí qué ID de artículo necesitas. ¿Me lo repites?"

    else:
        return "No entendí tu consulta, ¿quieres listar, buscar o ver un detalle?"


if __name__ == "__main__":
    print("🤖 Agente de IA (HuggingFace) listo. Escribe tu consulta:")
    while True:
        q = input("> ")
        if q.lower() in ["salir", "exit", "quit"]:
            break
        answer = agent_query(q)
        print(answer)