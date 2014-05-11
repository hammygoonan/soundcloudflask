'''
	Interface for VLC binding
	# @todo Merge into Player object
'''
import vlc
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

	def pause(self):
		self.player.pause()
