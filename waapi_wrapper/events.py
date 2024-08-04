from pydantic import BaseModel, computed_field, Field, Discriminator, Tag
from typing import Any, Dict, Literal, Annotated, Optional, Union


class WAAPIEvent(BaseModel):
    event: Literal["message", "group_join", "disconnected"]
    raw_data: Dict[str, Any]

    @computed_field  # type: ignore[misc]
    @property
    def instance_id(self) -> str:
        return self.raw_data["instanceId"]


class MessageEvent(WAAPIEvent):
    event: Literal["message"] = "message"  # type: ignore

    @computed_field  # type: ignore[misc]
    @property
    def notifyName(self) -> Optional[str]:
        return self.raw_data.get("data", {}).get("message", {}).get("notifyName")

    @computed_field  # type: ignore[misc]
    @property
    def from_(self) -> Optional[str]:
        return self.raw_data.get("data", {}).get("message", {}).get("from")

    @computed_field  # type: ignore[misc]
    @property
    def to(self) -> Optional[str]:
        return self.raw_data.get("data", {}).get("message", {}).get("to")

    @computed_field  # type: ignore[misc]
    @property
    def message_id(self) -> Optional[str]:
        return (
            self.raw_data.get("data", {})
            .get("message", {})
            .get("id", {})
            .get("_serialized")
        )


class TextMessageEvent(MessageEvent):
    @computed_field  # type: ignore[misc]
    @property
    def message_body(self) -> Optional[str]:
        return self.raw_data.get("data", {}).get("message", {}).get("body")


class VoiceMessageEvent(MessageEvent):
    @computed_field  # type: ignore[misc]
    @property
    def duration(self) -> Optional[int]:
        return self.raw_data.get("data", {}).get("message", {}).get("duration")

    @computed_field  # type: ignore[misc]
    @property
    def mimetype(self) -> Optional[str]:
        return self.raw_data.get("data", {}).get("media", {}).get("mimetype")

    @computed_field  # type: ignore[misc]
    @property
    def media_data(self) -> Optional[str]:
        return self.raw_data.get("data", {}).get("media", {}).get("data")


class GroupJoinEvent(WAAPIEvent):
    event: Literal["group_join"]  # type: ignore

    @computed_field  # type: ignore[misc]
    @property
    def chatId(self) -> Optional[str]:
        return self.raw_data.get("data", {}).get("notification", {}).get("chatId")

    @computed_field  # type: ignore[misc]
    @property
    def author(self) -> Optional[str]:
        return self.raw_data.get("data", {}).get("notification", {}).get("author")


class DisconnectedEvent(WAAPIEvent):
    event: Literal["disconnected"]  # type: ignore


def get_message_type(v: Any) -> str:
    if not isinstance(v, dict):
        raise ValueError("Invalid message data")
    raw_data = v.get("raw_data")

    if not raw_data:
        raise ValueError("Invalid message data. Please provide raw_data")

    type = raw_data.get("data", {}).get("message", {}).get("type", "")
    if type == "chat":
        return "text"
    elif type == "ptt":
        return "voice"
    else:
        raise ValueError(f"Invalid message type: {type}")


MESSAGE_EVENTS = Annotated[
    Union[
        Annotated[TextMessageEvent, Tag("text")],
        Annotated[VoiceMessageEvent, Tag("voice")],
    ],
    Discriminator(get_message_type),
]

ALL_EVENTS = Annotated[
    Union[MESSAGE_EVENTS, GroupJoinEvent, DisconnectedEvent],
    Field(discriminator="event"),
]
