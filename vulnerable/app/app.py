# app.py — Deliberately vulnerable Flask web application
# Vulnerability: OS Command Injection in the ping endpoint
# DO NOT use patterns like this in real applications

from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    # Serve the main page with the ping form
    return render_template('index.html', output=None)

@app.route('/ping', methods=['POST'])
def ping():
    # Get the IP address the user submitted in the form
    target = request.form.get('target', '')

    # !! VULNERABILITY HERE !!
    # We are directly passing user input into a shell command
    # An attacker can inject additional commands using ; | & etc.
    # Example: "127.0.0.1; id" runs ping AND the id command
    command = f"ping -c 2 {target}"

    try:
        # shell=True is what makes this dangerous
        # it passes the command to /bin/sh which interprets ; | & etc.
        output = subprocess.check_output(
            command,
            shell=True,
            stderr=subprocess.STDOUT,
            timeout=10
        )
        result = output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        result = e.output.decode('utf-8')
    except Exception as e:
        result = str(e)

    return render_template('index.html', output=result)

if __name__ == '__main__':
    # Listen on all interfaces so it is reachable from outside the container
    app.run(host='0.0.0.0', port=5000, debug=False)
