@title[Introduction]
## DICOM Web Viewer

#####A Web application to view and label medical images online 


---
Server side:

- Python and Flask web server:
    - offering API to read DICOM images and label them
    - uses PyPNG and Numpy libraries to work with pixel arrays
    
+++

@title[Server side code]
## Server side code

```python
@app.route('/api/0/stored_dicom/get_slice/<string:plane>/<int:slice_n>', methods=['GET'])

@app.route('/api/0/stored_dicom/get_segm_image/<string:plane>/<int:slice_n>', methods=['GET'])

@app.route('/api/0/segmentation/push_segm_image/<string:plane>/<int:slice_n>', methods=['POST'])

@app.route('/api/0/segmentation/saveToDisk', methods=['POST'])

```
@[1](Get a dicom image along one plane )
@[2](Get labeling image use for segmentation purposes)
@[3](Send labeling images to server memory, still not saved permanently)
@[4](Request to save labeling images on disk)

---

Client side:

- Vue.js to create the frontend single-page application
    - easy to learn and allows to create modular apps using components

- Canvas representation of PNGs
    - so that is possible to use Javascript code to iteract with images  


---

