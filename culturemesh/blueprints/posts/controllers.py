from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user
from culturemesh.client import Client
from culturemesh.utils import get_time_ago
from culturemesh.utils import get_network_title
from culturemesh.utils import safe_get_query_arg
from culturemesh.utils import is_logged_in

from culturemesh.blueprints.posts.forms.post_forms import *

from culturemesh.blueprints.posts.config import POST_TITLE_MAX_LEN
from culturemesh.blueprints.posts.config import NUM_REPLIES_TO_SHOW

import flask_login
import http.client as httplib

posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route("/", methods=['GET', 'POST'])
def render_post():

  current_post_id = safe_get_query_arg(request, 'id')

  user_id = current_user.get_id()
  c = Client(mock=False)
  post = c.get_post(current_post_id)

  post['network_title'] = get_network_title(c.get_network(post['id_network']))
  post['username'] = c.get_user(post["id_user"])["username"]
  post['time_ago'] = get_time_ago(post['post_date'])

  # NOTE: this will not show more than the latest 100 replies
  replies = c.get_post_replies(post["id"], NUM_REPLIES_TO_SHOW)
  replies = sorted(replies, key=lambda x: int(x['id']))

  error_msg = None

  for reply in replies:
      reply['username'] = c.get_user(reply["id_user"])["username"]
      reply['time_ago'] = get_time_ago(reply['reply_date'])

  if request.method == 'GET':
    pass
  elif not is_logged_in(current_user):
    return redirect(
        url_for('render_login_page')
    )
  else:
    data = request.form
    form_submitted = CreatePostReplyForm(request.form)
    if form_submitted.validate():
      post_reply_content = data['post_reply_content']

      reply = {
        'id_parent': current_post_id,
        'id_user': user_id,
        'id_network': post['id_network'],
        'reply_text': post_reply_content
      }

      c.create_post_reply(current_user, current_post_id, reply)
      return redirect(
        url_for('posts.render_post') + "?id=%s" % str(current_post_id)
      )
    else:
      error_msg = "Oops. An error occurred. Did you forget to type a reply \
        before submitting?"


  new_form = CreatePostReplyForm()

  return render_template(
    'post.html',
    post=post,
    replies=replies,
    num_replies=len(replies),
    curr_user_id=user_id,
    form=new_form,
    error_msg=error_msg
  )

@posts.route("/edit/", methods=["GET", "POST"])
@flask_login.login_required
def edit_post():
  c = Client(mock=False)
  post_id = safe_get_query_arg(request, 'id')
  post = c.get_post(post_id)
  post['network_title'] = get_network_title(c.get_network(post['id_network']))

  if post['id_user'] != current_user.id:
    abort(httplib.NOT_FOUND)

  edit_post_form = EditPostForm()
  edit_post_form.content.process_data(post['post_text'])
  error_msg = None

  if request.method == 'GET':
      pass
  else:
    data = request.form
    form_submitted = EditPostForm(request.form)
    if form_submitted.validate():
      post_text = data['content']

      post = {
        'id': post_id,
        'id_user': current_user.id,
        'id_network': post['id_network'],
        'post_text': post_text,
      }

      c.update_post(current_user, post)
      return redirect(
        url_for('posts.render_post') + "?id=%s" % str(post_id)
      )
    else:
      error_msg = "Oops. An error ocurred. Keep in mind posts can't be empty."

  return render_template(
    'edit_post.html',
    edit_post_form=edit_post_form,
    is_post_reply=False,
    post=post,
    network_title=post['network_title'],
    current_user=current_user,
    error_msg=error_msg
  )

@posts.route("/reply/edit/", methods=["GET", "POST"])
@flask_login.login_required
def edit_reply():
  c = Client(mock=False)
  post_reply_id = safe_get_query_arg(request, 'id')
  post_reply = c.get_post_reply(post_reply_id)
  id_parent = post_reply['id_parent']
  if post_reply['id_user'] != current_user.id:
    abort(httplib.NOT_FOUND)
  edit_post_reply_form = EditPostForm()

  post_reply['network_title'] = get_network_title(
    c.get_network(post_reply['id_network'])
  )

  edit_post_reply_form.content.process_data(post_reply['reply_text'])
  error_msg = None

  if request.method == 'GET':
      pass
  else:
    data = request.form
    form_submitted = EditPostForm(request.form)
    if form_submitted.validate():
      reply_text = data['content']

      post_reply = {
        'id': post_reply_id,
        'reply_text': reply_text,
      }

      c.update_post_reply(current_user, id_parent, post_reply)
      return redirect(
        url_for('posts.render_post') + "?id=%s" % str(id_parent)
      )
    else:
      error_msg = "Oops. An error ocurred. Keep in mind posts can't be empty."

  return render_template(
    'edit_post.html',
    edit_post_form=edit_post_reply_form,
    is_post_reply=True,
    post=post_reply,
    network_title=post_reply['network_title'],
    current_user=current_user,
    error_msg=error_msg
  )

@posts.route("/ping/")
@flask_login.login_required
def ping():
  c = Client(mock=False)
  return c.ping_post()
