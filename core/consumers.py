import json

from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

# - make a chat/([A-z0-9]) url and page where chat actually happens
# - routing for chat room
# - enforce slight ordering
# - join/leave message


# Connected to websocket.connect
@channel_session_user_from_http
def ws_connect(message):
    # Work out room name from path (ignore slashes)
    room = message.content['path'].strip("/")
    # Save room in session and add us to the group
    message.channel_session['room'] = room

    Group("chat-%s" % room).add(message.reply_channel)


# Connected to websocket.receive
@channel_session
@channel_session_user
def ws_message(message):
    Group("chat-%s" % message.channel_session['room']).send({
        "text": json.dumps({
            "username": message.user.username,
            "message": message['text'],
        }),
    })


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
