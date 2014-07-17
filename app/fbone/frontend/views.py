# -*- coding: utf-8 -*-

import os
import json
import twitter
import ConfigParser
from uuid import uuid4

from flask import (Blueprint, render_template, current_app, request, Response,
                   flash, url_for, redirect, session, abort, jsonify)
from flask.ext.mail import Message
from flask.ext.babel import gettext as _
from flask.ext.login import login_required, login_user, current_user, logout_user, confirm_login, login_fresh

from ..user import User, UserDetail
from ..extensions import  mail, login_manager
from .forms import SignupForm, LoginForm, RecoverPasswordForm, ReauthForm, ChangePasswordForm, OpenIDForm, CreateProfileForm

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.read(os.path.join(CURR_DIR, "../../../config.cfg"))


frontend = Blueprint('frontend', __name__)


def twitter_latest_status():
    t = twitter.Api(
        consumer_key=config.get('Tweet', 'CONSUMER_KEY'),
        consumer_secret=config.get('Tweet', 'CONSUMER_SECRET'),
        access_token_key=config.get('Tweet', 'ACCESS_TOKEN'),
        access_token_secret=config.get('Tweet', 'ACCESS_SECRET') )
    return t.VerifyCredentials()

def twitter_followers():
    t = twitter.Api(
        consumer_key=config.get('Tweet', 'CONSUMER_KEY'),
        consumer_secret=config.get('Tweet', 'CONSUMER_SECRET'),
        access_token_key=config.get('Tweet', 'ACCESS_TOKEN'),
        access_token_secret=config.get('Tweet', 'ACCESS_SECRET') )
    return t.GetFollowers()

def twitter_mentions():
    t = twitter.Api(
        consumer_key=config.get('Tweet', 'CONSUMER_KEY'),
        consumer_secret=config.get('Tweet', 'CONSUMER_SECRET'),
        access_token_key=config.get('Tweet', 'ACCESS_TOKEN'),
        access_token_secret=config.get('Tweet', 'ACCESS_SECRET') )
    return t.GetMentions()


@frontend.route('/')
def home():
    return render_template('home.html', user=current_user)

@frontend.route('/add_quote', methods=['POST'])
def add_quote():
    print request.data
    return Response(status=200, mimetype='application/json')

@frontend.route('/latest_tweet', methods=['GET', 'POST'])
def latest_tweet():
    user = twitter_latest_status().AsDict()
    print(json.dumps(user, default=lambda:obj.__dict__, indent=4))
    return jsonify(user)

@frontend.route('/new_followers', methods=['GET', 'POST'])
def new_followers():
    followers = twitter_followers()
    d = dict()
    count = 0
    for user in followers:
        d[count] = user.AsDict()
        count += 1
    print(json.dumps(d, default=lambda:obj.__dict__, indent=4))
    return render_template('partials/followers.html', followers=followers)

@frontend.route('/mentions', methods=['GET', 'POST'])
def mentions():
    mentions = twitter_mentions()
    d = dict()
    count = 0
    for mention in mentions:
        d[count] = mention.AsDict()
        count += 1
    print(json.dumps(d, default=lambda:obj.__dict__, indent=4))
    return render_template('partials/mentions.html', mentions=mentions)

# @frontend.route('/login/openid', methods=['GET', 'POST'])
# @oid.loginhandler
# def login_openid():
#     if current_user.is_authenticated():
#         return redirect(url_for('user.index'))

#     form = OpenIDForm()
#     if form.validate_on_submit():
#         return form.login(oid)
#     return render_template('frontend/login_openid.html', form=form, error=oid.fetch_error())


# @oid.after_login
# def create_or_login(resp):
#     user = User.query.filter_by(openid=resp.identity_url).first()
#     if user and login_user(user):
#         flash('Logged in', 'success')
#         return redirect(oid.get_next_url() or url_for('user.index'))
#     return redirect(url_for('frontend.create_profile', next=oid.get_next_url(),
#             name=resp.fullname or resp.nickname, email=resp.email,
#             openid=resp.identity_url))


# @frontend.route('/create_profile', methods=['GET', 'POST'])
# def create_profile():
#     if current_user.is_authenticated():
#         return redirect(url_for('user.index'))

#     form = CreateProfileForm(name=request.args.get('name'),
#             email=request.args.get('email'),
#             openid=request.args.get('openid'))

#     if form.validate_on_submit():
#         form.create_profile()

#         if login_user(user):
#             return redirect(url_for('user.index'))

#     return render_template('frontend/create_profile.html', form=form)


# @frontend.route('/root')
# def index():
#     current_app.logger.debug('debug')

#     if current_user.is_authenticated():
#         return redirect(url_for('user.index'))

#     page = int(request.args.get('page', 1))
#     pagination = User.query.paginate(page=page, per_page=10)
#     return render_template('index.html', pagination=pagination)


# @frontend.route('/search')
# def search():
#     keywords = request.args.get('keywords', '').strip()
#     pagination = None
#     if keywords:
#         page = int(request.args.get('page', 1))
#         pagination = User.search(keywords).paginate(page, 1)
#     else:
#         flash(_('Please input keyword(s)'), 'error')
#     return render_template('frontend/search.html', pagination=pagination, keywords=keywords)


# @frontend.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated():
#         return redirect(url_for('user.index'))

#     form = LoginForm(login=request.args.get('login', None),
#                      next=request.args.get('next', None))

#     if form.validate_on_submit():
#         user, authenticated = User.authenticate(form.login.data,
#                                     form.password.data)

#         if user and authenticated:
#             remember = request.form.get('remember') == 'y'
#             if login_user(user, remember=remember):
#                 flash(_("Logged in"), 'success')
#             return redirect(form.next.data or url_for('user.index'))
#         else:
#             flash(_('Sorry, invalid login'), 'error')

#     return render_template('frontend/login.html', form=form)


# @frontend.route('/reauth', methods=['GET', 'POST'])
# @login_required
# def reauth():
#     form = ReauthForm(next=request.args.get('next'))

#     if request.method == 'POST':
#         user, authenticated = User.authenticate(current_user.name,
#                                     form.password.data)
#         if user and authenticated:
#             confirm_login()
#             current_app.logger.debug('reauth: %s' % session['_fresh'])
#             flash(_('Reauthenticated.'), 'success')
#             return redirect('/change_password')

#         flash(_('Password is wrong.'), 'error')
#     return render_template('frontend/reauth.html', form=form)


# @frontend.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash(_('Logged out'), 'success')
#     return redirect(url_for('frontend.index'))


# @frontend.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if current_user.is_authenticated():
#         return redirect(url_for('user.index'))

#     form = SignupForm(next=request.args.get('next'))

#     if form.validate_on_submit():
#         user = form.signup()

#         if login_user(user):
#             return redirect(form.next.data or url_for('user.index'))

#     return render_template('frontend/signup.html', form=form)


# @frontend.route('/change_password', methods=['GET', 'POST'])
# def change_password():
#     user = None
#     if current_user.is_authenticated():
#         if not login_fresh():
#             return login_manager.needs_refresh()
#         user = current_user
#     elif 'activation_key' in request.values and 'email' in request.values:
#         activation_key = request.values['activation_key']
#         email = request.values['email']
#         user = User.query.filter_by(activation_key=activation_key) \
#                          .filter_by(email=email).first()

#     if user is None:
#         abort(403)

#     form = ChangePasswordForm(activation_key=user.activation_key)

#     if form.validate_on_submit():
#         user.change_password()

#         flash(_("Your password has been changed, please log in again"),
#               "success")
#         return redirect(url_for("frontend.login"))

#     return render_template("frontend/change_password.html", form=form)


# @frontend.route('/reset_password', methods=['GET', 'POST'])
# def reset_password():
#     form = RecoverPasswordForm()

#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()

#         if user:
#             flash('Please see your email for instructions on '
#                   'how to access your account', 'success')

#             user.recover_password()

#             url = url_for('frontend.change_password', email=user.email, activation_key=user.activation_key, _external=True)
#             html = render_template('macros/_reset_password.html', project=current_app.config['PROJECT'], username=user.name, url=url)
#             message = Message(subject='Reset your password in ' + current_app.config['PROJECT'], html=html, recipients=[user.email])
#             mail.send(message)

#             return render_template('frontend/reset_password.html', form=form)
#         else:
#             flash(_('Sorry, no user found for that email address'), 'error')

#     return render_template('frontend/reset_password.html', form=form)


# @frontend.route('/help')
# def help():
#     return render_template('frontend/footers/help.html', active="help")
