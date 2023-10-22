## About Version 1.2.0:
Wanted to push out this version as quickly as I could after noticing a silly issue I left in from testing which broke the credentials window with the dialog. This version also reduces the program launch time, and is something I am very much prioritising. This also integrates a dark mode toggle in the preferences window.
Hopefully future versions will provide even quicker launch times, however the next thing I wish to implement is live data retrieval (maybe using a cron job or some other alternative?).

## About Version 1.1.0:
This version adds the ability to hotswitch blood glucose units for countries which use
mg/dl (previously mmol/l was the only unit.) The units can now be toggled in the preferences
window, accessible from the menu. This version also introduces error handling for 
Dexcom SHARE credentials, along with a show password toggle. New features which would require
a new window can now probably move to this preferences window (e.g a dark mode toggle).

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
I understand how applications should start at 0.1.0, being the first implementation, but as this application
is fairly small in scope and functionality, I think it wont be necessary.

### DexViewer
This changelog documents the changes and updates to DexViewer, 
a GTK-4 interface for viewing Dexcom CGM data from the pydexcom API.

Avove, you'll find a list of versions and their respective changes, 
including new features, improvements, bug fixes, and any other 
significant modifications made to the application. 
Stay updated with the latest enhancements and bug resolutions in DexViewer through this changelog.

<hr>