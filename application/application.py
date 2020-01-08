import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from data.database import *
from data.data import *

from actions.searcher import *

from application.dialog import *
from application.window import *

class Application(Gtk.Application):
    title   = "Downloader gallery"
    icon    = "/usr/share/icons/downloader-gallery.png"
    prog_id = "Aurelia.Downloader-gallery"
    version = "1.1.3"

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

            if not self.data.pathdata or not self.data.pathimgs:
                self.open_dialog()

            self.data.data_load_db(self.database)
            self.data.data_load_records(self.database)

            self.dialog.set_data(self.data)
            self.window.content.control.set_data(self.data)

            self.window.content.gallery.update(self)
            self.window.content.info.update(self)

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