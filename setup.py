from setuptools import setup, find_packages

setup(
    name="dexviewer",
    version="1.0.0",
    description="A GTK-4 interface for viewing Dexcom CGM data from the pydexcom APIs",
    author="Narmis-E",
    author_email="narmisecurb@gmail.com",
    url="https://github.com/narmis-e/DexViewer",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      "PyGObject",
      "pandas",
      "pydexcom",
      "matplotlib",
    ],
    entry_points={
      'console_scripts': [
        'dexviewer = dexviewer.__main__:main',
      ],
    },
    classifiers=[
      "Intended Audience :: End Users/Desktop",
      "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      "Operating System :: POSIX :: Linux",
      "Programming Language :: Python :: 3",
      "Topic :: Desktop Environment",
      "Topic :: Utilities",
    ],
    scripts=['setup_dexviewer.sh'],
    license="GPLv3",
)
