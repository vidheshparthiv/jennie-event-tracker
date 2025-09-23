from flask import Flask, request, jsonify, render_template

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
    event_time = data.get('time')

    if not event_name or not event_date:
        return jsonify({'error': 'name and date are required'}), 400

    events.append({'name': event_name, 'date': event_date, 'time': event_time})
    return jsonify({'message': 'event added successfully!'})

@app.route('/delete-event', methods=['POST'])
def delete_event():
    data = request.json
    event_name = data.get('name')

    global events
    events = [event for event in events if event['name'] != event_name]
    return jsonify({'message': 'Event deleted successfully!'})

@app.route('/update-event', methods=['POST'])
def update_event():
    data = request.json
    old_name = data.get('oldName')
    new_name = data.get('newName')
    new_date = data.get('newDate')
    new_time = data.get('newTime')

    if not old_name or not new_name or not new_date:
        return jsonify({'error': 'Invalid input. Please provide all required fields.'}), 400

    for event in events:
        if event['name'] == old_name:
            event['name'] = new_name
            event['date'] = new_date
            event['time'] = new_time
            return jsonify({'message': 'Event updated successfully!'})

    return jsonify({'error': 'Event not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)
