import sys
import subprocess
import configparser
from pydexcom import Dexcom
import gi
import os
import pandas as pd
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, Gio, GLib

from configHandler import *

def apply_css():
  css_provider = Gtk.CssProvider()
  css_provider.load_from_file(Gio.File.new_for_path('style.css'))
  Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def get_glucose(time_scale):
  username, password, ous = load_credentials()
  if username is None or password is None:
    print("Credentials not found. Please set the DEXCOM_USER and DEXCOM_PASS environment variables.")

  dexcom = Dexcom(username, password, ous) # add ous=True if outside of US
  df = pd.DataFrame(columns=["BG", "TrendArrow"])
  bg = dexcom.get_glucose_readings(minutes=time_scale)
  for reading in bg:
    bg_value = reading.mmol_l  # Access the mmol_l attribute
    trend_arrow = reading.trend_arrow  # Access the trend_arrow attribute
    # Create a new DataFrame with the current data point
    new_data = pd.DataFrame({"BG": [bg_value], "TrendArrow": [trend_arrow]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv("BG_data.csv", index=False)
    
    
    #TODO
    #test no csv