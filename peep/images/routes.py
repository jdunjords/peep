import os
from flask import (Blueprint, render_template, url_for, 
                   flash, redirect, request, abort, current_app)
from flask_login import current_user, login_required
from peep import db
from peep.models import Image
from peep.images.forms import ImageForm
from peep.images.utils import model_classify, save_picture


images = Blueprint('images', __name__)


@images.route('/upload-image', methods=['GET', 'POST'])
@login_required
def new_image():
	form = ImageForm()
	# if form validates after user submits
	if form.validate_on_submit() and form.picture.data:
		image_file = save_picture(form.picture.data, 'user_uploads')
		image = Image(image_file=image_file, owner=current_user)
		db.session.add(image)
		db.session.commit()
		flash('Your image has been uploaded!', 'success')
		return redirect(url_for('users.user_images', username=current_user.username))
	return render_template('upload_image.html', title='Upload Image', 
                           form=form, legend='Upload Image')


# TODO without verifying that the user is current_user, this could be hacked I think?
@images.route('/user/<string:username>/delete/<int:image_id>', methods=['POST'])
@login_required
def delete_image(username, image_id):
	image = Image.query.get_or_404(image_id)
	if image.owner != current_user:
		# HTTP response for a forbidden route
		abort(403)
	db.session.delete(image)
	db.session.commit()
	full_image_path = os.path.join(current_app.root_path, 'static', \
		                        'user_uploads', image.image_file)
	os.remove(full_image_path)
	flash('Your image has been deleted!', 'success')
	return redirect(url_for('users.user_images', username=current_user.username))


@images.route('/classify-bird/<int:image_id>')
def classify_bird(image_id):
	image = Image.query.get_or_404(image_id)
	image.identified = True
	db.session.commit()
	flash(model_classify(image.image_file), 'info')
	return redirect(url_for('users.user_images', username=image.owner.username))


@images.route('/favorite-image/<int:image_id>')
def favorite_image(image_id):
	image = Image.query.get_or_404(image_id)
	image.favorited = True
	db.session.commit()
	flash('Added to favorites!', 'success')
	return redirect(url_for('users.user_images', username=image.owner.username))


@images.route('/unfavorite_image/<int:image_id>')
def unfavorite_image(image_id):
	image = Image.query.get_or_404(image_id)
	image.favorited = False
	db.session.commit()
	flash('Removed from favorites', 'success')
	return redirect(url_for('users.user_images', username=image.owner.username))


@images.route('/add_training_image/<int:image_id>')
def add_training_image(image_id):
	image = Image.query.get_or_404(image_id)
	image.submitForTraining = True
	db.session.commit()
	flash('Added to training images!', 'success')
	return redirect(url_for('users.user_images', username=image.owner.username))


@images.route('/remove_training_image/<int:image_id>')
def remove_training_image(image_id):
	image = Image.query.get_or_404(image_id)
	image.submitForTraining = False
	db.session.commit()
	flash('Removed from training images!', 'success')
	return redirect(url_for('users.user_images', username=image.owner.username))