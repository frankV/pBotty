# -*- coding: utf-8 -*-

import json
from functools import wraps
from flask import (Blueprint, render_template, current_app, g, request,
                   flash, url_for, redirect, session, abort, jsonify)
from flask.ext.login import login_user

from ..user import User
from ..extensions import db

from twitter import *
from facebook import facebook

auth = Blueprint('auth', __name__)


@auth.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@auth.after_request
def after_request(response):
    return response


@auth.route('/twitter_login')
def twitter_login():
    return twitter.authorize(callback=url_for('auth.twitter_authorized',
        next=request.args.get('next') or request.referrer or None))


@auth.route('/twitter_authorized')
@twitter.authorized_handler
def twitter_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    # user = User()
    session['twitter_token'] = resp['oauth_token']
    session['twitter_token_secret'] = resp['oauth_token_secret']

    data = twitter.get('account/verify_credentials.json').data
    print data

    return redirect(next_url)


@twitter.tokengetter
def get_twitter_token():
    # return user.TW_oauth_token, user.TW_oauth_secret
    return session.get('twitter_token')



@auth.route('/facebook_login')
def facebook_login():
  return facebook.authorize(callback=url_for('auth.facebook_authorized',
    next=request.args.get('next') or request.referrer or None,
    _external=True))


@auth.route('/facebook_authorized')
@facebook.authorized_handler
def facebook_authorized(resp):

  next_url = request.args.get('next') or url_for('index')
  if resp is None or 'access_token' not in resp:
    flash(u'You denied the request to sign in.')
    return redirect(next_url)

  session['facebook_token'] = (resp['access_token'], '')

  print resp

  basic_data = facebook.get('/me').data
  print(json.dumps(basic_data, default=lambda:obj.__dict__, indent=4))


  user = User.query.filter_by(facebook_id=basic_data['id']).first()

  # user never signed on
  if user is None:
      user = User()
      user.name = basic_data['first_name'] + " " + basic_data['last_name']
      db.session.add(user)

      # in any case we update the authenciation token in the db
      # In case the user temporarily revoked access we will have
      # new tokens here.
      user.oauth_token = resp['access_token']
      # user.oauth_secret = resp['oauth_token_secret']
      db.session.commit()

  session['user_id'] = user.id

  if login_user(user):
    flash("Logged in", 'success')

  print user.name
  g.user = user

  return redirect(next_url)


@facebook.tokengetter
def get_facebook_oauth_token():
  return session.get('facebook_token')
