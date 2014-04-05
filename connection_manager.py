'''
	Connection manage for SoundCloud
	
	Handles the connection/interactin with SoundCloud
'''
from connection import ScDetails
import soundcloud
class connectionManager(object):
	def __init__(self):
		details = ScDetails()
		self.client = soundcloud.Client(
		    client_id=details.client_id,
		    client_secret=details.client_secret,
		    username=details.username,
		    password=details.password,
		)
		