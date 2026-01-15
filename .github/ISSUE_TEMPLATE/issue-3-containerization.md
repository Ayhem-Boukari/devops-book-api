---
name: "Issue 3: Containerization"
about: Containerize application with Docker
title: "[TASK] Containerize application with Docker"
labels: enhancement, docker
assignees: ''
---

## 📋 Task Description

Create Docker configuration for the application including multi-stage Dockerfile and docker-compose for local development with monitoring stack.

## 🎯 Acceptance Criteria

- [ ] Create multi-stage Dockerfile
- [ ] Use python:3.11-slim as base image
- [ ] Create non-root user (appuser)
- [ ] Add HEALTHCHECK instruction
- [ ] Final image size < 150MB
- [ ] Create docker-compose.yml with API, Prometheus, and Grafana
- [ ] Configure Prometheus to scrape API metrics
- [ ] Configure Grafana with pre-built dashboard
- [ ] Test locally with docker-compose

## 📝 Implementation Details

### Dockerfile Requirements

```dockerfile
# Stage 1: Builder
- Install dependencies in virtual environment
- Copy only requirements.txt first (layer caching)

# Stage 2: Production
- Copy virtual environment from builder
- Create non-root user
- Set proper environment variables
- Use gunicorn for production server
- Expose port 5000
- Add HEALTHCHECK
```

### Docker Compose Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| api | Build from Dockerfile | 5000 | Flask application |
| prometheus | prom/prometheus:latest | 9090 | Metrics collection |
| grafana | grafana/grafana:latest | 3000 | Visualization |

### Image Size Optimization

- Use slim base image
- Multi-stage build
- Proper .dockerignore
- Remove cache after pip install

## 🔗 Related Issues

- Issue #2: Observability Implementation
- Issue #5: Kubernetes Deployment

## 📊 Definition of Done

- [ ] `docker build` succeeds
- [ ] Image size verified < 150MB
- [ ] `docker-compose up` starts all services
- [ ] API accessible at localhost:5000
- [ ] Prometheus accessible at localhost:9090
- [ ] Grafana accessible at localhost:3000
- [ ] Metrics visible in Prometheus targets
