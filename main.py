import os
import sys
from home import Home
from dexViewer import Viewer

config = os.path.isfile("config.ini")
bg_data = os.path.isfile("BG_data.csv")

if not config:
    print("Config file not found, showing home window")
    app = Home(application_id="com.github.Narmis-E.DexViewer")
    app.run(sys.argv)

elif not bg_data and config:
    print("CSV data file not found, loading credentials")
    app = Viewer(application_id="com.github.Narmis-E.DexViewer")
    app.run(sys.argv)

else:
    print("Files found, Running Viewer")
    app = Viewer(application_id="com.github.Narmis-E.DexViewer")
    app.run(sys.argv)