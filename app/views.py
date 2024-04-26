"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
from os.path import isdir
from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file, send_from_directory

from app.forms import LoginForm, RegisterForm, PostForm
from app.models import Posts, Follows, Likes, Users

from app.forms import LoginForm, RegisterForm
from app.models import Posts, Follows, Likes, Users, Token

from app.forms import LoginForm, RegisterForm
from app.models import Posts, Follows, Likes, Users, Token
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from werkzeug.security import check_password_hash
import jwt
from werkzeug.datastructures import CombinedMultiDict
from datetime import datetime, timedelta
import os
from sqlalchemy.orm import joinedload


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@app.route('/api/v1/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate():
        existing_user = db.session.execute(db.select(Users).filter(
            (Users.username == form.data["username"]) | (Users.email == form.data["email"]))).scalar()

        if existing_user:
            return jsonify({"message": "Username or email taken already"}), 409

        # Uncomment for accepting files (the profile pic)! Look in forms.py as well!

        file = form.profile_photo.data
        filename = secure_filename(file.filename)

        if not isdir(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])

        file.save(os.path.join(
            app.config["UPLOAD_FOLDER"], filename
        ))

        new_user = Users(username=form.data["username"], firstname=form.data["firstname"], lastname=form.data["lastname"],
                         password=form.data["password"], email=form.data["email"], location=form.data[
                             "location"], biography=form.data["biography"],
                         profile_photo=filename)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registration was successful, proceed to login"}), 200

    return jsonify({"message": "Registration Failed"}), 400


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate():
        user = db.session.execute(db.select(Users).filter_by(
            username=form.data["username"])).scalar()

        if not user or not check_password_hash(user.password, form.data["password"]):
            return jsonify({"message": "Login Failed"}), 401

        token = jwt.encode({
            'sub': user.username,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=120)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        login_user(user)

        return jsonify({
            "token": token,
            "message": "User successfully logged in"
        }), 200

    return jsonify({"message": "Login Failed"}), 400


@app.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def logout():
    auth_headers = request.headers.get('Authorization', '').split()
    if not auth_headers or len(auth_headers) != 2:
        return jsonify({"message": "Login required"}), 401

    expired_token = Token(token_string=auth_headers[1])
    db.session.add(expired_token)
    db.session.commit()

    logout_user()

    return jsonify({"message": "User logged out"}), 200


@app.route('/api/v1/posts', methods=['POST'])
@login_required
def add_post():
    user_id = current_user.id
    form = PostForm()

    if form.validate():
        photo_file = form.photo.data
        filename = secure_filename(photo_file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo_file.save(path)

        caption = request.form.get('caption', '')

        post = Posts(user_id=user_id, photo=filename, caption=caption)
        db.session.add(post)
        db.session.commit()
        return jsonify({"message": "Post added Sucessfully"}), 200

    else:

        return jsonify({"message": "Form validation failed"}), 400


@app.route('/api/v1/user/<user_id>')
@login_required
def get_user_info(user_id):
    user = db.session.execute(
        db.select(Users).options(joinedload(Users.posts), joinedload(Users.followers), joinedload(Users.follows)).filter_by(id=user_id)).scalar()

    return jsonify({
        'id': user.id,
        'username': user.username,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
        'location': user.location,
        'biography': user.biography,
        'profile_photo': user.profile_photo,
        'joined_on': user.joined_on,
        'posts': [
            {
                'id': p.id,
                'caption': p.caption,
                'photo': p.photo,
                'created_on': p.created_on,
            } for p in user.posts
        ],
        'follows': [
            {
                'user_id': f.follower_id
            } for f in user.follows
        ],
        'followers': [
            {
                'user_id': f.user_id
            } for f in user.followers
        ],
    })


@app.route('/api/v1/users/<user_id>/posts', methods=['get'])
@login_required
def get_user_posts(user_id):
    query = db.select(Posts).where(Posts.user_id == user_id)
    posts = db.session.execute(query).scalars().all()
    post_info = [{
        'id': post.id,
        'caption': post.caption,
        'photo': post.photo,
        'created_on': post.created_on.strftime('%m-%d-%Y %H:%M:%S'),
        'likes': len(post.likes)
    } for post in posts]

    return jsonify({'posts': post_info})


@app.route('/api/users/<user_id>/follow', methods=['POST'])
@login_required
def follow_user(user_id):
    print(current_user.id)
    print(user_id)
    if current_user.id == int(user_id):
        return jsonify({"message": "Not allowed"}), 400

    target_user = Users.query.get(user_id)
    if not target_user:
        return jsonify({"message": "User not found"}), 404

    if Follows.query.filter_by(follower_id=user_id, user_id=current_user.id).first():
        return jsonify({"message": "You are already following this user"}), 400

    follow = Follows(follower_id=user_id, user_id=current_user.id)
    db.session.add(follow)
    db.session.commit()

    return jsonify({"message": "You followed this user"}), 200


@app.route('/api/v1/posts', methods=['GET'])
@login_required
def get_posts():

    posts = db.session.query(Posts).options(
        joinedload(Posts.users), joinedload(Posts.likes)).all()

    current_user_id = current_user.id

    response_posts = []
    for p in posts:

        liked_by_current_user = any(
            like.user_id == current_user_id for like in p.likes)

        post_info = {
            "id": p.id,
            "caption": p.caption,
            "photo": p.photo,
            "user": {
                "id": p.users.id,
                "username": p.users.username,
                "profile_photo": p.users.profile_photo if p.users.profile_photo else ""
            },
            "likes": len(p.likes),
            "liked_by_current_user": liked_by_current_user,
            "created_on": p.created_on
        }
        response_posts.append(post_info)

    return jsonify({"posts": response_posts})


@app.route('/api/v1/posts/<post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Posts.query.get(post_id)
    if not post:
        return jsonify({"message": "Post not found"}), 404

    if Likes.query.filter_by(user_id=current_user.id, post_id=post_id).first():
        return jsonify({"message": "You already liked this post"}), 400

    like = Likes(user_id=current_user.id, post_id=post_id)
    db.session.add(like)
    db.session.commit()

    return jsonify({"message": "Post liked"}), 200


@app.route('/api/v1/image/<filename>', methods=['GET'])
def get_poster(filename):
    current_dir = os.getcwd()
    return send_from_directory(os.path.join(current_dir, app.config['UPLOAD_FOLDER']), filename)


@app.route('/api/v1/is_logged_in', methods=['GET'])
@login_required
def isLoggedIn():
    return jsonify({"message": "User is logged in"}), 200


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"message": "Login required"}), 401


@login_manager.request_loader
def load_user_from_request(request):
    auth_headers = request.headers.get('Authorization', '').split()
    if not auth_headers or len(auth_headers) != 2:
        return None
    try:
        token = auth_headers[1]
        expired_token = db.session.execute(
            db.select(Token).filter_by(token_string=token)).scalar()

        if expired_token:
            return None

        data = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user = db.session.execute(
            db.select(Users).filter_by(username=data['sub'])).scalar()

        if not user:
            return None

        return user
    except:
        return None

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use


def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)

    return error_messages


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
