import pkg_resources
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

def apply_css():
    css_path = 'data/styles/style.css'
    css_provider = Gtk.CssProvider()
    try:
        resource_stream = pkg_resources.resource_stream('dexviewer', css_path)
        css_provider.load_from_data(resource_stream.read())
    except FileNotFoundError as e:
        print(f"Error loading CSS: {e}")
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)