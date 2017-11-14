from flask import Flask, render_template, request, send_file, session

import io3d
import numpy as np
import os
import png
import argparse
import base64
import itertools
from enum import Enum
import sys

if sys.version_info.major == 2:
    import StringIO
else:
    from io import BytesIO

app = Flask(__name__)

app.secret_key = '\xd5\\x\xf6h6\xe1\x1f\xf3\xb9\x91\xa7\x93\x1a\xcd\xe9\xc4\\\xbd7\xea\xf32\x13'

images = np.empty(1)
dims = []
pixelSpacing = np.empty(1)
max_intensity = 255
min_intensity = 0
segm_images = np.empty(1)
segm_images_index = [[], [], []]

APP_PATH = os.path.dirname(__file__)
DICOM_PATH = 'DICOM_test/'
SEGM_IMAGE_PATH = 'segmentation_images/'


class Planes(Enum):
    AXIAL = 0
    CORONAL = 1
    SAGITTAL = 2


@app.route('/')
def index():
    session['dimension'] = dims
    session['ratios'] = [pixelSpacing[0], pixelSpacing[1], pixelSpacing[2]]
    return render_template('index.html')


@app.route('/api/0/stored_dicom/get_slice/<string:plane>/<int:slice_n>', methods=['GET'])
def get_slice(plane, slice_n):
    plane_n = getattr(Planes, plane.upper())
    if not issubclass(type(plane_n), int):
        plane_n = plane_n.value

    image = create_image_slice(plane_n, dims[plane_n] - slice_n - 1)
    return send_file(image,
                     attachment_filename=plane + str(slice_n) + '.png',
                     mimetype='image/png')


@app.route('/api/0/stored_dicom/get_segm_image/<string:plane>/<int:slice_n>', methods=['GET'])
def get_segm_image(plane, slice_n):
    plane_n = getattr(Planes, plane.upper())
    if not issubclass(type(plane_n), int):
        plane_n = plane_n.value
    image = create_segm_image(plane_n, dims[plane_n] - slice_n - 1)
    return send_file(image,
                     attachment_filename='segm-img-' + plane + str(slice_n) + '.png',
                     mimetype='image/png')


@app.route('/api/0/segmentation/push_segm_image/<string:plane>/<int:slice_n>', methods=['POST'])
def push_segm(plane, slice_n):
    files = request.values
    if files.__len__() > 0:
        plane_n = getattr(Planes, plane.upper())
        if not issubclass(type(plane_n), int):
            plane_n = plane_n.value
        img_string = files['imgBase64']
        img_string = img_string.replace("data:image/png;base64,", '')
        dec_image = base64.urlsafe_b64decode(img_string)  # decode base64 image to binary format
        r = png.Reader(bytes=dec_image)
        rgba = r.asRGBA()
        width = rgba[0]
        height = rgba[1]
        pixels = rgba[2]
        planes = rgba[3]['planes']
        pixel_array = np.fromiter(itertools.chain(*pixels), count=width * height * planes, dtype=np.uint8).reshape(
            height, width, -1)

        # modify opacity to 0.5 or 127
        pixel_array[..., 3] = np.where(pixel_array[..., 3] > 0, 127, 0)

        # maintaining the same order of the DICOM images, from upper body to lower in the array
        ind = [slice(None)] * 4
        ind[plane_n] = dims[plane_n] - slice_n - 1
        segm_images[tuple(ind)] = pixel_array

        # indexing modified images
        segm_images_index[plane_n].append(dims[plane_n] - slice_n - 1)

        return 'image pushed in memory array'
    else:
        return 'no image received'


@app.route('/api/0/segmentation/saveToDisk', methods=['POST'])
def save_segm_image_disk():
    # save all images on axial plane
    count = 0
    for plane in range(3):
        img_path = os.path.join(APP_PATH, SEGM_IMAGE_PATH)
        iterable = (save_image(i, plane, img_path) for i in segm_images_index[plane])
        count += len(segm_images_index[plane])
        np.fromiter(iterable, int, count=len(segm_images_index[plane]))
        segm_images_index[plane] = []
    return "saved " + str(count) + " images"


def save_image(i, plane, path):
    plane_name = Planes(plane).name.lower()
    img_path = os.path.join(path, plane_name + '-segm-' + str(i).zfill(4) + '.png')
    png.from_array(segm_images.take(i, plane), 'RGBA').save(img_path)
    return 1


def create_segm_image(plane, slice_n):
    image_pixel = segm_images.take(slice_n, plane)

    if sys.version_info.major == 2:
        png_file = StringIO.StringIO()
    else:
        png_file = BytesIO()

    # Writing the PNG file
    png.from_array(image_pixel, 'RGBA').save(png_file)
    png_file.seek(0)

    return png_file


def create_image_slice(plane, slice_n):
    image_pixel = images.take(slice_n, plane).astype(float)

    if sys.version_info.major == 2:
        png_file = StringIO.StringIO()
    else:
        png_file = BytesIO()

    # map intensity to the range [0, 255]
    image_pixel -= min_intensity
    image_pixel /= max_intensity - min_intensity
    image_pixel *= 255

    # Writing the PNG file
    if plane == 1:
        image_pixel[...] = np.fliplr(image_pixel)
    png.from_array(image_pixel, 'L', info={'bitdepth': 8}).save(png_file)
    png_file.seek(0)

    return png_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--datapath", help="input image path", default=None)
    parser.add_argument("-sn", "--seriesnumber", help="series number", default=None)
    args = parser.parse_args()

    if args.datapath is None:
        path_dicom = os.path.join(APP_PATH, DICOM_PATH)
    else:
        path_dicom = args.datapath

    dr = io3d.DataReader()
    datap = dr.Get3DData(path_dicom, dataplus_format=True, series_number=args.seriesnumber)

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
