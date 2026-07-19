# NBA Daily Digest 🏀

Servicio automatizado que obtiene noticias NBA de fuentes RSS, genera un resumen diario con IA y lo envía por Telegram.

## Arquitectura

```
[EventBridge Schedule (cron diario)]
        │
        ▼
[Lambda Handler]
        │
        ├──► [RSS Fetcher] → obtiene noticias de Reddit y ESPN
        │
        ├──► [Groq Summarizer] → genera resumen en español con Llama 3.3
        │
        └──► [Telegram Notifier] → envía el resumen al bot
```

## Stack

| Componente | Tecnología |
|-----------|-----------|
| Lenguaje | Python 3.12 |
| Fuentes | RSS feeds (feedparser + httpx) |
| Resumen IA | Groq API (Llama 3.3 70B) - free tier |
| Notificación | Telegram Bot API |
| Infra | AWS Lambda + EventBridge |
| Deploy | SAM |

## Estructura del proyecto

```
nba-daily-digest/
├── src/
│   ├── handler.py              # Entry point de Lambda
│   ├── scraper/
│   │   ├── rss_fetcher.py      # Obtiene y parsea feeds RSS
│   │   └── sources.py          # Configuración de fuentes
│   ├── summarizer/
│   │   └── groq_client.py      # Genera resumen con Groq/Llama 3.3
│   └── notifier/
│       └── telegram_bot.py     # Envía mensaje por Telegram
├── tests/
├── .env                        # Variables de entorno (no versionado)
├── .gitignore
├── requirements.txt
└── template.yaml               # SAM template para deploy
```

## Requisitos previos

- Python 3.12+
- Cuenta en [Groq](https://console.groq.com) (free tier)
- Bot de Telegram creado con [@BotFather](https://t.me/BotFather)
- AWS CLI configurado (para deploy)

## Instalación local

```bash
# Clonar el repositorio
git clone https://github.com/TomasAgustinDuro/nba-daily-digest.git
cd nba-daily-digest

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

Crear un archivo `.env` en la raíz con:

```
GROQ_API_KEY=tu_groq_api_key
TELEGRAM_BOT_TOKEN=tu_telegram_bot_token
TELEGRAM_CHAT_ID=tu_chat_id
```

### Obtener el chat_id de Telegram

1. Enviar un mensaje cualquiera a tu bot
2. Abrir en el browser: `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
3. Buscar `"chat":{"id": 123456789}` en la respuesta

## Ejecución local

```bash
# Pipeline completo (fetch + summarize + notify)
python -m src.handler

# Probar solo el fetcher
python -m src.scraper.rss_fetcher

# Probar solo el summarizer
python -m src.summarizer.groq_client

# Probar solo el notificador
python -m src.notifier.telegram_bot
```

## Fuentes RSS configuradas

| Fuente | URL | Artículos |
|--------|-----|-----------|
| Reddit r/nba (top diario) | `https://www.reddit.com/r/nba/top/.rss?t=day` | 5 |
| ESPN NBA | `https://www.espn.com/espn/rss/nba/news` | 5 |

## Variables de entorno

| Variable | Descripción |
|----------|-------------|
| `GROQ_API_KEY` | API key de Groq (console.groq.com) |
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram (BotFather) |
| `TELEGRAM_CHAT_ID` | ID del chat destino del mensaje |

## Deploy (pendiente)

El deploy se realizará con AWS SAM:

```bash
sam build
sam deploy --guided
```

El trigger será un EventBridge Schedule (cron diario a las 8:00 AM).

## Costos estimados

- **Lambda**: $0 (free tier: 1M invocaciones/mes)
- **Groq API**: $0 (free tier: 14,400 req/día)
- **Telegram**: $0 (API gratuita)
- **EventBridge**: $0 (free tier cubre ampliamente)

**Costo total: $0/mes**
