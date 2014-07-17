# -*- coding: utf-8 -*-

import os, json
from flask.ext.script import Manager
import ConfigParser

from fbone import create_app
from fbone.extensions import db, celery
from fbone.user import User, UserDetail, ADMIN, ACTIVE
from fbone.message import Message, StaredMessages
from fbone.utils import MALE


CURR_DIR = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.read(os.path.join(CURR_DIR, "../config.cfg"))


app = create_app()
manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""

    app.run()


@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()

    admin = User(
            name=u'admin',
            email=u'admin@example.com',
            password=u'123456',
            role_code=ADMIN,
            status_code=ACTIVE,
            user_detail=UserDetail(
                sex_code=MALE,
                age=10,
                url=u'http://admin.example.com',
                deposit=100.00,
                location=u'Tallahassee',
                bio=u'admin Guy is ... hmm ... just a admin guy.'))
    db.session.add(admin)
    db.session.commit()


@manager.command
def twitter():
    import twitter
    t = twitter.Api(
        consumer_key=config.get('Tweet', 'CONSUMER_KEY'),
        consumer_secret=config.get('Tweet', 'CONSUMER_SECRET'),
        access_token_key=config.get('Tweet', 'ACCESS_TOKEN'),
        access_token_secret=config.get('Tweet', 'ACCESS_SECRET') )
    # creds = t.VerifyCredentials()

    # print type(creds)
    # print creds

    allStatuses = []
    allStatuses.append(t.GetMentions())
    allStatuses.append(t.GetReplies())
    allStatuses.append(t.GetRetweetsOfMe())

    print type(allStatuses[0][0])
    print(json.dumps(allStatuses[0][0].AsDict(), default=lambda:obj.__dict__, indent=4)) + '\n\n\n'

    print(json.dumps(allStatuses[1][0].AsDict(), default=lambda:obj.__dict__, indent=4)) + '\n\n\n'

    print(json.dumps(allStatuses[2][0].AsDict(), default=lambda:obj.__dict__, indent=4)) + '\n\n\n'

    # print "followers: "
    # followers = [f for f in t.GetFollowers()]
    # print followers[0].screen_name
    # print followers[0].GetProfileImageUrl()
    # print dir(followers[0])

@manager.command
def celery():
    with app.app_context():
        celery.start()

manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
