from flask import Flask, send_file, request,jsonify
from psycopg2 import connect,extras
from cryptography.fernet import Fernet

app = Flask(__name__)
key= Fernet.generate_key()

host = 'localhost'
port = 5432
dbname = 'usersdb'
user = 'postgres'
password = 'alamo6402'


def get_connection():
    conn = connect(host=host, port=port, dbname=dbname,
                   user=user, password=password)
    return conn


@app.get('/api/users')
def get_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()
    return jsonify(users)

@app.post('/api/users')
def create_user():
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8')).decode()

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("INSERT INTO users (username,email,password) VALUES (%s,%s,%s) RETURNING *",
                (username, email, password))
    new_created_user=cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_created_user)

@app.delete('/api/users/<id>')
def delete_user(id):
    conn= get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s RETURNING *", (id, ))
    deleted_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if deleted_user is None:
        return jsonify({'message': 'User not found'})

    return jsonify(deleted_user)

@app.put('/api/users/<id>')
def update_user(id):
    conn= get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_user=request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8')).decode()

    cur.execute("UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s RETURNING *",
                (username, email, password, id))
    updated_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if updated_user is None:
        return jsonify({'message': 'User not found'})

    return jsonify(updated_user)

@app.get('/api/users/<id>')
def get_user(id):
    conn= get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (id, ))
    user = cur.fetchone()
    conn.close()
    return jsonify(user)

@app.get('/')
def home():
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run(debug=True)
