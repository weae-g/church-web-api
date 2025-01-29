import requests
from bs4 import BeautifulSoup

def get_calendar_today():
    url = 'https://www.pravmir.ru/pravoslavnyj-kalendar/widget-app'
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text

        # Создаем объект BeautifulSoup для анализа HTML-контента
        soup = BeautifulSoup(html_content, 'html.parser')

        # Извлекаем текст из тегов
        tags_data = []
        for tag in soup.find_all(['div']):  # Это пример, вы можете указать свои теги
            tags_data.append(tag.text.strip())

        img = [link.get('src') for link in soup.find_all('img')]

        # Извлекаем ссылки (URL)
        links = [link.get('href') for link in soup.find_all('a')]

        # Выводим извлеченные данные
        print("Текст из тегов:")
        for item in tags_data:
            print(item)

        print("\nСсылки:")
        for link in links:
            print(link)
            
        print("\Изображения:")
        for link in img:
            print(link)
    else:
        print("Ошибка при загрузке данных:", response.status_code)
