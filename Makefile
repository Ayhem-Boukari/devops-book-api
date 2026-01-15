# =============================================================================
# Makefile for DevOps Book API
# =============================================================================
# Provides convenient commands for development, testing, and deployment.
# Run 'make help' to see all available commands.
# =============================================================================

.PHONY: help install install-dev test lint format run docker-build docker-run docker-push k8s-deploy k8s-delete security-scan clean

# Default target
.DEFAULT_GOAL := help

# Variables
DOCKER_USERNAME ?= your-dockerhub-username
IMAGE_NAME = devops-book-api
IMAGE_TAG ?= latest
K8S_NAMESPACE = devops-book-api

# ======================== HELP ========================
help: ## Show this help message
	@echo "DevOps Book API - Available Commands"
	@echo "======================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ======================== INSTALLATION ========================
install: ## Install production dependencies
	pip install --upgrade pip
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install --upgrade pip
	pip install -r requirements-dev.txt

# ======================== TESTING ========================
test: ## Run tests with coverage
	pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

test-quick: ## Run tests without coverage
	pytest tests/ -v

# ======================== CODE QUALITY ========================
lint: ## Run linters (flake8 and black check)
	flake8 app/ tests/ --max-line-length=100 --statistics
	black --check --diff app/ tests/

format: ## Format code with black
	black app/ tests/
	@echo "Code formatted successfully!"

# ======================== LOCAL DEVELOPMENT ========================
run: ## Run Flask app locally (development mode)
	FLASK_ENV=development python -m app.main

run-gunicorn: ## Run with gunicorn (production mode)
	gunicorn --bind 0.0.0.0:5000 --workers 2 app.main:app

# ======================== DOCKER ========================
docker-build: ## Build Docker image
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	@echo "Image built: $(IMAGE_NAME):$(IMAGE_TAG)"

docker-run: ## Run with docker-compose (includes Prometheus + Grafana)
	docker-compose up --build -d
	@echo "Services started:"
	@echo "  - API: http://localhost:5000"
	@echo "  - Prometheus: http://localhost:9090"
	@echo "  - Grafana: http://localhost:3000 (admin/admin)"

docker-stop: ## Stop docker-compose services
	docker-compose down
	@echo "Services stopped"

docker-logs: ## View docker-compose logs
	docker-compose logs -f

docker-push: ## Push Docker image to Docker Hub
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(DOCKER_USERNAME)/$(IMAGE_NAME):$(IMAGE_TAG)
	docker push $(DOCKER_USERNAME)/$(IMAGE_NAME):$(IMAGE_TAG)
	@echo "Image pushed: $(DOCKER_USERNAME)/$(IMAGE_NAME):$(IMAGE_TAG)"

# ======================== KUBERNETES ========================
k8s-deploy: ## Deploy to Kubernetes
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml
	kubectl apply -f k8s/ingress.yaml
	kubectl rollout status deployment/$(IMAGE_NAME) -n $(K8S_NAMESPACE)
	@echo "Deployment complete!"

k8s-delete: ## Delete from Kubernetes
	kubectl delete -f k8s/ingress.yaml --ignore-not-found
	kubectl delete -f k8s/service.yaml --ignore-not-found
	kubectl delete -f k8s/deployment.yaml --ignore-not-found
	kubectl delete -f k8s/configmap.yaml --ignore-not-found
	kubectl delete -f k8s/namespace.yaml --ignore-not-found
	@echo "Resources deleted!"

k8s-status: ## Show Kubernetes deployment status
	@echo "=== Namespace ==="
	kubectl get namespace $(K8S_NAMESPACE) --ignore-not-found
	@echo "\n=== Pods ==="
	kubectl get pods -n $(K8S_NAMESPACE) -l app=$(IMAGE_NAME)
	@echo "\n=== Services ==="
	kubectl get svc -n $(K8S_NAMESPACE)
	@echo "\n=== Ingress ==="
	kubectl get ingress -n $(K8S_NAMESPACE)

k8s-logs: ## View Kubernetes pod logs
	kubectl logs -f -l app=$(IMAGE_NAME) -n $(K8S_NAMESPACE)

# ======================== SECURITY ========================
security-scan: ## Run security scans locally
	@echo "=== Running Bandit (SAST) ==="
	bandit -r app/ -f txt || true
	@echo "\n=== Running pip-audit ==="
	pip-audit || true
	@echo "\n=== Running safety check ==="
	safety check || true
	@echo "\nSecurity scans complete!"

trivy-scan: ## Scan Docker image with Trivy
	docker build -t $(IMAGE_NAME):scan .
	trivy image $(IMAGE_NAME):scan

# ======================== CLEANUP ========================
clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "coverage.xml" -delete 2>/dev/null || true
	find . -type f -name "*-report.json" -delete 2>/dev/null || true
	find . -type f -name "*-report.txt" -delete 2>/dev/null || true
	@echo "Cleanup complete!"

clean-docker: ## Remove Docker images and volumes
	docker-compose down -v --rmi local
	docker image prune -f
	@echo "Docker cleanup complete!"
