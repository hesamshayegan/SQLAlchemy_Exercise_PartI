"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "Chicken389"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)

app.app_context().push()

connect_db(app)
db.create_all()


#######################################################
@app.route('/')
def root():
    """ Homepage redirects to list of all users """
    return redirect("/users")

#######################################################
@app.route('/users')
def users_index():
    """Shows list of all pets in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    # breakpoint()
    return render_template('users/index.html', users=users)

#######################################################
@app.route('/users/new', methods = ["GET"])
def users_new_form():
    """ Show a form to creat a new user"""
    
    return render_template('users/new.html')

#######################################################
@app.route('/users/new', methods = ["POST"])
def users_new():
    """ Shows a form which adds new users"""
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]

    new_user = User(first_name = first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

#######################################################
@app.route('/users/<int:user_id>')
def users_show(user_id):
    """ Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user = user)

#######################################################
@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """ Show a form to edit an existing user """
    
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user = user)

#######################################################
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['image-url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def user_delete(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
