---
name: "Issue 2: Observability Implementation"
about: Implement observability (metrics, logs, tracing)
title: "[TASK] Implement observability (metrics, logs, tracing)"
labels: enhancement, observability
assignees: ''
---

## 📋 Task Description

Implement comprehensive observability features including Prometheus metrics, structured JSON logging, and request ID tracing.

## 🎯 Acceptance Criteria

- [ ] Add Prometheus metrics using prometheus_client library
- [ ] Implement structured JSON logging using python-json-logger
- [ ] Add request ID (UUID) tracing for all requests
- [ ] Return X-Request-ID header in all responses
- [ ] Test all observability features work correctly

## 📝 Implementation Details

### Metrics to Implement

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `http_requests_total` | Counter | method, endpoint, status | Total HTTP requests |
| `http_request_duration_seconds` | Histogram | - | Request latency |
| `books_total` | Gauge | - | Books in database |

### Log Format

Every log entry MUST include:
- timestamp (ISO 8601)
- level (INFO, ERROR, etc.)
- message
- request_id (UUID)
- method (GET, POST, etc.)
- path (/api/v1/books)
- status_code (200, 404, etc.)
- response_time_ms

### Example Log Output

```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "message": "Request processed",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "method": "GET",
  "path": "/api/v1/books",
  "status_code": 200,
  "response_time_ms": 12.5
}
```

## 🔗 Related Issues

- Issue #1: Project Setup & Flask API
- Issue #3: Containerization

## 📊 Definition of Done

- [ ] /metrics endpoint returns Prometheus format
- [ ] All requests logged in JSON format
- [ ] X-Request-ID header present in all responses
- [ ] Unit tests verify observability features
- [ ] Grafana dashboard configured
