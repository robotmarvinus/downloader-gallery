import os
import requests

from bs4 import BeautifulSoup

def save_image(application, image, fullpath):
    try:
        out = open(fullpath, "wb")
        out.write(image)
        out.close()
        return "OK"
    except Exception:
        application.event_print("Ошибка сохранения " + fullpath)
        return "Error"

def load_image(application, url, path, filename):
    fullpath = path + filename
    
    if not os.path.exists(fullpath):
        index = filename.rfind("/")
        if index != -1:
            path     = path + filename[:index]
            filename = filename[index:]

        if not os.path.exists(path):
            os.makedirs(path)

        try:
            picture = requests.get(url).content
        except Exception as e:
            application.event_print("Ошибка загрузки:" + str(e) + "\nurl: " + url + "\nfullpath: " + fullpath)
            return "Error"

        return save_image(application, picture, fullpath)

    else:
        return "OK"

    return result

def get_html(application, url):
    try:
        response = requests.get(url)
    except requests.Timeout:
        message = "GET_HTML: Ошибка timeout, url: " + url
        application.event_print(message)
        return "Error"
    except requests.HTTPError as error:
        message = "GET_HTML: Ошибка url  (0), код: (1)".format(url, code)
        application.event_print(message)
        return "Error"
    except requests.RequestException:
        message = "GET_HTML: Ошибка скачивания " + url
        application.event_print(message)
        return "Error"
    else:
        return response.text

def get_parser(application, url):
    html = get_html(application, url)
    if html != "Error":
        parser = BeautifulSoup(html, 'html.parser')
        return parser
    else:
        return None

def find_image(url):
    try:
        response = requests.head(url)
    except:
        return False

    if response.headers and response.headers['Content-Type'][:5] == "image":
        return True
    else:
        return False