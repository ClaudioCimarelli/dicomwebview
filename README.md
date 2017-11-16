

# Install

        conda create -c mjirik -c conda-forge -n dicomwebview python=3 pypng flask io3d
        
        source activate dicomwebview

in python version < 3.4  install enum:

        conda install enum34

# Run
   take DICOM from folder DICOM_test:
   
        python dicomwebview.py 
        
   or from your path:

        python dicomwebview.py -i <path/to/DICOM/images>

# Features

- view DICOM images projected in 3 planes: axial, coronal, sagittal

- scroll over the planes' slices and project selected point in all the planes

- draw colored shapes to label organs

- save and load from server all labeling images

# Command list


Draw disabled:

- left-click: 

  - select the other plane's slices corresponding to the coordinates below clicking point
  
Draw enabled:

 1. check the drawing mode

 2. select a color before drawing with the radio buttons on top

    - **Note**: the eraser color is really transparent!
    You won't see a line drawing until releasing the click. Then you will notice the draw below being deleted.

- left-click and moving mouse: 

  - draw closed shapes following mouse movements
  
General commands:
 
- hold left-click and moving mouse:

  - scroll slices of the other planes following coordinates below mouse position  
          
- hold ctrl + left-click and moving mouse:

  - scroll plane image along x and y axis
      
- mouse wheel:
    
  - zoom all planes around the selected point (visible by the two crossing yellow axis)

