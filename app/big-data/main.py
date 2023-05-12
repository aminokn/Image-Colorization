import io
import os

import flask
import numpy as np
import skimage
from PIL import Image, ImageOps
from PIL.Image import Image as PilImage
import tensorflow as tf

graph = tf.Graph()
width = 256
height = 256


app = flask.Flask(__name__, static_url_path="")
landscape_model = tf.keras.models.load_model('pix2pix_landscape6kp400e.h5')
people_model = tf.keras.models.load_model('pix2pix_people700e.h5')
coco_model = tf.keras.models.load_model('pix2pix_coco800e.h5')
manga_model = tf.keras.models.load_model('pix2pix_anime1000e.h5')

@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.post("/api/coloring-page")
def coloring_page():
    file = flask.request.files.get("input-image")
    if file is None:
        return "Missing input-image parameter", 400

    input_image = Image.open(file.stream)
    output_image = generate_coloring_page(input_image)

    image_io = io.BytesIO()
    output_format = "png"
    output_image.save(image_io, format=output_format)
    image_io.seek(0)

    return flask.send_file(image_io, mimetype=f"image/{output_format}")

@app.post("/api/model-a")
def model_a():
    file = flask.request.files.get("input-image")
    if file is None:
        return "Missing input-image parameter", 400

    
    input_image = Image.open(file.stream)
    output_image = process_a(file.filename)
    output_image = output_image.resize(input_image.size)
    image_io = io.BytesIO()
    output_format = "png"
    output_image.save(image_io, format=output_format, optimize=True)
    image_io.seek(0)

    return flask.send_file(image_io, mimetype=f"image/{output_format}")

@app.post("/api/model-b")
def model_b():
    file = flask.request.files.get("input-image")
    if file is None:
        return "Missing input-image parameter", 400

    
    input_image = Image.open(file.stream)
    
    output_image = process_b(file.filename)
    output_image = output_image.resize(input_image.size)
    image_io = io.BytesIO()
    output_format = "png"
    output_image.save(image_io, format=output_format, optimize=True)
    image_io.seek(0)

    return flask.send_file(image_io, mimetype=f"image/{output_format}")

@app.post("/api/model-c")
def model_c():
    file = flask.request.files.get("input-image")
    if file is None:
        return "Missing input-image parameter", 400

    
    input_image = Image.open(file.stream)
    output_image = process_c(file.filename)
    output_image = output_image.resize(input_image.size)
    image_io = io.BytesIO()
    output_format = "png"
    output_image.save(image_io, format=output_format, optimize=True)
    image_io.seek(0)

    return flask.send_file(image_io, mimetype=f"image/{output_format}")

@app.post("/api/model-d")
def model_d():
    file = flask.request.files.get("input-image")
    if file is None:
        return "Missing input-image parameter", 400

    
    input_image = Image.open(file.stream)
    output_image = process_d(file.filename)
    output_image = output_image.resize(input_image.size)
    image_io = io.BytesIO()
    output_format = "png"
    output_image.save(image_io, format=output_format, optimize=True)
    image_io.seek(0)

    return flask.send_file(image_io, mimetype=f"image/{output_format}")

@app.post("/api/model-e")
def model_e():
    file = flask.request.files.get("input-image")
    if file is None:
        return "Missing input-image parameter", 400

    
    input_image = Image.open(file.stream)
    output_image = process_e(file.filename)
    output_image = output_image.resize(input_image.size)
    image_io = io.BytesIO()
    output_format = "png"
    output_image.save(image_io, format=output_format, optimize=True)
    image_io.seek(0)

    return flask.send_file(image_io, mimetype=f"image/{output_format}")

def generate_coloring_page(input: PilImage) -> PilImage:
    # Convert to grayscale if needed
    if input.mode != "L":
        input = input.convert("L")
    # Transpose if taken in non-native orientation (rotated digital camera)
    NATIVE_ORIENTATION = 1
    if input.getexif().get(0x0112, NATIVE_ORIENTATION) != NATIVE_ORIENTATION:
        input = ImageOps.exif_transpose(input)
    np_image = np.asarray(input)

    # Remove some noise to keep the most visible edges
    np_image = skimage.restoration.denoise_tv_chambolle(np_image, weight=0.05)
    # Detect the edges
    np_image = skimage.filters.sobel(np_image)
    # Convert to 8 bpp
    np_image = skimage.util.img_as_ubyte(np_image)
    # Invert to get dark edges on a light background
    np_image = 255 - np_image
    # Improve the contrast
    np_image = skimage.exposure.rescale_intensity(np_image)

    return Image.fromarray(np_image)

def process_a(file):
    name = file.split('.')[0]

    input_image = tf.io.read_file(file)
    input_image = tf.io.decode_image(input_image, channels=3)
    input_image = tf.cast(input_image, tf.float32)

    input_image = tf.image.resize(input_image, [height, width],
                                method = tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    input_image = (input_image / 127.5) - 1

    input_image = tf.reshape(input_image, [1,height,width,3])
    output = landscape_model(input_image, training=False)

    output = tf.reshape(output, [height,width,3])
    
    tensor = (output+1)*127.5
    tensor = np.array(tensor, dtype=np.uint8)
    return Image.fromarray(tensor)

def process_b(file):
    name = file.split('.')[0]

    input_image = tf.io.read_file(file)
    input_image = tf.io.decode_image(input_image, channels=3)
    input_image = tf.cast(input_image, tf.float32)

    input_image = tf.image.resize(input_image, [height, width],
                                method = tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    input_image = (input_image / 127.5) - 1

    input_image = tf.reshape(input_image, [1,height,width,3])
    output = people_model(input_image, training=False)

    output = tf.reshape(output, [height,width,3])
    
    tensor = (output+1)*127.5
    tensor = np.array(tensor, dtype=np.uint8)
    return Image.fromarray(tensor)

def process_c(file):
    name = file.split('.')[0]

    input_image = tf.io.read_file(file)
    input_image = tf.io.decode_image(input_image, channels=3)
    input_image = tf.cast(input_image, tf.float32)

    input_image = tf.image.resize(input_image, [height, width],
                                method = tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    input_image = (input_image / 127.5) - 1

    input_image = tf.reshape(input_image, [1,height,width,3])
    output = coco_model(input_image, training=False)

    output = tf.reshape(output, [height,width,3])
    
    tensor = (output+1)*127.5
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return Image.fromarray(tensor)

def process_d(file):
    name = file.split('.')[0]

    input_image = tf.io.read_file(file)
    input_image = tf.io.decode_image(input_image, channels=3)
    input_image = tf.cast(input_image, tf.float32)

    input_image = tf.image.resize(input_image, [height, width],
                                method = tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    input_image = (input_image / 127.5) - 1

    input_image = tf.reshape(input_image, [1,height,width,3])
    output = coco_model(input_image, training=False)

    output = tf.reshape(output, [height,width,3])
    
    tensor = (output+1)*127.5
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return Image.fromarray(tensor)

def process_e(file):
    name = file.split('.')[0]

    input_image = tf.io.read_file(file)
    input_image = tf.io.decode_image(input_image, channels=3)
    input_image = tf.cast(input_image, tf.float32)

    input_image = tf.image.resize(input_image, [height, width],
                                method = tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    input_image = (input_image / 127.5) - 1

    input_image = tf.reshape(input_image, [1,height,width,3])
    output = manga_model(input_image, training=False)

    output = tf.reshape(output, [height,width,3])
    
    tensor = (output+1)*127.5
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return Image.fromarray(tensor)

if __name__ == "__main__":
    # Dev only: run "python main.py" (3.9+) and open http://localhost:8080
    os.environ["FLASK_ENV"] = "development"
    app.run(host="localhost", port=8080, debug=True)
else:
    # Prod only: cache static resources
    app.send_file_max_age_default = 3600  # 1 hour