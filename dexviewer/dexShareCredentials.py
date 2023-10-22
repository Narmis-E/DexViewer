import sys
import configparser
import gi
from pydexcom import Dexcom
from pydexcom import errors
import os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, Gio, GLib, GObject

class DexShareCredentials(Gtk.ApplicationWindow):
    credentials_provided_signal = GObject.Signal(flags=GObject.SignalFlags.RUN_FIRST, return_type=None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(350, 250)
        self.set_resizable(False)
        self.set_modal(True)
        self.set_title("Dexcom SHARE Credentials:")
        
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

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
        
        pass_toggle = Gtk.CheckButton(label="Show Password")
        pass_toggle.set_active(False)
        pass_toggle.connect("toggled", self.pass_toggled)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_spacing(10)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.CENTER)
        self.set_child(box)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.attach(self.username_entry, 0, 0, 3, 1)
        grid.attach(self.password_entry, 0, 1, 3, 1)
        grid.attach(ok_button, 0, 2, 1, 1)
        grid.attach(exit_button, 1, 2, 1, 1)
        grid.attach(self.ous_check, 2, 2, 1, 1)
        grid.attach(pass_toggle, 2, 3, 2, 1)
        box.append(grid)
    
    def pass_toggled(self, button):
        is_visible = button.get_active()
        self.password_entry.set_visibility(is_visible)

    def on_ok_clicked(self, button):
        self.username = self.username_entry.get_text()
        self.password = self.password_entry.get_text()
        self.ous = str(self.ous_check.get_active())
        if not self.username or not self.password:
            dialog = Gtk.AlertDialog()
            dialog.set_message("Invalid Credentials")
            dialog.set_detail("Credentials cannot be empty.")
            dialog.set_buttons(["OK"])
            dialog.show()
            return  # Return early to prevent further execution

        try:
            # Attempt to create a Dexcom session
            dexcom = Dexcom(self.username, self.password, self.ous)
        except errors.AccountError as e:
            if "Password not valid" in str(e):
                # Handle the incorrect password error
                dialog = Gtk.AlertDialog()
                dialog.set_message("Invalid Credentials")
                dialog.set_detail("The one or more of provided credentials are not valid.")
                dialog.set_buttons(["OK"])
                dialog.show()
            else:
                # Handle other AccountError cases
                dialog = Gtk.AlertDialog()
                dialog.set_message("Invalid Credentials")
                dialog.set_detail("Please check that your credentials are correct.")
                dialog.set_buttons(["OK"])
                dialog.show()
            return  # Return early if an error occurred

        self.save_credentials_to_config()

        # Emit the signal to indicate that credentials have been provided
        self.emit("credentials-provided-signal")
        self.destroy()

    def on_exit_clicked(self, button):
        self.destroy()
    
    def save_credentials_to_config(self):
        config = configparser.ConfigParser()
        config.read(os.path.expanduser("~/.local/share/dexviewer/config.ini"))
        if 'Details' not in config:
            config['Details'] = {}

        config['Details']['Username'] = self.username
        config['Details']['Password'] = self.password
        config['Details']['ous'] = self.ous
        if self.ous == 'True':
            config['Details']['units'] = 'mmol/l'
        else:
            config['Details']['units'] = 'mg/dl'
        with open(os.path.expanduser("~/.local/share/dexviewer/config.ini"), 'w') as configfile:
            config.write(configfile)
        return self.username, self.password, self.ous