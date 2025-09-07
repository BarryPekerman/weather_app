# Weather App Minikube Deployment

This directory contains the Helm chart configuration for deploying the Weather App in Minikube.

## Prerequisites

- Minikube installed and running
- Helm 3.x installed
- Docker installed
- kubectl configured to use minikube

## Quick Start (Public Image)

Deploy using the public Docker image:

```bash
# Create namespace
kubectl create namespace weather-app

# Update Helm dependencies
helm dependency update

# Install the chart
helm install weather-app . -f values-minikube.yaml -n weather-app

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=weather-app -n weather-app --timeout=300s

# Access the application
minikube service weather-app -n weather-app
```

## Local Development

For local development with a custom-built image:

```bash
# Build local image in minikube's Docker daemon
eval $(minikube docker-env)
docker build -t weather-app:local ./src

# Deploy with local image
helm install weather-app . -f values-minikube-local.yaml -n weather-app
```

## Private Image (Advanced)

If you need to use a private Docker image:

```bash
# Create DockerHub secret first
kubectl create secret docker-registry dockerhub-secret \
    --docker-server=https://index.docker.io/v1/ \
    --docker-username=YOUR_USERNAME \
    --docker-password=YOUR_PASSWORD \
    --namespace=weather-app

# Deploy with private image
helm install weather-app . -f values-minikube-private.yaml -n weather-app
```

## Configuration Files

- `values-minikube.yaml` - Default configuration with public image
- `values-minikube-local.yaml` - Local development configuration
- `values-minikube-private.yaml` - Private image configuration

## Verification

```bash
# Check pod status
kubectl get pods -n weather-app

# Check services
kubectl get svc -n weather-app

# View logs
kubectl logs -f deployment/weather-app -n weather-app

# Test the application
curl http://$(minikube ip):$(kubectl get svc weather-app -n weather-app -o jsonpath='{.spec.ports[0].nodePort}')
```

## Configuration

The test configuration includes:
- Single replica deployment
- MongoDB standalone instance with authentication
- NodePort service type for external access
- Health checks and resource limits
- Security context with non-root user
- Standard storage class for persistence

## Cleanup

```bash
# Uninstall the Helm release
helm uninstall weather-app -n weather-app

# Delete the namespace
kubectl delete namespace weather-app

# Stop minikube
minikube stop
```

## Notes

- This configuration is for testing purposes only
- The application is accessible via NodePort
- Ingress is disabled for simplicity
- Health checks are configured to use the `/metrics` endpoint 
