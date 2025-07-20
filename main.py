import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


KEYWORDS = ['дизайн', 'фото', 'web', 'python']

url = "https://habr.com/ru/articles/"
headers = {"User-Agent": "Mozilla/5.0"}

try:
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    articles = soup.find_all(class_="tm-article-snippet")

    if not articles:
        print("Статьи не найдены")
    else:
        for article in articles:
            title = article.find('h2', class_='tm-title')
            article_text = (title.text.strip() + " " + article.get_text(strip=True)).lower()

            found_keywords = [word for word in KEYWORDS if word in article_text]

            if found_keywords:
                print("\n" + "=" * 50)
                print(f"Найдено {len(found_keywords)} совпадений(-е):")
                print("Ключевое(-ые) слово(-а):", ", ".join(found_keywords))

                time = article.find('time')
                if time:
                    print("Дата:", time['datetime'])

                if title:
                    print("Заголовок:", title.text.strip())
                    print("Ссылка:", urljoin(url, title.a['href']))

except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе: {e}")