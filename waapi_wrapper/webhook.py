from typing import Any
from pydantic import (
    TypeAdapter,
)

from waapi_wrapper.events import (
    ALL_EVENTS,
    WAAPIEvent,
)


def handle_waapi_event(request_json: Any) -> WAAPIEvent:
    """
    Handles incoming WAAPI events by validating and constructing an event object.

    Args:
        request_json (dict): A dictionary containing the event data.

    Returns:
        WAAPIEvent: An event object representing the WhatsApp API event.
    """
    event = request_json.get("event")
    data = {
        "event": event,
        "raw_data": request_json,
    }
    adapter: TypeAdapter = TypeAdapter(ALL_EVENTS)
    return adapter.validate_python(data)
