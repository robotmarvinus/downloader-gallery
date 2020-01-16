import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

import os
import subprocess

from application.button import *

class DialogHeader(Gtk.HeaderBar):
    def __init__(self, application):
        Gtk.HeaderBar.__init__(self)
        self.set_show_close_button(False)
        self.set_title("Настройки")

        self.button = Gtk.Button.new_from_icon_name("window-close-symbolic", Gtk.IconSize.BUTTON)
        self.button.set_margin_right(5)
        self.button.connect("clicked", self.action_close, application)

        if not application.data.pathdata or not application.data.pathimgs:
            self.button.set_sensitive(False)

        self.pack_end(self.button)

    def action_close(self, widget, application):
        application.dialog.dialog_close()

class DialogContent(Gtk.VBox):
    def __init__(self, application):
        Gtk.HBox.__init__(self)

        self.set_property("width-request", 800)

        self.set_margin_top(10)
        self.set_margin_left(20)
        self.set_margin_right(20)
        self.set_margin_bottom(10)

        self.label_version = self.create_version("Версия: ", application.version)

        self.check_load = self.create_check("Загрузка изображений: ", application.data.load)
        self.check_send = self.create_check("Отправка изображений: ", application.data.send)

        self.yandex_token = self.create_yandex_entry("Яндекс токен", application.data.yandex_token)
        self.yandex_collection = self.create_yandex_entry("Яндекс коллекция: ", application.data.yandex_collection)

        self.create_config("Каталог настроек: ", application.data.pathconf[:application.data.pathconf.rindex("/")])
        self.create_preview("Каталог превью: ", application.data.pathview)

        self.entry_data = self.create_entry(application, "Каталог базы данных: ", application.data.pathdata)
        self.entry_load = self.create_entry(application, "Каталог загрузки: ", application.data.pathimgs)

        self.create_separator()

        self.message = self.create_message(application)

    def create_box(self, text):
        box     = Gtk.HBox()
        label   = Gtk.Label(text)

        box.set_margin_top(5)
        box.set_margin_bottom(5)

        label.set_xalign(0.0)
        label.set_property("width-request", 200)

        box.pack_start(label, False, False, 0)
        self.pack_start(box, False, False, 0)
        return box

    def create_version(self, title, value):
        box     = self.create_box(title)
        label   = Gtk.Label()
        label.set_xalign(0.0)
        label.set_margin_left(20)
        label.set_text(value)

        box.pack_start(label, True, True, 0)

        return label

    def create_check(self, title, value):
        box     = self.create_box(title)
        check   = Gtk.CheckButton()
        check.set_margin_top(5)
        check.set_margin_bottom(5)
        check.set_margin_left(20)
        box.pack_start(check, False, False, 0)

        check.set_active(value)
        
        return check

    def create_yandex_entry(self, title, value=None):
        box     = self.create_box(title)
        entry   = Gtk.Entry()
        entry.set_margin_left(10)
        entry.set_margin_right(100)
        if value:
            entry.set_text(value)  
        box.pack_start(entry, True, True, 0)
        return entry

    def create_config(self, title, value):
        box     = self.create_label(title, value)

        button  = Button("folder-open-symbolic", box, 0, 0, 0, 0, width=100)
        button.connect("clicked", self.action_open, value)

    def create_preview(self, title, value):
        box     = self.create_label(title, value)

        button  = Button("folder-open-symbolic", box, 0, 0, 0, 0, width=50)
        button.connect("clicked", self.action_open, value)

        button  = Button("edit-delete-symbolic", box, 0, 0, 0, 0, width=50)
        button.connect("clicked", self.action_delete, value)

    def create_label(self, title, value):
        box     = self.create_box(title)
        label   = Gtk.Label()
        label.set_xalign(0.0)
        label.set_margin_left(20)
        label.set_text(value)

        box.pack_start(label, True, True, 0)

        return box

    def create_entry(self, application, title, value=None):
        box     = self.create_box(title)
        entry   = Gtk.Entry()
        entry.set_margin_left(10)

        if value:
            entry.set_text(value)  

        box.pack_start(entry, True, True, 0)

        button  = Button("edit-find-symbolic", box, 0, 0, 0, 0, width=50)
        button.connect("clicked", self.select_dir, application, entry)

        button  = Button("folder-open-symbolic", box, 0, 0, 0, 0, width=50)
        button.connect("clicked", self.action_open, value)

        return entry

    def create_separator(self):
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        self.pack_start(separator, True, True, 0)

    def create_message(self, application):
        box     = self.create_box("Сообщение: ")
        label   = Gtk.Label()
        button  = Gtk.Button.new_from_icon_name("document-save-symbolic", Gtk.IconSize.BUTTON)

        button.set_property("width-request", 100)

        label.set_xalign(0.0)
        label.set_margin_left(20)

        button.connect("clicked", self.action_save, application)

        box.pack_start(label, True, True, 0)
        box.pack_start(button, False, False, 0)

        return label

    def select_dir(self, button, application, entry):
        application.dialog.child_run = True

        dialog = Gtk.FileChooserDialog()
        dialog.set_transient_for(application.dialog)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        dialog.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.set_current_folder(application.data.pathhome)
        dialog.set_title("Select folder")

        dialog.connect("close", self.dialog_close)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            entry.set_text(dialog.get_filename())

        dialog.destroy()

    def action_open(self, button, path):
        subprocess.Popen(["xdg-open", path])

    def action_save(self, button, application):
        application.dialog.save_data(application)

    def action_delete(self, button, value):
        os.system(f"rm -rf {value}")

    def dialog_close(self, dialog):
        dialog.destroy()
            
class Dialog(Gtk.Window):
    def __init__(self, application):
        Gtk.Window.__init__(self)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.set_skip_taskbar_hint(True)

        self.set_property("destroy-with-parent", True)

        self.connect("key-release-event", self.on_key_release, application)

        self.child_run = False

        self.header    = DialogHeader(application)
        self.content   = DialogContent(application)

        self.set_titlebar(self.header)
        self.add(self.content)

        self.update(application)

    def on_key_release(self, widget, event, application):
        if event.keyval == Gdk.KEY_Escape:
            if self.child_run == True:
                self.child_run = False
            else:
                self.dialog_quit()

    def save_data(self, application):
        load         = self.content.check_load.get_active()
        send         = self.content.check_send.get_active()
        path_one     = self.content.entry_data.get_text()
        path_two     = self.content.entry_load.get_text()
        yandex_token = self.content.yandex_token.get_text()
        yandex_collection = self.content.yandex_collection.get_text()

        if not path_one:
            self.content.message.set_text("Не указан каталог с базой данных")
        elif not path_two:
            self.content.message.set_text("Не указан каталог загрузки изображений...")
        elif not application.data.file_exist(path_one):
            self.content.message.set_text("Путь к базе данных не существует...")
        elif not application.data.file_exist(path_two):
            self.content.message.set_text("Путь для загрузки изображений не существует...")
        elif application.data.load == load \
            and application.data.send == send \
            and application.data.yandex_token == self.content.yandex_token.get_text() \
            and application.data.yandex_collection == self.content.yandex_collection.get_text() \
            and application.data.pathdata == path_one \
            and application.data.pathimgs == path_two:
            self.content.message.set_text("Настройки не изменялись...")
        else:
            if not application.data.pathdata or not application.data.pathimgs:
                if application.data.data_save(load, send, yandex_token, yandex_collection, path_one, path_two) != "Error":
                    if self.header.button.get_sensitive() == False:
                        self.header.button.set_sensitive(True)

                    application.database.set_path(application.data.pathdata)
                    application.database.update_config()

                    application.data.load_db_config(application.database)
                    application.data.load_db_sites(application.database)
                    application.data.load_db_records(application.database)

                    application.window.content.update(application)

                    self.content.message.set_text("Настройки сохранены...")
                else:
                    self.content.message.set_text("Ошибка при сохранении настроек...")                    
            else:
                if application.data.data_save(load, send, yandex_token, yandex_collection, path_one, path_two) != "Error":
                    if self.header.button.get_sensitive() == False:
                        self.header.button.set_sensitive(True)
                    self.content.message.set_text("Настройки сохранены...")
                else:
                    self.content.message.set_text("Ошибка при сохранении настроек...")

    def update(self, application):
        self.content.check_load.set_active(application.data.load)
        self.content.check_send.set_active(application.data.send)
        self.content.yandex_token.set_text(application.data.yandex_token)
        self.content.yandex_collection.set_text(application.data.yandex_collection)

    def dialog_close(self):
        if self.header.button.get_sensitive():
            self.hide()