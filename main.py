# Код, который записывает в txt и excel файлы все города России, Беларуси и Казахстана, а также их координаты
import requests
from openpyxl import Workbook
from bs4 import BeautifulSoup


def data_entry_excel(cities):
    """Создание xlsx файла и запись в него"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Города"
    ws.append(['№', 'Город', 'Координаты'])
    [ws.append([number, elem[0], elem[1]]) for number, elem in zip(range(1, len(cities)+2), sorted(cities.items()))]
    wb.save("cities.xlsx")
    wb.close()
    return print('Успешно выполнилось')


def data_entry_txt(cities):
    """Создание txt файла и запись в него"""
    with open("DataCities.txt", "w+", encoding="utf-8") as file:
        [file.write(f"{num},{elem[0]},{elem[1]}\n") for num, elem in
         zip(range(1, len(cities) + 2), sorted(cities.items()))]
    return print('Успешно выполнилось')


def receiving_coordinates(cell_data):
    """Получения координат"""
    new_url = "https://ru.wikipedia.org" + cell_data.find('a')['href']
    new_response = requests.get(new_url)
    new_soup = BeautifulSoup(new_response.text, 'lxml')
    result = new_soup.find('span', title="Показать карту").text.replace('\xa0', '')
    return result


def cities_russia(cities) -> dict:
    """Вписывает в словарь все города России с их координатами"""
    url = "https://ru.wikipedia.org/wiki/Список_городов_России"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    tables = soup.find_all('table', class_='sortable')
    for table in tables:
        for item in table.find_all('tr')[1::]:
            cell_data = item.find('td').next_sibling.next_sibling
            town = cell_data.find('a').text
            name_cites = str(town) + ' (' + str(cell_data.next_sibling.find('a').text) + ')' if town in cities else town
            coordinates = receiving_coordinates(cell_data)  # Функция, для получения координат
            cities[name_cites] = coordinates
    return cities


def cities_belarus(cities) -> dict:
    """Вписывает в словарь все города Белоруссии с их координатами"""
    url = "https://ru.wikipedia.org/wiki/Города_Белоруссии#Города_в_Республике_Беларусь"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    tables = soup.find_all('table', class_='sortable')
    for table in tables:
        for item in table.find_all('tr')[1::]:
            cell_data = item.find('td').next_sibling.next_sibling
            town = cell_data.find('a').text
            name_cites = str(town) + '(Беларусь)' if town in cities else town
            coordinates = receiving_coordinates(cell_data)  # Функция, для получения координат
            cities[name_cites] = coordinates
    return cities


def cities_kazakhstan(cities) -> dict:
    """Вписывает в словарь все города Казахстана с их координатами"""
    url = "https://ru.wikipedia.org/wiki/Список_городов_Казахстана"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', class_='sortable')
    for item in table.find_all('tr')[1::]:
        cell_data = item.find('td')
        town = cell_data.find('a').text
        name_cites = str(town) + '(Казахстан)' if town in cities else town
        coordinates = receiving_coordinates(cell_data)     # Функция, для получения координат
        cities[name_cites] = coordinates
    return cities


if __name__ == "__main__":
    my_cities = {}
    cities_russia(my_cities)
    cities_belarus(my_cities)
    cities_kazakhstan(my_cities)
    data_entry_txt(my_cities)
    data_entry_excel(my_cities)
