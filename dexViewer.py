from pydexcom import Dexcom
import pandas as pd
import configparser
import sys
import gi
import os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, Gio, GLib, GdkPixbuf

import dexShareCredentials
import bgPlotter

def load_credentials():
    config_exists = os.path.isfile('config.ini')
    if config_exists:
        config = configparser.ConfigParser()
        config.read('config.ini')
        if 'Credentials' in config:
            global username, password, ous
            username = config['Credentials'].get('Username', '')
            password = config['Credentials'].get('Password', '')
            ous = config['Credentials'].get('ous', '')
            print(f"Loaded credentials for {username}")
            return username, password, ous
    return None, None, None

def get_glucose(time_scale):
    dexcom = Dexcom(username, password, ous)
    df = pd.DataFrame(columns=["BG", "TrendArrow"])
    bg = dexcom.get_glucose_readings(minutes=time_scale + 1)

    # Determine the expected number of data points based on time_scale
    expected_data_points = int(time_scale/5)

    for i in range(expected_data_points):
        if i < len(bg):
            bg_value = bg[i].mmol_l
            trend_arrow = bg[i].trend_arrow
        else:
            # Set a placeholder value for offline data
            bg_value = ""
            trend_arrow = "?"

        # Create a new DataFrame with the current data point
        new_data = pd.DataFrame({"BG": [bg_value], "TrendArrow": [trend_arrow]})
        df = pd.concat([df, new_data], ignore_index=True)

    df.to_csv("BG_data.csv", index=False)
    
class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_css()
        self.set_default_size(800, 400)
        self.set_title("DexViewer")
        self.connect("close-request", self.on_delete_event)
        username, password, ous = load_credentials()
        get_glucose(3*60)

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        
        menu = Gio.Menu.new()
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        # Create a menu button
        self.menu_button = Gtk.MenuButton()
        self.menu_button.set_popover(self.popover)
        self.menu_button.set_icon_name("open-menu-symbolic")
        self.menu_button.add_css_class('menu_button')
        self.header.pack_end(self.menu_button)
        
        GLib.set_application_name("DexViewer")

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.show_about)
        self.add_action(action)
        menu.append("About", "win.about")
        
        self.add_share_source = Gtk.Button(label="Sync")
        self.add_share_source.add_css_class('sync_glucose')
        self.add_share_source.connect("clicked", self.sync_glucose)
        self.add_share_source.set_icon_name("view-refresh-symbolic")
        self.header.pack_start(self.add_share_source)
        
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.box1)
        self.box1.append(self.box2)
        self.box1.append(self.box3)
        
        self.time_scale_combo = Gtk.ComboBoxText()
        self.time_scale_combo.append("0", "1 Hour")
        self.time_scale_combo.append("1", "3 Hours")
        self.time_scale_combo.append("2","6 Hours")
        self.time_scale_combo.append("3","12 Hours")
        self.time_scale_combo.set_active(1)
        self.time_scale_combo.connect("changed", self.on_time_scale_changed)
        self.box3.append(self.time_scale_combo)
        
        self.plotter = bgPlotter.BgPlotter()
        self.box2.append(self.plotter.canvas)

        self.number_label = Gtk.Label(label="5.5")
        self.number_label.set_hexpand(True)
        self.number_label.set_vexpand(True)
        self.number_label.set_justify(Gtk.Justification.CENTER)
        self.box3.append(self.number_label)

    def show_about(self, action, param):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)
        self.about.set_modal(self)

        self.about.set_authors(["Narmis-E - Not possible without the pydexcom API from gagebenne!"])
        self.about.set_copyright("Copyright 2023 Narmis Ecurb")
        self.about.set_license_type(Gtk.License.GPL_3_0)
        self.about.set_website("http://github.com/Narmis-E/DexViewer")
        self.about.set_website_label("DexViewer Github")
        self.about.set_version("1.0.0")
        logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file("./Dexviewer.png")
        texture = Gdk.Texture.new_for_pixbuf(logo_pixbuf)
        self.about.set_logo(texture)

        self.about.set_visible(True)
    
    def show_credentials(self):
        if username and password:
            credentials_window.username_entry.set_text(username)
            credentials_window.password_entry.set_text(password)
        if ous == 'True':
            credentials_window.ous_check.set_active(True)
        else:
            credentials_window.ous_check.set_active(False)

    def on_delete_event(self, event):
        Gtk.Application.get_default().quit()

    def sync_glucose(self, button):
        active_text = self.time_scale_combo.get_active_text()
        if username is not None and password is not None:
            if active_text == "1 Hour":
                get_glucose(1*60)
                self.plotter.set_time_scale(1)
            elif active_text == "3 Hours":
                get_glucose(3*60)
                self.plotter.set_time_scale(3)
            elif active_text == "6 Hours":
                get_glucose(6*60)
                self.plotter.set_time_scale(6)
            elif active_text == "12 Hours":
                get_glucose(12*60)
                self.plotter.set_time_scale(12)
        print("Synchronised Blood Glucose")
        
    def on_add_share_source_clicked(self, button):
        self.show_credentials()
        credentials_window.present()
    
    def on_time_scale_changed(self, combo):
        active_text = combo.get_active_text()

        # Update the plot based on the selected time scale
        if active_text == "1 Hour":
            get_glucose(1*60)
            self.plotter.set_time_scale(1)
        elif active_text == "3 Hours":
            get_glucose(3*60)
            self.plotter.set_time_scale(3)
        elif active_text == "6 Hours":
            get_glucose(6*60)
            self.plotter.set_time_scale(6)
        elif active_text == "12 Hours":
            get_glucose(12*60)
            self.plotter.set_time_scale(12)
    
    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_file(Gio.File.new_for_path('style.css'))
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

class Viewer(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()