from waapi_wrapper.webhook import handle_waapi_event
from waapi_wrapper.events import (
    DisconnectedEvent,
    GroupJoinEvent,
    TextMessageEvent,
    VoiceMessageEvent,
)
import json


def test_handle_message_event():
    raw_data_message = """
    {
        "event": "message",
        "instanceId": "33",
        "data": {
            "message": {
                "id": {
                    "fromMe": false,
                    "remote": "50611223344@c.us",
                    "id": "V6B05T14AAIWWPEL7MJC",
                    "_serialized": "false_50611223344@c.us_V6B05T14AAIWWPEL7MJC"
                },
                "body": "Hey. I am fine. Thanks. Your test message was successful ;)",
                "type": "chat",
                "timestamp": 1669994807,
                "from": "50611223344@c.us",
                "to": "50611223355@c.us",
                "notifyName": "John"
            }
        }
    }
    """
    event = handle_waapi_event(json.loads(raw_data_message))
    assert isinstance(event, TextMessageEvent)
    assert event.instance_id == "33"
    assert event.notifyName == "John"
    assert (
        event.message_body == "Hey. I am fine. Thanks. Your test message was successful ;)"
    )
    assert event.from_ == "50611223344@c.us"
    assert event.to == "50611223355@c.us"


def test_voice_message_event():
    raw_data_voice_message = json.load(open("tests/data/audio_message.json"))
    event = handle_waapi_event(raw_data_voice_message)
    assert isinstance(event, VoiceMessageEvent)
    assert event.mimetype == "audio/ogg; codecs=opus"
    assert event.duration == "5"
    assert event.media_data != ""


def test_disconnected_event():
    raw_data_disconnected = """
    {
        "event": "disconnected",
        "instanceId": "12345",
        "data": {}
    }
    """
    event = handle_waapi_event(json.loads(raw_data_disconnected))
    assert isinstance(event, DisconnectedEvent)
    assert event.instance_id == "12345"


def test_group_join_event():
    raw_data_group_join = """
    {
        "event": "group_join",
        "instanceId": "12345",
        "data": {
            "notification": {
                "id": {
                    "fromMe": false,
                    "remote": "120363279485465785@g.us",
                    "id": "21781889331718643453",
                    "participant": "3197010267647@c.us"
                },
                "body": null,
                "type": "add",
                "timestamp": 1718643453,
                "chatId": "120363279485465785@g.us",
                "author": "31633767338@c.us",
                "recipientIds": [
                    "3197010267647@c.us"
                ]
            }
        }
    }
    """
    event = handle_waapi_event(json.loads(raw_data_group_join))
    assert isinstance(event, GroupJoinEvent)
    assert event.instance_id == "12345"
    assert event.author == "31633767338@c.us"
