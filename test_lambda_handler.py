from json import load
from file_validation import lambda_handler

with open("event.json", "r") as f:
    event = load(f)

lambda_handler(event, None)
