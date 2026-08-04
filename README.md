# SpaceBnB

A microservices-based rental booking platform demonstrating modern cloud-native architecture, containerization, orchestration, CI/CD, and observability.

## Local Development

### Initializing and migrating database

To initialize and migrate auth database for local development, run the following
```python
python3 -m services.auth_service.migrate
```

### Root docker-compose.yml
The root docker-compose.yml runs the complete application stack for local development and cross-service integration testing. Kubernetes manifests under /deployment are used to validate Kubernetes behavior in Minikube and deploy to AKS.