import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from application.header import *
from application.content import *

class Window(Gtk.ApplicationWindow):
    def __init__(self, application):
        Gtk.ApplicationWindow.__init__(self, title=application.title, application=application)
        Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", True)

        self.set_property("resizable", False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_from_file(application.icon)
        self.set_wmclass(application.title, application.title)
        
        self.connect("key-release-event", self.on_key_release, application)

        self.header  = Header()
        self.content = Content(application)

        self.set_titlebar(self.header)
        self.add(self.content)

        self.show_all()

    def set_minimize(self, widget):
        self.iconify()

    def on_key_release(self, widget, event, application):
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        if ctrl and event.keyval == Gdk.KEY_w or event.keyval == Gdk.KEY_Escape:
            application.exit()

    def action_open_dialog(self, widget, application):
        application.open_dialog()

    def action_quit(self, widget, application):
        application.exit()