from pydantic import BaseModel, Field, computed_field
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
    def message_body(self) -> Optional[str]:
        return self.raw_data.get("data", {}).get("message", {}).get("body")

    @computed_field  # type: ignore[misc]
    @property
    def from_(self) -> Optional[str]:
        return self.raw_data.get("data", {}).get("message", {}).get("from")

    @computed_field  # type: ignore[misc]
    @property
    def to(self) -> Optional[str]:
        return self.raw_data.get("data", {}).get("message", {}).get("to")


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


ALL_EVENTS = Annotated[
    Union[MessageEvent, GroupJoinEvent, DisconnectedEvent],
    Field(discriminator="event"),
]
