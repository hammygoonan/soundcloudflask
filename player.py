'''
	Player control class
	# @todo merge vlc_player into this
'''

from track import track
from vlc_player import vlcPlayer
from connection_manager import connectionManager
class player(object):
	def __init__(self):
		# @todo Use track object to manage current track, such as title
# 		self.track = track()
# 		self.track.test()
		self.track = '';
		self.vlc_player = vlcPlayer()
		connection_manager = connectionManager()
		self.client = connection_manager.client

	def play(self, track_id):
		# Play new track
		if track_id:
			track = self.client.get('/tracks/' + track_id)
			self.track = track
		# Play current/last track
		else:
			track = self.track

		print '=' * 20
		print track.title
		print '=' * 20

		stream_url = self.client.get(track.stream_url, allow_redirects=False)
		self.vlc_player.play(stream_url.location)
		return stream_url.location

	def stop(self):
		self.vlc_player.stop()

	def pause(self):
		self.vlc_player.pause()
