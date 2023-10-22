import pkg_resources
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

def get_logo():
    logo_path = 'data/icons/dexviewer.png'
    try:
        resource_stream = pkg_resources.resource_stream('dexviewer', logo_path)
    except FileNotFoundError as e:
        print(f"{e}: Cannot find dexviewer.png")
    return str(resource_stream.name)

def apply_css():
    css_path = 'data/styles/style.css'
    css_provider = Gtk.CssProvider()
    try:
        resource_stream = pkg_resources.resource_stream('dexviewer', css_path)
        css_provider.load_from_data(resource_stream.read())
    except FileNotFoundError as e:
        print(f"{e}: Cannot find style.css")
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def show_about(action, param, window):
    about = Gtk.AboutDialog()
    about.set_transient_for(window)
    about.set_modal(window)

    about.set_authors(["Narmis-E - Not possible without the pydexcom API from gagebenne!"])
    about.set_copyright("Copyright 2023 Narmis Ecurb")
    about.set_license_type(Gtk.License.GPL_3_0)
    about.set_website("http://github.com/Narmis-E/DexViewer")
    about.set_website_label("DexViewer Github")
    about.set_version("1.2.0")
    logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file(get_logo())
    texture = Gdk.Texture.new_for_pixbuf(logo_pixbuf)
    about.set_logo(texture)
    about.set_visible(True)