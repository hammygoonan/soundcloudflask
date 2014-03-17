#!/usr/bin/python

from flask import Flask, request, render_template, url_for
from connection import ScDetails
import soundcloud
import datetime
import json

details = ScDetails()

app = Flask(__name__)
client = soundcloud.Client(
    client_id=details.client_id,
    client_secret=details.client_secret,
    username=details.username,
    password=details.password,
)

@app.route("/", methods=['GET'])
def index():
	raw_data = open('data.txt')
	processed_data = []
	keys = ['title', 'user', 'permalink', 'embed', 'duration', 'date']
	for line in raw_data:
		processed_data.append(dict(zip(keys, line.split(' | '))))
	try: # if there's a sort provided
		sort = request.args.get('sort')
		newlist = sorted(processed_data, key=lambda k: k[sort])
		return render_template('index.html', tracks=newlist)
	except KeyError:
		pass
 	return render_template('index.html', tracks=processed_data)

@app.route("/update/")
def update():
	following_ids = get_followers()
	tracks = ''
	errors = open('errors.txt', 'w+')
	for user in following_ids:
		user_tracks = client.get('/tracks/', user_id=user.id, limit=30, embeddable_by='me')
		for x in user_tracks:
			try:
				user = x.user['username']
				permalink =  x.permalink_url
		 		embed = client.get('/oembed', url=permalink)
				embed_html = embed.html
				duration = datetime.timedelta(milliseconds=x.duration)
				title = x.title
				date = x.created_at
	 			tracks += title + ' | ' + user + ' | ' + permalink + ' | ' + embed_html + ' | ' + str(duration) + ' | ' + date + "\n"
		 	except:
		 		error = 'Error - user: ' + x.user['username'] + ' track: ' + x.title
		 		errors.write(error.encode('utf8'))
	f = open('data.txt', 'w')
	f.write(tracks.encode('utf8'))
	f.close()
	errors.close()
	return 'update'
	
def get_favorites():
	following = get_followers()
	favourites = {}
	for person in following:
		tracks = client.get('/users/' + str(person.id) + '/favorites')
		if len(tracks) > 0:
			track_details = []
			for track in tracks:
				if track.embeddable_by == 'all':
					embed = client.get('/oembed', url=track.permalink_url)
				else:
					embed = 'not embeddable'
				track_details.append({'user' : track.user['username'], 'user_id' : track.user['id'], 'embed' : embed, 'title' : track.title, 'date' : track.created_at, 'track_id' : track.id })
			favourites[person.username] = track_details
	return favourites
	
def get_followers():
	return client.get('/me/followings')

if __name__ == "__main__":
	app.debug = True
	app.run()
