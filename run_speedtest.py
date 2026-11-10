#!/usr/bin/env python3
import json, sqlite3, subprocess, os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DB = os.path.join(BASEDIR, 'data.db')

# run the speedtest, capture JSON output
res = subprocess.check_output(['speedtest-cli', '--json'])
data = json.loads(res)

dl = data['download'] / 1e6       # convert from bps to Mbps
ul = data['upload'] / 1e6
ping = data['ping']

# store in SQLite
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute(
    "INSERT INTO results(download_mbps, upload_mbps, ping_ms) VALUES (?, ?, ?)",
    (dl, ul, ping)
)
conn.commit()
conn.close()
