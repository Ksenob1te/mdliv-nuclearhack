import requests
import json
import logging

logger = logging.getLogger(__name__)

def send_to_neuro(url: str, webhook: str, prompt: str, ray_id: str, system: str):
    try:
        requests.post(url=url, headers={'Content-Type': 'application/json'},
                           data=json.dumps({"content": prompt, "ray_id": ray_id, "webhook": webhook, "system": system}))
    except:
        logger.error("Unable to send request to "+url)

def send_to_telegram(url: str, response: str, ray_id: str):
    try:
        requests.post(url=url, headers={'Content-Type': 'application/json'},
                           data=json.dumps({"text": response, "ray_id": ray_id}))
    except:
        logger.error("Unable to send request to "+url)