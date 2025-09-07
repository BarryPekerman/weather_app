#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Minikube setup...${NC}"

# Check if minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "Minikube is not installed. Please install it first."
    exit 1
fi

# Check if minikube is running
if ! minikube status | grep -q "Running"; then
    echo -e "${YELLOW}Starting minikube...${NC}"
    # Start minikube without ingress (causes hangs)
    minikube start \
        --driver=docker \
        --cpus=2 \
        --memory=4096 \
        --disk-size=20g \
        --addons=storage-provisioner
else
    echo "Minikube is already running"
fi

# Enable required addons (skip ingress)
echo -e "${YELLOW}Enabling required addons...${NC}"
minikube addons enable metrics-server
minikube addons enable dashboard

# Configure Docker to use minikube's daemon
echo -e "${YELLOW}Configuring Docker to use minikube's daemon...${NC}"
eval $(minikube docker-env)

# Create namespace for the application
echo -e "${YELLOW}Creating namespace...${NC}"
kubectl create namespace weather-app --dry-run=client -o yaml | kubectl apply -f -

# Update Helm repositories
echo -e "${YELLOW}Updating Helm repositories...${NC}"
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install the chart
echo -e "${YELLOW}Installing the Weather App chart...${NC}"
helm dependency update
helm install weather-app . -f values-minikube.yaml -n weather-app

# Wait for pods to be ready (FIXED LABEL)
echo -e "${YELLOW}Waiting for pods to be ready...${NC}"
kubectl wait --for=condition=ready pod -l app=weather-app -n weather-app --timeout=300s

# Get the NodePort
echo -e "${YELLOW}Getting service information...${NC}"
NODEPORT=$(kubectl get svc weather-app -n weather-app -o jsonpath='{.spec.ports[0].nodePort}')
MINIKUBE_IP=$(minikube ip)

echo -e "${GREEN}Setup complete!${NC}"
echo -e "You can access the application at: ${YELLOW}http://${MINIKUBE_IP}:${NODEPORT}${NC}"
echo -e "To view the dashboard: ${YELLOW}minikube dashboard${NC}"
echo -e "To check pod status: ${YELLOW}kubectl get pods -n weather-app${NC}"
echo -e "To check service status: ${YELLOW}kubectl get svc -n weather-app${NC}" 
