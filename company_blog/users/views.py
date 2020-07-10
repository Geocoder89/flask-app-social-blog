#############################
from flask import render_template, url_for, redirect, request, flash, Blueprint

from flask_login import login_user, current_user, logout_user, login_required

from company_blog import db
from company_blog.models import User, BlogPost
from company_blog.users.forms import RegistrationForm, LoginForm, UpdateProfileForm
from company_blog.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)


###########################


# register view
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration was successful')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


# login view
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Login Successful')
            # next here is the next page the user wants to navigate upon login
            next = request.args.get('next')
            # if there is no next page we produce the index page
            if next == None or next[0] == '/':
                next = url_for('core.index')
            # else we redirect the user to the either the next page they requested for or the index page
            return redirect(next)
    return render_template('login.html', form=form)


# logout view

@users.route('/logout')
def logout():
    # the logout_user function handles logout
    logout_user()
    return redirect(url_for('core.index'))


# accounts view
@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        #  to check if you want to add a new picture we use the add_profile_pic of the pictures_handler function to make the input data for the picture the picture itself
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic
        # if there are changes to the username or email we handle that as well
        current_user.username = form.username.data
        current_user.email = form.email.data
        # we commit that change to the db
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.profile'))
    # else if there is no change in the info the initial form data still remains the same
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


# list of blog post
# /username
@users.route('/<username>')
def user_posts(username):
    # to get each page of the request
    page = request.args.get('page', 1, type=int)
    # we then query the database for the first occurence of the username if there is no existence of it,we raise a 404 error
    user = User.query.filter_by(username=username).first_or_404()
    # we render all blog posts we filter by the user who has the backref of 'author'  we order by the earliest to the least earliest(desc) and we run the paginate for 5 pages
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    # we render the template
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
