"""
pbotty.py

Author: Frank Valcarel

Description: This is a small Python script that post tweets on the behalf of Preston Hamlin.
The tweets are constructed from a collection of written texts by Preston Hamlin himself.
"""

import re
import os
import sys
import twitter
import sqlite3
import argparse
import ConfigParser
from time import sleep
from datetime import datetime

from utils import *


CURR_DIR = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser.ConfigParser()
config.read(os.path.join(CURR_DIR, "config.cfg"))

parser = argparse.ArgumentParser(
  description='pbotty(Peabody): script that posts tweets on behalf of one Preston Hamlin.')
parser.add_argument('-d', help='debug mode', action="store_true")
parser.add_argument('--init', help='initialize', action="store_true")
parser.add_argument('--stats', help='run stats analysis', action="store_true")
parser.add_argument('--quote', help='tweet a random quote', action="store_true")
parser.add_argument('--sonnet', help='tweet a random sonnet (on schedule)', action="store_true")
# parser.add_argument('--haiku', help='begin haiku tweet schedule')

args = parser.parse_args()



def stats():
  f = open(os.path.join(CURR_DIR, "data/cleaned.txt"))
  utils.unique_words(f)


def initdb():
  """
  initialize the database
  if the db exists DO NOTHING
  """
  db = sqlite3.connect('quotes.db')
  cursor = db.cursor()

  cursor.execute('CREATE TABLE IF NOT EXISTS quotes(id INTEGER PRIMARY KEY, \
    quote TEXT UNIQUE, use_count INTEGER, last_used DATETIME)')

  cursor.execute('CREATE TABLE IF NOT EXISTS sonnets(id INTEGER PRIMARY KEY, \
    sonnet TEXT UNIQUE, use_count INTEGER, last_used DATETIME)')

  db.commit()
  db.close()

def updatedb():
  """
  update database without dropping tables
  """
  pass

def get_quotes():
  """
  get_quotes(): loads the data file and splits on each sentence
  then inserts each line under 140 characters into the database
  quotes are unique
  """
  f = open(os.path.join(CURR_DIR, "data/cleaned.txt"))
  quotes = [line.split('. ') for line in f]

  db = sqlite3.connect(os.path.join(CURR_DIR,"quotes.db"))
  cursor = db.cursor()

  for quote in quotes:
      for _ in quote:
        if len(_) <= 140:
          _ = _.decode('utf-8')
          print '.',
          cursor.execute('INSERT OR IGNORE INTO quotes VALUES(NULL, ?, 0, NULL)', (_,))
          db.commit()
  db.close()


def get_sonnets():
  """
  get_sonnets(): loads the sonnet file and splits on any sequence of '[number].'

  """
  src = open(os.path.join(CURR_DIR, "sonnets/sonnets.txt"))
  sonnets = re.split('\d.', src.read())
  sonnets = [line.strip() for line in sonnets]

  db = sqlite3.connect(os.path.join(CURR_DIR,"quotes.db"))
  cursor = db.cursor()

  for sonnet in sonnets:
    if sonnet != '':
        sonnet = sonnet.decode('utf-8')
        print '.',
        cursor.execute('INSERT OR IGNORE INTO sonnets VALUES(NULL, ?, 0, NULL)', (sonnet,))
        db.commit()
  db.close()


def tweet_quote():
  """
  the tweet_quote() function handles all of our tweet bots biz logic for
  tweeting single quotes
  1. the API connection is established
  2. loads the quotes database and randomly selects a quote to tweet
  3. composes and posts tweet to twitter
  4. updates the use_count and last_used fields for the tweeted quote
  """

  t = twitter.Api(
    consumer_key=config.get('Tweet', 'CONSUMER_KEY'),
    consumer_secret=config.get('Tweet', 'CONSUMER_SECRET'),
    access_token_key=config.get('Tweet', 'ACCESS_TOKEN'),
    access_token_secret=config.get('Tweet', 'ACCESS_SECRET') )


  db = sqlite3.connect(os.path.join(CURR_DIR, "quotes.db"))
  cursor = db.cursor()

  cursor.execute('SELECT MIN(use_count) FROM quotes')
  m = cursor.fetchone()

  cursor.execute('SELECT * FROM quotes WHERE use_count=? ORDER BY RANDOM() LIMIT 1', (m[0],))
  tweet = cursor.fetchone()

  use_count = tweet[2] + 1
  last_used = datetime.now()
  update = tweet[1]

  """
  tweet tweet
  """
  if args.d:
    # if debugging enabled testing output
    print 'DEBUG MODE: ', str(update)
  else:
    status = t.PostUpdate(update)
    print str(last_used) + ":" + status.text

  cursor.execute('UPDATE quotes SET use_count=?, last_used=? WHERE id=?', (use_count, last_used, tweet[0],))
  db.commit()
  db.close()


def tweet_sonnet():
  """
  the tweet_sonnet() function handles all of our tweet bots biz logic for
  tweeting a sonnet on a schedule of 2 lines per tweet
  and finnsh with a closing tweet and hashtag
  1. the API connection is established
  2. loads the quotes database and randomly selects a sonnet to tweet
  3. composes and posts sonnet (two lines per tweet) to twitter
  4. updates the use_count and last_used fields for the tweeted sonnet
  """

  t = twitter.Api(
    consumer_key=config.get('Tweet', 'CONSUMER_KEY'),
    consumer_secret=config.get('Tweet', 'CONSUMER_SECRET'),
    access_token_key=config.get('Tweet', 'ACCESS_TOKEN'),
    access_token_secret=config.get('Tweet', 'ACCESS_SECRET') )


  db = sqlite3.connect(os.path.join(CURR_DIR, "quotes.db"))
  cursor = db.cursor()

  cursor.execute('SELECT MIN(use_count) FROM sonnets')
  m = cursor.fetchone()

  cursor.execute('SELECT * FROM sonnets WHERE use_count=? ORDER BY RANDOM() LIMIT 1', (m[0],))
  tweet = cursor.fetchone()

  use_count = tweet[2] + 1
  last_used = datetime.now()

  sonnet = tweet[1].split('\n')

  """
  tweet tweet
  """

  count = 1
  for a, b in zip(*[iter(sonnet)]*2):
    update = a + '\n' + b
    # if debugging enabled testing output
    if args.d:
      print 'DEBUG MODE: ', str(update)
    else:
      status = t.PostUpdate(update)
      print str(last_used), str(count) + ": " + status.text
    if (count * 2) == len(sonnet):
      break
    sleep(2 ** (count))
    count += 1

  cursor.execute('UPDATE sonnets SET use_count=?, last_used=? WHERE id=?', (use_count, last_used, tweet[0],))
  db.commit()
  db.close()

def main():
  """
  main function runs the script in the correct sequence
  """
  if not len(sys.argv) > 1:
    parser.error('mode not specified')
    sys.exit(1)

  elif args.stats:
    stats()
    sys.exit(1)

  elif args.init:
    if utils.query_yes_no("this will delete and rebuild the database. Are you sure"):
      print "initializing database"

      if args.d:
        print 'DEBUG MODE: No changes made to database'
        sys.exit()

      initdb()
      print "updating quotes"
      get_quotes()
      print "\nupdating sonnets"
      get_sonnets()
    else:
      sys.exit()


  elif args.quote:
    tweet_quote()


  elif args.sonnet:
    tweet_sonnet()


if __name__ == '__main__':
  main()