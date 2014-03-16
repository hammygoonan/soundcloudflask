#!/usr/bin/python

from flask import Flask, request, 	render_template
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
	following = client.get('/me/followings')
	following_ids = []
	for person in following:
	 	following_ids.append(person.id)
	tracks = ''
	errors = open('errors.txt', 'w+')
	for user in following_ids:
		user_tracks = client.get('/tracks/', user_id=user, limit=10, embeddable_by='me')
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


if __name__ == "__main__":
	app.debug = True
	app.run()

# raw_data = open('data.txt')
# processed_data = []
# keys = ['title', 'user', 'permalink', 'embed', 'duration', 'date']
# for line in raw_data:
# 	print line.split(' | ')
# 	processed_data.append(dict(zip(keys, line.split(' | '))))
