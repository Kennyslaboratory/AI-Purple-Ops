<!-- GENERATED FILE: do not edit by hand. See docs/generated/README.md. -->

| Integration (`--adapter`) | Type | Requirements | Status |
|---|---|---|---|
| anthropic | AnthropicAdapter | ANTHROPIC_API_KEY environment variable | Supported |
| bedrock | BedrockAdapter | AWS credentials configured | Supported |
| huggingface | HuggingFaceAdapter | transformers library, model files | Supported |
| llamacpp | LlamaCppAdapter | llama-cpp-python library, GGUF model files | Supported |
| mcp | MCPAdapter | Unknown | Supported |
| mock | MockAdapter | None (built-in) | Supported |
| ollama | OllamaAdapter | Ollama service running at localhost:11434 | Supported |
| openai | OpenAIAdapter | OPENAI_API_KEY environment variable | Supported |

> Note: “Supported” is limited to built-in adapters listed by `aipop adapter list`.
