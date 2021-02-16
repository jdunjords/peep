# modules for classification
import numpy as np
import tensorflow as tf
import cv2
from tensorflow import keras
from tensorflow.keras.models import load_model

model = load_model('models/3birds.h5')
labels = ['Purple Finch', 'Blue Jay', 'Redheaded Woodpecker']

def model_classify(img_path):
	# get the image, and process it into format that keras expects
	img = cv2.imread('./static/uploads/' + img_path)
	img = cv2.resize(img, (224,224))
	img = np.expand_dims(img, axis=0)
	y_prob = model.predict(img)
	y_classes = y_prob.argmax(axis=-1).item()
	predicted_label = labels[y_classes]
	return "Model prediction: " + repr(predicted_label)
