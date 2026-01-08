from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

# Connect to Redis
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', 6379)
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route('/')
def home():
    return '''
    <html>
        <head><title>Docker Compose Example</title></head>
        <body>
            <h1>Multi-Container Application 🐳</h1>
            <p>This application demonstrates Docker Compose with multiple services.</p>
            <ul>
                <li><a href="/visits">Check Visit Counter</a></li>
                <li><a href="/health">Health Check</a></li>
            </ul>
        </body>
    </html>
    '''

@app.route('/visits')
def visits():
    # Increment visit counter in Redis
    count = redis_client.incr('visit_count')
    return jsonify({
        'message': 'Hello from Docker Compose!',
        'visits': count,
        'redis_host': redis_host
    })

@app.route('/health')
def health():
    try:
        # Check Redis connection
        redis_client.ping()
        return jsonify({
            'status': 'healthy',
            'redis': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'redis': 'disconnected',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
