from waapi_wrapper.sample_data import sample_text_message_event, sample_voice_message_event
from waapi_wrapper.events import TextMessageEvent, VoiceMessageEvent


def test_sample_text_message_event():
    event = sample_text_message_event()
    assert isinstance(event, TextMessageEvent)


def test_sample_voice_message_event():
    event = sample_voice_message_event()
    assert isinstance(event, VoiceMessageEvent)
