import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from application.gallery import *
from application.control import *
from application.console import *
from application.info import *

class Window(Gtk.ApplicationWindow):
    def __init__(self, application):
        Gtk.ApplicationWindow.__init__(self, title=application.title, application=application)
        Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", True)

        self.set_property("resizable", False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_from_file(application.icon)
        self.set_wmclass(application.title, application.title)
        
        self.connect("key-release-event", self.on_key_release, application)

        self.header  = self.create_header(application)
        self.content = self.create_content(application)

        self.set_titlebar(self.header)
        self.add(self.content)

        self.show_all()

    def create_header(self, application):
        header = Gtk.HeaderBar()
        header.set_show_close_button(False)
        header.set_title("Downloader gallery")
        header.set_property("height-request", 40)

        button = Gtk.Button.new_from_icon_name("window-close-symbolic", Gtk.IconSize.BUTTON)
        button.connect("clicked", self.action_quit, application)
        header.pack_end(button)

        button = Gtk.Button.new_from_icon_name("window-minimize-symbolic", Gtk.IconSize.BUTTON)
        button.connect("clicked", self.set_minimize)
        header.pack_end(button)

        button = Gtk.Button.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.BUTTON)
        button.connect("clicked", self.action_open_dialog, application)
        header.pack_end(button)

        return header
        
    def create_content(self, application):
        content = Gtk.VBox()

        content.gallery = Gallery(application)
        content.control = Control(application)
        content.console = Console()
        content.info    = Info(application)

        content.pack_start(content.gallery, True, True, 0)
        content.pack_start(content.control, False, False, 0)
        content.pack_start(content.console, False, False, 0)
        content.pack_start(content.info, False, False, 0)

        return content

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