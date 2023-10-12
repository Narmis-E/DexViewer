#!/bin/bash
# Script to copy logo and .desktop file to correct path
if [ "$EUID" -ne 0 ]
  then echo "Please run as root to copy icon and .desktop file to /usr"
  exit
else
  cp ./dexviewer.svg /usr/share/icons/hicolor/scalable/apps/
  cp ./dexviewer.desktop /usr/share/applications
fi
echo "Copied logo and .desktop file. You can now use your GUI to run dexviewer"