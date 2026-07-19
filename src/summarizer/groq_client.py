from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def create_prompt(articles: list):
    system_prompt = "Sos un periodista deportivo de NBA. Generá un resumen diario breve y entretenido en español de las siguientes noticias. Usá un tono casual pero informativo. Máximo 500 palabras."
    rol_prompt = "Las noticias son: "

    for index, article in enumerate(articles, start=1): 
        rol_prompt += f"{index}. {article['title']} - {article['summary']}"

    return rol_prompt, system_prompt

def groq_client(system_prompt: str, rol_prompt: str):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": rol_prompt}
    ]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    from src.scraper.rss_fetcher import getter  
    
    articles = getter()
    system_prom, rol_prompt = create_prompt(articles)
    summary = groq_client(system_prom, rol_prompt)
    print(summary)