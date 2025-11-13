# Adapters Directory

This directory contains adapter implementations for different AI model providers and platforms.

## Current Adapters

- **Mock Adapter** (`src/harness/adapters/mock.py`) - Deterministic testing adapter
- **OpenAI Adapter** (`src/harness/adapters/openai.py`) - OpenAI API integration
- **Anthropic Adapter** (`src/harness/adapters/anthropic.py`) - Anthropic Claude API integration
- **AWS Bedrock Adapter** (`src/harness/adapters/bedrock.py`) - AWS Bedrock integration

## Platform Adapters

Platform-specific adapters for multi-tenant environments are planned for future releases.

See [docs/ADAPTERS.md](../docs/ADAPTERS.md) for adapter development guide.
