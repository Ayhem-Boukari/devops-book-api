"""Book Library REST API with full observability support."""
import uuid
import time
import logging
from functools import wraps
from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from pythonjsonlogger import jsonlogger

# Initialize Flask app
app = Flask(__name__)

# ==================== METRICS ====================
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')
BOOKS_TOTAL = Gauge('books_total', 'Total number of books in database')

# ==================== LOGGING ====================
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(timestamp)s %(level)s %(message)s %(request_id)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# ==================== IN-MEMORY DATABASE ====================
books_db = []
next_id = 1

# ==================== DECORATORS ====================
def track_request(f):
    """Decorator to track metrics and add request tracing."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        request_id = str(uuid.uuid4())
        request.request_id = request_id
        start_time = time.time()
        try:
            response = f(*args, **kwargs)
            status = response[1] if isinstance(response, tuple) else 200
            return response
        except Exception as e:
            status = 500
            raise e
        finally:
            duration = time.time() - start_time
            REQUEST_COUNT.labels(request.method, request.path, status).inc()
            REQUEST_LATENCY.observe(duration)
            logger.info("Request processed", extra={
                'request_id': request_id, 'method': request.method, 'path': request.path,
                'status_code': status, 'response_time_ms': round(duration * 1000, 2)
            })
    return wrapper

@app.after_request
def add_request_id(response):
    """Add X-Request-ID header to all responses."""
    response.headers['X-Request-ID'] = getattr(request, 'request_id', str(uuid.uuid4()))
    return response

# ==================== HEALTH ENDPOINTS ====================
@app.route('/health')
@track_request
def health():
    """Health check endpoint for liveness probe."""
    return jsonify({"status": "healthy"}), 200

@app.route('/ready')
@track_request
def ready():
    """Readiness check endpoint for Kubernetes."""
    return jsonify({"status": "ready", "books_count": len(books_db)}), 200

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint."""
    BOOKS_TOTAL.set(len(books_db))
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# ==================== BOOK CRUD ENDPOINTS ====================
@app.route('/api/v1/books', methods=['GET'])
@track_request
def get_books():
    """Retrieve all books from the library."""
    return jsonify(books_db), 200

@app.route('/api/v1/books', methods=['POST'])
@track_request
def create_book():
    """Create a new book in the library."""
    global next_id
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'author', 'year')):
        return jsonify({"error": "Missing required fields: title, author, year"}), 400
    if not isinstance(data.get('year'), int):
        return jsonify({"error": "Year must be an integer"}), 400
    book = {"id": next_id, "title": data['title'], "author": data['author'], "year": data['year']}
    books_db.append(book)
    next_id += 1
    BOOKS_TOTAL.set(len(books_db))
    return jsonify(book), 201

@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
@track_request
def get_book(book_id):
    """Retrieve a specific book by ID."""
    book = next((b for b in books_db if b['id'] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200

@app.route('/api/v1/books/<int:book_id>', methods=['PUT'])
@track_request
def update_book(book_id):
    """Update an existing book by ID."""
    book = next((b for b in books_db if b['id'] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    book.update({k: data[k] for k in ('title', 'author', 'year') if k in data})
    return jsonify(book), 200

@app.route('/api/v1/books/<int:book_id>', methods=['DELETE'])
@track_request
def delete_book(book_id):
    """Delete a book by ID."""
    global books_db
    book = next((b for b in books_db if b['id'] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    books_db = [b for b in books_db if b['id'] != book_id]
    BOOKS_TOTAL.set(len(books_db))
    return jsonify({"message": "Book deleted successfully"}), 200

# ==================== ERROR HANDLERS ====================
@app.errorhandler(400)
def bad_request(e):
    """Handle 400 Bad Request errors."""
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(404)
def not_found(e):
    """Handle 404 Not Found errors."""
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 Internal Server errors."""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
