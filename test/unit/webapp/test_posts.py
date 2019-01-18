from test.unit.webapp import client
import mock
from mock import call


view_post_post = {'id': 626, 'id_network': 1, 'id_user': 157, 'img_link': None,
                  'post_class': 'o',
                  'post_date': 'Sun, 26 Aug 2018 22:31:04 GMT',
                  'post_original': None,
                  'post_text': "Hi everyone! I'm hoping to move here soon, but "
                               "I'd like to get a better sense of the local "
                               "community. Would anyone be willing to take a "
                               "few minutes to talk with me about there "
                               "experiences living here, particularly after "
                               "leaving home? Thanks!\n", 'vid_link': None}
view_post_net = {'city_cur': 'Palo Alto', 'city_origin': None,
                 'country_cur': 'United States',
                 'country_origin': 'United States',
                 'date_added': 'Tue, 12 Jan 2016 05:51:19 GMT', 'id': 1,
                 'id_city_cur': 332851, 'id_city_origin': None,
                 'id_country_cur': 47228, 'id_country_origin': 47228,
                 'id_language_origin': None, 'id_region_cur': 55833,
                 'id_region_origin': 56020, 'img_link': None,
                 'language_origin': None, 'network_class': 'rc',
                 'region_cur': 'California', 'region_origin': 'Michigan',
                 'twitter_query_level': 'A'}
view_post_replies = [{'id': 465, 'id_network': 1, 'id_parent': 626,
                      'id_user': 157,
                      'reply_date': 'Sun, 02 Dec 2018 18:20:40 GMT',
                      'reply_text': "This is a test reply, but I'd be happy "
                                    "to talk to you.  "},
                     {'id': 461, 'id_network': 1, 'id_parent': 626,
                      'id_user': 172,
                      'reply_date': 'Tue, 18 Sep 2018 16:09:13 GMT',
                      'reply_text': 'This is another test reply.  Do not mind '
                                    'me, but welcome to Palo Alto! Hope you '
                                    'like it here'},
                     {'id': 460, 'id_network': 1, 'id_parent': 626,
                      'id_user': 171,
                      'reply_date': 'Tue, 18 Sep 2018 16:07:16 GMT',
                      'reply_text': 'This is only a test reply.  But I am sure '
                                    'someone else here can help you out.'}]


def mock_client_get_user(id):
    users = [
        {'about_me': "I'm from Michigan",
         'act_code': '764efa883dda1e11db47671c4a3bbd9e',
         'company_news': None, 'confirmed': 0,
         'events_interested_in': None, 'events_upcoming': None,
         'first_name': 'c', 'fp_code': None, 'gender': 'n', 'id': 157,
         'img_link': 'https://www.culturemesh.com/user_images/null',
         'last_login': '0000-00-00 00:00:00', 'last_name': 's',
         'network_activity': None,
         'register_date': 'Sun, 02 Dec 2018 16:33:20 GMT', 'role': 0,
         'username': 'cs'},
        {'about_me': 'I like to cook and watch movies.  I recently made some '
                     'clam chowder and it was amazing :D.  Originally from '
                     'Mexico, now living in the bay area.',
         'act_code': '', 'company_news': None, 'confirmed': 0,
         'events_interested_in': None, 'events_upcoming': None,
         'first_name': 'Alan', 'fp_code': None, 'gender': None, 'id': 171,
         'img_link': None, 'last_login': '0000-00-00 00:00:00',
         'last_name': 'Last name', 'network_activity': None,
         'register_date': 'Thu, 20 Sep 2018 10:30:04 GMT', 'role': 0,
         'username': 'aefl'},
        {'about_me': 'Live and learn', 'act_code': '', 'company_news': None,
         'confirmed': 0, 'events_interested_in': None, 'events_upcoming': None,
         'first_name': 'Alan 2.0', 'fp_code': None, 'gender': None, 'id': 172,
         'img_link': None, 'last_login': '0000-00-00 00:00:00',
         'last_name': 'Lastname', 'network_activity': None,
         'register_date': 'Wed, 19 Sep 2018 22:15:15 GMT', 'role': 0,
         'username': 'aefl2'}
    ]
    for user in users:
        if user['id'] == id:
            return user
    raise ValueError("User ID {} is unknown to mock_client_get_user".format(id))


@mock.patch('culturemesh.blueprints.posts.controllers.Client.get_post',
            return_value=view_post_post)
@mock.patch('culturemesh.blueprints.posts.controllers.Client.get_network',
            return_value=view_post_net)
@mock.patch('culturemesh.blueprints.posts.controllers.Client.get_user',
            side_effect=mock_client_get_user)
@mock.patch('culturemesh.blueprints.posts.controllers.Client.get_post_replies',
            return_value=view_post_replies)
def test_view_post(replies, user, net, post, client):
    result = client.get('/post/?id=626')
    html = result.data.decode()

    # Check that replies are displayed
    assert "This is another test reply.  Do not mind me, " in html
    assert 'This is only a test reply.' in html

    # Check that reply author username displayed
    assert 'aefl' in html

    # Check that post text displayed
    assert 'Hi everyone!' in html

    # Check that post author username displayed
    assert 'cs' in html

    # Check that network name displayed
    assert 'From Michigan, United States in Palo Alto, California, ' \
           'United States' in html

    replies.assert_called_with(626, 100)
    user.assert_has_calls([call(157), call(171), call(172), call(157)],
                          any_order=False)
    net.assert_called_with(1)
    post.assert_called_with('626')
