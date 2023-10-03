import sys
import subprocess
import gi
import os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, Gio, GLib

def apply_css():
  css_provider = Gtk.CssProvider()
  css_provider.load_from_file(Gio.File.new_for_path('style.css'))
  Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)