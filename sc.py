#!/usr/bin/python

from flask import Flask, request, render_template, url_for
from connection import ScDetails
import soundcloud
import datetime
import os
import vlc

details = ScDetails()

app = Flask(__name__)
client = soundcloud.Client(
    client_id=details.client_id,
    client_secret=details.client_secret,
    username=details.username,
    password=details.password,
)

class vlcPlayer:
	def __init__(self):
		self.instance = vlc.Instance()
		self.player = self.instance.media_player_new()
	def play(self, stream_url):
		self.media = self.instance.media_new(stream_url)
		self.player.set_media(self.media)
		self.player.play()
		return self.player
	def stop(self):
		self.player.stop()

vlc_player = vlcPlayer()

def update():
	following_ids = get_followers()
	tracks = ''
	errors = open('errors.txt', 'w+')
	for user in following_ids:
		user_tracks = client.get('/tracks/', user_id=user.id, limit=30, embeddable_by='me')
		for track in user_tracks:
			try:
				user = track.user['username']
				permalink =  track.permalink_url
				duration = datetime.timedelta(milliseconds=track.duration)
				title = track.title
				date = track.created_at
				track_id = str(track.id)
	 			tracks += title + ' | ' + user + ' | ' + permalink + ' | ' + str(duration) + ' | ' + date + ' | ' + track_id + "\n"
		 	except:
		 		error = 'Error - user: ' + track.user['username'] + ' track: ' + track.title
		 		errors.write(error.encode('utf8'))
	f = open('data.txt', 'w')
	f.write(tracks.encode('utf8'))
	f.close()
	errors.close()
	return 'update'

def update_favorites():
	following = get_followers()
	favourites = []
	for person in following:
		tracks = client.get('/users/' + str(person.id) + '/favorites')
		if len(tracks) > 0:
			track_details = []
			for track in tracks:
				if track.embeddable_by == 'all':
					embed = track.permalink_url
				else:
					embed = 'not embeddable'
				track_user = track.user['username']
				track_user_id = track.user['id']
				track_title = track.title
				track_date = track.created_at
				track_id = track.id
				track_duration = datetime.timedelta(milliseconds=track.duration)
				track_details.append({'user' : track_user, 'user_id' : str(track_user_id), 'embed' : embed, 'title' : track_title, 'date' : str(track_date), 'track_id' : str(track_id), 'duration' : str(track_duration) })
			favourites.append({'user' : person.username, 'tracks' : track_details})
	for person in favourites:
		fav_file = open('favourites/' + person['user'] + '.txt', 'w+')
		for track in person['tracks']:
			to_write = track['user'] + ' | ' + track['user_id'] + ' | ' + track['embed'] + ' | ' + track['title'] + ' | ' + track['date'] + ' | ' + track['track_id'] + ' | ' + track['duration']  + "\n"
			fav_file.write(to_write.encode('utf-8'))
		fav_file.close()
	
def get_followers():
	return client.get('/me/followings')
	
@app.route("/", methods=['GET'])
def index():
	raw_data = open('data.txt')
	processed_data = []
	keys = ['title', 'user', 'permalink', 'duration', 'date', 'track_id']
	for line in raw_data:
		processed_data.append(dict(zip(keys, line.split(' | '))))
	try: # if there's a sort provided
		sort = request.args.get('sort')
		newlist = sorted(processed_data, key=lambda k: k[sort])
		return render_template('index.html', tracks=newlist)
	except KeyError:
		pass
 	return render_template('index.html', tracks=processed_data)
	
@app.route('/favorites/')
def favourites():
	track_list = []
	for file in os.listdir("favourites"):
		if file.endswith('.txt'):
			fav_file = open('favourites/' + file)
			keys = ['user', 'user_id', 'permalink', 'title', 'date', 'track_id', 'duration']
			processed_data = []
			for line in fav_file:
				processed_data.append(dict(zip(keys, line.split(' | '))))
			track_list.append({'user' : file[:-4], 'tracks' : processed_data})
	return render_template('favourites.html', tracks=track_list)

@app.route('/embedcode/', methods=['GET'])
def embedcode():
	track = request.args.get('track')
	embed = client.get('/oembed', url=track)
	return embed.html.encode('utf8')

@app.route('/vlc/', methods=['GET'])
def vlc():
	track = request.args.get('track')
	stream = client.get('/tracks/' + track)
	stream_url = client.get(stream.stream_url, allow_redirects=False)
	vlc_player.play(stream_url.location)
	return "playing"

@app.route('/stop_vlc/')
def stop_vlc():
	vlc_player.stop()
	return "stopped"

if __name__ == "__main__":
#	app.debug = True
	app.run(host='0.0.0.0')
