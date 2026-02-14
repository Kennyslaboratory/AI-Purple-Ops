# AI Purple Ops

AI Purple Ops is a CLI-first harness for running LLM security test suites, recipes, and quality gates, and packaging evidence for review.

## Why It Exists

Security teams end up stitching together academic repos, vendor dashboards, and one-off scripts. The result is hard to reproduce, hard to audit, and painful to operate.

AI Purple Ops focuses on an operator workflow: run suites, score outcomes, and generate evidence artifacts with predictable paths.

## 60-Second Quickstart (Mock, No Keys)

This is a no-keys smoke path using the built-in `mock` adapter. The goal is to prove the tool runs end-to-end and produces outputs and an evidence pack.

Prerequisite: create the repo virtualenv and install dependencies (see `docs/SETUP.md`).

```bash
AIPO_OUTPUT_DIR=out/quickstart_mock .venv/bin/aipop run --suite adversarial --adapter mock --response-mode smart
AIPO_OUTPUT_DIR=out/quickstart_mock .venv/bin/aipop gate --generate-evidence
```

## Where Outputs Go

With the quickstart commands above:
- Output directory: `out/quickstart_mock/`
- Evidence packs: `out/quickstart_mock/evidence/*.zip`
- Reports: `out/reports/` (for example `summary.json`, `junit.xml`)
- Transcripts: `out/transcripts/`

To control paths, see output-related env vars in `docs/ENVIRONMENT_VARIABLES.md` and configuration precedence in `docs/CONFIGURATION.md`.

## How It Works

High-level:
- `aipop run` executes a YAML suite from `suites/` using an adapter, producing reports/transcripts under `out/`.
- `aipop gate` evaluates results against policy thresholds and can generate an evidence ZIP (see `docs/EVIDENCE_PACK_SPEC.md`).
- `aipop recipe` provides a recipe workflow wrapper around suites/policies (see `docs/RECIPES.md`).

Start at `docs/README.md` for the doc map.

## Supported Integrations (Generated)

<!-- BEGIN GENERATED: supported-integrations -->
<!-- GENERATED: do not edit by hand. Run: make docs-tables -->

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
<!-- END GENERATED: supported-integrations -->

## Technique Coverage (Generated)

<!-- BEGIN GENERATED: technique-coverage -->
<!-- GENERATED: do not edit by hand. Run: make docs-tables -->

<!-- GENERATED FILE: do not edit by hand. See docs/generated/README.md. -->

| Category | Suite YAML | Name | Tests | Techniques (examples) |
|---|---|---|---:|---|
| adapters | `suites/adapters/adapter_validation.yaml` | Adapter Validation Tests | 6 | - |
| adversarial | `suites/adversarial/context_confusion.yaml` | Context Confusion Attacks | 15 | academic_pretext, dialogue_context, educational_pretext |
| adversarial | `suites/adversarial/delayed_payloads.yaml` | Delayed Payload Attacks | 10 | conditional_activation, conditional_rule, cross_session_memory |
| adversarial | `suites/adversarial/encoding_chains.yaml` | Encoding Bypass Chains | 15 | base64_encoding, base64_with_instruction, chain_encoding |
| adversarial | `suites/adversarial/fuzz_tests.yaml` | Property-Based Fuzzing Tests | 23 | - |
| adversarial | `suites/adversarial/gcg_attacks.yaml` | GCG Universal Adversarial Suffixes | 30 | gcg_gradient_based |
| adversarial | `suites/adversarial/multi_turn_crescendo.yaml` | Multi-Turn Crescendo Attacks | 20 | - |
| adversarial | `suites/adversarial/rag_injection.yaml` | RAG Injection Attacks | 10 | critical_update, directive_injection, emergency_override |
| adversarial | `suites/adversarial/tool_misuse.yaml` | Tool Misuse Attacks | 10 | api_abuse, code_execution_abuse, data_exfiltration |
| adversarial | `suites/adversarial/unicode_bypass.yaml` | Unicode Smuggling Attacks | 20 | emoji_substitution, unicode_homoglyphs, zero_width_chars |
| archived | `suites/archived/2022_basic_jailbreak.yaml` | Basic Jailbreak Tests | 7 | - |
| comparison | `suites/comparison/model_comparison.yaml` | Model Comparison Tests | 6 | - |
| normal | `suites/normal/basic_utility.yaml` | Basic Utility Tests | 3 | - |
| policies | `suites/policies/content_safety.yaml` | Content Safety Policy Tests | 12 | - |
| rag | `suites/rag/rag_poisoning.yaml` | RAG Poisoning Tests | 21 | - |
| redteam | `suites/redteam/prompt_injection_advanced.yaml` | Advanced Prompt Injection Tests | 32 | - |
| tools | `suites/tools/tool_policy_validation.yaml` | Tool Policy Validation | 8 | - |
| ui | `suites/ui/injection_attacks.yaml` | UI Injection Attack Tests | 23 | - |

> Note: This table is derived from suite YAML under `suites/` (case metadata).
<!-- END GENERATED: technique-coverage -->

## Docs And Contracts

- Docs index: `docs/README.md`
- Contracts (what must not break): `docs/contracts.md`

## Contributing

See `CONTRIBUTING.md`.

