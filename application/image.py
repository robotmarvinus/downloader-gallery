import os
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GLib", "2.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gio, Gtk, GLib, GdkPixbuf

import threading

from actions.parser import *

class Image(Gtk.EventBox):
    def __init__(self, application):
        Gtk.EventBox.__init__(self)
        self.width   = 200
        self.height  = 300
        self.path    = application.data.pathview
        self.site    = None
        self.view    = None
        self.name    = None
        self.gallery = None
        self.image   = Gtk.Image()

        self.connect("button-press-event", self.action_press_image, application)
        self.add(self.image)

    def get_filename(self):
        return self.site + "_" + self.view[self.view.rindex('/') + 1:]

    def get_pixbuf(self, application):
        image    = "http://" + self.view
        filename = self.get_filename()
        pathdir  = self.path + "/"
        fullpath = pathdir + filename
        result   = load_image(application, image, pathdir, filename)
        if result == "OK":
            return GdkPixbuf.Pixbuf.new_from_file_at_scale(fullpath, self.width, self.height, True)
        elif result == "Error":
            return "Error"

    def action_press_image(self, widget, event, application):
        if event.button == 1:
            status = "search"
            text   = "Добавлено в очередь загрузки: "
        elif event.button == 3:
            status = "no"
            text   = "Удалено из очереди загрузки: "

        filename = self.get_filename()
        fullpath = os.path.abspath(self.path + "/" + filename)

        if os.path.exists(fullpath):
            os.remove(fullpath)

        if self.name == "unknown":
            application.database.update(self.gallery, self.site, self.name, status)
            application.window.content.console.print_text(text + self.name + ", " + self.gallery)

            application.data.records_main    = application.data.records_main - 1
            if status == "search":
                application.data.records_search  = application.data.records_search + 1
        else:
            for item in application.database.select("name", [self.name, self.site]):
                application.database.update(item[0], self.site, self.name, status)
                application.window.content.console.print_text(text + self.name + ", " + item[0])

                application.data.records_main    = application.data.records_main - 1
                if status == "search":
                    application.data.records_search  = application.data.records_search + 1

        application.window.content.info.update(application)

        self.update(application)

    def set_image(self, event, application, data):
        self.gallery = data[0]
        self.site    = data[2]
        self.name    = data[3]
        self.view    = data[4]

        result = self.get_pixbuf(application)
        if result != "Error":
            self.image.set_from_pixbuf(result)
        
        event.set()
        
    def update(self, application):
        data   = application.database.select("unknown")
        update = threading.Thread(target=application.event_pixbuf, args=(self, data))
        update.start()