# babur

Webhook service to handle requests from Dialogflow.com. At the moment only supports interactions with garage door.

# connecting to Raspberry Py

Upon receiving proper webhook request, babur will set GPIO PIN 25 to HIGH for a bit.