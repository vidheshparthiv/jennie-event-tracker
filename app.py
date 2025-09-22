from flask import Flask, request, jsonify, render_template
from datetime import datetime
import uuid

app = Flask(__name__)

events = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-events', methods=['GET'])
def get_events():
    return jsonify(events)

@app.route('/add-event', methods=['POST'])
def add_event():
    data = request.json
    event_name = data.get('name')
    event_date = data.get('date')
    event_time = data.get('time', '23:59')

    if not event_name or not event_date:
        return jsonify({'error': 'name and date are required'}), 400

    try:
        datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({'error': 'Invalid date or time format'}), 400

    event_id = str(uuid.uuid4())
    events.append({'id': event_id, 'name': event_name, 'date': event_date, 'time': event_time})
    return jsonify({'message': 'Event added successfully!', 'id': event_id})

@app.route('/delete-event', methods=['POST'])
def delete_event():
    data = request.json
    event_id = data.get('id')

    global events
    events = [event for event in events if event['id'] != event_id]
    return jsonify({'message': 'Event deleted successfully!'})

@app.route('/update-event', methods=['POST'])
def update_event():
    data = request.json
    event_id = data.get('id')
    new_name = data.get('newName')
    new_date = data.get('newDate')
    new_time = data.get('newTime', '23:59')

    if not event_id or not new_name or not new_date:
        return jsonify({'error': 'Invalid input. Please provide all required fields.'}), 400

    try:
        datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({'error': 'Invalid date or time format'}), 400

    for event in events:
        if event['id'] == event_id:
            event['name'] = new_name
            event['date'] = new_date
            event['time'] = new_time
            return jsonify({'message': 'Event updated successfully!'})

    return jsonify({'error': 'Event not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
