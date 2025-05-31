from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def scrape_the_hindus(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []

    for li in soup.select("ul.latest-news-list li a"):
        if len(headlines) >= 10:
            break
        title = li.text.strip()
        link = li['href']
        if title and link:
            headlines.append({
                "title": title,
                "url": link
            })

    return headlines



def scrape_timesOfIndia(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    news_items = soup.select('ul.HytnJ li')
    
    headlines = []
    for item in news_items[:10]:
        headline_tag = item.select_one("p.CRKrj")
        link_tag = item.find("a", href=True)
        
        if headline_tag and link_tag:
            title = headline_tag.text.strip()
            url = link_tag['href']
            if not url.startswith("http"):
                url = "https://timesofindia.indiatimes.com" + url
            headlines.append({"title": title, "url": url})
    
    return headlines


def scrape_economic_times(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    headlines=[]
    for li in soup.select("ul.data > li")[:10]:
        headline_tag = li.find("a", itemprop='url')
        if headline_tag :
            title = headline_tag.get_text(strip=True)
            url = headline_tag.get('href', '')
            if url and not url.startswith("http"):
                url = "https://economictimes.indiatimes.com" + url
            headlines.append({"title":title, "url":url})
    return headlines
    

# Helper function
def extract_links(base_url, selector, relative=True):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    for h in soup.select(selector)[:10]:
        link = h.get('href', '')
        if relative and not link.startswith("http"):
            link = base_url + link
        headlines.append({"title": h.get_text(strip=True), "url": link})
    return headlines


@app.get("/headlines/timesofindia")
def get_toi():
    return {
        "source": "Times of India",
        "headlines": scrape_timesOfIndia("https://timesofindia.indiatimes.com/news")
    }


@app.get("/headlines/economictimes")
def get_et():
    return {
        "source": "Economic Times",
        "headlines": scrape_economic_times("https://economictimes.indiatimes.com/news/latest-news")
    }

@app.get("/headlines/businesstoday")
def get_bt():
    return {
        "source": "Business Today",
        "headlines": extract_links("https://www.businesstoday.in/latest", "h2 a", relative=False)
    }

@app.get("/headlines/thehindus")
def get_th():
    return{
        "source": "The hindus",
        "headlines": scrape_the_hindus("https://www.thehindu.com/latest-news/")
    }