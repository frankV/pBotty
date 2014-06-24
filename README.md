pBotty (Peabody) :: The Preston Twitter Bot
=================================

This is a small Python script that post tweets on the behalf of one Preston Hamlin.

The tweets are constructed from a collection of written texts by Preston Hamlin himself.

Our current collection has generated about 52 seemingly "complete thoughts" that arrive under 140 characters.
This was not a small feat... If you know the Preston Hamlin, you know this.


Current Schedule
-----------------
**Tweets**
* 2 tweets per day
  * posted at `0 10,17 * * *` (Eastern)

**Sonnet Schedule**
* 3 sonnets per week
  * posted at `00 13 * * 1,3,5` (Eastern)
    * 14 Lines, 2 lines per tweet


How it Works
------------
Command overview:
```bash
$ python pbotty.py -h
usage: pbotty.py [-h] [-d] [--init] [--stats] [--quote] [--sonnet]

pbotty(Peabody): script that posts tweets on behalf of one Preston Hamlin.

optional arguments:
  -h, --help  show this help message and exit
  -d          debug mode
  --init      initialize
  --stats     run stats analysis
  --quote     tweet a random quote
  --sonnet    tweet a random sonnet (on schedule)
```

Tweeting a random quote:
```bash
$ python pbotty.py --quote
```

Tweeting a random sonnet:
```bash
$ python pbotty.py --sonnet
```


###Statistics
__________

```bash
$ python pbotty.py --stats
most frequently used (23): number
largest word: parameterization
unique words: 1599
```


Currently the data source is a stripped body of text which we curated from many pieces that Preston **actually** wrote.

<br>
To Do
----------
[ ] Add update command to add entries to databases
<br>
[ ] Add web interface for collecting public submissions
<br>
[X] Add Statistical Analysis Data


<br>
Shout Outs
----------

**[python-twitter](https://github.com/bear/python-twitter)** by [bear](https://github.com/bear)<br>
This library provides a pure Python interface for the Twitter API. It works with Python versions from 2.5 to 2.7. Python 3 support is under development.

**[sonnetizer.py](https://github.com/rossgoodwin/sonnetizer)** by [rossgoodwin](https://github.com/rossgoodwin)<br>
Generates rhyming sonnets in (mostly) iambic pentameter from any text corpus
[http://rossgoodwin.com/sonnetizer](http://rossgoodwin.com/sonnetizer)

**[nltk](http://www.nltk.org/)**<br>
NLTK is a leading platform for building Python programs to work with human language data.