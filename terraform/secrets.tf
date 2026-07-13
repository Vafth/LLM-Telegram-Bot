resource "kubernetes_secret" "bot_secret" {
  metadata {
    name = "bot-secret"
    namespace = kubernetes_namespace.llm_bot.metadata[0].name
  }

  data = {
    TOKEN        = var.telegram_token
    GATEWAY_URL  = var.gateway_url
    OLLAMA_URL   = var.ollama_url
    OLLAMA_MODEL = var.ollama_model
    LLM_PROVIDER = var.llm_provider
  }
}