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
	form = ImageForm(meta={'csrf': False})
	if form.validate_on_submit() and form.picture.data:

		max_uploads = current_app.config['BASIC_MAX_UPLOAD']
		new_upload_len = len(form.picture.data)
		
		# check to see if new upload will exceed free upload limit
		if not current_user.is_premium_member and \
			current_user.num_uploads + new_upload_len > max_uploads:
			flash('New upload exceeds free upload limit for non-premium peeps.', 'info')
			flash(f"{max_uploads-current_user.num_uploads}/{max_uploads} free uploads remaining.", 'info')
			# redirect the user back to their images page
			return redirect(url_for('users.user_images', username=current_user.username))

		# otherwise, they still have enough free uploads, so update their upload count
		current_user.num_uploads += new_upload_len
		
		# check if current user not premium peep and new upload exceeds free limit
		if not current_user.is_premium_member and \
			current_user.num_uploads + new_upload_len > max_uploads:
			flash('New upload exceeds free uploads for non-premium peeps', 'info')
		
		# if the filename is empty, user didn't select any files
		if request.files['picture'].filename == '':
			flash('No file selected.', 'danger')
			return redirect(request.url)
		
		# else, iterate through the list of picture uploads
		for picture in form.picture.data:
			image_file = save_picture(picture, 'user_uploads')
			image = Image(image_file=image_file, owner=current_user)
			db.session.add(image)
			db.session.commit()
		
		# custom flash for single or multi upload
		if new_upload_len > 1:
			flash('Your images have been uploaded successfully!', 'success')
		else:
			flash('Your image has been uploaded successfully!', 'success')
		flash(f"{max_uploads-current_user.num_uploads}/{max_uploads} free uploads remaining.", 'info')
		
		# redirect the user back to their images page
		return redirect(url_for('users.user_images', username=current_user.username))
	
	# if GET request, render image upload page
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
	# update num_uploads of current user
	current_user.num_uploads -= 1
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
	image.submit_for_training = True
	db.session.commit()
	flash('Added to training images!', 'success')
	return redirect(url_for('users.user_images', username=image.owner.username))


@images.route('/remove_training_image/<int:image_id>')
def remove_training_image(image_id):
	image = Image.query.get_or_404(image_id)
	image.submit_for_training = False
	db.session.commit()
	flash('Removed from training images!', 'success')
	return redirect(url_for('users.user_images', username=image.owner.username))
