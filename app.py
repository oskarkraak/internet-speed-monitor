from flask import Flask, jsonify, render_template, request
import sqlite3
import os

app = Flask(__name__)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DB = os.path.join(BASEDIR, 'data.db')

def get_data(limit=288):  # default to last 288 tests ≈ 24 hours @5 min intervals
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT timestamp, download_mbps, upload_mbps, ping_ms FROM results ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return list(reversed(rows))

@app.route('/data')
def data():
    limit = int(request.args.get('interval', 288))  # Get interval from query parameter, default to 288
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
