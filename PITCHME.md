@title[Introduction]
## DICOM Web Viewer
Server side:

- Python and Flask web server:
    - offering API to read DICOM images and label them
    - uses PyPNG and Numpy libraries to work with pixel arrays
    
+++

@title[Server side code]
## Flask API


+++?code=dicomwebview.py&lang=pyhton
@[41, 48, 60, 71,106]


---

Client side:

- Vue.js to create the frontend single-page application
    - easy to learn and allows to create modular apps using components

- Canvas representation of PNGs
    - so that is possible to use Javascript code to iteract with images  


---

