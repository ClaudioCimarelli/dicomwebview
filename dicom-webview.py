from flask import Flask, render_template, request, send_file, session

import io3d
import numpy as np
import os
import StringIO
import png
import argparse
import base64
import itertools


app = Flask(__name__)

app.secret_key = '\xd5\\x\xf6h6\xe1\x1f\xf3\xb9\x91\xa7\x93\x1a\xcd\xe9\xc4\\\xbd7\xea\xf32\x13'

images = np.empty(1)
dims = []
pixelSpacing = np.empty(1)
max_intensity = 255
min_intensity = 0


APP_PATH = os.path.dirname(__file__)
DICOM_PATH = 'DICOM_test/'
SEGM_IMAGE_PATH = 'segmentation_images/'


ALLOWED_EXTENSIONS = set(['png'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    session['dimension'] = dims
    session['ratios'] = [pixelSpacing[0], pixelSpacing[1], pixelSpacing[2]]
    return render_template('index.html')


@app.route('/api/0/stored_dicom/get_slice/axial/<int:slice_n>', methods=['GET'])
def get_slice_axial(slice_n):
    image = create_image_slice(0, dims[0] - slice_n -1)
    return send_file(image,
                     attachment_filename='axial' + str(slice_n) + '.png',
                     mimetype='image/png')


@app.route('/api/0/stored_dicom/get_slice/coronal/<int:slice_n>', methods=['GET'])
def get_slice_coronal(slice_n):
    image = create_image_slice(1, dims[1] - slice_n - 1)
    return send_file(image,
                     attachment_filename='coronal' + str(slice_n) + '.png',
                     mimetype='image/png')


@app.route('/api/0/stored_dicom/get_slice/sagittal/<int:slice_n>', methods=['GET'])
def get_slice_sagittal(slice_n):
    image = create_image_slice(2, dims[2] - slice_n - 1)
    return send_file(image,
                     attachment_filename='sagittal' + str(slice_n) + '.png',
                     mimetype='image/png')


@app.route('/api/0/segmentation/push_segm/axial/<int:slice_n>', methods=['POST'])
def push_segm_axial(slice_n):
    files = request.values
    if files.__len__()>0:
        img_string = files['imgBase64']
        img_string = img_string.replace("data:image/png;base64,", '')
        dec_image = base64.decodestring(img_string)
        r = png.Reader(bytes=dec_image)
        rgba = r.asRGBA()
        width = rgba[0]
        height = rgba[1]
        pixels = rgba[2]
        planes = rgba[3]['planes']
        pixel_array = np.fromiter(itertools.chain(*pixels), dtype=np.uint8).reshape(height, width, planes)
        img_path = os.path.join(APP_PATH, SEGM_IMAGE_PATH)
        img_path = os.path.join(img_path, 'segm-slice' + str(slice_n) + '.png')
        png.from_array(pixel_array, 'RGBA').save(img_path)
        return 'image saved'
    else:
        return 'no images'


def create_image_slice(plane, slice_n):
    image_pixel = images.take(slice_n, plane).astype(float)

    png_file = StringIO.StringIO()

    # map intensity to the range [0, 255]
    image_pixel -= min_intensity
    image_pixel /= max_intensity - min_intensity
    image_pixel *= 255

    # Writing the PNG file
    w = png.Writer(image_pixel.shape[1], image_pixel.shape[0], greyscale=True)
    w.write(png_file, image_pixel)
    png_file.seek(0)

    return png_file


if __name__ == '__main__':
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

    pixelSpacing = datap["voxelsize_mm"]
    pixelSpacing[0] = pixelSpacing[0] if pixelSpacing[0] != 0 else 1
    max_intensity = images.max()
    min_intensity = images.min()

    app.run(debug=True)
