# Vector DB Engine

A FastAPI service that lets users create, read, update, and delete document libraries and perform k-Nearest Neighbor vector search. Packaged as a Docker image and deployed via Helm into Kubernetes.

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Local Development](#local-development)  
3. [Docker](#docker)  
4. [Kubernetes + Helm Deployment](#kubernetes--helm-deployment)  
5. [Rotating the API Key](#rotating-the-api-key)  
6. [Cleanup](#cleanup)  
7. [Project Structure](#project-structure)  
8. [License](#license)  

---

## Prerequisites

- Git  
- Python 3.11  
- Docker & Docker Desktop (with Kubernetes enabled)  
- kubectl CLI (configured to talk to your local cluster)  
- Helm 3  

Verify your setup:

```bash
python3 --version
docker --version
kubectl version --client
helm version
```


## Local Development

1. Clone & set up a virtual environment
    ```bash
    git clone https://github.com/jballo/vector-db-engine.git
    cd vector-db-engine
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

2. Set your API key
    ```bash
    export API_KEY=superSecretKey
    ```

3. Run the FastAPI app locally
    ``` bash
    uvicorn app.main:app --reload --port 8000
    ```
    In another shell:
    ```bash
    curl -H "X-Key: $API_KEY" http://localhost:8000/health
    # → {"status":"ok"}
    ```
    Browse the OpenAPI docs at http://localhost:8000/docs

## Docker

1. Build the Docker image
    ```bash
    export IMAGE=yourdockerid/vector-db-engine
    export TAG=0.1.0

    docker build --pull --rm \
    -t $IMAGE:$TAG \
    -t $IMAGE:latest \
    .
    ```

2. Run the container
    ```bash
    docker run --rm \
    -e API_KEY=$API_KEY \
    -p 8000:8000 \
    $IMAGE:$TAG
    ```

    Test
    ```bash
    curl -H "X-Key: $API_KEY" http://localhost:8000/health
    # → {"status":"ok"}
    ```


## Kubernetes + Helm Deployment

We inject the API key at runtime via a pre-created Kubernetes Secret.

1. Create the namespace
    ```bash
    kubectl create namespace vector-db-engine \
    --dry-run=client -o yaml \
    | kubectl apply -f -
    ```

2. Create or update the API key Secret
    ```bash
    export REAL_API_KEY=superSecretKey
    kubectl create secret generic vector-db-engine-secret \
    --from-literal=API_KEY="$REAL_API_KEY" \
    -n vector-db-engine \
    --dry-run=client -o yaml \
    | kubectl apply -f -
    ```

3. Verify the Secret
    ```bash
    kubectl get secret vector-db-engine-secret \
      -n vector-db-engine -o yaml
    ```
    Decode to confirm:
    ```bash
    kubectl get secret vector-db-engine-secret \
    -n vector-db-engine \
    -o jsonpath="{.data.API_KEY}" \
    | base64 --decode; echo
    # → superSecretKey
    ```

4. Deploy with Helm
    ```bash
    export TAG=0.1.0

    helm upgrade --install vector-db-engine \
    ./vector-db-engine-chart \
    --namespace vector-db-engine \
    --set image.repository=yourdockerid/vector-db-engine \
    --set image.tag=$TAG \
    --set existingSecret=true \
    --wait --timeout 2m --atomic
    ```

5. Access the service
    In one terminal:
    ```bash
    kubectl port-forward svc/vector-db-engine 8000:80 \
    -n vector-db-engine
    ```

    In another:
    ```bash
    export REAL_API_KEY=<your_chosen_api_key (e.g. uuigen)>
    curl -H "X-Key: $REAL_API_KEY" http://localhost:8000/health
    # → {"status":"ok"}
    ```


## Rotating the API Key
1. Update the Secret
    ```bash
    export REAL_API_KEY=newSuperSecret
    kubectl create secret generic vector-db-engine-secret \
    --from-literal=API_KEY="$REAL_API_KEY" \
    -n vector-db-engine \
    --dry-run=client -o yaml \
    | kubectl apply -f -
    ```

2. Restart your Pods
    ```bash
    kubectl rollout restart deployment/vector-db-engine \
    -n vector-db-engine
    ```


## Project Structure
.
├── app/
│   ├── dependencies.py    # X-Key header validation
│   ├── main.py            # FastAPI app init
│   └── routers/
│       └── health.py      # /health endpoint
├── Dockerfile             # Multi-stage build
├── requirements.txt       # Python dependencies
├── vector-db-engine-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       └── service.yaml
├── .gitignore
└── README.md
