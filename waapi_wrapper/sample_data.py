from waapi_wrapper.webhook import handle_waapi_event
from waapi_wrapper.events import (
    TextMessageEvent,
    VoiceMessageEvent,
)
import json
from importlib import resources as impresources
from waapi_wrapper import data


def sample_text_message_event() -> TextMessageEvent:
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
    if not isinstance(event, TextMessageEvent):
        raise ValueError("Event is not an instance of TextMessageEvent")
    return event


def sample_voice_message_event() -> VoiceMessageEvent:
    # with pkg_resources.path("waapi_wrapper", "test/data/audio_message.json") as path:
    data_file = impresources.files(data) / "audio_message.json"
    with data_file.open("r") as f:
        raw_data_voice_message = json.load(f)

    event = handle_waapi_event(raw_data_voice_message)
    assert isinstance(event, VoiceMessageEvent)
    return event
