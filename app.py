from flask import Flask, request, jsonify, render_template
from datetime import datetime
import uuid, json, os

app = Flask(__name__)
EVENTS_FILE = 'events.json'

# Load events
if os.path.exists(EVENTS_FILE):
    with open(EVENTS_FILE, 'r') as f:
        events = json.load(f)
else:
    events = []

def save_events():
    with open(EVENTS_FILE, 'w') as f:
        json.dump(events, f, indent=2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-events', methods=['GET'])
def get_events():
    now = datetime.now()
    upcoming_events = []
    for event in events:
        event_time = datetime.strptime(f"{event['date']} {event['time']}", "%Y-%m-%d %H:%M")
        if event_time >= now or (now - event_time).days <= 1:
            upcoming_events.append(event)
    return jsonify({'status': 'success', 'events': upcoming_events})

@app.route('/add-event', methods=['POST'])
def add_event():
    data = request.json
    name = data.get('name')
    date = data.get('date')
    time = data.get('time', '23:59')

    if not name or not date:
        return jsonify({'status': 'error', 'message': 'name and date are required'}), 400

    try:
        event_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        if event_dt < datetime.now():
            return jsonify({'status': 'error', 'message': 'Event cannot be in the past'}), 400
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid date or time format'}), 400

    event_id = str(uuid.uuid4())
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events.append({'id': event_id, 'name': name, 'date': date, 'time': time, 'created_at': created_at})
    save_events()
    return jsonify({'status': 'success', 'message': 'Event added!', 'id': event_id})

@app.route('/delete-event', methods=['POST'])
def delete_event():
    data = request.json
    event_id = data.get('id')
    global events
    events = [e for e in events if e['id'] != event_id]
    save_events()
    return jsonify({'status': 'success', 'message': 'Event deleted!'})

@app.route('/update-event', methods=['POST'])
def update_event():
    data = request.json
    event_id = data.get('id')
    new_name = data.get('newName')
    new_date = data.get('newDate')
    new_time = data.get('newTime', '23:59')

    if not event_id or not new_name or not new_date:
        return jsonify({'status': 'error', 'message': 'All fields required'}), 400

    try:
        datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid date or time format'}), 400

    for e in events:
        if e['id'] == event_id:
            e['name'] = new_name
            e['date'] = new_date
            e['time'] = new_time
            save_events()
            return jsonify({'status': 'success', 'message': 'Event updated!'})

    return jsonify({'status': 'error', 'message': 'Event not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
