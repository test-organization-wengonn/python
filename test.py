import os
import subprocess
import pickle
import hashlib
import jwt
from flask import Flask, request

app = Flask(__name__)

# 1. Hardcoded secret key (Insecure)
SECRET_KEY = "supersecretkey1234"

# 2. Insecure deserialization using pickle
@app.route('/deserialize', methods=['POST'])
def deserialize_data():
    data = request.data
    obj = pickle.loads(data)  # ⚠️ Vulnerable to code execution
    return str(obj)

# 3. Command injection via unsanitized input

@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host', '')
    response = subprocess.check_output(f"ping -c 1 {host}", shell=True)  # ⚠️ Potential command injection
    return response

# 4. Use of weak hash function (MD5)
def create_hash(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()  # ⚠️ Insecure hash

# 5. Insecure JWT encoding without algorithm restriction
@app.route('/get_jwt', methods=['GET'])
def get_jwt():
    username = request.args.get('username', 'guest')
    token = jwt.encode({"user": username}, SECRET_KEY, algorithm="HS256")  # ⚠️ Could be misused if not careful
    return token

@app.route('/')
def index():
    return "Test app with vulnerabilities"
    

if __name__ == "__main__":
    app.run(debug=True)
