variable "telegram_token" {
  description = "Telegram Bot API Token"
  sensitive = true
}

variable "ollama_model" {
  description = "Ollama model name"
  default = "qwen2.5:1.5b"
}

variable "ollama_url" {
  description = "URL to external ollama service"
  default = "http://host.minikube.internal:11434"
}

variable "gateway_url" {
  description = "URL to Gateway"
  default = "http://gateway:8000"
}

variable "llm_provider" {
  description = "LLM provider name"
  default = "ollama"
}