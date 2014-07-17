# -*- coding: utf-8 -*-

import os
import ConfigParser

from ..extensions import oauth


CURR_DIR = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.read(os.path.join(CURR_DIR, "config.cfg"))


FACEBOOK_APP_ID = config.get('Facebook', 'APP_ID')
FACEBOOK_APP_SECRET = config.get('Facebook', 'APP_SECRET')

facebook = oauth.remote_app('facebook',

    # unless absolute urls are used to make requests, this will be added
    # before all URLs.  This is also true for request_token_url and others.
    base_url = 'https://graph.facebook.com/',

    # where flask should look for new request tokens
    request_token_url = None,

    # where flask should exchange the token with the remote application
    access_token_url = '/oauth/access_token',

    authorize_url = 'https://www.facebook.com/dialog/oauth',

    # the consumer keys from the facebook application registry.
    consumer_key = FACEBOOK_APP_ID,
    consumer_secret = FACEBOOK_APP_SECRET,
)