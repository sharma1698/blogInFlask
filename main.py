from flask import Flask, render_template, request
from models import db
from models.contact import Contact
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize db and migrations
db.init_app(app)  #initialization
migrate = Migrate(app, db)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=["GET","POST"])
def contact():
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    email = request.form.get('email')
    message = request.form.get('message')
    Contact(name=name, mobile=mobile, email=email, msg=message)
    return render_template('contact.html')

@app.route('/post')
def post():
    return render_template('post.html')


if __name__ == "__main__":
    app.run(debug=True)
