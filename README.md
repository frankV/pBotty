pBotty :: The Preston Twitter Bot
=================================

This is a small Python script that post tweets on the behalf of Preston Hamlin.

The tweets are constructed from a collection of written texts by Preston Hamlin himself.

Our current collection has generated about 52 "complete thoughts" that arrive under 140 characters.
This was not a small feat... If you know The Preston Hamlin, you know this.


Current Schedule
-----------------
**Tweets**
* 2 tweets per day
  * posted at `00 10,17 * * *`
  * Every day at 10am and 5pm (Eastern)
  * **#Pweets**

**Sonnet Schedule (WIP)**
* 3 sonnets per week
  * posted at `00 13 * * 1,3,5`
  * Every Monday, Wednesday, and Friday beginning at 1pm (Eastern)
    * 14 Lines, 2 lines per tweet
    * **#Ponnets**


How it Works
------------
When pbotty.py is ran:
```python
$ python pbotty.py
```

A quote is randomly chosen based on the following SQL expressions:

First, we find the value for quotes with the minimum number of uses
```
SELECT MIN(use_count) FROM quotes
```
Then we select one random quote
```
SELECT * FROM quotes WHERE use_count=__ ORDER BY RANDOM() LIMIT 1
```

The quote is then tweeted via [@prestonhamlin](http://twitter.com/prestonhamlin) and the `use_count` and `last_used` columns are updated.

Currently the data source is a stripped body of text which we curated from many pieces that Preston **actually** wrote.


Data Schema
-----------
####Tweets
| id | quote | use_count | last_used |
| ---- | ----------------- | -------------------| -------------------|
| 1 | However, However, ... |                 1 | 2014-06-18 10:00:24.592390|
| 2 | Smalltalk took the ... |                2 | 2014-06-17 13:00:37.930239|
| 3 | This includes built-in ... |            1 | 2014-06-17 10:00:12.002932|

<br>

####Sonnets
**coming soon...**

Shout Outs
----------

**[python-twitter](https://github.com/bear/python-twitter)** by [bear](https://github.com/bear)<br>
This library provides a pure Python interface for the Twitter API. It works with Python versions from 2.5 to 2.7. Python 3 support is under development.

**[sonnetizer.py](https://github.com/rossgoodwin/sonnetizer)** by [rossgoodwin](https://github.com/rossgoodwin)<br>
Generates rhyming sonnets in (mostly) iambic pentameter from any text corpus
[http://rossgoodwin.com/sonnetizer](http://rossgoodwin.com/sonnetizer)

**[nltk](http://www.nltk.org/)**<br>
NLTK is a leading platform for building Python programs to work with human language data.