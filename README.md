# LLM Telegram Bot - Local Ollama Infrastructure

Telegram bot powered by a locally deployed LLM (Qwen2.5:1.5b) via Ollama,
wrapped in a FastAPI gateway. Full conversation history per chat session.

## Architecture
Telegram → Bot (aiogram) → Gateway (FastAPI) → Ollama (Qwen2.5:1.5b)

## Stack
Python, FastAPI, aiogram, Ollama, Docker Compose

## Requirements
- Docker & Docker Compose
- Telegram Bot Token (from @BotFather)

## Setup
1. Copy `.env.example` to `.env` and fill in your `TOKEN`
2. `docker-compose up --build`

## Commands
- Any text → LLM response with conversation context
- `/clear` → Clear conversation history