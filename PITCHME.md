
## DICOM Web Viewer

##### A Web application to view and label medical images online 

---
### Server side:

<br> 

- Python and Flask web server:
    - offering API to read DICOM images and label them
    - uses PyPNG and Numpy libraries to work with pixel arrays
    
+++?code=dicomwebview.py&lang=elixir&title=API declaration

@[48](Get a dicom image along one plane )

@[60](Get labeling image use for segmentation purposes)

@[71](Send labeling images to server memory, still not saved permanently)

@[106](Request to save labeling images on disk)

---
### Client side:

<br>

- Vue.js to create the frontend single-page application
    - easy to learn and allows to create modular apps using components

- Canvas representation of PNGs
    - so that is possible to use Javascript code to iteract with images  


---

