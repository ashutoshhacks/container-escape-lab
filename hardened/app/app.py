# app.py — HARDENED version
# Fixes applied:
#   1. shell=False — command args passed as list, never interpreted by shell
#   2. Input validation — strict regex, only valid IPs accepted
#   3. No user-controlled data touches the shell in any way

from flask import Flask, request, render_template
import subprocess
import re

app = Flask(__name__)

# Strict regex — only valid IPv4 addresses allowed
# Rejects anything with ; | & $ ( ) etc.
IP_PATTERN = re.compile(
    r'^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)'
    r'(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$'
)

@app.route('/')
def index():
    return render_template('index.html', output=None, error=None)

@app.route('/ping', methods=['POST'])
def ping():
    target = request.form.get('target', '').strip()

    # FIX 1: Input validation
    # Reject anything that is not a valid IPv4 address
    if not IP_PATTERN.match(target):
        return render_template(
            'index.html',
            output=None,
            error="Invalid input. Only valid IPv4 addresses are accepted."
        )

    # FIX 2: shell=False with args as a list
    # The shell never sees this command — subprocess calls ping directly
    # Even if somehow a bad value slipped through, ; | & have no meaning
    # when passed as arguments to a process directly
    try:
        result = subprocess.run(
            ["ping", "-c", "2", target],   # list of args — no shell involved
            capture_output=True,
            text=True,
            timeout=10,
            shell=False                     # explicit — never passes through sh
        )
        output = result.stdout + result.stderr

    except subprocess.TimeoutExpired:
        output = "Request timed out."
    except Exception as e:
        output = "An error occurred."      # never expose internal errors to user

    return render_template('index.html', output=output, error=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # debug=False in production
