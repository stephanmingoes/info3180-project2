"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file
from app.forms import LoginForm, RegisterForm
from app.models import Posts, Follows, Likes, Users
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
import os


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

    if form.validate_on_submit():
        existing_user = db.session.execute(db.select(Users).filter(
            (Users.username == form.data["username"]) | (Users.email == form.data["email"]))).scalar()

        if existing_user:
            return jsonify({"message": "User or email taken already"}), 401

        # Uncomment for accepting files
        # file = form.profile_photo.data
        # filename = secure_filename(file.filename)

        # file.save(os.path.join(
        #     app.config["UPLOAD_FOLDER"], filename
        # ))

        new_user = Users(username=form.data["username"], firstname=form.data["firstname"], lastname=form.data["lastname"],
                         password=form.data["password"], email=form.data["email"], location=form.data["location"], biography=form.data["biography"])

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registration was successful"}), 200

    return jsonify({"message": "Registration Failed"}), 401


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
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
            "token": token
        }), 200

    return jsonify({"message": "Login Failed"}), 401


@app.route('/api/v1/auth/logout', methods=['POST'])
def logout():
    logout_user()

    return jsonify({"message": "User logged out"}), 200


@app.route('/api/v1/posts')
@login_required
def get_posts():
    posts = db.session.execute(db.select(Posts)).scalars().all()
    return jsonify({
        "posts": [{"id": p.id, "caption": p.caption, "photo": p.photo, "likes": len(p.likes)} for p in posts]
    })


@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(Users).filter_by(id=id)).scalar()


@login_manager.request_loader
def load_user_from_request(request):
    auth_headers = request.headers.get('Authorization', '').split()
    if len(auth_headers) != 2:
        return None
    try:
        token = auth_headers[1]
        data = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user = db.session.execute(
            db.select(Users).filter_by(username=data['sub'])).scalar()

        if user:
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
