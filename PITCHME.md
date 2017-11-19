
## DICOM Web Viewer

##### A Web application to view and label medical images online 

---
### Backend:

<br> 

- Python and Flask web server:
    - offering API to read DICOM images and label them
    - uses PyPNG and Numpy libraries to work with pixel arrays
    
+++?code=dicomwebview.py&lang=elixir&title=Server side code snippets

@[48-56](API: Get a DICOM image along a plane )

@[140](Method to convert a pixel array to PNG)
@[141](Take selected slice using plane dimension and slice number given)
@[156](Trasform ndarray of pixel data into PNG image using PyPNG)

@[59-67](API: Get labeling image use for segmentation purposes)

@[70-71](API: Post labeling images to server memory , still not saved permanently)
@[77-79](Decode PNG from Base64 string to binary readable by PyPNG)

@[105-106](API: Post request to save labeling images on disk)

---
### Frontend:
<br>
- Vue.js to build the single-page application
    - easy to learn and allows to create modular apps using **components**  

- Canvas representation of PNGs
    - so that is possible to use Javascript code to interact with images  

+++?code=templates/index.html&lang=elixir&title=Vue js application code

@[720, 14-17](Root della applicazione contenente dati della sessione utente)

@[691, 19-31](Contenitore principale per la visualizzazione del file DICOM)

@[450](Component that manage a single plane visualization)

@[221](Component to draw on the images. Five of them are overlaid on each plane to allow different zooming level for drawing)

@[162](Component for selecting different color to label images)