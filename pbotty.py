"""
pbotty.py

Author: Frank Valcarel

Description: This is a small Python script that post tweets on the behalf of Preston Hamlin.
The tweets are constructed from a collection of written texts by Preston Hamlin himself.
"""

import os
import twitter
import sqlite3
from datetime import datetime
import ConfigParser

CURR_DIR = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser.ConfigParser()
config.read(os.path.join(CURR_DIR, "config.cfg"))


def initdb():
  """
  initialize the database
  if the db exists DO NOTHING
  """
  db = sqlite3.connect('quotes.db')
  cursor = db.cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS quotes(id INTEGER PRIMARY KEY, \
    quote TEXT UNIQUE, use_count INTEGER, last_used DATETIME)')
  db.commit()
  db.close()


def get_quotes():
  """
  get_quotes(): loads the data file and splits on each sentence
  then inserts each line under 140 characters into the database
  quotes are unique
  """
  f = open(os.path.join(CURR_DIR, "data/cleaned.txt"))
  l = [line.split('. ') for line in f]

  db = sqlite3.connect(os.path.join(CURR_DIR,"quotes.db"))
  cursor = db.cursor()

  for k in l:
      for j in k:
        if len(j) <= 140:
          j = j.decode('utf-8')
          cursor.execute('INSERT OR IGNORE INTO quotes VALUES(NULL, ?, 0, NULL)', (j,))
          db.commit()
  db.close()



def tweet():
  """
  the tweet() function handles all of our tweet bots biz logic
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

  # print tweet
  use_count = tweet[2] + 1
  last_used = datetime.now()
  update = tweet[1]

  """
  tweet tweet
  """
  # print t.VerifyCredentials()
  # print str(update)
  status = t.PostUpdate(update)
  print str(last_used) + ":" + status.text

  cursor.execute('UPDATE quotes SET use_count=?, last_used=? WHERE id=?', (use_count, last_used, tweet[0],))
  db.commit()
  db.close()


def main():
  """
  main function runs the script in the correct sequence
  """
  initdb()
  get_quotes()
  tweet()


if __name__ == '__main__':
  main()