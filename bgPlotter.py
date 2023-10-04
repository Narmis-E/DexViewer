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
    def __init__(self):
      super().__init__(orientation=Gtk.Orientation.HORIZONTAL)

      self.current_time = datetime.now()
      self.time_scale_hours = 3
      self.df = None
      
      # Create a Matplotlib Figure and Axes for the plot
      self.fig, self.ax = plt.subplots()
      self.ax.yaxis.tick_right()
      self.fig.subplots_adjust(left=0.03, top=0.97, right=0.95, bottom=0.08)  # Adjust the top parameter to reduce space at the top
      # Create a DrawingArea for Matplotlib plot
      self.canvas = FigureCanvas(self.fig)
      self.canvas.set_size_request(600, 400)  # Set the size of the canvas
      self.custom_yticks = [2, 6, 10, 14, 16]
      self.ax.set_yticks(self.custom_yticks)

      self.ax.spines['left'].set_visible(False)
      self.ax.spines['right'].set_visible(False)
      self.ax.spines['top'].set_visible(False)
      self.ax.spines['bottom'].set_visible(False)

      self.create_background_rectangles()
      self.load_csv_data()

    def set_time_scale(self, time_scale_hours):
      self.time_scale_hours = time_scale_hours
      self.update_plot()
        
    def update_plot(self):
      if self.df is None:
        return
      
      # Clear the existing plot
      self.ax.clear()
      
      self.load_csv_data()
      
      if self.time_scale_hours == 1:
        num_data_points = 12
        num_x_labels = 5  # Show 5 x-axis labels for 1-hour scale
      elif self.time_scale_hours == 3:
          num_data_points = 12 * 3
          num_x_labels = 5  # Show 5 x-axis labels for 3-hour scale
      elif self.time_scale_hours == 6:
          num_data_points = 12 * 6
          num_x_labels = 5  # Show 5 x-axis labels for 6-hour scale
      elif self.time_scale_hours == 12:
          num_data_points = 140
          num_x_labels = 6

      # Calculate time passed in minutes for the x-axis
      now = datetime.now()
      time_passed = [(now - timedelta(minutes=i * 5)).strftime('%I:%M %p') for i in range(num_data_points)]

      # Reverse the list to display the time in ascending order
      time_passed = time_passed[::-1]

      # Get the corresponding BG data for the selected time scale
      bg_data = self.df['BG'].tail(num_data_points)

      # Reverse the BG data to invert the plotting
      bg_data = bg_data[::-1]

      for i in range(len(time_passed)):
        if i == len(time_passed) - 1:
          # Set the most recent point as white with a black outline
          self.ax.scatter(time_passed[i], bg_data.iloc[i], marker='o', zorder=2, color='white', edgecolors='black')
        else:
          # Set other points as black
          self.ax.scatter(time_passed[i], bg_data.iloc[i], marker='o', zorder=2, color='black')
            
      # Customize x-axis labels and rotation for better readability
      step = max(1, len(time_passed) // num_x_labels)
      self.ax.set_xticks(time_passed[::step])
      self.ax.set_xticklabels(time_passed[::step])
      
      self.custom_yticks = [2, 6, 10, 14, 16]
      self.ax.set_yticks(self.custom_yticks)

      self.ax.spines['left'].set_visible(False)
      self.ax.spines['right'].set_visible(False)
      self.ax.spines['top'].set_visible(False)
      self.ax.spines['bottom'].set_visible(False)

      self.create_background_rectangles()
      
      # Update the canvas
      self.canvas.draw()
      
    def create_background_rectangles(self):
      # Create a Rectangle patch for the background
      self.low_bg_background = Rectangle((self.ax.get_xlim()[0], 0), self.ax.get_xlim()[1] - self.ax.get_xlim()[0], 4.2, fc='lightcoral', alpha=0.5)
      self.bg_background = Rectangle((self.ax.get_xlim()[0], 4.4), self.ax.get_xlim()[1] - self.ax.get_xlim()[0], 5.35, fc='lightgrey', alpha=0.5)
      self.high_bg_background = Rectangle((self.ax.get_xlim()[0], 10), self.ax.get_xlim()[1] - self.ax.get_xlim()[0], 16, fc='lightgoldenrodyellow', alpha=0.5)
      self.ax.add_patch(self.low_bg_background)
      self.ax.add_patch(self.high_bg_background)
      self.ax.add_patch(self.bg_background)
      
    def load_csv_data(self):
      self.df = pd.read_csv("BG_data.csv")