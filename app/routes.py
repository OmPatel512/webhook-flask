from flask import Blueprint, request, jsonify, render_template
from .models import insert_event, get_recent_events
from .utils import format_push
from datetime import datetime

bp = Blueprint("main", __name__)

@bp.route("/", methods=['GET'])
def index():
    events = get_recent_events(limit=10)
    return render_template("index.html", events=events)

@bp.route("/events", methods=['GET'])
def events():
    return jsonify(get_recent_events(limit=10))

@bp.route("/webhook", methods=["POST"])
def webhook():
    event = request.headers.get('X-Github-Event')
    payload = request.json
    
    timestamp = datetime.utcnow()
    
    if event == "push":
        msg = format_push(payload)
        insert_event(msg, timestamp)
    elif event == 'pull_request':
        action = payload['action']
        author = payload['pull_request']['user']['login']
        from_branch = payload['pull_request']['head']['ref']
        to_branch = payload['pull_request']['base']['ref']
        if action == 'opened':
            msg = f'{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}'
            insert_event(msg, timestamp)
        elif action == 'closed' and payload['pullrequest']['merged']:
            msg = f'{author} merged branch {from_branch} to {to_branch} on {timestamp}'
            insert_event(msg, timestamp)
    
    return "", 200

@bp.route('/events', methods=['GET'])
def get_events():
    events = get_recent_events()
    return jsonify(events)
