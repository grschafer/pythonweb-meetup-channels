from channels.routing import route


channel_routing = [
    route("websocket.connect", "core.consumers.ws_connect"),
    route("websocket.receive", "core.consumers.ws_message"),
    route("websocket.disconnect", "core.consumers.ws_disconnect"),
]
