from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'db4test$'
app.config['MYSQL_DB'] = 'db_test'

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def get_hello():
    return "Hello"

@app.route('/users', methods=['GET'])
def get_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT uid, name, age FROM users")
        users = cur.fetchall()
        cur.close()
        user_list = []
        for user in users:
            user_dict = {
                'uid': user[0],
                'name': user[1],
                'age': user[2]
            }
            user_list.append(user_dict)
        return jsonify(user_list)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/users/<int:uid>', methods=['GET'])
def get_user(uid):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT uid, name, age FROM users WHERE uid = %s", (uid,))
        user = cur.fetchone()
        cur.close()
        if user:
            user_dict = {
                'uid': user[0],
                'name': user[1],
                'age': user[2]
            }
            return jsonify(user_dict)
        else:
            return jsonify({'message': 'User not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        name = data['name']
        age = data['age']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'User created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/users/<int:uid>', methods=['PUT'])
def update_user(uid):
    try:
        data = request.get_json()
        name = data['name']
        age = data['age']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET name = %s, age = %s WHERE uid = %s", (name, age, uid))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE uid = %s", (uid,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
