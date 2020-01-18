import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from data.data import *
from data.database import *

from actions.searcher import *

from application.dialog import *
from application.window import *

class Application(Gtk.Application):
    title   = "Downloader gallery"
    icon    = "/usr/share/icons/downloader-gallery.png"
    prog_id = "Aurelia.Downloader-gallery"
    version = "1.1.23"

    def __init__(self):
        Gtk.Application.__init__(self, application_id=self.prog_id)

        self.data     = Data()
        self.database = Database(self)

        self.finder   = None
        self.searcher = None        
        self.loader   = None
        self.sender   = None

        self.dialog   = None
        self.window   = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        if not self.window:
            self.window   = Window(self)
            self.dialog   = Dialog(self)

            self.window.header.update(self)

            if not self.data.pathdata or not self.data.pathimgs:
                self.open_dialog()
            else:
                self.data.load_db_config(self.database)
                self.data.load_db_sites(self.database)
                self.data.load_db_records(self.database)

                self.window.content.update(self)
                self.dialog.content.update(self)

    def event_print(self, text, line=None):
        event = threading.Event()

        if line:
            GLib.idle_add(self.window.content.console.set_text, event, text, line)
        else:
            GLib.idle_add(self.window.content.console.set_text, event, text)

        event.wait()

    def event_progress(self, value):
        event = threading.Event()
        GLib.idle_add(self.window.content.control.set_progress, event, value)
        event.wait()

    def event_info(self):
        event = threading.Event()        
        GLib.idle_add(self.window.content.info.event_update, event, self)
        event.wait()

    def event_end(self, value):
        event = threading.Event()
        GLib.idle_add(self.window.content.control.set_progress, event, 0.0)
        if value == "find":
            GLib.idle_add(self.window.content.control.find_end, event, self)
        elif value == "search":
            GLib.idle_add(self.window.content.control.search_end, event, self)
        elif value == "load":
            GLib.idle_add(self.window.content.control.load_end, event, self)
        elif value == "send":
            GLib.idle_add(self.window.content.control.send_end, event, self)

    def event_pixbuf(self, image, data):
        event = threading.Event()
        GLib.idle_add(image.set_image, event, self, data)
        event.wait()

    def event_buttons_status(self, value):
        event = threading.Event()
        GLib.idle_add(self.window.content.control.set_buttons_status, event, value)

    def open_dialog(self):
        self.dialog.show_all()

    def exit(self):
        if self.finder:
            self.finder.find_stop()

        if self.loader:
            self.loader.load_stop()

        if self.sender:
            self.sender.send_stop()

        self.quit()
