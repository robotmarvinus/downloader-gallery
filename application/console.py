import os
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GLib", "2.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gio, Gtk, Gdk, GLib, GdkPixbuf

class Console(Gtk.HBox):
    def __init__(self):
        Gtk.HBox.__init__(self)
        self.modify_bg (Gtk.StateType.NORMAL, Gdk.Color (0, 0, 0))
        self.modify_fg (Gtk.StateType.NORMAL, Gdk.Color (65535, 65535, 65535))
        self.set_property("height-request", 100)

        scroll  = Gtk.ScrolledWindow()
        boxmain = Gtk.Box()
        align   = Gtk.Alignment(xalign=0.0, yalign=0.0, xscale=1.0, yscale=0.0)

        scroll.set_hexpand(False)
        scroll.set_vexpand(True)
        scroll.set_border_width(0)
        scroll.set_size_request(-1, 200)

        self.label = Gtk.Label()
        self.label.set_property("margin", 5)
        self.label.set_property("selectable", True)
        self.label.select_region(0, 0)

        self.add(scroll)
        scroll.add(boxmain)
        boxmain.pack_start(align, False, False, 10)
        align.add(self.label)

        self.print_text("Hello!...")
        
    def print_text(self, newtext, line=None):
        if not line or line == "\n":
            self.label.set_text(self.label.get_text() + "\n" + newtext)
        elif line == "\r":
            text = self.label.get_text()
            text = text[:text.rfind("\n")]
            self.label.set_text(text + "\n" + newtext)
        elif line == "+":
            self.label.set_text(self.label.get_text() + newtext)
        elif line == "clear":
            self.label.set_text("")

    def set_text(self, event, value, line=None):
        if not line:
            self.print_text(value)
        else:
            self.print_text(value, line)
        event.set()
