
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

@[59](Get labeling image use for segmentation purposes)

@[70](Send labeling images to server memory , still not saved permanently)

@[105](Request to save labeling images on disk)

+++?code=dicomwebview.py&lang=elixir&title=Convert pixel array to PNG

@[140-159]

@[141](Take selected slice using plane dimension and slice number given)
@[156](Trasform ndarray of pixel data into PNG image using PyPNG)

---
### Client side:
<br>
- Vue.js to create the frontend single-page application
    - easy to learn and allows to create modular apps using **components**  

- Canvas representation of PNGs
    - so that is possible to use Javascript code to interact with images  

+++?code=templates/index.html&lang=javascript&title=Vue components

@[720](Root della applicazione contenente dati della sessione utente)

@[691](Contenitore principale per la visualizzazione del file DICOM)

@[450](Component that manage a single plane visualization)

@[221](Component to draw on the images. Five of them are overlaid on each plane to allow different zooming level for drawing)

@[162](Component for selecting different color to label images)