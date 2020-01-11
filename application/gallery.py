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
        application.event_buttons_status(False)

        data = application.database.select("unknowns")
        if data:
            i = 0
            l = len(data)
            m = self.max_y * self.max_x

            for y in range(self.max_y):
                for x in range(self.max_x):
                    if l < m and i == l:
                        break

                    application.event_pixbuf(self.get_child_at(x, y), data[i])

                    i = i + 1

        application.event_buttons_status(True)
               
    def update(self, application):
        update = threading.Thread(target=self.set_images, args=(application,))
        update.start()