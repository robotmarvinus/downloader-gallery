import threading

from actions.parser import *

class Loader(threading.Thread):
    def __init__(self, application):
        threading.Thread.__init__(self, target=self.load, args=(application,))
        self.event = threading.Event()

    def load(self, application):
        application.event_print("Загрузка: старт...")

        data    = application.database.select("load")
        if data:
            gallery = data[0]
            title   = data[1]
            site    = data[2]
            name    = data[3]
            images  = data[5].split(" ")
            status  = data[7]
            index   = 0
            i = 0.0

            while data:
                if not self.event.is_set() or not images:
                    break

                i = 0.0
                step = round(1.0/len(images), 3)

                pathdir = application.data.pathimgs + '/' + name + '/'

                for image in images:
                    if not self.event.is_set():
                        break

                    if image:
                        extension = image[image.rindex("."):]
                        filename  = gallery + '-' + str(index) + extension

                        result = load_image(application, image, pathdir, filename)
                        if result != "Error":
                            if status == "action":
                                result = application.database.update(gallery, site, name, "send")
                            elif status == "load":
                                result = application.database.update(gallery, site, name, "ok")

                            if result == "Error":
                                break

                            i = i + step
                            index = index + 1

                            application.event_progress(i)
                            application.event_print("Загружено: " + name + " - " + title[:25] + "[" + str(index) + "]", "\r")

                if result != "Error":
                    if status == "load":
                        application.data.records_ok = application.data.records_ok + 1
                    application.data.records_load = application.data.records_load - 1

                    application.event_print("...Готово", "+")
                    application.event_info()

                break

                data    = application.database.select("load")
                gallery = data[0]
                title   = data[1]
                site    = data[2]
                name    = data[3]
                images  = data[5].split(" ")
                status  = data[7]
                index   = 0
            
        if not self.event.is_set():
            application.event_print("Загрузка остановлена...")
        else:
            application.event_print("Загрузка завершенa...")
            self.event.clear()

        application.event_end("load")

    def load_start(self):
        self.event.set()
        self.start()

    def load_stop(self):
        self.event.clear()