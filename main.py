from flask import Flask, render_template, request, flash, redirect, url_for
from models import db
from models.contact import Contact
from models.post import Post
from flask_migrate import Migrate
from config import Config
from contact_form import *
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
@app.context_processor   #to access contact everywhere
def inject_urls():
    return {key: app.config[key] for key in ['FB_URL', 'TW_URL', 'GT_URL']}

mail = Mail(app)

# Initialize db and migrations
db.init_app(app)  #initialization
migrate = Migrate(app, db)


@app.route('/')
def home():
    posts=Post.query.order_by(Post.date.desc()).limit(2).all()
    return render_template('index.html', posts=posts)


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


@app.route('/post/<string:post_slug>',methods=["GET"])
def post_route(post_slug):
    post=Post.query.filter_by(slug=post_slug).first()
    return render_template('post.html',post=post)

if __name__ == "__main__":
    app.run(debug=True)
