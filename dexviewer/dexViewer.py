from pydexcom import Dexcom
import pandas as pd
import configparser
import sys
import gi
import os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, Gio, GLib, GdkPixbuf, Pango

import dexviewer.dexShareCredentials
import dexviewer.bgPlotter
from dexviewer.utils import *

credentials_window = dexviewer.dexShareCredentials.DexShareCredentials()
logo = get_logo()

class Viewer(Adw.Application):
    GLib.set_application_name("DexViewer")
    
    @staticmethod
    def switch_to_home_window():
        # Switch to the home window
        if Viewer.viewer_window:
            Viewer.viewer_window.destroy()
        Viewer.home_window = HomeWindow(application=Viewer.application)
        Viewer.home_window.present()
    
    @staticmethod
    def switch_to_viewer_window():
        # Switch to the viewer window
        if Viewer.home_window:
            Viewer.home_window.destroy()
        Viewer.viewer_window = MainWindow(application=Viewer.application)
        Viewer.viewer_window.present()
    
    def __init__(self, flag, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        Viewer.home_window = None
        Viewer.viewer_window = None
        Viewer.application = self  # Store the application instance
        self.current_window = None  # Initially, no window is shown
        self.flag = flag

    def on_activate(self, app):
        if self.current_window is None:
            if self.flag == 1:
                # Show the HomeWindow by default
                Viewer.switch_to_home_window()
            else:
                Viewer.switch_to_viewer_window()

def load_credentials():
    config_exists = os.path.isfile(os.path.expanduser("~/.local/share/dexviewer/config.ini"))
    if config_exists:
        config = configparser.ConfigParser()
        config.read(os.path.expanduser("~/.local/share/dexviewer/config.ini"))
        if 'Details' in config:
            global username, password, ous, units
            username = config['Details'].get('Username', '')
            password = config['Details'].get('Password', '')
            ous = config['Details'].get('ous', '')
            units = config['Details'].get('units', '')
            #print(f"Loaded credentials for {username}")
            return username, password, ous, units
    return None, None, None, None

def get_glucose(time_scale):
    ### Loading in the credentials here for the unit change. Will probably be fixed sometime if there are probelms with this method.
    username, password, ous, units = load_credentials()
    dexcom = Dexcom(username, password, ous)
    df = pd.DataFrame(columns=["BG", "TrendArrow"])
    bg = dexcom.get_glucose_readings(minutes=time_scale + 1)
    # Determine the expected number of data points based on time_scale
    expected_data_points = int(time_scale/5)
    if units == 'mmol/l':
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
        df.to_csv(os.path.expanduser("~/.local/share/dexviewer/BG_data.csv"), index=False)
    else:
        for i in range(expected_data_points):
            if i < len(bg):
                bg_value = bg[i].mg_dl
                trend_arrow = bg[i].trend_arrow
            else:
                # Set a placeholder value for offline data
                bg_value = ""
                trend_arrow = "?"
            # Create a new DataFrame with the current data point
            new_data = pd.DataFrame({"BG": [bg_value], "TrendArrow": [trend_arrow]})
            df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(os.path.expanduser("~/.local/share/dexviewer/BG_data.csv"), index=False)
        
    global latest_bg_mmol_l, latest_bg_mg_dl, latest_trend_arrow
    
    latest_bg = dexcom.get_latest_glucose_reading()
    latest_trend_arrow = latest_bg.trend_arrow
    latest_bg_mmol_l = latest_bg.mmol_l
    latest_bg_mg_dl = latest_bg.mg_dl
    
class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #username, password, ous, units = load_credentials()
        self.set_default_icon_name(logo)
        apply_css()
        self.set_default_size(800, 400)
        self.set_title("DexViewer | Viewer")
        self.connect("close-request", self.on_delete_event)
        get_glucose(180)

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        
        menu = Gio.Menu.new()
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        self.menu_button = Gtk.MenuButton()
        self.menu_button.set_popover(self.popover)
        self.menu_button.set_icon_name("open-menu-symbolic")
        self.menu_button.add_css_class('menu_button')
        self.header.pack_end(self.menu_button)        

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", show_about, self)
        self.add_action(action)
        menu.append("About", "win.about")
        
        preferences_action = Gio.SimpleAction.new("preferences", None)
        preferences_action.connect("activate", self.show_preferences)
        self.add_action(preferences_action)
        menu.append("Preferences", "win.preferences")
        
        action = Gio.SimpleAction.new("stop", None)
        action.connect("activate", self.stop_viewer)
        self.add_action(action)
        menu.append("Change Accounts", "win.stop")
        
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
        
        global plotter
        plotter = dexviewer.bgPlotter.BgPlotter(units)
        self.box2.append(plotter.canvas)

        self.grid = Gtk.Grid()
        self.box3.append(self.grid)
        
        self.time_scale_combo = Gtk.ComboBoxText()
        self.time_scale_combo.append("0", "1 Hour")
        self.time_scale_combo.append("1", "3 Hours")
        self.time_scale_combo.append("2","6 Hours")
        self.time_scale_combo.append("3","12 Hours")
        self.time_scale_combo.set_active(1)
        self.time_scale_combo.connect("changed", self.on_time_scale_changed)
        
        combo_box_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        combo_box_box.set_hexpand(False)
        combo_box_box.set_margin_bottom(8)
        combo_box_box.set_margin_start(8)
        combo_box_box.set_margin_end(8)

        combo_box_box.append(self.time_scale_combo)
        self.grid.attach(combo_box_box, 0, 4, 1, 1)
        
        self.trend_label = Gtk.Label(label=latest_trend_arrow)
        self.trend_label.set_hexpand(True)
        self.trend_label.set_vexpand(True)
        self.trend_label.set_justify(Gtk.Justification.CENTER)
        self.trend_label.set_valign(Gtk.Align.START)
        self.grid.attach(self.trend_label, 0, 3, 1, 1)
    
        self.bg_label = Gtk.Label()
        self.update_labels(units)
        self.bg_label.set_hexpand(True)
        self.bg_label.set_vexpand(True)
        self.bg_label.set_justify(Gtk.Justification.CENTER)
        self.bg_label.set_valign(Gtk.Align.END)
        self.grid.attach(self.bg_label, 0, 2, 1, 1)
    
    def show_preferences(self, action, param):
        preferences_window = PreferencesWindow(application=Viewer.application, main_window=self)
        preferences_window.present()
    
    def stop_viewer(self, action, param):
        config_exists = os.path.isfile(os.path.expanduser("~/.local/share/dexviewer/config.ini"))
        if config_exists:
            os.remove(os.path.expanduser("~/.local/share/dexviewer/config.ini"))
            print("config.ini removed")
        Viewer.switch_to_home_window()

    def update_labels(self, units):
        if units == 'mmol/l':
            self.bg_label.set_markup(f'<span size="xx-large" weight="bold">{latest_bg_mmol_l}</span>')
        else:
            self.bg_label.set_markup(f'<span size="xx-large" weight="bold">{latest_bg_mg_dl}</span>')
        self.trend_label.set_markup(f'<span size="xx-large" weight="bold">{latest_trend_arrow}</span>')

    def on_delete_event(self, event):
        Gtk.Application.get_default().quit()

    def sync_glucose(self, button):
        active_text = self.time_scale_combo.get_active_text()
        if username is not None and password is not None:
            if active_text == "1 Hour":
                get_glucose(60)
                plotter.set_time_scale(1)
            elif active_text == "3 Hours":
                get_glucose(180)
                plotter.set_time_scale(3)
            elif active_text == "6 Hours":
                get_glucose(360)
                plotter.set_time_scale(6)
            elif active_text == "12 Hours":
                get_glucose(720)
                plotter.set_time_scale(12)
        self.update_labels(units)
        print("Synchronised Blood Glucose")
        
    def on_add_share_source_clicked(self, button):
        self.show_credentials()
        credentials_window.present()
    
    def on_time_scale_changed(self, combo):
        active_text = combo.get_active_text()

        # Update the plot based on the selected time scale
        if active_text == "1 Hour":
            get_glucose(60)
            plotter.set_time_scale(1)
        elif active_text == "3 Hours":
            get_glucose(180)
            plotter.set_time_scale(3)
        elif active_text == "6 Hours":
            get_glucose(360)
            plotter.set_time_scale(6)
        elif active_text == "12 Hours":
            get_glucose(720)
            plotter.set_time_scale(12)

class HomeWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        directory = os.path.expanduser("~/.local/share/dexviewer/")
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.set_default_icon_name(logo)
        apply_css()
        self.set_default_size(800, 400)
        self.set_title("DexViewer | Home")
        self.connect("close-request", self.on_delete_event)
        
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        
        menu = Gio.Menu.new()
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        self.menu_button = Gtk.MenuButton()
        self.menu_button.set_popover(self.popover)
        self.menu_button.set_icon_name("open-menu-symbolic")
        self.menu_button.add_css_class('menu_button')

        self.header.pack_end(self.menu_button)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", show_about, self)
        self.add_action(action)
        menu.append("About", "win.about")
        
        self.add_share_source = Gtk.Button(label="Open")
        self.add_share_source.add_css_class('add_share_source')
        self.add_share_source.connect("clicked", self.on_add_share_source_clicked)
        self.add_share_source.set_icon_name("list-add")
        self.header.pack_start(self.add_share_source)
        
        self.grid = Gtk.Grid()
        self.set_child(self.grid)
        self.grid.set_hexpand(True)
        self.grid.set_vexpand(True)
        self.grid.set_margin_start(20)
        self.grid.set_margin_end(20)
        self.grid.set_margin_top(20)
        self.grid.set_margin_bottom(20)
        
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_valign(Gtk.Align.CENTER)

        self.image = Gtk.Image()
        self.image.set_from_file(logo)
        self.image.set_size_request(128, 128)
        self.title_label = Gtk.Label(label="DexViewer v1.1.0")
        self.title_label.set_hexpand(True)
        self.title_label.set_justify(Gtk.Justification.CENTER)

        self.grid.attach(self.image, 0, 0, 1, 1)
        self.grid.attach(self.title_label, 0, 1, 1, 1)
    
    def show_credentials(self):
        if username and password:
            credentials_window.username_entry.set_text(username)
            credentials_window.password_entry.set_text(password)
        if ous == 'True':
            credentials_window.ous_check.set_active(True)
        else:
            credentials_window.ous_check.set_active(False)

    def on_credentials_provided(self, widget, data=None):
        credentials_window.destroy()
        self.hide()
        Viewer.switch_to_viewer_window()

    def on_delete_event(self, event):
        Gtk.Application.get_default().quit()

    def on_add_share_source_clicked(self, button):
        credentials_window = dexviewer.dexShareCredentials.DexShareCredentials()
        # Present the credentials window to get user input
        credentials_window.connect(credentials_window.credentials_provided_signal, self.on_credentials_provided)
        credentials_window.present()

class PreferencesWindow(Gtk.Window):
    def __init__(self, application, main_window):
        super().__init__(title="Preferences", application=application)
        self.set_default_size(400, 200)
        self.set_modal(True)
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        self.connect("close-request", self.on_delete_event)
        self.main_window = main_window

        self.box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.box1)

        # Unit Selection Combo Button
        self.unit_combo = Gtk.ComboBoxText()
        self.unit_combo.append("0", "mmol/l")
        self.unit_combo.append("1", "mg/dl")
        if units == 'mmol/l':
            self.unit_combo.set_active(0)
        else:
            self.unit_combo.set_active(1)
        self.unit_combo.connect("changed", self.on_unit_changed)

        self.unit_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.unit_box.set_vexpand(True)
        self.unit_box.set_halign(Gtk.Align.CENTER)
        self.unit_box.set_valign(Gtk.Align.CENTER)

        self.label = Gtk.Label(label="Blood Glucose Unit")
        self.unit_box.append(self.label)
        self.unit_box.set_spacing(5)

        self.unit_box.append(self.unit_combo)
        self.box1.append(self.unit_box)
    
    def on_delete_event(self, event):
        self.main_window.update_labels(units)
        return False

    def on_unit_changed(self, combo):
        unit = combo.get_active_text()
        config = configparser.ConfigParser()
        config.read(os.path.expanduser("~/.local/share/dexviewer/config.ini"))
        if unit == "mmol/l":
            config['Details']['units'] = 'mmol/l'
            with open(os.path.expanduser("~/.local/share/dexviewer/config.ini"), 'w') as configfile:
                config.write(configfile)
            get_glucose(180)
            plotter.change_units('mmol/l')
            print('units changed to mmol/l')
        else:
            config['Details']['units'] = 'mg/dl'
            with open(os.path.expanduser("~/.local/share/dexviewer/config.ini"), 'w') as configfile:
                config.write(configfile)
            get_glucose(180)
            plotter.change_units('mg/dl')
            print('units changed to mg/dl')

def main(flag):
    app = Viewer(application_id="com.github.Narmis-E.DexViewer", flag=flag)
    app.run(sys.argv)