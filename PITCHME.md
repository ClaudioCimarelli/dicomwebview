
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
@[86-87](create ndarry of pixel from binary data iterator)
@[90, 95](modify opacity to 0.5 for all colored pixels and put it in a 3d-ndarray)

@[105-106](API: Post request to save labeling images on disk)

---
### Frontend:
<br>
- Vue.js to build the single-page application
    - easy to learn and allows to create modular apps using **components**  

- Canvas representation of PNGs
    - so that is possible to use Javascript code to interact with images  

+++?code=templates/index.html&lang=elixir&title=Vue js application code

@[719](Vuejs app root)
@[14-17](HTML template root)

@[690](Container for 3 sub-component, one for different plane)
@[19-31](HTML template slices container)

@[449](Component that manage a single plane visualization)
@[50-60](HTML template single slice)

@[220](Component to draw on the images. Five of them are overlaid on each plane to allow different zooming level for drawing)
@[108-115](HTML template segmentation drawing layer)

@[161](Component for selecting different color to label images)
@[117-127](HTML template color selector)