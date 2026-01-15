# 📚 DevOps Book API

A production-ready **Book Library REST API** built with Python Flask, featuring comprehensive DevOps implementation including CI/CD, containerization, Kubernetes orchestration, observability, and security scanning.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-blue)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Observability](#-observability)
- [Security](#-security)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## Overview

This project demonstrates a complete DevOps workflow for a simple Book Library REST API. It showcases:

- ✅ **RESTful API** with Flask (< 150 lines of code)
- ✅ **Containerization** with multi-stage Docker builds
- ✅ **Orchestration** with Kubernetes manifests
- ✅ **CI/CD** with GitHub Actions (lint, test, build, deploy)
- ✅ **Observability** with Prometheus metrics, structured logging, and request tracing
- ✅ **Security** with SAST (Bandit, Semgrep), DAST (OWASP ZAP), and container scanning (Trivy)

---

## 🏗️ Architecture

```
                                    ┌─────────────────────────────────────┐
                                    │           KUBERNETES CLUSTER        │
                                    │                                     │
    ┌──────────┐     ┌──────────┐  │  ┌─────────┐      ┌─────────────┐   │
    │          │     │          │  │  │         │      │             │   │
    │  Users   │────▶│  Ingress │──┼─▶│ Service │─────▶│   Pod (x2)  │   │
    │          │     │          │  │  │         │      │  Flask API  │   │
    └──────────┘     └──────────┘  │  └─────────┘      └──────┬──────┘   │
                                   │                          │          │
                                   └──────────────────────────┼──────────┘
                                                              │
                                                              ▼
                                   ┌──────────────────────────────────────┐
                                   │           OBSERVABILITY STACK        │
                                   │                                      │
                                   │  ┌────────────┐    ┌─────────────┐  │
                                   │  │            │    │             │  │
                                   │  │ Prometheus │───▶│   Grafana   │  │
                                   │  │  (Metrics) │    │ (Dashboard) │  │
                                   │  └────────────┘    └─────────────┘  │
                                   │                                      │
                                   └──────────────────────────────────────┘

    CI/CD Pipeline (GitHub Actions):
    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │  Lint   │───▶│  Test   │───▶│  Build  │───▶│Security │───▶│ Deploy  │
    │(flake8) │    │(pytest) │    │(Docker) │    │ (SAST/  │    │  (K8s)  │
    │ (black) │    │         │    │         │    │  DAST)  │    │         │
    └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- kubectl
- minikube or kind (for local Kubernetes)

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/devops-book-api.git
cd devops-book-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install-dev

# Run tests
make test

# Run locally
make run
```

### Docker

```bash
# Build Docker image
make docker-build

# Run with Docker Compose (includes Prometheus + Grafana)
make docker-run

# Access services:
# - API: http://localhost:5000
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)

# Stop services
make docker-stop
```

### Kubernetes Deployment (Minikube)

```bash
# Start minikube
minikube start

# Enable ingress addon
minikube addons enable ingress

# Build image in minikube's Docker
eval $(minikube docker-env)
docker build -t devops-book-api:latest .

# Deploy to Kubernetes
make k8s-deploy

# Add hostfile entry (get minikube IP with: minikube ip)
echo "$(minikube ip) bookapi.local" | sudo tee -a /etc/hosts

# Access the API
curl http://bookapi.local/health

# View deployment status
make k8s-status
```

---

## 📡 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check (liveness probe) |
| `GET` | `/ready` | Readiness check (readiness probe) |
| `GET` | `/metrics` | Prometheus metrics |
| `GET` | `/api/v1/books` | List all books |
| `POST` | `/api/v1/books` | Create a new book |
| `GET` | `/api/v1/books/<id>` | Get book by ID |
| `PUT` | `/api/v1/books/<id>` | Update book by ID |
| `DELETE` | `/api/v1/books/<id>` | Delete book by ID |

### Book Schema

```json
{
  "id": 1,
  "title": "The DevOps Handbook",
  "author": "Gene Kim",
  "year": 2016
}
```

### cURL Examples

```bash
# Health check
curl http://localhost:5000/health

# Create a book
curl -X POST http://localhost:5000/api/v1/books \
  -H "Content-Type: application/json" \
  -d '{"title": "The Phoenix Project", "author": "Gene Kim", "year": 2013}'

# List all books
curl http://localhost:5000/api/v1/books

# Get book by ID
curl http://localhost:5000/api/v1/books/1

# Update a book
curl -X PUT http://localhost:5000/api/v1/books/1 \
  -H "Content-Type: application/json" \
  -d '{"year": 2018}'

# Delete a book
curl -X DELETE http://localhost:5000/api/v1/books/1
```

---

## 📊 Observability

### Metrics

The API exposes Prometheus metrics at `/metrics`:

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total HTTP requests (labels: method, endpoint, status) |
| `http_request_duration_seconds` | Histogram | Request latency distribution |
| `books_total` | Gauge | Current number of books in database |

**Access Prometheus:** http://localhost:9090

**Example Queries:**
```promql
# Request rate by endpoint
sum(rate(http_requests_total[5m])) by (endpoint)

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
```

### Logs

All logs are in structured JSON format:

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

### Tracing

Every request receives a unique `X-Request-ID` header for distributed tracing:

```bash
curl -i http://localhost:5000/api/v1/books
# Response header: X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
```

### Grafana Dashboard

**Access Grafana:** http://localhost:3000 (admin/admin)

The pre-configured dashboard includes:
- Total Books
- Request Rate (5m)
- P95 Latency
- Total Requests
- Request Rate by Endpoint
- Request Latency Percentiles (P50, P95, P99)
- Requests by Status Code
- Books in Database Over Time

---

## 🔒 Security

### SAST (Static Application Security Testing)

```bash
# Run Bandit
bandit -r app/ -f txt

# Run Semgrep
semgrep scan --config=p/python --config=p/flask app/
```

### DAST (Dynamic Application Security Testing)

```bash
# Start the application
make docker-run

# Run OWASP ZAP baseline scan
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://host.docker.internal:5000
```

### Dependency Scanning

```bash
# Check for vulnerable packages
pip-audit

# Safety check
safety check
```

### Container Image Scanning

```bash
# Scan with Trivy
make trivy-scan
```

---

## 🔄 CI/CD Pipeline

### Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CI PIPELINE (ci.yml)                            │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────┐     ┌─────────┐     ┌─────────────────────────────────┐   │
│  │  Lint   │     │  Test   │     │            Build                │   │
│  │─────────│     │─────────│     │─────────────────────────────────│   │
│  │ flake8  │────▶│ pytest  │────▶│ Docker Build & Push to Registry │   │
│  │ black   │     │ coverage│     │                                 │   │
│  └─────────┘     └─────────┘     └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                     SECURITY PIPELINE (security.yml)                    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌───────────┐  ┌─────────┐  ┌─────────┐    │
│  │ Bandit  │  │ Semgrep │  │ Dep Check │  │  Trivy  │  │   ZAP   │    │
│  │ (SAST)  │  │ (SAST)  │  │pip-audit  │  │ (Image) │  │ (DAST)  │    │
│  │         │  │         │  │  safety   │  │         │  │         │    │
│  └─────────┘  └─────────┘  └───────────┘  └─────────┘  └─────────┘    │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         CD PIPELINE (cd.yml)                            │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐     ┌────────────────┐     ┌───────────────────┐    │
│  │ Apply K8s     │────▶│ Wait Rollout   │────▶│   Smoke Tests     │    │
│  │ Manifests     │     │   Complete     │     │                   │    │
│  └───────────────┘     └────────────────┘     └───────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### Triggers

| Pipeline | Trigger |
|----------|---------|
| CI | Push/PR to `main` |
| Security | Push/PR to `main`, Weekly schedule |
| CD | Push to `main` (after CI passes) |

### Required Secrets

Configure these in GitHub repository settings:

| Secret | Description |
|--------|-------------|
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub password/token |
| `KUBECONFIG` | Base64-encoded kubeconfig |

---

## 📁 Project Structure

```
devops-book-api/
│
├── app/                           # Application source code
│   ├── __init__.py               # Package initialization
│   └── main.py                   # Flask REST API (< 150 lines)
│
├── tests/                        # Unit tests
│   ├── __init__.py
│   └── test_app.py              # Pytest test cases
│
├── k8s/                          # Kubernetes manifests
│   ├── namespace.yaml           # Namespace definition
│   ├── configmap.yaml           # Environment configuration
│   ├── deployment.yaml          # Deployment with 2 replicas
│   ├── service.yaml             # ClusterIP service
│   └── ingress.yaml             # Ingress for external access
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── task.md              # Issue template
│   └── workflows/
│       ├── ci.yml               # CI: lint, test, build
│       ├── security.yml         # SAST + DAST scans
│       └── cd.yml               # CD: deploy to Kubernetes
│
├── prometheus/
│   └── prometheus.yml           # Prometheus configuration
│
├── grafana/
│   ├── dashboard.json           # Grafana dashboard
│   └── provisioning/            # Auto-provisioning configs
│
├── Dockerfile                   # Multi-stage Docker build
├── docker-compose.yml           # Local dev environment
├── .dockerignore               # Docker build exclusions
├── .gitignore                  # Git exclusions
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── Makefile                    # Automation commands
├── README.md                   # This file
└── REPORT.md                   # Project report
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting:
   ```bash
   make lint
   make test
   ```
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Standards

- Follow PEP 8 style guide
- Use Black for code formatting
- Write tests for new features
- Keep main.py under 150 lines
- Add docstrings to all functions

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Prometheus](https://prometheus.io/) - Monitoring system
- [Grafana](https://grafana.com/) - Visualization platform
- [OWASP ZAP](https://www.zaproxy.org/) - Security testing

---

**Made by Ayhem Boukari for DevOps learning**
