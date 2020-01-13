import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from application.gallery import *
from application.control import *
from application.console import *
from application.info import *

class Content(Gtk.VBox):
    def __init__(self, application):
        Gtk.VBox.__init__(self)
        self.gallery = Gallery(application)
        self.control = Control(application)
        self.console = Console()
        self.info    = Info(application)

        self.pack_start(self.gallery, False, False, 0)
        self.pack_start(self.control, False, False, 0)
        self.pack_start(self.console, False, False, 0)
        self.pack_start(self.info, False, False, 0)

    def update(self, application):
        self.control.update(application)
        self.info.update(application)
        self.gallery.update(application)        