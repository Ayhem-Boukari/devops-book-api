---
name: "Issue 5: Kubernetes Deployment"
about: Deploy to Kubernetes
title: "[TASK] Deploy to Kubernetes"
labels: enhancement, kubernetes
assignees: ''
---

## 📋 Task Description

Create Kubernetes manifests for deploying the application to a Kubernetes cluster with proper resource management, health checks, and scaling capabilities.

## 🎯 Acceptance Criteria

- [ ] Create namespace.yaml for logical isolation
- [ ] Create configmap.yaml for environment configuration
- [ ] Create deployment.yaml with 2 replicas
- [ ] Create service.yaml (ClusterIP)
- [ ] Create ingress.yaml for external access
- [ ] Configure liveness and readiness probes
- [ ] Set resource limits and requests
- [ ] Deploy to minikube and verify
- [ ] Test health checks work correctly

## 📝 Implementation Details

### Namespace (namespace.yaml)

```yaml
name: devops-book-api
labels:
  app: devops-book-api
  environment: production
```

### ConfigMap (configmap.yaml)

```yaml
data:
  FLASK_ENV: production
  LOG_LEVEL: INFO
  APP_NAME: devops-book-api
```

### Deployment (deployment.yaml)

| Configuration | Value |
|---------------|-------|
| Replicas | 2 |
| Strategy | RollingUpdate |
| CPU Request | 100m |
| CPU Limit | 200m |
| Memory Request | 128Mi |
| Memory Limit | 256Mi |
| Liveness Probe | /health (period: 10s) |
| Readiness Probe | /ready (period: 5s) |

### Service (service.yaml)

```yaml
type: ClusterIP
ports:
  - port: 80
    targetPort: 5000
selector:
  app: devops-book-api
```

### Ingress (ingress.yaml)

```yaml
host: bookapi.local
path: /
pathType: Prefix
backend:
  service: devops-book-api
  port: 80
```

### Testing Steps

```bash
# Start minikube
minikube start
minikube addons enable ingress

# Build image in minikube
eval $(minikube docker-env)
docker build -t devops-book-api:latest .

# Deploy
kubectl apply -f k8s/

# Verify
kubectl get all -n devops-book-api

# Test
curl http://bookapi.local/health
```

## 🔗 Related Issues

- Issue #3: Containerization
- Issue #4: CI/CD Pipeline

## 📊 Definition of Done

- [ ] All manifests valid YAML
- [ ] `kubectl apply` succeeds
- [ ] 2 pods running and healthy
- [ ] Service endpoint accessible
- [ ] Ingress routes traffic correctly
- [ ] Health checks pass
- [ ] Prometheus annotations present
