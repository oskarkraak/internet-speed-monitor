from flask import Flask, jsonify, render_template, request
import sqlite3
import os

app = Flask(__name__)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DB = os.path.join(BASEDIR, 'data.db')

def get_data(limit=288):  # last 288 tests ≈ 24 hours @5 min intervals
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT timestamp, download_mbps, upload_mbps, ping_ms FROM results ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    # reverse so oldest first
    return list(reversed(rows))

@app.route('/data')
def data():
    try:
        limit = int(request.args.get('interval', 288))
    except ValueError:
        return jsonify({'error': 'interval must be an integer between 1 and 2016'}), 400
    if not 1 <= limit <= 2016:
        return jsonify({'error': 'interval must be an integer between 1 and 2016'}), 400
    rows = get_data(limit)
    return jsonify([{
        'time': ts,
        'download': dl,
        'upload': ul,
        'ping': ping
    } for ts, dl, ul, ping in rows])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
