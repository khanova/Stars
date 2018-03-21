# Starry Sky
Version 1.2 

Author: Khanova Anna (khanovaanna1@gmail.com)


## Description
This application is a visualisation of the stars in current star data


## Dependencies
* Python version 3.4+
* PyQt5 (for visualisation)
* PIL (for screenshoting)

## Structure
* Module for data parsing 'parse.py'
* Module with global constants 'global_vars.py'
* Kernel of geometry is in module 'geometry.py'
* Controller is in module 'star.py'
* Visualisation form is module 'paint.py'
* Scroonshoting module 'screenshoot.py'
* Constellations data is in directory 'txt'

## Usage && Features
* Run: './main.py'
* You may write date and time in range [1.1.2000 00:00, 31.12.2099 23:59]
* You may write coordinates of observer in spherical coordinate system in ranges [0, 180] and [0, 360)
* Left mouse button click: select nearest constellation
* Right mouse button click: remove selection
* Left mouse button drag and drop: rotate camera
* Left mouse button drag and drop: rotate camera angle
* Key `P`: 'P'lay or 'P'ause of performance
* Arrow buttons: move the sky
* Scroll: zoom
* Stars are disappear and appear up to zoom and they apparent magnitude
* Stars have different colors up to they stellar classification
* Stars are pulsate during the time
* Application not broken because of precission error


Test coverage of strings is:

Name             Stmts   Miss  Cover
------------------------------------
geometry.py        120     19    84%
global_vars.py       9      0   100%
parse.py            59     23    61%
stars.py           134     36    73%
tests.py           138      0   100%
------------------------------------
TOTAL              460     78    83%
