import threading

from gi.repository import GLib

from actions.finders import finder_theomegaproject_org

class Finder(threading.Thread):
    def __init__(self, application):
        threading.Thread.__init__(self, target=self.find, args=(application,))
        self.event   = threading.Event()
        self.site    = None

    def find(self, application):
        application.event_print("Поиск по сайту: " + self.site + "\n")

        if self.site == "theomegaproject.org":
            finder_theomegaproject_org.start_find_galleries(application, self)

        if not self.event.is_set():
            application.event_print("Поиск по сайту остановлен...")
        else:
            application.event_print("Поиск по сайту завершен...")
            self.event.clear()

        application.event_end("find")

    def find_start(self, site):
        self.site = site
        self.event.set()
        self.start()

    def find_stop(self):
        self.event.clear()