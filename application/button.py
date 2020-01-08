import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Button(Gtk.Button):
    def __init__(self, icon_name, box, top, bottom, left, right, width=None):
        Gtk.Button.__init__(self)

        if type(width) == int:
            self.set_property("width-request", width)

        self.set_margin_top(top)
        self.set_margin_bottom(bottom)
        self.set_margin_left(left)
        self.set_margin_right(right)

        self.set_image(Gtk.Image.new_from_icon_name (icon_name, Gtk.IconSize.BUTTON))

        box.pack_start(self, False, False, 0)