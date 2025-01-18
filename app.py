from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)

# Enable SocketIO and CORS
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# MySQL Connection Configuration
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='crickscore',
            user='root',  # Replace with your MySQL username
            password='Sudhir@1304'  # Replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Serve the main HTML file
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user')
def user_view():
    return render_template('user.html')


# Fetch Match Data
@app.route('/get_match', methods=['GET'])
def get_match():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM matches ORDER BY id DESC LIMIT 1")
            match = cursor.fetchone()
            if match:
                cursor.execute("SELECT * FROM balls WHERE match_id = %s ORDER BY over_number, ball_number", (match['id'],))
                balls = cursor.fetchall()
                match['balls'] = balls
                return jsonify(match)
            return jsonify({'error': 'No match found'}), 404
        except Error as e:
            print(f"Error: {e}")
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    return jsonify({'error': 'Database connection failed'}), 500

# Update Score
@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM matches ORDER BY id DESC LIMIT 1")
            match = cursor.fetchone()
            if match:
                match_id = match['id']
                cursor.execute(
                    "INSERT INTO balls (match_id, over_number, ball_number, runs, is_out) VALUES (%s, %s, %s, %s, %s)",
                    (match_id, data['overNumber'], data['ballNumber'], data['runs'], data['isOut'])
                )

                new_score = match['current_score'] + data['runs']
                new_wickets = match['wickets'] + (1 if data['isOut'] else 0)
                new_ball = (data['ballNumber'] + 1) % 6
                new_over = data['overNumber'] + (1 if data['ballNumber'] == 5 else 0)

                cursor.execute(
                    """
                    UPDATE matches
                    SET current_score = %s, wickets = %s, current_over = %s, current_ball = %s
                    WHERE id = %s
                    """,
                    (new_score, new_wickets, new_over, new_ball, match_id)
                )
                connection.commit()

                updated_match = {
                    'current_score': new_score,
                    'wickets': new_wickets,
                    'current_over': new_over,
                    'current_ball': new_ball,
                    'match_id': match_id
                }
                socketio.emit('match_update', updated_match)
                return jsonify({'success': True})
            return jsonify({'error': 'No match found'}), 404
        except Error as e:
            connection.rollback()
            print(f"Error: {e}")
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    return jsonify({'error': 'Database connection failed'}), 500

# Reset Score
@app.route('/reset_score', methods=['POST'])
def reset_score():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM matches ORDER BY id DESC LIMIT 1")
            match = cursor.fetchone()
            if match:
                match_id = match['id']
                cursor.execute(
                    """
                    UPDATE matches
                    SET current_score = 0, wickets = 0, current_over = 0, current_ball = 0
                    WHERE id = %s
                    """,
                    (match_id,)
                )
                cursor.execute("DELETE FROM balls WHERE match_id = %s", (match_id,))
                connection.commit()

                reset_match = {
                    'current_score': 0,
                    'wickets': 0,
                    'current_over': 0,
                    'current_ball': 0,
                    'match_id': match_id
                }
                socketio.emit('match_update', reset_match)
                return jsonify({'success': True})
            return jsonify({'error': 'No match found'}), 404
        except Error as e:
            connection.rollback()
            print(f"Error: {e}")
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    return jsonify({'error': 'Database connection failed'}), 500

# WebSocket: Client Connected
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit_initial_data()

# Emit Initial Data
def emit_initial_data():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM matches ORDER BY id DESC LIMIT 1")
            match = cursor.fetchone()
            if match:
                cursor.execute("SELECT * FROM balls WHERE match_id = %s ORDER BY over_number, ball_number", (match['id'],))
                balls = cursor.fetchall()
                match['balls'] = balls
                emit('match_update', match)
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# WebSocket: Client Disconnected
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
    
