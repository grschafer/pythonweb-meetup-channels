import json

from channels import Group
from channels.sessions import channel_session, enforce_ordering
from channels.auth import channel_session_user, channel_session_user_from_http

# - buddy list


# Connected to websocket.connect
@enforce_ordering(slight=True)
@channel_session_user_from_http
def ws_connect(message):
    # Work out room name from path (ignore slashes)
    room = message.content['path'].strip('/').replace('/', '-')
    # Save room in session and add us to the group
    message.channel_session['room'] = room

    Group("chat-%s" % room).add(message.reply_channel)
    Group("chat-%s" % room).send({
        "text": json.dumps({
            "username": None,
            "message": "{} joined".format(message.user.username),
            "styles": "system",
            "type": "chat",
        }),
    })


# Connected to websocket.receive
@enforce_ordering(slight=True)
@channel_session
@channel_session_user
def ws_message(message):
    payload = json.loads(message['text'])
    Group("chat-%s" % message.channel_session['room']).send({
        "text": json.dumps({
            "username": message.user.username,
            "message": payload['data'],
            "type": payload['type'],
        }),
    })


# Connected to websocket.disconnect
@enforce_ordering(slight=True)
@channel_session
@channel_session_user
def ws_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
    Group("chat-%s" % message.channel_session['room']).send({
        "text": json.dumps({
            "username": None,
            "message": "{} left".format(message.user.username),
            "styles": "system",
            "type": "chat",
        }),
    })
