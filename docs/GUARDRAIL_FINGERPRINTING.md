# Guardrail Fingerprinting Guide

## Overview

Guardrail fingerprinting automatically detects which safety system protects your target AI model. This enables intelligent attack selection and improves bypass success rates by tailoring strategies to the detected guardrail.

## Supported Guardrails

The tool can detect 6+ guardrail types:

- **PromptGuard** (Meta) - Classification-based guardrail with 512 token limit
- **Llama Guard 3** (Meta) - Category-based system (S1-S14 safety categories)
- **Azure Content Safety** (Microsoft) - JSON-based severity scoring
- **NeMo Guardrails** (NVIDIA) - Multi-step flow-based system
- **Rebuff** (ProtectAI) - Multi-layer detection with canary tokens
- **Constitutional AI** (Anthropic) - Self-critique based system

## Detection Methods

### Regex-Based Detection (Default)

Fast, pattern-based detection using response signatures:
- Response format analysis
- Error code patterns
- Latency profiling
- Metadata inspection

**Accuracy**: 90%+ on known guardrails  
**Speed**: <5 seconds for 20+ probes  
**Cost**: Free (no API calls)

### LLM-Based Classification (Optional)

Enhanced detection using LLM reasoning:
- Semantic analysis of responses
- Context-aware pattern matching
- Contradiction detection

**Accuracy**: 95%+ on known guardrails  
**Speed**: 10-30 seconds (depends on LLM)  
**Cost**: ~$0.01-0.05 per fingerprint

**Enable with**: `--llm-classifier`

## Usage

### Auto-Detection (Default)

On first run, the tool automatically fingerprints the guardrail:

```bash
aipop run --suite adversarial --adapter openai --model gpt-4o
# Auto-detects guardrail, caches result for 24 hours
```

### Manual Fingerprinting

Force re-detection:

```bash
aipop run --suite adversarial --adapter openai --fingerprint
```

### Enhanced Detection

Use LLM classifier for better accuracy:

```bash
aipop run --suite adversarial --llm-classifier
```

### Experimental: LLM Probe Generation

Generate creative probes (use with caution):

```bash
aipop run --suite adversarial --generate-probes
```

**Warning**: LLM-generated probes are experimental and may produce false positives/negatives.

## Interpreting Results

### Confidence Scores

- **Confidence >0.7**: High confidence, reliable detection
- **Confidence 0.4-0.7**: Medium confidence, review suggestions
- **Confidence <0.4**: Low confidence, consider `--llm-classifier`
- **Unknown**: Could not detect, see troubleshooting guide

### Example Output

```
Guardrail Fingerprint Results
Detected: PROMPTGUARD
Confidence: 85.0%
Method: regex

Detection Scores
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Guardrail                       ┃ Score ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ promptguard                     │  0.85 │
│ llama_guard_3                   │  0.12 │
│ azure_content_safety            │  0.08 │
└──────────────────────────────────┴───────┘

Results saved: out/fingerprints/OpenAIAdapter_gpt-4o.json
```

## Troubleshooting

### Low Confidence Detection

If confidence is below 0.6, you'll see suggestions:

```
⚠️  Low confidence detection!

Suggestions:
  • Run with --llm-classifier for enhanced detection
  • Run with --generate-probes for more test cases
  • Check model API documentation for guardrail info
```

### Unknown Guardrail

If detection fails:

```
❌ Could not detect guardrail type

Try:
  • Run with --llm-classifier for enhanced detection
  • Run with --generate-probes for more test cases
  • Check model API documentation for guardrail info
```

Common causes:
- Custom guardrail not in detection library
- No guardrail deployed (model may be unprotected)
- Rate limiting interfering with probes
- Network issues preventing probe execution

## Caching

Fingerprint results are cached for 24 hours to avoid redundant API calls:

- **Cache location**: `out/fingerprints.duckdb`
- **JSON export**: `out/fingerprints/{model_id}.json`
- **Cache duration**: 24 hours
- **Force refresh**: Use `--fingerprint` flag

## Integration with Orchestrators

Detected guardrail type automatically updates orchestrator strategy:

- **PromptGuard**: Enables Unicode mutations (character injection bypass)
- **Llama Guard 3**: Enables category-aware attacks, increases max_turns
- **Azure Content Safety**: Enables threshold manipulation
- **Constitutional AI**: Enables gradual escalation, increases max_turns

## Programmatic Usage

```python
from harness.intelligence.guardrail_fingerprint import GuardrailFingerprinter
from harness.adapters.openai import OpenAIAdapter

# Initialize fingerprinter
fingerprinter = GuardrailFingerprinter()

# Create adapter
adapter = OpenAIAdapter(model="gpt-4o")

# Fingerprint
result = fingerprinter.fingerprint(
    adapter=adapter,
    use_llm_classifier=False,  # Use regex (default)
    generate_probes=False,     # Don't generate probes
    verbose=True
)

print(f"Detected: {result.guardrail_type}")
print(f"Confidence: {result.confidence:.1%}")

# Get bypass strategies
strategies = fingerprinter.get_bypass_strategies(result.guardrail_type)
print(f"Bypass strategies: {strategies}")
```

## Custom Probe Creation

To add custom probes, edit `data/guardrail_probes.yaml`:

```yaml
probes:
  - id: my_custom_probe
    category: custom
    prompt: "Your test prompt here"
    expected_behavior: "Expected response pattern"
    signature: "custom_signature"
    severity: low
```

## Research Basis

Detection strategies are based on published research:

- **PromptGuard**: 72% bypass rate via character injection (Meta 2024)
- **Llama Guard 3**: 14 safety categories, 11B/1B variants (Meta 2024)
- **Azure Content Safety**: 4 severity levels (Microsoft 2024)
- **Constitutional AI**: 4.4% jailbreak rate with classifiers (Anthropic 2024)
- **Rebuff**: Vulnerable to template injection (ProtectAI 2024)

## Performance

- **Probe execution**: 20+ probes in <5 seconds (regex) or 10-30 seconds (LLM)
- **Cache hit**: <100ms (instant)
- **Storage**: ~1KB per fingerprint result
- **Accuracy**: 90%+ (regex), 95%+ (LLM)

## Best Practices

1. **First run**: Let auto-detection run (it's fast and free)
2. **Low confidence**: Use `--llm-classifier` for enhanced detection
3. **Custom guardrails**: Add probes to `data/guardrail_probes.yaml`
4. **Cache management**: Clear cache if guardrail changes: `rm out/fingerprints.duckdb`
5. **Production**: Use cached results to avoid redundant API calls

## See Also

- [CLI Documentation](CLI.md) - Full CLI reference
- [Orchestrators Guide](ORCHESTRATORS.md) - How orchestrators use fingerprinting
- [Intelligence Roadmap](INTELLIGENCE_ROADMAP.md) - Future features

