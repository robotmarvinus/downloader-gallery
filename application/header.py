import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Header(Gtk.HeaderBar):
    def __init__(self):
        Gtk.HeaderBar.__init__(self)
        self.set_show_close_button(False)
        self.set_property("height-request", 40)
        self.set_title("Downloader gallery")

    def update(self, application):
        button = Gtk.Button.new_from_icon_name("window-close-symbolic", Gtk.IconSize.BUTTON)
        button.connect("clicked", self.action_quit, application)
        self.pack_end(button)

        button = Gtk.Button.new_from_icon_name("window-minimize-symbolic", Gtk.IconSize.BUTTON)
        button.connect("clicked", application.window.set_minimize)
        self.pack_end(button)

        button = Gtk.Button.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.BUTTON)
        button.connect("clicked", self.action_open, application)
        self.pack_end(button)

    def action_open(self, widget, application):
        application.open_dialog()

    def action_quit(self, widget, application):
        application.exit()
