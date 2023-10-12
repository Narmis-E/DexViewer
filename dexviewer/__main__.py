import os
import sys
import dexviewer.dexViewer

config = os.path.isfile(os.path.expanduser("~/.local/share/dexviewer/config.ini"))
bg_data = os.path.isfile(os.path.expanduser("~/.local/share/dexviewer/BG_data.csv"))

if not config:
    flag = 1
else:
    flag = 0

def main():
    dexviewer.dexViewer.main(flag)

if __name__ == '__main__':
    main()
    