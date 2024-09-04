import json
import yaml
from datetime import datetime

def serialize_conversation(conversation):
    return json.dumps(conversation)

def deserialize_conversation(conversation_json):
    return json.loads(conversation_json)

def format_timestamp(timestamp):
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")