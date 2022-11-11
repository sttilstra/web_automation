import requests
import json


# this function sends a teams message to a predetermined channel
def send_alert(title, message_text):
    url = "<webhookGoesHere>"

    message = {
        "title": f"{title}",
        "text": f"{message_text}"
    }

    response = requests.post(url=url, data=json.dumps(message))
    response.raise_for_status()

    return
