from . import db
from werkzeug.security import generate_password_hash


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    likes = db.relationship('Likes', backref='posts', lazy=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Post %r>' % (self.id)


class Likes(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Likes %r>' % (self.post_id)


class Follows(db.Model):
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Follows %r>' % (self.id)


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(128), unique=True)
    location = db.Column(db.Text)
    biography = db.Column(db.Text)
    profile_photo = db.Column(db.String(128))
    joined_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    posts = db.relationship('Posts', backref='users', lazy=True)
    likes = db.relationship('Likes', backref='users', lazy=True)
    follows = db.relationship('Follows', foreign_keys=[
                              Follows.user_id], lazy=True)
    followers = db.relationship('Follows', foreign_keys=[
                                Follows.follower_id], backref='followers', lazy=True)

    def __init__(self, username, password, firstname, lastname, email, location, biography, profile_photo):
        self.username = username
        self.password = generate_password_hash(
            password, method='pbkdf2:sha256')
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = profile_photo

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Users %r>' % (self.username)


class Token(db.Model):
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True)
    token_string = db.Column(db.Text)
    expired_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Token %r>' % (self.id)
