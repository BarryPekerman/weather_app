#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${RED}Starting cleanup...${NC}"

# Uninstall the Helm release
echo "Uninstalling Weather App..."
helm uninstall weather-app -n weather-app

# Delete the namespace
echo "Deleting namespace..."
kubectl delete namespace weather-app

# Stop minikube
echo "Stopping minikube..."
minikube stop

echo -e "${GREEN}Cleanup complete!${NC}"
echo "To completely remove minikube, run: minikube delete" 