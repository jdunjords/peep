import numpy as np
import tensorflow as tf
import cv2
from tensorflow import keras
from tensorflow.keras.models import load_model
import os
import secrets
from PIL import Image
from flask import current_app

model = load_model('peep/classifiers/3birds.h5')
labels = ['Purple Finch', 'Blue Jay', 'Redheaded Woodpecker']

def model_classify(img_path):
	# get the image, and process it into format that keras expects
	img = cv2.imread('peep/static/user_uploads/' + img_path)
	img = cv2.resize(img, (224,224))
	img = np.expand_dims(img, axis=0)
	y_prob = model.predict(img)
	y_classes = y_prob.argmax(axis=-1).item()
	predicted_label = labels[y_classes]
	return "Model prediction: " + repr(predicted_label)

def save_picture(form_picture, folder_name):
	# create random 8-byte hex
	random_hex = secrets.token_hex(8)
	# throw away filename return with _
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext.lower()
	picture_path = os.path.join(current_app.root_path, 'static', \
		                        folder_name, picture_fn)
	img = Image.open(form_picture)
	img.save(picture_path)
	return picture_fn

def delete_picture(image_file, folder_name):
	if image_file and folder_name:
		picture_path = os.path.join(current_app.root_path, 'static', \
		                        folder_name, image_file)
		os.remove(picture_path)
		return True
	return False
