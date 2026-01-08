from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <html>
        <head><title>Docker Learning - Simple Web App</title></head>
        <body>
            <h1>Welcome to Docker Learning! 🐳</h1>
            <p>This is a simple Flask web application running in a Docker container.</p>
            <p>Container hostname: {}</p>
        </body>
    </html>
    '''.format(os.environ.get('HOSTNAME', 'unknown'))

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    # NOTE: debug=True is used for learning purposes only
    # In production, always use debug=False for security
    app.run(host='0.0.0.0', port=5000, debug=False)
