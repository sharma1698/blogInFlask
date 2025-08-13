from flask import Flask, render_template, request, flash, redirect, url_for, session
from models import db
from models.contact import Contact
from models.post import Post
from flask_migrate import Migrate
from config import Config
from contact_form import *
from edit_post import *
from flask_mail import Mail
from pprint import pprint
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
@app.context_processor   #to access contact everywhere
def inject_urls():
    return {key: app.config[key] for key in ['FB_URL', 'TW_URL', 'GT_URL','ADMIN_USERNAME','ADMIN_PASSWORD','UPLOAD_FOLDER']}

mail = Mail(app)

# Initialize db and migrations
db.init_app(app)  #initialization
migrate = Migrate(app, db)


@app.route('/')
def home():
    # Get the current page number from the URL (default to 1)
    # The 'type=int' ensures it's a safe integer
    page = request.args.get('page', 1, type=int)

    # Use paginate() to get a Pagination object
    # per_page: how many items to show on each page
    # error_out: when you use error_out=False, It prevents a 404 Not Found error and instead returns an empty pagination object.
    # When you enter page=4.7, Flask's request.args.get() tries to convert the string "4.7" to an integer. This conversion fails because "4.7" is not a valid integer. Because the conversion fails, the get() method falls back to its default value, which is 1.

    pagination = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=2, error_out=True)
    return render_template('index.html', pagination=pagination)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=["GET","POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
    # if request.method == 'POST':
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        message = request.form.get('message')
        contact = Contact(name=name, mobile=mobile, email=email, msg=message)
        db.session.add(contact)
        db.session.commit()
        mail.send_message('New message from '+name,sender=app.config['MAIL_DEFAULT_SENDER'],  recipients =[email],body=message+"\n"+mobile)
        flash("Thanks for contacting us!", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html',form=form)

# # get post by slug
# @app.route('/post/<string:post_slug>',methods=["GET"])
# def post_route(post_slug):
#     post=Post.query.filter_by(slug=post_slug).first()
#     return render_template('post.html',post=post)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user'] != app.config['ADMIN_USERNAME']:
            flash("You must be logged in to view this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login',methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if  username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD'] :
            session['user'] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


# after login go to dashboard
@app.route('/dashboard',methods = ["GET","POST"])
@login_required
def dashboard():
    if 'user' in session and session['user'] == app.config['ADMIN_USERNAME']:
        posts = Post.query.filter(Post.deleted_at.is_(None)).all()
        return render_template('dashboard.html', posts=posts)
    else:
        return redirect(url_for('login'))


@app.route('/post', methods=['GET', 'POST'], defaults={'id': None})
@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = None
    form = EditPostForm()

    if id:
        post = Post.query.get_or_404(id)
        form = EditPostForm(obj=post)
        form.is_edit = True # Set the flag for edit

    if form.validate_on_submit():
        if not id:
            # Handle creating a new post
            new_post =Post(
            title=form.title.data,
            slug=form.slug.data,
            content=form.content.data,
            tag_line=form.tag_line.data,
                 )
            # The custom validator already ensured the file exists
            filename = secure_filename(form.img_file.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.img_file.data.save(file_path)
            new_post.img_file = filename
            db.session.add(new_post)
            db.session.commit()
            flash("New post added successfully!", "success")
            return redirect(url_for('edit_post', id=new_post.id))
        else:
            # Handle editing an existing post
            form.populate_obj(post)

            # Check if a new file was uploaded
            if hasattr(form.img_file.data, 'filename') and form.img_file.data.filename:
                filename = secure_filename(form.img_file.data.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                form.img_file.data.save(file_path)
                post.img_file = filename
            db.session.commit()
            flash("Post updated successfully!", "success")
            return redirect(url_for('edit_post', id=post.id))

    return render_template('editPost.html', form=form, post=post)





# add post
# @login_required
# @app.route('/add-post', methods=['GET','POST'])
# def add_post():
#  try:
#     form = EditPostForm()
#     if form.validate_on_submit():
#             new_post = Post(
#             title=form.title.data,
#             slug=form.slug.data,
#             content=form.content.data,
#             tag_line=form.tag_line.data,
#             img_file=form.img_file.data
#                  )
#             db.session.add(new_post)
#             db.session.commit()
#             flash("Blog added successfully!", "success")
#             return redirect(url_for('/add-post'))
#     return render_template('editPost.html', form=form)

#  except SQLAlchemyError as e:
#       db.session.rollback() # Rollback the session to a clean state
#       flash(f"A database error occurred: {str(e)}", "danger")
#       return redirect(url_for('login'))
#  except Exception as e:
#       flash(f"An unexpected error occurred: {str(e)}", "danger")
#       return redirect(url_for('login'))

# # edit post
# @login_required
# @app.route('/post/<string:id>', methods=['GET','POST'])
# def edit_post(id):
#  try:
#     post = Post.query.filter_by(id=id).first_or_404()
#     form = EditPostForm(obj=post)
#     if form.validate_on_submit():
#             post.title = form.title.data
#             post.tag_line = form.content.data
#             post.content = form.content.data
#             post.slug = form.slug.data
#             post.tag_line = form.tag_line.data
#             if form.img_file.data:
#                 filename = secure_filename(form.img_file.data.filename)
#                 file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 form.img_file.data.save(file_path)
#                 post.img_file = filename
#             db.session.commit()
#             flash("Blog updated successfully!", "success")
#             return redirect(url_for('edit_post', id=post.id))
#     return render_template('editPost.html', form=form, post=post)

#  except SQLAlchemyError as e:
#       db.session.rollback() # Rollback the session to a clean state
#       flash(f"A database error occurred: {str(e)}", "danger")
#       return redirect(url_for('login'))
#  except Exception as e:
#       flash(f"An unexpected error occurred: {str(e)}", "danger")
#       return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def soft_delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.deleted_at is None: # Only soft-delete if not already deleted
        post.deleted_at = datetime.utcnow() # Mark as deleted with current timestamp
        db.session.commit()
        flash("Post moved to trash successfully!", "success")
    else:
        flash("Post is already soft-deleted.", "info")

    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True)
