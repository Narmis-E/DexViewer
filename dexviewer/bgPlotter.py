import gi
import os
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas

class BgPlotter(Gtk.Box):
    def __init__(self, units):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.current_time = datetime.now()
        self.time_scale_hours = 3
        self.load_data()
        self.units = units
        
        self.fig, self.ax = plt.subplots()
        self.ax.yaxis.tick_right()
        self.fig.subplots_adjust(left=0.039, top=0.97, right=0.95, bottom=0.08)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(600, 400)

        self.graph_decor()
        self.update_plot()
    
    def change_units(self, units):
        self.units = units  # Update the units
        self.update_plot()

    def set_time_scale(self, time_scale_hours):
        self.time_scale_hours = time_scale_hours
        self.update_plot()

    def update_plot(self):
        self.ax.clear()
        self.load_data()

        if self.time_scale_hours == 1:
            num_data_points = 12
            num_x_labels = 3
        elif self.time_scale_hours == 3:
            num_data_points = 36
            num_x_labels = 5
        elif self.time_scale_hours == 6:
            num_data_points = 72
            num_x_labels = 5
        elif self.time_scale_hours == 12:
            num_data_points = 144
            num_x_labels = 6

        now = datetime.now()
        time_passed = [(now - timedelta(minutes=i * 5)).strftime('%I:%M %p') for i in range(num_data_points)]
        bg_data = self.df['BG'].tail(num_data_points)

        # Reverse the time_passed and bg_data lists
        time_passed = time_passed[::-1]
        bg_data = bg_data[::-1]

        # Plot the BG data using the reversed time passed as x-axis
        self.scatter = self.ax.scatter(time_passed, bg_data, marker='o', zorder=2)
        step = max(1, len(time_passed) // num_x_labels)
        self.ax.set_xticks(time_passed[::step])
        self.ax.set_xticklabels(time_passed[::step])

        self.graph_decor()
        self.canvas.draw()

    def graph_decor(self):
        if self.units == 'mmol/l':
            self.low_bg_background = Rectangle((self.ax.get_xlim()[0], 0), self.ax.get_xlim()[1] - self.ax.get_xlim()[0], 4.2, fc='lightcoral', alpha=0.5)
            self.bg_background = Rectangle((self.ax.get_xlim()[0], 4.4), self.ax.get_xlim()[1] - self.ax.get_xlim()[0], 5.35, fc='lightgrey', alpha=0.5)
            self.high_bg_background = Rectangle((self.ax.get_xlim()[0], 10), self.ax.get_xlim()[1] - self.ax.get_xlim()[0], 16, fc='lightgoldenrodyellow', alpha=0.5)
            self.custom_yticks = [2, 6, 10, 14, 16]
        else:
            self.low_bg_background = Rectangle((self.ax.get_xlim()[0], 0), self.ax.get_xlim()[1] - self.ax.get_xlim()[0], 75, fc='lightcoral', alpha=0.5)
            self.bg_background = Rectangle((self.ax.get_xlim()[0], 79), self.ax.get_xlim()[1] - self.ax.get_xlim()[0], 95, fc='lightgrey', alpha=0.5)
            self.high_bg_background = Rectangle((self.ax.get_xlim()[0], 180), self.ax.get_xlim()[1] - self.ax.get_xlim()[0], 288, fc='lightgoldenrodyellow', alpha=0.5)
            self.custom_yticks = [36, 106, 180, 252, 288]
        self.ax.set_yticks(self.custom_yticks)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.add_patch(self.low_bg_background)
        self.ax.add_patch(self.high_bg_background)
        self.ax.add_patch(self.bg_background)

    def load_data(self):
        self.df = pd.read_csv(os.path.expanduser("~/.local/share/dexviewer/BG_data.csv"))