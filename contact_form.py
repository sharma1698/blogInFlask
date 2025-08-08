from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField ,SubmitField , IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp


class ContactForm(FlaskForm):
    name = StringField("Name", render_kw={"placeholder": "Enter your name"} ,validators=[DataRequired(message="Name is required"), Length(min=3, max=50, message="Name must be between 3 and 50 characters")])
    email = StringField("Email", render_kw={"placeholder": "Enter your email"},validators=[DataRequired(message="Email is required"), Email(message="Enter a valid email address")])
    mobile = StringField("Phone", render_kw={"placeholder": "Enter your phone"},validators=[DataRequired(message="Mobile number is required"),Regexp(r'^[0-9]{10}$', message="Enter a valid 10-digit mobile number")])
    message = TextAreaField("Message", render_kw={"rows": 4, "cols": 100, "placeholder": "Enter your message"}, validators=[DataRequired(message="Message is required"), Length(min=5, message="Message must be at least 5 characters long")])
    submit = SubmitField("Submit")
