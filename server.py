from flask import Flask, request, jsonify
import threading
from generateapp import generateApps

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/process_data', methods=['POST'])
def process_data():
    # Get data from request body
    data = request.json
    username = data.get('username')
    app_name = data.get('app_name')
    email = data.get('email')
    template_path = data.get('template_path')

    # Process the data (you can replace this with your own logic)
    result = {
        'username': username,
        'app_name': app_name,
        'email': email,
        'template_path': template_path
    }


    # Return a response
    return jsonify({'message': 'Job added to the queue'})


if __name__ == '__main__':

    # Run the Flask app on port 5000
    app.run(debug=True, port=5111)