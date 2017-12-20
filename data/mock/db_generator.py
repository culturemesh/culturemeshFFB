#
# For dev use only!
#

import sys
import json
import random
from faker import Faker

if hasattr(sys, 'real_prefix'):
	print("This should not be run from inside a virtualenv")
	exit()

""" Creates a randomly generated mock database """

def make_users(faker, num_users):
	"""
	Makes NUM_USERS fake users and dumps them to a json file.
	"""

	user_id_ctr = 1
	users = []
	for _ in range(num_users):
		user = {}
		user['user_id'] = user_id_ctr
		user['username'] = faker.user_name()
		user['firstName'] = faker.first_name()
		user['lastName'] = faker.last_name()
		user['email'] = faker.email()
		user['registerDate'] = str(faker.past_datetime(start_date="-1000d", tzinfo=None))
		user['role'] = 1 # Not sure
		user['last_login'] = str(faker.past_datetime(start_date="-7d", tzinfo=None))
		user['gender'] = random.choice(['male', 'female'])
		user['about_me'] = faker.text(max_nb_chars=200, ext_word_list=None)
		user['confirmed'] = random.choice([True, False])
		user['act_code'] = "IDK"
		user['img_link'] = faker.image_url(width=None, height=None)
		user['fp_code'] = "IDK"

		user_id_ctr += 1
		users.append(user)

	with open('db_mock_users.json', 'w+') as outfile:
		json.dump(users, outfile)

def make_posts(faker, num_posts, userIds, networkIds):
	"""
	Makes NUM_POSTS fake posts and dumps them to a json file.
	Assigns post ownership randomly to userIds in userIds.
	"""

	posts_id_ctr = 1
	posts = []
	for _ in range(num_posts):
		post = {}
		post['id'] = posts_id_ctr
		post['user_id'] = random.choice(userIds)
		post['network_id'] = random.choice(networkIds)
		post['post_date'] = str(faker.past_datetime(start_date="-500d", tzinfo=None))
		post['post_text'] = faker.text(max_nb_chars=250, ext_word_list=None)
		post['post_class'] = 0
		post['post_original'] = "Not sure what this field is"
		post['vid_link'] = faker.image_url(width=None, height=None)
		post['img_link'] = faker.image_url(width=None, height=None)

		posts_id_ctr += 1
		posts.append(post)

	with open('db_mock_posts.json', 'w+') as outfile:
		json.dump(posts, outfile)

def make_events(faker, num_events, userIds, networkIds):
	"""
	Makes NUM_EVENTS fake events and dumps them to a json file.
	Assigns event ownership randomly to userIds in userIds, as 
	well as user attendance.
	"""

	events = []
	for i in range(1, num_events + 1):
		event = {}
		event['id'] = i
		event['network_id'] = random.choice(networkIds)
		event['host_id'] = random.choice(userIds)
		event['date_created'] = str(faker.past_datetime(start_date="-100d", tzinfo=None))
		event['event_date'] = str(faker.past_datetime(start_date="-25d", tzinfo=None))
		event['title'] = faker.catch_phrase()
		event['address_1'] = faker.address()
		event['address_2'] = faker.address()
		event['location'] = (faker.country(), faker.city(), faker.city())
		event['description'] = faker.text(max_nb_chars=250, ext_word_list=None)

		events.append(event)

	with open('db_mock_events.json', 'w+') as outfile:
		json.dump(events, outfile)

# Just one network to which all users belong for now. 
def create_culturemesh_db(num_users=5, num_networks=1, num_events=4, num_posts=5):
	"""
	Makes a fake culture mesh database in the form of json files. 
	"""

	faker = Faker()
	faker.seed(1)
	
	# Create some Users
	make_users(faker, num_users)

	# Create some Networks
		# TODO

	# Create some Events
	make_events(faker, num_events, range(1, num_users + 1), range(1, num_networks + 1))

	# Create some Posts
	make_posts(faker, num_posts, range(1, num_users + 1), range(1, num_networks + 1))

if __name__ == "__main__":
	create_culturemesh_db()