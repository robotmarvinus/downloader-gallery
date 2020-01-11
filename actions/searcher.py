import threading

from actions.searchers import searcher_theomegaproject_org

class Searcher(threading.Thread):
    def __init__(self, application):
        threading.Thread.__init__(self, target=self.search, args=(application,))
        self.event   = threading.Event()

    def search(self, application):
        application.event_print("Поиск изображений: ")
        
        data    = application.database.select("search")
        gallery = None
        title   = None
        site    = None
        name    = None

        while data:
            if not self.event.is_set():
                break

            gallery = data[0]
            title   = data[1]
            site    = data[2]
            name    = data[3]

            if site == "theomegaproject.org":
                url = "https://www.theomegaproject.org/" + gallery

                result = searcher_theomegaproject_org.start_search_images(application, self, url, gallery, title, name)
                if result != "Error" and result != "Stop":
                    result_db = application.database.update(gallery, site, name, "action", images=result[0], tags=result[1])
                    if result_db != "Error":
                        application.data.records_search = application.data.records_search - 1
                        application.data.records_load = application.data.records_load + 1
                        application.data.records_send = application.data.records_send + 1            

                        application.event_print("...Готово", "+")
                        application.event_info()

            data    = application.database.select("search")

        if not self.event.is_set():
            application.event_print("Поиск изображений остановлен...")
        else:
            application.event_print("Поиск изображений завершен...")
            self.event.clear()

        application.event_end("search")

    def search_start(self):
        self.event.set()
        self.start()

    def search_stop(self):
        self.event.clear()