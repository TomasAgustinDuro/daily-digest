from src.scraper.rss_fetcher import getter
from src.summarizer.groq_client import create_prompt, groq_client
from src.notifier.telegram_bot import send_message


def handler(event, context): 
    try:
        response = getter()

        system_prom, rol_prompt = create_prompt(response)
        summary = groq_client(system_prom, rol_prompt)

        return send_message(summary)
    except Exception as error:
        print(error)

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    load_dotenv()
    handler(None, None)