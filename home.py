import configparser
import sys
import gi
import os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, Gio, GLib, GdkPixbuf

import dexShareCredentials
import dexViewer

credentials_window = dexShareCredentials.DexShareCredentials()
    
class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_css()
        self.set_default_size(800, 400)
        self.set_title("DexViewer")
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
        GLib.set_application_name("DexViewer")

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.show_about)
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
        self.image.set_from_file("Dexviewer.png")
        self.image.set_size_request(128, 128)
        self.title_label = Gtk.Label(label="DexViewer v1.0.0")
        self.title_label.set_hexpand(True)
        self.title_label.set_justify(Gtk.Justification.CENTER)

        self.grid.attach(self.image, 0, 0, 1, 1)
        self.grid.attach(self.title_label, 0, 1, 1, 1)

    def show_about(self, action, param):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)
        self.about.set_modal(self)

        self.about.set_authors(["Narmis-E\n\nNot possible without the pydexcom API from gagebenne!"])
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
        
    def on_add_share_source_clicked(self, button):
        credentials_window.present()
    
    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_file(Gio.File.new_for_path('style.css'))
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

class Home(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()