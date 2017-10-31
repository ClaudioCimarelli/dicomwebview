

# Install

        conda create -c mjirik -c conda-forge -n dicomwebview python=3 pypng flask io3d
        
        activate dicomwebview

in python version < 3.4  install enum:

        conda install enum34

# Run

        python dicom-webview.py -i ~/projects/io3d/sample_data/jatra_5mm/
