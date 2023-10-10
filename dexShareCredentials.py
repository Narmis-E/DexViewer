import sys
import configparser
import gi
import os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, Gio, GLib

class DexShareCredentials(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(250, 150)
        self.set_resizable(False)
        self.set_modal(True)

        self.username_entry = Gtk.Entry()
        self.username_entry.set_placeholder_text("Username")
        self.password_entry = Gtk.Entry()
        self.password_entry.set_placeholder_text("Password")
        self.password_entry.set_visibility(False)  # Hide password characters

        ok_button = Gtk.Button(label="Ok")
        exit_button = Gtk.Button(label="Cancel")

        ok_button.connect("clicked", self.on_ok_clicked)
        exit_button.connect("clicked", self.on_exit_clicked)
        
        self.ous_check = Gtk.CheckButton(label="Outside US")
        self.ous_check.set_active(False)  # By default, set it to False (inside US)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.attach(self.username_entry, 0, 0, 3, 1)
        grid.attach(self.password_entry, 0, 1, 3, 1)
        grid.attach(ok_button, 0, 2, 1, 1)
        grid.attach(exit_button, 1, 2, 1, 1)
        grid.attach(self.ous_check, 2, 2, 1, 1)
        self.set_child(grid)

    def on_ok_clicked(self, button):
        self.username = self.username_entry.get_text()
        self.password = self.password_entry.get_text()
        self.ous = str(self.ous_check.get_active())
        self.save_credentials_to_config()
        
        self.destroy()

    def on_exit_clicked(self, button):
        self.destroy()
    
    def save_credentials_to_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        if 'Credentials' not in config:
            config['Credentials'] = {}

        config['Credentials']['Username'] = self.username
        config['Credentials']['Password'] = self.password
        config['Credentials']['ous'] = self.ous
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        return self.username, self.password, self.ous
    
class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = DexShareCredentials(application=app)
        self.win.present()

if __name__ == "__main__":
    app = MyApp(application_id="com.github.Narmis-E.DexViewer")
    app.run(sys.argv)