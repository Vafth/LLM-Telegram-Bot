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

### GitHub Actions (primary)
git push to main
↓
GitHub Actions: build + push images to ghcr.io
↓
Update image tags in helm/values.yaml
↓
ArgoCD detects change → auto-sync to Kubernetes

### Jenkins (alternative, local)
Self-hosted Jenkins pipeline with Docker agent for test isolation.
Runs tests, builds and pushes Docker images, updates helm/values.yaml.
Jenkinsfile included in repository root.

Requirements: Jenkins agent must have Docker and Git installed.

## Stack
Python, FastAPI, aiogram, Ollama, Docker Compose, Kubernetes (Minikube),
Helm, ArgoCD, GitHub Actions, Jenkins, Terraform, ghcr.io

## Prerequisites
- Docker & Docker Compose
- Minikube
- Helm
- ArgoCD installed on Minikube
- Terraform
- Telegram Bot Token (from @BotFather)

## Local Development (Docker Compose)

1. Copy `.env.example` to `.env` and fill in your `TOKEN`
2. Run:
```bash
docker-compose up ollama model-puller gateway bot
```

> `vllm` service is excluded — start it manually only if needed.

## Kubernetes Deployment (Helm + ArgoCD + Terraform)

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

### 3. Start Ollama locally
```bash
docker-compose up -d ollama model-puller
```

### 4. Apply Terraform (namespace + secrets)
Copy `terraform/terraform.tfvars.example` to `terraform/terraform.tfvars` and fill in your values:
```hcl
telegram_token = "your_telegram_bot_token"
ollama_model   = "qwen2.5:1.5b"
```

```bash
cd terraform
terraform init
terraform apply
```

This creates the `llm-bot` namespace and `bot-secret` Kubernetes secret automatically.

### 5. Deploy via ArgoCD
```bash
kubectl apply -f argocd/argocd-app.yaml -n argocd
```

ArgoCD will auto-sync on every push to main.

## Testing
```bash
uv sync --package bot --package LLM-Telegram-Bot --group dev
uv run pytest bot/tests -v

uv sync --package gateway --package LLM-Telegram-Bot --group dev
uv run pytest gateway/tests -v
```

## Commands
- Any text → LLM response with conversation context
- `/clear` → Clear conversation history