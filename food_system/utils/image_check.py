# -*- coding: utf-8 -*-
# FileName  : image_check.py
import tensorflow as tf
from .conf import model_path
import numpy as np

model = tf.keras.models.load_model(model_path)

class_names = ['Bread', 'Dairy product', 'Dessert', 'Egg', 'Fried food', 'Meat', 'Noodles-Pasta', 'Rice', 'Seafood',
               'Soup', 'Vegetable-Fruit']


def load_and_preprocess_image(path):
    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [224, 224])
    image = tf.cast(image, tf.float32)
    image = image / 255.0  # normalize to [0,1] range
    return image


def check_handle(img_path):
    test_img = img_path
    test_tensor = load_and_preprocess_image(test_img)
    test_tensor = tf.expand_dims(test_tensor, axis=0)
    pred = model.predict(test_tensor)
    pred_num = np.argmax(pred)
    result = class_names[int(pred_num)]
    return result
