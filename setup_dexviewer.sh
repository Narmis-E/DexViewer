#!/bin/bash
# Script to copy logo and .desktop file to correct path

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root to copy icon and .desktop file to /usr"
    exit 1
fi

# Search for svg and .desktop files in the user's home directory
svg_path=$(find "/home/`sh -c 'echo $SUDO_USER'`/.local/lib" -name "dexviewer.svg" | head -n 1)
desktop_path=$(find "/home/`sh -c 'echo $SUDO_USER'`/.local/lib" -name "dexviewer.desktop" | head -n 1)

if [ -z "$svg_path" ] || [ -z "$desktop_path" ]; then
    echo "Could not locate dexviewer.svg or dexviewer.desktop files in the user's home directory."
    exit 1
fi

cp "$svg_path" /usr/share/icons/hicolor/scalable/apps/
cp "$desktop_path" /usr/share/applications
echo "Copied logo and .desktop file. You can now use your GUI to run dexviewer."