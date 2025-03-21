from flask import Flask, render_template, request
import logging

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_id = request.form.get('user_id')
    if user_id:
        user = get_user(user_id)
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    return jsonify({"error": "No user ID provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)
