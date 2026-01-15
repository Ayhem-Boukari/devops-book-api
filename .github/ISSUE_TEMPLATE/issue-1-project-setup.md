---
name: "Issue 1: Project Setup & Flask API"
about: Set up project structure and Flask REST API
title: "[TASK] Set up project structure and Flask REST API"
labels: enhancement, priority-high
assignees: ''
---

## 📋 Task Description

Initialize the project structure and create the Flask REST API with all required endpoints.

## 🎯 Acceptance Criteria

- [ ] Initialize project directory structure following best practices
- [ ] Create Flask application with all REST endpoints
- [ ] Implement CRUD operations for books (GET, POST, PUT, DELETE)
- [ ] Add health check endpoints (/health, /ready)
- [ ] Add Prometheus metrics endpoint (/metrics)
- [ ] Implement proper error handling (400, 404, 500)
- [ ] Keep total code under 150 lines
- [ ] Add docstrings to all functions

## 📝 Implementation Details

### Endpoints to Implement

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Liveness probe |
| GET | /ready | Readiness probe |
| GET | /metrics | Prometheus metrics |
| GET | /api/v1/books | List all books |
| POST | /api/v1/books | Create book |
| GET | /api/v1/books/<id> | Get book by ID |
| PUT | /api/v1/books/<id> | Update book |
| DELETE | /api/v1/books/<id> | Delete book |

### Book Schema

```json
{
  "id": 1,
  "title": "string",
  "author": "string",
  "year": 2024
}
```

## 🔗 Related Issues

- Issue #2: Observability Implementation

## 📊 Definition of Done

- [ ] All endpoints return correct status codes
- [ ] Error responses are consistent JSON format
- [ ] Code passes flake8 linting
- [ ] Code is formatted with black
- [ ] README updated with API documentation
