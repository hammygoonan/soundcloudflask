class storage(object):
	def __init__(self):
		connection_manager = connectionManager()
		self.client = connection_manager.client

def update(self):
	following_ids = get_followers()
	tracks = ''
	errors = open('errors.txt', 'w+')
	for user in following_ids:
		user_tracks = self.client.get('/tracks/', user_id=user.id, limit=30, embeddable_by='me')
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
		tracks = self.client.get('/users/' + str(person.id) + '/favorites')
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
	return self.client.get('/me/followings')