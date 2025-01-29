import requests
import re
from bs4 import BeautifulSoup
from loguru import logger
from config import REGEX, PATH_TO_WEBSITE_NEWS


# Настройка логирования
logger.add(
    'church.parser/src/parser/tatmetropolia/logs/debug.log',
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 week",
    compression="zip",
)

def build_url(id):
    return f"{PATH_TO_WEBSITE_NEWS}{id}"

def check_response_code(url) -> bool:
    response = requests.get(url)
    if response.status_code == 200:
        logger.info(f"Подключение к странице: [{url}] - успешно.")
        return True
    elif response.status_code == 404:
        logger.error("Страница не найдена", exc_info=True)
        return False

def extract_date(soup: BeautifulSoup) -> str:
    date = soup.find('time')
    return re.sub('\s+', '', date.text)

def extract_images(soup: BeautifulSoup, limit=5):
    all_images = soup.find('div', class_='gallery')
    if all_images is None:
        logger.trace("Фотографии отсутствуют", exc_info=True)
        return None
    image_list = []
    for data in all_images.find_all('a', limit=limit, href=True):
        image_list.append(data['href'])
        """with open(PATH_TO_SAVE + data['href'].split('/')[-1], "wb") as f:
            f.write(requests.get(PATH_TO_WEBSITE + data['href']).content)"""
    return image_list

def extract_title_image(soup: BeautifulSoup, limit=1) -> str:
    all_image_block = soup.find('div', class_='ImgBlock')
    if all_image_block is None:
        logger.trace("Фотография отсутствует", exc_info=True)
        return None
    """for data in all_image_block.find_all('img', limit=limit, src=True):
        with open(PATH_TO_SAVE + data['src'].split('/')[-1], "wb") as f:
            f.write(requests.get(PATH_TO_WEBSITE + data['src']).content)"""
    for data in all_image_block.find_all('img', limit=limit, src=True):
        return data['src']

def extract_date_from_dom(soup: BeautifulSoup) -> str:
    date = soup.find('time')
    return re.sub('\s+', '', date.text)

def extract_title(soup) -> str:
    data = soup.find('h1')
    return data.text

def extract_text_blocks_from_dom(soup: BeautifulSoup) -> list:
    text_list = []
    all_info_block = soup.select_one('div', class_='picture-of-the-day')
    for data in all_info_block.find_all('p'):
        for x in all_info_block.select('a'):
            x.decompose()
        if str(data).find(REGEX) != -1:
            break
        text_list.append(data.text)
    return text_list

def check_title_exists(id) -> bool:
    if not check_response_code(build_url(id)):
        return None
    response_text = requests.get(build_url(id)).text
    soup = BeautifulSoup(response_text, "lxml")
    data = soup.find('h1')
    return True if data is None else False

from time import sleep

def get_json_data(id: int):
    logger.info(f"Поиск страницы с идентификатором: [{id}].")
    if not check_response_code(build_url(id)):
        return 'None'
    response_text = requests.get(build_url(id)).text
    soup = BeautifulSoup(response_text, "lxml")
    try:
        json_data = {
            "news": {
                "title": extract_title(soup),
                "other_image": extract_images(soup),
                "title_image": extract_title_image(soup),
                "context": extract_text_blocks_from_dom(soup),
                "time": extract_date_from_dom(soup)
            }
        }
    except ValueError:
        logger.error("Неверный формат данных.", exc_info=True)
        return None
    except Exception:
        logger.error("Данные страницы для чтения отсутствуют.", exc_info=True)
        return None
    logger.info(f"Получение новости с наименованием: [{json_data['news']['title']}] : [{json_data['news']['time']}] - успешно.")
    return json_data

