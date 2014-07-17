# -*- coding: utf-8 -*-

import os
import twitter

from sqlalchemy import Column, ForeignKey, not_
from ..extensions import db
from ..utils import get_current_time, diff



CURR_DIR = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.read(os.path.join(CURR_DIR, "../../../config.cfg"))


def twitter_credentials():
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


class Twitter_Poll(db.Model):

    __tablename__ = 'twitter_poll'

    id = Column(db.Integer, primary_key=True)
    last_updated = Column(db.Datetime)

    # credentials
    credentials = Column(db.PickleType)

    # followers
    followers = Column(db.PickleType)

    # mentions
    mentions = Column(db.PickleType)