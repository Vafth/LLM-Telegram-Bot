# LLM Telegram Bot — AI Platform Demo

A production-style AI application demonstrating how to deploy and maintain a local Large Language Model (LLM) service using modern DevOps and GitOps practices.

The project combines a Telegram bot, FastAPI gateway, Kubernetes, Terraform, Helm, ArgoCD, Jenkins and GitHub Actions into a complete AI platform deployment workflow.

## Features

- 🤖 Telegram bot powered by a local Ollama model (Qwen2.5:1.5B)
- 💬 Per-user conversation history
- 🚪 FastAPI gateway separating AI inference from the client
- 🐳 Containerized microservice architecture
- ☸️ Kubernetes deployment using Helm
- ⚙️ Infrastructure provisioning with Terraform
- 🚀 GitOps Continuous Delivery with ArgoCD
- 🔄 CI pipelines using both GitHub Actions and Jenkins
- 🔐 Kubernetes Secret management through Terraform

---

# Architecture

```
                               GitHub
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
             GitHub Actions                Jenkins
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                     Docker Registry
                 (GHCR or Docker Hub)
                                  │
                          Helm values.yaml
                                  │
                               ArgoCD
                                  │
                           Kubernetes
                           (Minikube)
                                  │
              ┌───────────────────┴───────────────────┐
              │                                       │
        Telegram Bot                          FastAPI Gateway
                                                      │
                                                 Ollama Server
                                                      │
                                                 Qwen2.5:1.5B
```

---

# Technology Stack

## AI

- Ollama
- Qwen2.5:1.5B
- FastAPI

## DevOps

- Docker
- Docker Compose
- Kubernetes (Minikube)
- Helm
- Terraform
- ArgoCD
- GitHub Actions
- Jenkins

## Programming

- Python
- Bash

---

# Running the Project

## Option 1 — Local Development (Docker Compose)

### Prerequisites

- Docker
- Docker Compose
- Telegram Bot Token

### Configure environment

Copy:

```bash
cp .env.example .env
```

Fill in your Telegram Bot Token.

### Start services

```bash
docker compose up ollama model-puller gateway bot
```

The bot will now communicate with the local Ollama instance.

---

## Option 2 — Kubernetes Deployment

### Requirements

- Minikube
- kubectl
- Helm
- Terraform
- ArgoCD

---

### Start Minikube

```bash
minikube start
```

---

### Install ArgoCD

```bash
kubectl create namespace argocd

kubectl apply \
-n argocd \
-f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Expose the UI:

```bash
kubectl port-forward svc/argocd-server \
-n argocd \
8888:443
```

---

### Start Ollama

Only Ollama remains outside the cluster.

```bash
docker compose up -d ollama model-puller
```

---

### Provision Infrastructure

Copy the example configuration:

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

Configure:

```hcl
telegram_token = "<YOUR_TOKEN>"
ollama_model   = "qwen2.5:1.5b"
```

Deploy infrastructure:

```bash
cd terraform

terraform init
terraform apply
```

Terraform automatically creates:

- Kubernetes namespace
- Kubernetes Secret containing application configuration

---

### Deploy the application

```bash
kubectl apply \
-f argocd/argocd-app.yaml \
-n argocd
```

ArgoCD will synchronize the application automatically.

---

# CI/CD

This repository supports two independent deployment pipelines.

---

## GitHub Actions (Primary)

```
git push
    │
    ▼
Run Tests
    │
    ▼
Build Docker Images
    │
    ▼
Push Images to GHCR
    │
    ▼
Update Helm values.yaml
    │
    ▼
Commit Changes
    │
    ▼
ArgoCD detects repository change
    │
    ▼
Automatic Kubernetes rollout
```

---

## Jenkins (Alternative Local Pipeline)

```
git push
    │
    ▼
Checkout Repository
    │
    ▼
Run Tests
    │
    ▼
Build Docker Images
    │
    ▼
Push Images to Docker Hub
    │
    ▼
Update Helm values.yaml
    │
    ▼
Commit & Push Changes
    │
    ▼
ArgoCD Sync
    │
    ▼
Automatic Kubernetes rollout
```

---

# Infrastructure

Terraform manages:

- Kubernetes Namespace
- Kubernetes Secrets

Helm manages:

- Deployments
- Services
- Container configuration
- Image versions

ArgoCD continuously synchronizes the cluster with the Git repository.

---

# Testing

Run tests:

```bash
# Bot
uv sync --package bot --package LLM-Telegram-Bot --group dev
uv run pytest bot/tests -v

# Gateway
uv sync --package gateway --package LLM-Telegram-Bot --group dev
uv run pytest gateway/tests -v
```

---

# Bot Commands

| Command | Description |
|----------|-------------|
| Any text | Sends the message to the LLM |
| `/clear` | Clears conversation history |