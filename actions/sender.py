import threading
import math
import requests
import json
import time

#https://oauth.yandex.ru

class Sender(threading.Thread):
    def __init__(self, application):
        threading.Thread.__init__(self, target=self.send, args=(application,))
        self.event      = threading.Event()
        self.token      = "AgAAAAA5lcFYAAYBS37o67UnWkqnh-jXkmMDeiI"
        self.collection = "5df9d8a840a3238279b61bf1"
        self.tags       = "#models, #actress, #womans, #girls, #beaty"

    def get_collections_count(self):
        request_url     = "https://api.collections.yandex.net/v1/boards/?page_size=1"
        request_headers = {
            'Host': 'api.collections.yandex.net',
            'Authorization': 'OAuth ' + self.token,
            'Accept': 'application/json'
        }
        response = requests.get(request_url, headers=request_headers)
        count    = response.json()['count']

        print("Всего коллекций", count)

        return count

    def get_collections(self):
        count           = get_collections_count()
        request_url     = "https://api.collections.yandex.net/v1/boards/?page_size=" + str(count)
        request_headers = {
            'Host': 'api.collections.yandex.net',
            'Authorization': 'OAuth ' + self.token,
            'Accept': 'application/json'
        }
        response = requests.get(request_url, headers=request_headers)

        return response.json()['results']

    def create_collection(self, title, description, is_private):
        request_url     = "https://api.collections.yandex.net/v1/boards/"
        request_headers = {
            'Host': 'api.collections.yandex.net',
            'Authorization': 'OAuth ' + self.token,
            'Content-Type': 'application/json; charset=utf-8'
        }
        request_body    = {
            'description': description,
            'is_private': is_private,
            'title': title
        }

        jsonBody = json.dumps(request_body, ensure_ascii=False).encode('utf8')
        response = requests.post(request_url, jsonBody, headers=request_headers)

        print(response)

    def print_collections(self):
        collections = get_collections()

        print("Коллекций:", len(collections))

        for collection in collections:
            print (collection['title'], collection['id'])

    def get_cards_count(self):
        url      = "https://api.collections.yandex.net/v1/cards/?page_size=1"
        headers  = {
            'Host': 'api.collections.yandex.net',
            'Authorization': 'OAuth ' + self.token,
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        count    = response.json()['count']
        return count

    def get_pages_count(self, cards, cards_page):
        return math.ceil(cards / cards_page)

    def get_cards(self):
        count = self.get_cards_count()
        size  = 100
        pages = self.get_pages_count(count, size)
        cards = []

        for i in range(pages):
            page    = i + 1
            url     = "https://api.collections.yandex.net/v1/cards/?page=" + str(page) + "&page_size=" + str(size)
            headers = {
                'Host': 'api.collections.yandex.net',
                'Authorization': 'OAuth ' + self.token,
                'Accept': 'application/json'
            }
            response = requests.get(url, headers=headers)
            result   = response.json()['results']

            for item in result:
                cards.append(item['content'][0]['content']['url'])
                cards.append(item['content'][0]['source']['url'])

        return cards

    def create_card(self, image_url, description):
        request_url     = "https://api.collections.yandex.net/v1/cards/"
        request_headers = {
            'Host': 'api.collections.yandex.net',
            'Authorization': 'OAuth ' + self.token,
            'Content-Type': 'application/json; charset=utf-8'
        }
        request_body    = {
            'board_id': self.collection,
            'content': [{
                'source': {
                    'url': image_url
                },
                'source_type': 'image'
            }],
            'description': description,
            'source_meta': {
                'page_domain': '',
                'page_title': '',
                'page_url': image_url
            }
        }

        jsonBody = json.dumps(request_body, ensure_ascii=False).encode('utf8')
        response = requests.post(request_url, jsonBody, headers=request_headers)

        if str(response) != "<Response [200]>":
            return str(response)
        else:
            None

    def send(self, application):
        application.window.content.console.print_text("Отправка: старт...")

        data    = application.database.select("send")
        gallery = None
        title   = None
        site    = None
        name    = None
        images  = None
        tags    = None
        status  = None        
        index   = 0
        i       = 0.0

        while data:
            if not self.event.is_set():
                break

            gallery = data[0]
            title   = data[1]
            site    = data[2]
            name    = data[3]
            images  = data[5].split(" ")
            tags    = data[6]
            status  = data[7]
            index   = 0
            i       = 0.0

            if not tags:
                tags  = self.tags

            step  = round(1.0/len(images), 3)

            application.event_print("Отправка: галлерея " + name + ", " + gallery)
            application.event_progress(i)

            for image in images:
                if image:
                    about  = title + " [" + str(index)+ "]\nModel: " + name + "\n" + tags
                    result = self.create_card(image, about)
                    
                    print("result", result)

                    if result == "Error":
                        application.event_print("Отправка: ошибка при создании карточки (" + result[1] + ")...")
                        break
                    else:
                        if status == "action":
                            result = application.database.update(gallery, site, name, "load")
                        elif status == "send":
                            result = application.database.update(gallery, site, name, "ok")

                        if result == "Error":
                            break

                        i = i + step
                        index = index + 1

                        application.event_progress(i)
                        application.event_print("Отправлено: " + name + " - " + title[:25] + "[" + str(index) + "]", "\r")

            if result != "Error":
                if status == "send":
                    application.data.records_ok = application.data.records_ok + 1
                application.data.records_send = application.data.records_send - 1

                application.event_print("...Готово", "+")
                application.event_info()

            data    = application.database.select("send")

        if not self.event.is_set():
            application.window.content.console.print_text("Отправка: остановлена...")
        else:
            self.event.clear()
            application.window.content.console.print_text("Отправка: завершена...")

        application.event_end("send")

    def send_start(self):
        self.event.set()
        self.start()

    def send_stop(self):
        self.event.clear()