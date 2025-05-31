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
def get_events():
    """Get recent events as JSON"""
    limit = request.args.get('limit', 10, type=int)
    events = get_recent_events(limit=limit)
    return jsonify(events)

@bp.route("/debug/events", methods=['GET'])
def debug_events():
    """Debug view of all events with formatting"""
    events = get_recent_events(limit=50)
    html = "<h1>Recent Events</h1>"
    html += f"<p>Total events found: {len(events)}</p><ul>"
    for event in events:
        html += f"<li><strong>{event.get('timestamp', 'No timestamp')}</strong>: {event.get('message', 'No message')}</li>"
    html += "</ul>"
    return html

@bp.route("/debug/test-insert", methods=['POST'])
def test_insert():
    """Test inserting a dummy event"""
    from datetime import datetime
    test_msg = f"Test event inserted at {datetime.utcnow()}"
    test_timestamp = datetime.utcnow()
    
    try:
        insert_event(test_msg, test_timestamp)
        return jsonify({"success": True, "message": "Test event inserted", "inserted": test_msg})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route("/debug/stats", methods=['GET'])
def debug_stats():
    """Show database statistics"""
    from .models import get_event_stats
    stats = get_event_stats()
    return jsonify(stats)

@bp.route("/webhook", methods=["POST", "OPTIONS"])
def webhook():
    print(f"Webhook received: {request.method} method")  # Debug line
    
    if request.method == "OPTIONS":
        # Handle CORS preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,X-Github-Event')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    
    # Handle POST request
    event = request.headers.get('X-Github-Event')
    payload = request.json
    
    print(f"GitHub event: {event}")  # Debug line
    
    if not payload:
        return jsonify({'error': 'No payload received'}), 400
    
    timestamp = datetime.utcnow()
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')
    
    try:
        if event == "push":
            msg = format_push(payload)
            insert_event(msg, timestamp)
            print(f"✅ Inserted push event: {msg}")  # Debug line
        elif event == 'pull_request':
            action = payload.get('action')
            pr = payload.get('pull_request', {})
            
            if not pr:
                return jsonify({'error': 'Invalid pull request payload'}), 400
                
            author = pr.get('user', {}).get('login', 'Unknown')
            from_branch = pr.get('head', {}).get('ref', 'unknown')
            to_branch = pr.get('base', {}).get('ref', 'unknown')
            
            if action == 'opened':
                msg = f'{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp_str}'
                insert_event(msg, timestamp)
                print(f"✅ Inserted PR opened: {msg}")  # Debug line
            elif action == 'closed' and pr.get('merged', False):
                msg = f'{author} merged branch {from_branch} to {to_branch} on {timestamp_str}'
                insert_event(msg, timestamp)
                print(f"✅ Inserted PR merged: {msg}")  # Debug line
        else:
            print(f"Unhandled GitHub event: {event}")
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    
    return jsonify({'status': 'success', 'event': event}), 200