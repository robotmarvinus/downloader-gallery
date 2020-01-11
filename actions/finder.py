import threading

from gi.repository import GLib

from actions.finders import finder_theomegaproject_org

class Finder(threading.Thread):
    def __init__(self, application, site, value):
        threading.Thread.__init__(self, target=self.find, args=(application,))
        self.event   = threading.Event()
        self.site    = site
        self.status  = value

    def find(self, application):
        if self.status == False:
            application.event_print("Полное сканирование сайта: " + self.site + " ...")
        elif self.status == True:
            application.event_print("Поиск новых галлерей: " + self.site + " ...")

        if self.site == "theomegaproject.org":
            finder_theomegaproject_org.start_find_galleries(application, self)

        if not self.event.is_set():
            application.event_print("Поиск по сайту остановлен...")
        else:
            if self.status == False:
                application.database.update_site(self.site)
                application.data.load_db_sites(self.database)

            application.event_print("Поиск по сайту завершен...")
            self.event.clear()

        application.event_end("find")

    def find_start(self):
        self.event.set()
        self.start()

    def find_stop(self):
        self.event.clear()