soundcloudflask
===============

This bad boy is a pretty simple way of getting what I want out of soundcloud. Basically it hits up the Soundcloud API, creating a few text files which can then be read into some HTML output


Requirements
------------

* [Flask](http://flask.pocoo.org/)
* [A Python wrapper](https://github.com/soundcloud/soundcloud-python) for the Soundcloud API
* A [Soundcloud](https://developers.soundcloud.com/) account and API Key
* [VLC](http://www.videolan.org/vlc/index.html)

Setup
-----

Basically you just need to run it: python sc.py

You also need to update the text files from time to time: python update.py

Might be wise to set it up as a cron

Future Development
------------------

* A list of my favourites
* A list of my follow's favourites
* Be able to follow my followers favourites

* Playlists
* Smart playlists
* Improved "incoming" stream, with recommendations
