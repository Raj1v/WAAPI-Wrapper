# WAAPI Wrapper

The WAAPI Wrapper is a Python library designed to simplify the integration with the [WAAPI WhatsApp API](https://waapi.app/), making it easier to send messages, manage contacts, and automate responses on WhatsApp.

## Installation


```bash
pip install git+https://github.com/Raj1v/WAAPI-Wrapper
```

## Usage

Here are a couple of examples of how you can use the WAAPI Package to interact with WhatsApp:

### Sending a Message

```python
from waapi_wrapper.webhook import send_message

send_message("Hello, world!", recipient_id="1234567890")
```

### Webhook Event Handling

This section provides a simple example of how to set up a webhook to receive messages via WhatsApp. We'll use the Flask framework to create a small web server that listens for incoming WhatsApp messages.

```python
from flask import Flask, request, jsonify
from waapi_wrapper.webhook import handle_waapi_event

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Parse the incoming JSON data
    request_data = request.get_json()
    
    # Handle the WhatsApp API event
    event = handle_waapi_event(request_data)

    # Access some data from the event
    message_body = event.message_body
    sender = event.sender

    # Do something with the data
    print(f"Received message from {sender}: {message_body}")

    # Respond to the webhook
    return jsonify({
        'status': 'success',
        'message_body': message_body,
        'sender': sender
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

```

## Contributing
Contributions are welcome! Please feel free to fork the repository, make your changes, and submit a pull request. We appreciate your input and will review each PR carefully and discuss potential changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


