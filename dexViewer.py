import sys
import configparser
import gi
import datetime as datetime
import os
import pandas
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, Gio, GLib

from utils import *
import dexShareCredentials
from dexcom import get_glucose
import bgPlotter

credentials_window = dexShareCredentials.DexShareCredentials()
plotter = bgPlotter.BgPlotter()

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_css()
        self.set_default_size(800, 400)
        self.set_title("DexViewer")
        self.connect("close-request", self.on_delete_event)
        self.load_credentials_from_config()

        # Create a header bar
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        self.add_share_source = Gtk.Button(label="Open")
        self.add_share_source.add_css_class('add_share_source')
        self.add_share_source.connect("clicked", self.on_add_share_source_clicked)
        self.add_share_source.set_icon_name("list-add")
        self.header.pack_start(self.add_share_source)
        
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.box1)
        self.box1.append(self.box2)  # Put vert box in that box
        self.box1.append(self.box3)  # And another one, empty for now
        
        self.time_scale_combo = Gtk.ComboBoxText()
        self.time_scale_combo.append("0", "1 Hour")
        self.time_scale_combo.append("1", "3 Hours")
        self.time_scale_combo.append("2","6 Hours")
        self.time_scale_combo.append("3","12 Hours")
        self.time_scale_combo.connect("changed", self.on_time_scale_changed)
        self.box3.append(self.time_scale_combo)
        self.time_scale_combo.set_active(1)

        self.box2.append(plotter.canvas)
        
        # Create a Gtk.Label to display the number
        self.number_label = Gtk.Label(label="5.5")
        self.number_label.set_hexpand(True)
        self.number_label.set_vexpand(True)
        self.number_label.set_justify(Gtk.Justification.CENTER)
        # Add the label to the box3 container
        self.box3.append(self.number_label)
        
        action = Gio.SimpleAction.new("sync_glucose", None)
        action.connect("activate", self.sync_glucose)
        self.add_action(action) 
        menu = Gio.Menu.new()
        menu.append("Sync Glucose", "win.sync_glucose")
        
        # Create a popover
        self.popover = Gtk.PopoverMenu()  # Create a new popover menu
        self.popover.set_menu_model(menu)

        # Create a menu button
        self.menu_button = Gtk.MenuButton()
        self.menu_button.set_popover(self.popover)
        self.menu_button.set_icon_name("open-menu-symbolic")  # Give it a nice icon
        self.menu_button.add_css_class('menu_button')

        # Add menu button to the header bar
        self.header.pack_end(self.menu_button)
        # Set app name
        GLib.set_application_name("DexViewer")

        # Create an action to run a *show about dialog* function we will create 
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.show_about)
        self.add_action(action)
        
        menu.append("About", "win.about")  # Add it to the menu we created in previous section

    def show_about(self, action, param):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)  # Makes the dialog always appear in from of the parent window
        self.about.set_modal(self)  # Makes the parent window unresponsive while dialog is showing

        self.about.set_authors(["Narmis-E\n\nNot possible without the pydexcom API from gagebenne!"])
        self.about.set_copyright("Copyright 2023 Narmis Ecurb")
        self.about.set_license_type(Gtk.License.GPL_3_0)
        self.about.set_website("http://github.com/Narmis-E/DexViewer")
        self.about.set_website_label("DexViewer Github")
        self.about.set_version("1.0.0")
        self.about.set_logo_icon_name("./Dexviewer_circle.png")  # The icon will need to be added to appropriate location
                                                # E.g. /usr/share/icons/hicolor/scalable/apps/org.example.example.svg

        self.about.set_visible(True)

    def on_delete_event(self, event):
        Gtk.Application.get_default().quit()

    def sync_glucose(self, action, param):
        active_text = self.time_scale_combo.get_active_text()
        if self.username is not None and self.password is not None:
            if active_text == "1 Hour":
                self.fetch_dexcom_data(1)
                plotter.set_time_scale(1)
            elif active_text == "3 Hours":
                self.fetch_dexcom_data(3)
                plotter.set_time_scale(3)
            elif active_text == "6 Hours":
                self.fetch_dexcom_data(6)
                plotter.set_time_scale(6)
            elif active_text == "12 Hours":
                self.fetch_dexcom_data(12)  
                plotter.set_time_scale(12)
                get_glucose(int(time_scale_hours)*60)
        print("Synchronised Blood Glucose")
        
    def on_add_share_source_clicked(self, button):
        credentials_window.present()
    
    def load_credentials_from_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        if 'Credentials' in config:
            self.username = config['Credentials'].get('username', '')
            self.password = config['Credentials'].get('password', '')
            self.ous = config['Credentials'].get('ous', 'False')  # Default to 'False' if not present
            print(f"Loaded credentials for {self.username}")

            if self.username and self.password:
                credentials_window.username_entry.set_text(self.username)
                credentials_window.password_entry.set_text(self.password)

            if self.ous == 'True':
                credentials_window.ous_check.set_active(True)
            else:
                credentials_window.ous_check.set_active(False)
    
    def fetch_dexcom_data(self, time_scale_hours):
        if self.username is not None and self.password is not None:
            # Call get_glucose with the specified time scale
            get_glucose(int(time_scale_hours)*60)
    
    def on_time_scale_changed(self, combo):
        # Get the selected time scale
        active_text = combo.get_active_text()

        # Update the plot based on the selected time scale
        if active_text == "1 Hour":
            self.fetch_dexcom_data(1)
            plotter.set_time_scale(1)
        elif active_text == "3 Hours":
            self.fetch_dexcom_data(3)
            plotter.set_time_scale(3)
        elif active_text == "6 Hours":
            self.fetch_dexcom_data(6)
            plotter.set_time_scale(6)
        elif active_text == "12 Hours":
            self.fetch_dexcom_data(12)  
            plotter.set_time_scale(12)

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

if __name__ == "__main__":
    app = MyApp(application_id="com.github.Narmis-E.DexViewer")
    app.run(sys.argv)