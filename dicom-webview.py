from flask import Flask, render_template, send_file, session

import io3d
import numpy as np
import os
import StringIO
import png

app = Flask(__name__)

app.secret_key = '\xd5\\x\xf6h6\xe1\x1f\xf3\xb9\x91\xa7\x93\x1a\xcd\xe9\xc4\\\xbd7\xea\xf32\x13'

images = np.empty(1)
dims = np.empty(1)
pixelSpacing = np.empty(1)
max_intensity = 255
min_intensity = 0


@app.route('/')
def index():
    session['dimension'] = dims
    return render_template('index.html')


@app.route('/api/0/stored_dicom/get_slice/axial/<int:slice_n>', methods=['GET'])
def get_slice_axial(slice_n):
    image = create_image_slice(0, slice_n)
    return send_file(image,
                     attachment_filename='axial' + str(slice_n) + '.png',
                     mimetype='image/png')


@app.route('/api/0/stored_dicom/get_slice/sagittal/<int:slice_n>', methods=['GET'])
def get_slice_sagittal(slice_n):
    image = create_image_slice(2, slice_n)
    return send_file(image,
                     attachment_filename='sagittal' + str(slice_n) + '.png',
                     mimetype='image/png')


@app.route('/api/0/stored_dicom/get_slice/coronal/<int:slice_n>', methods=['GET'])
def get_slice_coronal(slice_n):
    image = create_image_slice(1, slice_n)
    return send_file(image,
                     attachment_filename='coronal' + str(slice_n) + '.png',
                     mimetype='image/png')


def create_image_slice(plane, slice_n):
    image_pixel = images.take(slice_n, plane).astype(float)

    png_file = StringIO.StringIO()

    # map intensity to the range [0, 255]
    image_pixel -= min_intensity
    image_pixel /= max_intensity-min_intensity
    image_pixel *= 255

    session['width'] = image_pixel.shape[1]
    session['height'] = image_pixel.shape[0]

    # Writing the PNG file
    # w = png.Writer(image_pixel.shape[1], image_pixel.shape[0], greyscale=True)
    if(plane==0):
        w = png.Writer(image_pixel.shape[1], image_pixel.shape[0], greyscale=True,
                   x_pixels_per_unit=1/pixelSpacing[1], y_pixels_per_unit=1/pixelSpacing[2], unit_is_meter=True)
    else:
        w = png.Writer(image_pixel.shape[1], image_pixel.shape[0], greyscale=True,
                       x_pixels_per_unit=1/pixelSpacing[1], y_pixels_per_unit=1/pixelSpacing[0], unit_is_meter=True)
    w.write(png_file, image_pixel)
    png_file.seek(0)

    return png_file


if __name__ == '__main__':
    path = os.path.dirname(__file__)

    path_dicom = os.path.join(path, "DICOM_test/")

    dr = io3d.DataReader()
    datap = dr.Get3DData(path_dicom, dataplus_format=True)

    images = datap["data3d"]

    dims = images.shape

    pixelSpacing = datap["voxelsize_mm"]
    pixelSpacing[0] = pixelSpacing[0] if pixelSpacing[0] != 0 else 1

    x = np.arange(0.0, (dims[1] + 1) * pixelSpacing[1], pixelSpacing[1])
    y = np.arange(0.0, (dims[2] + 1) * pixelSpacing[2], pixelSpacing[2])
    z = np.arange(0.0, (dims[0] + 1) * pixelSpacing[0], pixelSpacing[0])

    max_intensity = images.max()
    min_intensity = images.min()

    app.run(debug=True)
