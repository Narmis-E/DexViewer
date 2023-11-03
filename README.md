<img src="dexviewer/data/icons/dexviewer.svg" align="right" width="186"/>

# DexViewer [![Please do not theme this app](https://stopthemingmy.app/badge.svg)](https://stopthemingmy.app)

> A GTK-4 application for viewing Dexcom CGM data from the pydexcom API.

<hr width=0>

## Features:
DexViewer is an application that allows you to visualise and track your blood glucose data from your Dexcom continuous glucose monitoring (CGM) device. Here are some of the key features:

#### Periodic Glucose Monitoring (real-time is WIP)
DexViewer provides periodic glucose data directly from your Dexcom CGM device, helping you stay informed about your current blood glucose levels and trends.

#### Data Visualisation
- View your blood glucose data with a user-friendly interface (alike the Dexcom app).
- Analyse trends in your glucose levels over various time scales (1 hour, 3 hours, 6 hours, 12 hours)

#### Configurable Credentials
- Stores your Dexcom credentials for seamless access to your blood glucose data.

<div align="center">
  <br>
  <img src="https://github.com/Narmis-E/DexViewer/assets/109248529/fc111824-c016-445e-95ad-e0e65b05f923"/>
  <p>Here is a screenshot of the Viewer Window.</p>
  <br>
</div>

## Installing DexViewer
You can install DexViewer by simply installing the PyPI package:
```
pip install dexviewer
```
and run it from the terminal:
```
dexviewer
```
See the pip page here: https://pypi.org/project/dexviewer/

#### If you wish to install from source, please clone this respository:
```
git clone https://github.com/Narmis-E/DexViewer/ && cd DexViewer
```
then pip install in the current directory:
```
pip install .
```
#### Note:
If you want to run Dexviewer from a GUI (GNOME app menu, rofi, etc) run the `setup_dexviewer.sh` script which is provided in your local $PATH on install:

```
sudo setup_dexviewer.py
```
*sudo needed to copy .desktop and icon to /usr/share/*


## Compatibility
As far as I am aware, DexViewer should be able to provide data through the pydexcom api for sensors which have the Dexcom Share functionality, which are the G4, G5, G6 (as listed on the [pydexcom github](https://github.com/gagebenne/pydexcom)) and G7 ([maybe?](https://github.com/gagebenne/pydexcom/issues/55)). 
Currently I only have access to a G6 sensor so I cannot confirm functionality for the other sensors.

If you want to learn more about the pydexcom api, please read through the informative documentation provided by gagebene [here](https://gagebenne.github.io/pydexcom/pydexcom.html).

## Acknowledgment
Special thanks to:
- [gagebene](https://github.com/gagebenne) for creating the [pydexcom api](https://github.com/gagebenne/pydexcom)
- [Taiko2k](https://github.com/Taiko2k) for creating their [Python GTK4 tutorial](https://github.com/Taiko2k/GTK4PythonTutorial)


DexViewer is licensed under GPLv3, allowing the wider community to contribute and improve the application.
Feel free to contribute, report issues, or provide feedback to help make DexViewer even better.

## Theming...
Just as an FYI, I'm not trying to act like a *you know who* dev and preach 10 billion reasons as to why you shouldn't use GTK themes. 
I am an avid desktop ricer and have/do use countless themes, especially as I want a cohesive desktop experience.
But for the sake of making sure you have a positive experience with DexViewer, 
I highly suggest that you do not use a **GTK4** theme for your desktop while using DexViewer (**GTK3 themes are fine**). 
I cannot guarrantee the application will look or even function the same from desktop to desktop because of this, especially being a programming noob.

I realise that for most users, this probably wont be a problem as they may not have a gtk4 theme set in `~/.config/gtk-4.0`, 
but I will still fly the 'pls dont theme' badge to let people know it will and does effect the look of the program 
(embedding a matplotlib canvas with a white background does not mix well with many GTK themes!).  

## TODO
- [x] Implement unit swicthing between mmol/l and mg/dl
- [x] Light and dark mode toggle in preferences window
- [x] Decrease data load times?
- [x] Implement account switching
- [ ] Implement real time data
- [ ] Package for flatpak
- [ ] NightScout integration?
- [ ] Interactive graphs (may need to switch graphing lib)

#### Disclaimer
DexViewer currently stores your Dexcom SHARE password in plaintext inside the config.ini file, which I understand is something which is perhaps the epitome of bad security, but I don't plan on changing this unless I really need to (I know I could use some hashing library and then retrieve it when needed).
