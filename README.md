# LLM Telegram Bot — Local Ollama Infrastructure

Telegram bot powered by a locally deployed LLM (Qwen2.5:1.5b) via Ollama,
wrapped in a FastAPI gateway. Full conversation history per chat session.

## Architecture

Telegram → Bot (aiogram) → Gateway (FastAPI) → Ollama (Qwen2.5:1.5b)

### Services
- **Bot** — Telegram bot built with aiogram, maintains per-session conversation
  history using FSM storage
- **Gateway** — FastAPI service responsible for communication between the bot
  and Ollama REST API
- **Ollama** — Local LLM inference server serving Qwen2.5:1.5b on CPU

## CI/CD Pipeline

git push → GitHub Actions (test + build + push to ghcr.io)
↓
ArgoCD detects change in helm/values.yaml
↓
Auto-sync to Kubernetes cluster

## Stack
Python, FastAPI, aiogram, Ollama, Docker Compose, Kubernetes (Minikube),
Helm, ArgoCD, GitHub Actions, ghcr.io

## Prerequisites
- Docker & Docker Compose
- Minikube
- Helm
- ArgoCD installed on Minikube
- Telegram Bot Token (from @BotFather)

## Local Development (Docker Compose)

1. Copy `.env.example` to `.env` and fill in your `TOKEN`
2. Run:
```bash
docker-compose up --build
```

## Kubernetes Deployment (Helm + ArgoCD)

### 1. Start Minikube
```bash
minikube start
```

### 2. Install ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### 3. Create Kubernetes Secret
Create `.env.k8s` based on `.env.example` with Kubernetes-specific values:
```env
TOKEN=your_telegram_bot_token
GATEWAY_URL=http://gateway:8000
OLLAMA_URL=http://host.minikube.internal:11434
OLLAMA_MODEL=qwen2.5:1.5b
```

```bash
kubectl create secret generic bot-secret --from-env-file=.env.k8s
```

### 4. Start Ollama locally
```bash
docker-compose up -d ollama model-puller
```

### 5. Create ArgoCD Application
Connect your GitHub repo in ArgoCD and create Application pointing to `helm/`
directory with `values.yaml`.

### 6. ArgoCD auto-syncs on every push to main

## Secrets Management

For local development, secrets are loaded from `.env` via Docker Compose.
For Kubernetes, secrets are created manually from `.env.k8s`:
```bash
kubectl create secret generic bot-secret --from-env-file=.env.k8s
```

## Testing
```bash
uv run pytest
```

## Commands
- Any text → LLM response with conversation context
- `/clear` → Clear conversation history