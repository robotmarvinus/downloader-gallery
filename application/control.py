import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import subprocess

from application.button import *

from actions.finder import *
from actions.searcher import *
from actions.loader import *
from actions.sender import *

class Control(Gtk.HBox):
    def __init__(self, application):
        Gtk.HBox.__init__(self)
        self.set_property("height-request", 40)

        self.set_margin_left(10)
        self.set_margin_right(10)

        self.button_update = Button("object-rotate-right-symbolic", self, 5, 5, 0, 0)
        self.button_update.connect("clicked",  self.action_update, application)

        box    = Gtk.HBox()
        box.get_style_context().add_class("linked")
        self.pack_start(box, False, False, 0)

        self.combo  = self.create_combo(application, box)
        self.combo.connect("changed", self.action_changed)

        self.button_find = Button("edit-find-symbolic", box, 5, 5, 0, 0)
        self.button_find.connect("clicked",  self.action_find, application)

        self.button_search = Button("image-x-generic-symbolic", box, 5, 5, 0, 0)
        self.button_search.connect("clicked",  self.action_search, application)
        
        self.button_load = Button("document-save-symbolic", box, 5, 5, 0, 0)
        self.button_load.connect("clicked",  self.action_load, application)       

        self.button_send = Button("mail-message-new-symbolic", box, 5, 5, 0, 0)
        self.button_send.connect("clicked",  self.action_send, application)       

        label = Gtk.Label("Статус: ")
        label.set_margin_left(5)
        self.pack_start(label, False, False, 5)

        label = Gtk.Label()
        label.set_margin_left(5)
        label.set_margin_right(5)
        label.set_property("width-request", 100)
        self.pack_start(label, False, False, 5)
        self.status = label

        progress = Gtk.ProgressBar()
        progress.set_margin_left(10)
        progress.set_margin_right(10)
        progress.set_margin_bottom(15)
        progress.set_property("height-request", 10)
        self.pack_start(progress, True, True, 5)
        self.progress = progress

        button = Button("folder-open-symbolic", self, 5, 5, 0, 0)
        button.connect("clicked", self.action_open, application)       
        
    def create_combo(self, application, box):
        combo = Gtk.ComboBoxText()
        combo.set_margin_top(5)
        combo.set_margin_bottom(5)

        combo.set_property("width-request", 200)

        for item in application.data.sites:
            combo.append_text(item[0])

        box.pack_start(combo, False, False, 0)

        combo.set_active(-1)

        return combo

    def action_update(self, button, application):
        application.window.content.gallery.update(application)
        application.window.content.console.print_text("", "clear")

    def action_changed(self, widget):
        self.set_button_status()

    def set_button_status(self):
        if self.combo.get_active() == -1:
            self.button_find.set_sensitive(False)
        else:
            self.button_find.set_sensitive(True)

    def set_buttons_status(self, event, value):
        if value == False:
            self.combo.set_button_sensitivity(Gtk.SensitivityType.OFF)
            self.button_find.set_sensitive(False)
        elif value == True:
            self.combo.set_button_sensitivity(Gtk.SensitivityType.ON)
            self.set_button_status()

        self.button_update.set_sensitive(value)
        self.button_search.set_sensitive(value)        
        self.button_load.set_sensitive(value)
        self.button_send.set_sensitive(value)

    def action_find(self, button, application):
        if application.finder == None:
            if self.combo.get_active() == -1:
                application.window.content.console.print_text("Поиск: не выбран сайт...")
            else:
                site  = self.combo.get_active_text()
                value = application.data.get_site_status(site)

                self.status.set_text("Поиск...")
                self.button_search.set_sensitive(False)                
                self.button_load.set_sensitive(False)
                self.button_send.set_sensitive(False)

                application.finder = Finder(application, site, value)
                application.finder.find_start()

        elif application.finder.event.is_set():
            application.finder.find_stop()

    def action_search(self, button, application):
        if application.searcher == None:
            self.status.set_text("Поиск...")

            self.button_find.set_sensitive(False)
            self.button_load.set_sensitive(False)
            self.button_send.set_sensitive(False)

            application.searcher = Searcher(application)
            application.searcher.search_start()

        elif application.searcher.event.is_set():
            application.searcher.search_stop()

    def action_load(self, button, application):
        if application.loader == None:
            self.status.set_text("Загрузка...")

            self.button_search.set_sensitive(False) 
            self.button_find.set_sensitive(False)
            self.button_send.set_sensitive(False)

            application.loader = Loader(application)
            application.loader.load_start()

        elif application.loader.event.is_set():
            application.loader.load_stop()

    def action_send(self, button, application):
        if application.sender == None:
            self.status.set_text("Отправка...")

            self.button_find.set_sensitive(False)
            self.button_search.set_sensitive(False)            
            self.button_load.set_sensitive(False)

            application.sender = Sender(application)
            application.sender.send_start()

        elif application.sender.event.is_set():
            application.sender.send_stop()

    def find_end(self, event, application):
        self.button_search.set_sensitive(True)
        self.button_load.set_sensitive(True)
        self.button_send.set_sensitive(True)
        self.status.set_text("Поиск завершен")
        if application.finder.is_alive() == False:
            application.finder = None

    def search_end(self, event, application):
        self.button_find.set_sensitive(True)
        self.button_load.set_sensitive(True)
        self.button_send.set_sensitive(True)
        self.status.set_text("Поиск завершен")
        if application.searcher.is_alive() == False:
            application.searcher = None

    def load_end(self, event, application):
        self.button_find.set_sensitive(True)
        self.button_search.set_sensitive(True)        
        self.button_send.set_sensitive(True)
        self.status.set_text("Загрузка завершена")
        if application.loader.is_alive() == False:
            application.loader = None

    def send_end(self, event, application):
        self.button_find.set_sensitive(True)
        self.button_search.set_sensitive(True)        
        self.button_load.set_sensitive(True)
        self.status.set_text("Отправка завершена")
        if application.sender.is_alive() == False:
            application.sender = None

    def set_progress(self, event, value):
        self.progress.set_fraction(value)
        event.set()

    def action_open(self, button, application):
        subprocess.Popen(["xdg-open", application.data.pathimgs])

    def update(self, application):
        if application.data.load == False:
            self.button_load.set_visible(False)
        elif application.data.load == True:
            self.button_load.set_visible(True)

        if application.data.send == False:
            self.button_send.set_visible(False)
        elif application.data.load == True:
            self.button_load.set_visible(True)