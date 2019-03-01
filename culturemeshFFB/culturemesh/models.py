"""
Contains the CultureMesh user class.

Add any other CultureMesh objects here as needed.
"""
import json
import time

from flask_login import UserMixin
from utils import parse_date

class User(object):
	"""
	A CultureMesh user. This object is available to views
	via the 'current_user' variable for the current logged-in session.
	"""

	def __init__(self,
				 user_dict,
				 api_token=None):
		self.id = int(user_dict['id'])
		self.username = user_dict['username']
		self.first_name = user_dict['first_name']
		self.last_name = user_dict['last_name']
		self.register_date = parse_date(user_dict['register_date'])
		self.role = int(user_dict['role'])
		self.gender = user_dict['gender']
		self.confirmed = user_dict['confirmed']
		self.act_code = user_dict['act_code']
		self.img_link = user_dict['img_link']
		self.fp_code = user_dict['fp_code']
		self.about_me = user_dict['about_me']
		self.last_login = parse_date(user_dict['last_login'])

		if api_token:
			self.token_ = api_token['token']
			self.token_expiration_epoch_ = api_token['token_expiration_epoch']
		elif 'token_' in user_dict and 'token_expiration_epoch_' in user_dict:
			self.token_ = user_dict['token_']
			self.token_expiration_epoch_ = int(
				user_dict['token_expiration_epoch_']
			)

	def get_id(self):
		"""The user 'id' is actually just
		a serialized version of the user object itself. This allows
		us to persist the session token without a user store, and it
		prevents extra calls to the API.

		NOTE: this may be too inefficient in the long run.  When ready,
		session data should be moved to something like a Redis store that
		maps user_id to user info, including session data.
		"""
		self_dict = self.as_dict
		for k in self_dict:
			self_dict[k] = str(self_dict[k])
		return json.dumps(self_dict)

	def secs_til_token_expiration(self):
		"""
		How many seconds before this user's
		CultureMesh API token expires.
		"""
		return self.token_expiration_epoch_ - int(time.time())

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	@property
	def is_authenticated(self):
		"""
		True if the user's API token is valid.
		"""
		return self.secs_til_token_expiration() > 0

	@property
	def api_token(self):
		"""
		Return this user's CultureMesh API token.
		"""
		return self.token_

	@property
	def as_dict(self):
		"""Return object as a dictionary.
		"""
		return vars(self)
