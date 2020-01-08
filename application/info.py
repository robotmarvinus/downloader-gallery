import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Label(Gtk.Label):
    def __init__(self):
        Gtk.Label.__init__(self)
        self.set_xalign(0.0)
        self.set_margin_top(5)
        self.set_margin_bottom(5)
        self.set_margin_left(10)
        self.set_property("width-request", 90)

class Info(Gtk.HBox):
    def __init__(self, application):
        Gtk.HBox.__init__(self)

        self.label_all    = Label()
        self.label_main   = Label()
        self.label_search = Label()
        self.label_load   = Label()
        self.label_send   = Label()
        self.label_ok     = Label()

        self.pack_start(self.label_all, True, True, 0)
        self.pack_start(self.label_main, True, True, 0)
        self.pack_start(self.label_search, True, True, 0)
        self.pack_start(self.label_load, True, True, 0)
        self.pack_start(self.label_send, True, True, 0)
        self.pack_start(self.label_ok, True, True, 0)

        if application.database:
            self.update(application)

    def update(self, application):
        self.label_all.set_text("Всего записей: " + str(application.data.records_all))
        self.label_main.set_text("Основная очередь: " + str(application.data.records_main))
        self.label_search.set_text("Поиск: " + str(application.data.records_search))
        self.label_load.set_text("Загрузка: " + str(application.data.records_load))
        self.label_send.set_text("Отправка: " + str(application.data.records_send))
        self.label_ok.set_text("Готово: " + str(application.data.records_ok))

    def event_update(self, event, application):
        self.update(application)
        event.set()