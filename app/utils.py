from datetime import datetime

def format_push(payload):
    author = payload['pusher']['name']
    branch = payload['ref'].split('/')[-1]
    timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
    return f'{author} pushed to {branch} on {timestamp}'
