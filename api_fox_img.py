import os
import requests


def load_fox_img():
    # Запрос к апи получить рандомную картинку лисички
    req = requests.request(method='GET', url='https://randomfox.ca/floof/?ref=apilist.fun')
    image_url = req.json().get('image')

    # Получить файл картинки
    res = requests.get(image_url)

    # Сохранить файл под оригинальным именем
    name_img = str(image_url).replace('https://randomfox.ca/images/', '')
    img_fox = open(f'{name_img}', 'wb')
    img_fox.write(res.content)
    img_fox.close()
    return f'{name_img}'

def delete_fox_img(name_img):
    # Удалить файл после отправки юзеру
    os.remove(f'{name_img}')



