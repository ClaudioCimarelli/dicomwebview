

# Install

        conda create -n dicomwebview python=3
        activate dicomwebview


        conda install -c mjirik pypng flask io3d

in python version < 3.4  install enum:

        conda install enum34

# Run

        python dicom-webview.py -i ~/projects/io3d/sample_data/jatra_5mm/
