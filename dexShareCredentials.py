import sys
import subprocess
import configparser
import gi
import os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, Gio, GLib

from utils import *

class DexShareCredentials(Gtk.Window):
    def __init__(self, get_glucose_func, load_credentials_func):
        super().__init__(title="Dexcom Share Credentials")
        self.get_glucose = get_glucose_func
        self.load_credentials = load_credentials_func
        self.set_default_size(250, 150)
        self.set_resizeable = False
        self.set_modal(True)  # Make it a modal window

        # Create username and password Entry widgets
        self.username_entry = Gtk.Entry()
        self.username_entry.set_placeholder_text("Username")
        self.password_entry = Gtk.Entry()
        self.password_entry.set_placeholder_text("Password")
        self.password_entry.set_visibility(False)  # Hide password characters

        # Create OK and Exit buttons
        ok_button = Gtk.Button(label="Ok")
        exit_button = Gtk.Button(label="Cancel")

        # Connect button signals
        ok_button.connect("clicked", self.on_ok_clicked)
        exit_button.connect("clicked", self.on_exit_clicked)
        
        # Create OUS switch
        self.ous_check = Gtk.CheckButton(label="Outside US")
        self.ous_check.set_active(False)  # By default, set it to False (inside US)

        # Create a layout container for widgets
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
        config_exists = os.path.isfile('config.ini')
        if config_exists:
            self.username, self.password, self.ous = self.load_credentials()
        self.username = self.username_entry.get_text()
        self.password = self.password_entry.get_text()
        self.ous = str(self.ous_check.get_active())  # Get the state of the OUS checkbox

        self.save_credentials_to_config()

        # Close the window
        self.destroy()
        self.get_glucose(3*60)

    def on_exit_clicked(self, button):
        # Close the window without taking any action
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
        