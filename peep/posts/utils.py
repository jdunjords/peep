import os
import secrets
from PIL import Image
from flask import current_app


# TODO do we need to check for collisions before saving??
def save_picture(form_picture):
	# create random 8-byte hex
	random_hex = secrets.token_hex(8)
	# throw away filename return with _
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static', \
		                        'post_pics', picture_fn)
	img = Image.open(form_picture)
	img.save(picture_path)
	return picture_fn