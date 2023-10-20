## About Version 1.0.3:
Fixed the setup script to correctly find the svg and .desktop file.
Dexviewer now correctly changes from the viewer to the home window.
Also implemented a action to the menu which deletes the config file 
and returns to the home window, allowing the user to switch accounts.

## About Version 1.0.2:
Fixed a mistake with the icon path for every icon in dexviewer.py. the 'about' section
and home window should now be correctly displayed. Also fixed the .desktop file so that
GNOME users can see it and pin it to their dash. This should work across all GNOME based
DEs. 

## About Version 1.0.1:
This is an initial release in the spirit of "release early, release often".\
Using version 1.0.1 because I had a skill issue with PyPI and now can't use 1.0.0.
Currently the interface can retrieve the past 1, 3, 6 and 12 hours of BG data.\
Dexviewer is currently limited for 1 user and has no option to change users 
on the fly, something planned for 1.1.x.\
Also planned for near future updates is functionality for live updating, as
currently Dexviewer only displays static timeframes with the exception of the sync glucose function.

<hr>

### Versioning explanation:
Dexviewer will take after the semantic versioning scheme proposed by https://semver.org, as I believe
it best reflects the changes made to Dexviewer with an x.y.z format 
(x = major change, y = minor change and z = bugfix). I doubt there will ever be a X.y.z change,
as Dexiewer will most likely not be written in another toolkit, nor will it likely be updated to future versions
of GTK. I expect there will be many x.Y.Z version changes however.

### DexViewer
This changelog documents the changes and updates to DexViewer, 
a GTK-4 interface for viewing Dexcom CGM data from the pydexcom API.

Avove, you'll find a list of versions and their respective changes, 
including new features, improvements, bug fixes, and any other 
significant modifications made to the application. 
Stay updated with the latest enhancements and bug resolutions in DexViewer through this changelog.

<hr>