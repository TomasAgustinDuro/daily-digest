from src.scraper.sources import sources
import httpx
import feedparser

def getter(): 
    articles = []

    for source in sources:
        response = httpx.get(source["url"]) 

        if response.is_success: 
            response_parsed = feedparser.parse(response.text)

            if response_parsed:
                for entry in response_parsed.entries[:source["max_articles"]]:
                    articles.append({
                        "source":response_parsed.feed.title,
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.summary,
                        "published": entry.published
                    }
                    )
    return articles

if __name__ == "__main__":
    getter()