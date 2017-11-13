#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

# import click
import logging

logger = logging.getLogger(__name__)
import logging.handlers
import argparse

# import begin
import sys
import os
import os.path as op
import numpy as np

import io3d

from dicomwebview import



def main():
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    logger.addHandler(ch)


    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--datapath", help="input image path", default=None)
    args = parser.parse_args()

    if args.datapath is None:
        path_dicom = os.path.join(APP_PATH, DICOM_PATH)
    else:
        path_dicom = args.datapath

    dr = io3d.DataReader()
    datap = dr.Get3DData(path_dicom, dataplus_format=True)

    images = datap["data3d"]
    dims = images.shape
    segm_images = np.empty(shape=[dims[0], dims[1], dims[2], 4], dtype=np.uint8)

    for dirName, subdirList, fileList in os.walk(os.path.join(APP_PATH, SEGM_IMAGE_PATH)):
        for filename in fileList:
            if ".png" in filename.lower():
                r = png.Reader(filename=os.path.join(dirName, filename))
                rgba = r.asRGBA()
                width = rgba[0]
                height = rgba[1]
                pixels = rgba[2]
                planes = rgba[3]['planes']
                pixel_array = np.fromiter(itertools.chain(*pixels), count=width * height * planes,
                                          dtype=np.uint8).reshape(height, width, -1)
                slice_n = int(''.join(list(filename)[-8:-4]))

                plane_n = Planes[filename.split('-')[0].upper()].value
                # maintaining the same order of the DICOM images, from upper body to lower in the array
                ind = [slice(None)] * 4
                ind[plane_n] = slice_n
                segm_images[tuple(ind)] = pixel_array

    pixelSpacing = datap["voxelsize_mm"]
    pixelSpacing[0] = pixelSpacing[0] if pixelSpacing[0] != 0 else 1
    max_intensity = images.max()
    min_intensity = images.min()

    app.run(debug=True)

if __name__ == "__main__":
    main()