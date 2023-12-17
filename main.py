from flask import Flask, render_template_string
from flask_socketio import SocketIO, send
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret! 123"
socketio = SocketIO(app, cors_allowed_origins="*")

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        /* Your CSS styles here */
        body {
            background-color: black;
            color: white;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        
        h1 {
            color: #FFD700; /* Gold heading color */
            font-size: 36px;
            margin-bottom: 20px;
        }
        
        #messages {
            max-height: 300px;
            overflow-y: auto;
            border: 2px solid #FFFFFF; /* White border */
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 20px;
        }
        
        input[type="text"], button {
            margin: 5px;
            padding: 8px;
            border: none;
            border-radius: 5px;
        }
        
        input[type="text"] {
            width: 150px;
        }
        
        button {
            background-color: #FF0000; /* Red button color */
            color: white;
            cursor: pointer;
        }
        
        button:hover {
            background-color: #990000; /* Darker red on hover */
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>
</head>
<body>
<script type="text/javascript">
    $(document).ready(function () {
        var socket = io.connect(window.location.origin)
        socket.on('connect', function() {
            socket.send("User connected!")
        })

        socket.on('message', function(data) {
            $('#messages').append($('<p>').text(data));
        });

        $('#sendBtn').on('click', function () {
            socket.send($('#username').val() + ': ' + $('#message').val());
            $('#message').val('');
        });
    });
</script>
<div id="messages"></div>
<input type="text" id="username" placeholder="Username">
<input type="text" id="message" placeholder="Message">
<button id="sendBtn">Send</button>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@socketio.on('message')
def handle_message(message):
    print("Received message: " + message)
    if message != "User connected!":
        send(message, broadcast=True)

if __name__ == "__main__":
    # Use environment variables to get the port assigned by Replit
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
