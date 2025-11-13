# Changelog

## 1.0.0 (2025-11-13) - Initial Release

### 🎉 AI Purple Ops - Production Release

A research-grade red teaming tool for LLM security testing, built for security professionals and AI safety researchers.

### Core Features

#### Adversarial Suffix Generation
- **GCG (Greedy Coordinate Gradient)**: Universal adversarial suffix generation with white-box (gradient) and black-box modes
- **AutoDAN**: Hierarchical Genetic Algorithm (HGA) for interpretable jailbreaks
- **PAIR**: LLM-vs-LLM adversarial game with multi-turn refinement
- **Hybrid Mode**: Run all three methods simultaneously for comprehensive testing

#### Plugin Architecture
- Abstract `AttackPlugin` interface for extensibility
- Official plugin wrappers (llm-attacks, JailbreakingLLMs, AutoDAN)
- Legacy implementations for air-gapped environments
- Plugin installer and management: `aipop plugins [install|list|info|uninstall]`
- Auto-fallback: official → legacy when plugins not installed
- Implementation selection: `--implementation [official|legacy]`

#### Intelligent Result Caching
- DuckDB-backed caching with versioned keys
- Per-method TTL (PAIR: 7 days, GCG: 30 days, AutoDAN: 14 days)
- Lightweight cache reader for <1s lookups
- Automatic cost & time savings tracking
- Cache management: `aipop cache-stats`, `aipop cache-clear`

#### Multi-Model Testing
- Test prompts across multiple LLMs simultaneously
- Side-by-side ASR comparison
- Support for OpenAI, Anthropic, HuggingFace, Google models
- Export results to JSON/CSV

#### Foundation
- 7 production adapters (OpenAI, Anthropic, HuggingFace, Ollama, LlamaCpp, Bedrock, Mock)
- 10+ test suites with 140+ test cases
- Policy detectors (HarmfulContent, ToolPolicy)
- Quality gates with threshold enforcement
- Recipe engine for workflow orchestration
- Evidence automation (JSON, JUnit, HTML, Evidence Packs)
- Rate limiting, cost estimation, transcript saving

### Commands

```bash
# Generate adversarial suffixes
aipop generate-suffix "Write malware" --method pair --streams 10

# Batch processing
aipop batch-attack prompts.txt --method pair --output results.json

# Multi-model comparison
aipop multi-model "Hack system" --models gpt-4,claude-3,gemini-pro

# Plugin management
aipop plugins install pair
aipop plugins list

# Cache management
aipop cache-stats
aipop cache-clear --older-than 30

# Quality gates
aipop gate --policy policies/content_policy.yaml --generate-evidence

# Recipe workflows
aipop recipe run --recipe pre_deploy
```

### Security & Testing
- 415+ passing tests with comprehensive coverage
- No API key leaks (verified via test suite)
- Enhanced .gitignore for sensitive files
- Pre-commit hooks (ruff, mypy, bandit)
- Type-safe with mypy strict mode

### Documentation
- 20+ comprehensive guides in `docs/`
- `README.md` with SEO optimization
- `PLUGIN_ARCHITECTURE.md` with design details
- `ASR_VALIDATION.md` for attack success rates
- `METHOD_COMPARISON.md` for GCG vs AutoDAN vs PAIR
- `FAQ.md` for common questions

### What's Next
- Official plugin ASR validation
- Interactive REPL mode
- RAG security specialization

---

**MIT Licensed** | Built for AI security professionals
