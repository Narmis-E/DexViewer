from pydexcom import Dexcom
import time
import sys
import configparser
import os
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')

if 'Credentials' in config:
		username = config['Credentials'].get('username', '')
		password = config['Credentials'].get('password', '')
		ous = config['Credentials'].get('ous', '')

if username is None or password is None:
	print("Credentials not found. Please set the DEXCOM_USER and DEXCOM_PASS environment variables.")

dexcom = Dexcom(username, password, ous) # add ous=True if outside of US

def get_glucose(time_scale):
	df = pd.DataFrame(columns=["BG", "TrendArrow"])
	bg = dexcom.get_glucose_readings(minutes=time_scale)
	for reading in bg:
		bg_value = reading.mmol_l  # Access the mmol_l attribute
		trend_arrow = reading.trend_arrow  # Access the trend_arrow attribute
		# Create a new DataFrame with the current data point
		new_data = pd.DataFrame({"BG": [bg_value], "TrendArrow": [trend_arrow]})
		df = pd.concat([df, new_data], ignore_index=True)
		df.to_csv("BG_data.csv", index=False)
