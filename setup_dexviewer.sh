#!/bin/bash
# Script to copy logo and .desktop file to correct path

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root to copy icon and .desktop file to /usr"
    exit 1
fi

svg=""
desktop=""

if svg_path=$(plocate --limit 1 dexviewer/data/icons/dexviewer.svg); then
    svg="$svg_path"
    echo "Found svg at $svg"
fi

if desktop_path=$(plocate --limit 1 dexviewer/data/dexviewer.desktop); then
    desktop="$desktop_path"
    echo "Found .desktop at $desktop"
fi

if [ -z "$svg" ] || [ -z "$desktop" ]; then
    echo "Could not locate dexviewer.png or dexviewer.desktop files. Make sure they are installed."
    exit 1
fi

cp "$svg" /usr/share/icons/hicolor/scalable/apps/
cp "$desktop" /usr/share/applications
echo "Copied logo and .desktop file. You can now use your GUI to run dexviewer."