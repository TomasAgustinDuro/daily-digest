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

## Deploy en AWS

### Requisitos

- [AWS CLI](https://aws.amazon.com/cli/) instalado y configurado (`aws configure`)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) instalado

### Primer deploy

```bash
sam build
sam deploy --guided
```

Durante el `--guided` se piden:
- **Stack name**: `daily-digest`
- **Region**: `us-east-1`
- **GroqApiKey**: tu API key de Groq
- **TelegramBotToken**: token del bot de Telegram
- **TelegramChatId**: tu chat ID de Telegram

La config queda guardada en `samconfig.toml` para futuros deploys.

### Actualizar despues de cambios en el codigo

```bash
sam build
sam deploy
```

### Actualizar solo las API keys (sin cambios de codigo)

```bash
sam deploy --parameter-overrides GroqApiKey=TU_KEY TelegramBotToken=TU_TOKEN TelegramChatId=TU_CHAT_ID
```

### Invocar manualmente

```bash
aws lambda invoke --function-name daily-digest-NbaDailyDigestFunction-XXXX output.json
```

(El nombre exacto de la funcion se muestra al final del deploy)

### Ver logs

```bash
sam logs --name NbaDailyDigestFunction --stack-name daily-digest
```

### Schedule

La Lambda se ejecuta automaticamente todos los dias a las **11:00 UTC (8:00 AM Argentina)** via EventBridge.

## Costos estimados

- **Lambda**: $0 (free tier: 1M invocaciones/mes)
- **Groq API**: $0 (free tier: 14,400 req/día)
- **Telegram**: $0 (API gratuita)
- **EventBridge**: $0 (free tier cubre ampliamente)

**Costo total: $0/mes**
