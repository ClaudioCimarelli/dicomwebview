@title[Introduction]
## DICOM Web Viewer
Server side:

- Python and Flask web server:
    - offering API to read DICOM images and label them
    - uses PyPNG and Numpy libraries to work with pixel arrays
 
Client side:

- Vue.js to create the frontend single-page application
    - easy to learn and allows to create modular apps using components

- Canvas representation of PNGs
    - so that is possible to use Javascript code to iteract with images  



---
@title[Server side]
## Flask API


+++

@title[Api code]


@[11-14]
