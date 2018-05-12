from flask import Blueprint, render_template, request
from culturemesh.client import Client
import flask_login
from flask_login import current_user

posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route("/")
@flask_login.login_required
def render_post():
  current_post_id = request.args.get('id')
  user_id = current_user.get_id()
  c = Client(mock=True)
  fake_post = c.get_post(current_post_id)
  post_text_arr = fake_post["post_text"].split(" ")
  title = ""
  for i in range(10):
      title += post_text_arr[i] + " "
  title += "..."
  num_replies = 1
  replies = c.get_post_replies(fake_post["id"], num_replies)
  usernames = []
  for reply in replies:
      username = c.get_user(reply["user_id"])["username"]
      usernames.append(username)
  return render_template('post.html', title=title, post=fake_post, replies=replies, reply_usernames=usernames, num_replies=num_replies)

@posts.route("/ping")
@flask_login.login_required
def ping():
  c = Client()
  return c.ping_post()
