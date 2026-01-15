"""Comprehensive unit tests for the Book Library REST API."""
import pytest
from app.main import app, books_db


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_database():
    """Reset the in-memory database before each test."""
    global books_db
    from app import main
    main.books_db = []
    main.next_id = 1
    yield
    main.books_db = []
    main.next_id = 1


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_health_endpoint_returns_200(self, client):
        """Test that /health returns 200 and healthy status."""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'

    def test_ready_endpoint_returns_200(self, client):
        """Test that /ready returns 200 and ready status."""
        response = client.get('/ready')
        assert response.status_code == 200
        assert response.json['status'] == 'ready'
        assert 'books_count' in response.json


class TestMetricsEndpoint:
    """Tests for Prometheus metrics endpoint."""

    def test_metrics_endpoint_returns_prometheus_format(self, client):
        """Test that /metrics returns Prometheus format data."""
        response = client.get('/metrics')
        assert response.status_code == 200
        assert b'http_requests_total' in response.data
        assert b'http_request_duration_seconds' in response.data
        assert b'books_total' in response.data


class TestBooksCRUD:
    """Tests for Book CRUD operations."""

    def test_get_all_books_empty(self, client):
        """Test getting all books when database is empty."""
        response = client.get('/api/v1/books')
        assert response.status_code == 200
        assert response.json == []

    def test_create_book_success(self, client):
        """Test successfully creating a new book."""
        book_data = {"title": "Test Book", "author": "Test Author", "year": 2024}
        response = client.post('/api/v1/books', json=book_data)
        assert response.status_code == 201
        assert response.json['title'] == "Test Book"
        assert response.json['author'] == "Test Author"
        assert response.json['year'] == 2024
        assert 'id' in response.json

    def test_create_book_invalid_data(self, client):
        """Test creating a book with invalid/missing data."""
        # Missing required fields
        response = client.post('/api/v1/books', json={"title": "Only Title"})
        assert response.status_code == 400
        assert 'error' in response.json

        # Invalid year type
        response = client.post('/api/v1/books', json={
            "title": "Test", "author": "Author", "year": "not-a-number"
        })
        assert response.status_code == 400

    def test_get_book_by_id_success(self, client):
        """Test successfully retrieving a book by ID."""
        # First create a book
        book_data = {"title": "Test Book", "author": "Test Author", "year": 2024}
        create_response = client.post('/api/v1/books', json=book_data)
        book_id = create_response.json['id']

        # Then retrieve it
        response = client.get(f'/api/v1/books/{book_id}')
        assert response.status_code == 200
        assert response.json['id'] == book_id
        assert response.json['title'] == "Test Book"

    def test_get_book_by_id_not_found(self, client):
        """Test retrieving a non-existent book."""
        response = client.get('/api/v1/books/9999')
        assert response.status_code == 404
        assert 'error' in response.json

    def test_update_book_success(self, client):
        """Test successfully updating a book."""
        # Create a book first
        book_data = {"title": "Original Title", "author": "Original Author", "year": 2020}
        create_response = client.post('/api/v1/books', json=book_data)
        book_id = create_response.json['id']

        # Update the book
        update_data = {"title": "Updated Title", "year": 2024}
        response = client.put(f'/api/v1/books/{book_id}', json=update_data)
        assert response.status_code == 200
        assert response.json['title'] == "Updated Title"
        assert response.json['year'] == 2024
        assert response.json['author'] == "Original Author"  # Unchanged

    def test_delete_book_success(self, client):
        """Test successfully deleting a book."""
        # Create a book first
        book_data = {"title": "To Delete", "author": "Author", "year": 2024}
        create_response = client.post('/api/v1/books', json=book_data)
        book_id = create_response.json['id']

        # Delete the book
        response = client.delete(f'/api/v1/books/{book_id}')
        assert response.status_code == 200
        assert 'message' in response.json

        # Verify it's deleted
        get_response = client.get(f'/api/v1/books/{book_id}')
        assert get_response.status_code == 404


class TestRequestTracing:
    """Tests for request ID tracing."""

    def test_request_id_header_present(self, client):
        """Test that X-Request-ID header is present in all responses."""
        # Test on health endpoint
        response = client.get('/health')
        assert 'X-Request-ID' in response.headers
        assert len(response.headers['X-Request-ID']) == 36  # UUID format

        # Test on books endpoint
        response = client.get('/api/v1/books')
        assert 'X-Request-ID' in response.headers

        # Test on POST endpoint
        book_data = {"title": "Test", "author": "Author", "year": 2024}
        response = client.post('/api/v1/books', json=book_data)
        assert 'X-Request-ID' in response.headers
