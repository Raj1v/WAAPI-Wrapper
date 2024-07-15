import requests
from os import getenv
from typing import Dict, Any, Optional

BASE_URL = "https://waapi.app/api/v1/instances"
SEND_MESSAGE_ENDPOINT = "client/action/send-message"
SEND_MEDIA_ENDPOINT = "client/action/send-media"
SEND_VCARD_ENDPOINT = "client/action/send-vcard"
GET_ALL_CHATS_ENDPOINT = "client/action/get-chats"
GET_GROUP_INFO_ENDPOINT = "client/action/get-group-info"
SEND_SEEN_ENDPOINT = "client/action/send-seen"


def _construct_api_url(instance_id: str, endpoint: str):
    """Construct the API URL."""
    return f"{BASE_URL}/{instance_id}/{endpoint}"


def send_message(message: str, chat_id: str, instance_id: str) -> requests.Response:
    payload = {"message": message}

    response = _send_request(
        chat_id=chat_id,
        instance_id=instance_id,
        endpoint=SEND_MESSAGE_ENDPOINT,
        payload=payload,
    )
    return response


def send_seen(chat_id: str, instance_id: str) -> requests.Response:
    return _send_request(
        chat_id=chat_id, instance_id=instance_id, endpoint=SEND_SEEN_ENDPOINT
    )


def _send_request(
    chat_id: str,
    instance_id: str,
    endpoint: str,
    payload: Optional[Dict[str, Any]] = None,
) -> requests.Response:
    """Send a message to a WhatsApp number."""
    url = _construct_api_url(instance_id=instance_id, endpoint=endpoint)

    if not chat_id.endswith("@c.us") and not chat_id.endswith("@g.us"):
        raise ValueError("chat_id must end with @c.us or @g.us for groups")

    if getenv("WAAPI_API_KEY") is None:
        raise ValueError("WAAPI_API_KEY environment variable is not set")

    if payload is None:
        payload = {}

    payload["chatId"] = chat_id

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {getenv('WAAPI_API_KEY')}",
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"WAAPI request failed. Status code: {response.status_code}. "
            f"Response: {response.text}"
        )
    return response
