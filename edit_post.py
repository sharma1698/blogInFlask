from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField ,SubmitField , IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed


class EditPostForm(FlaskForm):
    title = StringField("Title", render_kw={"placeholder": "Update Title"} ,validators=[DataRequired(message="Title is required"), Length(min=3, max=50, message="Title must be between 3 and 50 characters")])
    tag_line = StringField("TagLine", render_kw={"placeholder": "Enter your TagLine"},validators=[DataRequired(message="TagLine is required"), Length(min=3, max=50, message="Tagline must be between 3 and 50 characters")])
    slug = StringField("Slug",validators=[DataRequired(message="Slug is required"), Length(min=3, max=20, message="Slug must be between 3 and 20 characters")])
    content = TextAreaField("Content", render_kw={"placeholder": "Enter your content"},validators=[DataRequired(message="Content is required")])
    img_file = FileField("Image Upload", validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message="Only image files are allowed")])
    submit = SubmitField("Submit")
    is_edit = False


  # Custom validator for the image field
    def validate_img_file(self, field):
        # If it's a new post AND no file was provided, raise a validation error
        if not self.is_edit and not field.data:
            raise ValidationError("Image is required for new posts.")