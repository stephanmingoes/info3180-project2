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
    # profile_photo = FileField("Poster", validators=[FileRequired(), FileAllowed(
    #     ['jpg', 'png'], 'Upload a .png or .jpg file')])

class PostForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    caption = StringField('Caption')
=======
    profile_photo = FileField("Profile Photo", validators=[FileRequired(), FileAllowed(
        ['jpg', 'png', 'jpeg'], 'Upload a .png or .jpg file')])
>>>>>>> origin/main
