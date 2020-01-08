import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import threading

from application.image import *

class Gallery(Gtk.Grid):
    def __init__(self, application):
        Gtk.Grid.__init__(self)
        self.set_property("width-request", 1000)
        self.set_property("height-request", 600)

        self.max_x   = 5
        self.max_y   = 2

        for y in range(self.max_y):
            for x in range(self.max_x):
                image = Image(application)
                self.attach(image, x, y, 1, 1)

    def set_images(self, application):
        application.window.content.control.button_find.set_sensitive(False)
        application.window.content.control.button_search.set_sensitive(False)
        application.window.content.control.button_load.set_sensitive(False)
        application.window.content.control.button_send.set_sensitive(False)

        data = application.database.select("unknowns")
        if data:
            i = 0
            l = len(data)
            m = self.max_y * self.max_x

            for y in range(self.max_y):
                for x in range(self.max_x):
                    if l < m and i == l:
                        break

                    self.get_child_at(x, y).update(application, data[i])
                    i = i + 1

        application.window.content.control.button_find.set_sensitive(True)
        application.window.content.control.button_search.set_sensitive(True)        
        application.window.content.control.button_load.set_sensitive(True)
        application.window.content.control.button_send.set_sensitive(True)
               
    def update(self, application):
        update = threading.Thread(target=self.set_images, args=(application,))
        update.start()