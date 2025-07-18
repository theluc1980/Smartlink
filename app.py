from flask import Flask, request, render_template
import sqlite3
import time

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS links (
                    label TEXT PRIMARY KEY,
                    url TEXT,
                    updated_at TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT label, url FROM links")
    links = c.fetchall()
    conn.close()
    return render_template('index.html', links=links)

@app.route('/api/update', methods=['POST'])
def update_link():
    data = request.json
    label = data.get('label')
    url = data.get('url')
    if not label or not url:
        return {"status": "error", "message": "Missing label or url"}, 400

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("REPLACE INTO links (label, url, updated_at) VALUES (?, ?, ?)",
              (label, url, time.strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Link updated"}

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
