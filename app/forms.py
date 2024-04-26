from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, Email


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    biography = TextAreaField('Location', validators=[InputRequired()])
<<<<<<< HEAD
<<<<<<< HEAD
    # profile_photo = FileField("Poster", validators=[FileRequired(), FileAllowed(
    #     ['jpg', 'png'], 'Upload a .png or .jpg file')])


=======
    profile_photo = FileField("Profile Photo", validators=[FileRequired(), FileAllowed(
        ['jpg', 'png', 'jpeg'], 'Upload a .png or .jpg file')])
>>>>>>> origin/main
=======
    profile_photo = FileField("Profile Photo", validators=[FileRequired(), FileAllowed(
        ['jpg', 'png', 'jpeg'], 'Upload a .png or .jpg file')])
>>>>>>> ddbfeb93c1c1e39c138eda047a5e0c2d4ea9c4a9

class PostForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    caption = StringField('Caption')