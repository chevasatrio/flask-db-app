import os
import psycopg2
from flask import Flask, jsonify
#flask-db-app
app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', '5432'),
        dbname=os.getenv('DB_NAME', 'appdb'),
        user=os.getenv('DB_USER', 'appuser'),
        password=os.getenv('DB_PASSWORD', 'apppass'),
        connect_timeout=5,
    )

@app.route('/')
def hello():
    return 'Halo dari Flask + PostgreSQL + Docker + Jenkins!'

@app.route('/health')
def health():
    return jsonify(status='ok')

@app.route('/db')
def db_check():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS visits ('
                    'id SERIAL PRIMARY KEY, visited_at TIMESTAMP DEFAULT NOW())')
        cur.execute('INSERT INTO visits DEFAULT VALUES')
        cur.execute('SELECT COUNT(*) FROM visits')
        total = cur.fetchone()[0]
        cur.execute('SELECT version()')
        version = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(database='connected', total_visits=total, version=version)
    except Exception as e:
        return jsonify(database='error', detail=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)