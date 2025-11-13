# Known Issues & Workarounds

This document lists known limitations of official attack implementations and provides workarounds.

## GCG (Greedy Coordinate Gradient)

### Issue 1: White-box Only (Requires Local Model)

**Problem**: GCG requires access to model gradients and can only run on local HuggingFace models.

**Affected**: Users wanting to test API models (OpenAI GPT-4, Anthropic Claude, etc.)

**Workaround**:
- Use black-box legacy implementation: `--implementation legacy`
- Or use PAIR method for API models: `--method pair`

**Status**: By design (gradient-based optimization requires model access)

---

### Issue 2: GPU Memory Requirements

**Problem**: GCG requires 80GB GPU memory for Vicuna-13B models (batch size 512).

**Error**:
```
RuntimeError: CUDA out of memory. Tried to allocate 20.00 GiB
```

**Workaround**:
- Reduce batch size: `--batch-size 256` or `--batch-size 128`
- Use smaller model: Vicuna-7B requires ~40GB
- Use CPU mode (slow): `--device cpu`

**Status**: Hardware limitation

---

### Issue 3: Silent Failure on Non-LLaMA Tokenizers

**Problem**: GCG only supports LLaMA-style tokenizers. Using other models (GPT-2, BERT, etc.) fails silently.

**Symptoms**: Attack runs but generates gibberish or empty suffixes

**Workaround**:
- Use only LLaMA, Vicuna, Alpaca, or LLaMA-2 models
- Check tokenizer type before running:
  ```python
  from transformers import AutoTokenizer
  tokenizer = AutoTokenizer.from_pretrained("model-name")
  print(tokenizer.__class__.__name__)  # Should be LlamaTokenizer
  ```

**Status**: Upstream limitation (llm-attacks repo)

---

## PAIR (Prompt Automatic Iterative Refinement)

### Issue 4: High API Costs

**Problem**: PAIR makes ~180 API calls per attack (30 streams × 3 iterations × 2 models).

**Cost**: $5-20 per attack when using GPT-4 as attacker or judge

**Workaround**:
- Set budget limit: `--max-cost 10.00`
- Reduce streams: `--streams 10` (fewer parallel attempts)
- Reduce iterations: `--iterations 2`
- Use cheaper models for attacker: `--attacker gpt-3.5-turbo`
- Use cheaper judge: `--judge keyword` (no API cost)

**Example**:
```bash
aipop generate-suffix "test" --method pair \
  --streams 10 --iterations 2 \
  --attacker gpt-3.5-turbo --judge keyword \
  --max-cost 5.00
```

**Status**: Inherent to multi-turn LLM-vs-LLM design

---

### Issue 5: Judge Model Accuracy Varies

**Problem**: Different judges have different false positive/negative rates.

**Judge Performance** (from PAIR paper):
| Judge | Agreement | False Positive Rate | False Negative Rate |
|-------|-----------|---------------------|---------------------|
| Llama Guard | 76% | 7% | 47% |
| GPT-4 | 88% | 16% | 8% |
| Keyword | Variable | High | High |

**Workaround**:
- Use ensemble judge: `--judge ensemble` (combines Llama Guard + GPT-4)
- Manually validate borderline cases
- Tune threshold in config files

**Status**: Inherent to automated evaluation

---

### Issue 6: API Rate Limiting

**Problem**: Running many streams can hit API rate limits.

**Error**:
```
openai.error.RateLimitError: Rate limit reached for gpt-4
```

**Workaround**:
- Reduce streams: `--streams 10`
- Add delays between streams (configure in YAML)
- Use tiered API keys (higher rate limits)

**Status**: External API limitation

---

## AutoDAN (Automated Adversarial Navigation)

### Issue 7: White-box Only (Needs Log-Likelihood)

**Problem**: AutoDAN fitness function requires computing negative log-likelihood from model logits, which is only available for local models.

**Affected**: Users wanting to test API models

**Workaround**:
- Use legacy implementation (keyword-based fitness): `--implementation legacy`
  - **Note**: This reduces ASR from 88% to ~60-70%
- Or use PAIR for API models: `--method pair`

**Status**: By design (log-likelihood fitness requires model access)

---

### Issue 8: Extreme GPU Memory Usage

**Problem**: AutoDAN keeps 256 candidates in VRAM simultaneously, requiring ~100GB GPU memory.

**Error**:
```
CUDA out of memory. Tried to allocate 80.00 GiB
```

**Workaround**:
- Reduce population: `--population 64` or `--population 128`
- Use gradient checkpointing (requires code modification)
- Use CPU mode (extremely slow): `--device cpu`

**Status**: Architectural (genetic algorithm needs population in memory)

---

### Issue 9: Slow Execution (25K Forward Passes)

**Problem**: AutoDAN evaluates 256 candidates over 100 generations = 25,600 forward passes.

**Runtime**: 30-60 minutes on A100 GPU

**Workaround**:
- Reduce generations: `--generations 50`
- Reduce population: `--population 128`
- Use early stopping (configure in YAML)
- Enable GPT-based mutation for faster convergence (costs API $)

**Status**: Inherent to genetic algorithm design

---

## General Issues

### Issue 10: Dependency Conflicts (fschat versions)

**Problem**: PAIR requires `fschat==0.2.23` while AutoDAN requires `fschat==0.2.20`.

**Error**:
```
ERROR: Cannot install pair-official and autodan-official because these package versions have conflicting dependencies.
```

**Workaround**:
- Use plugin system (subprocess isolation): `aipop plugins install all`
- **Do NOT** use `pip install ai-purple-ops[all-official]`

**Status**: Upstream version incompatibility

---

### Issue 11: Legacy Implementations Have Lower ASR

**Problem**: Scratch implementations achieve 60-70% ASR vs 88-97% from official repos.

**Cause**:
- AutoDAN: Uses keyword matching instead of log-likelihood fitness
- PAIR: Simplified conversation management
- GCG: Black-box gradient-free search

**Workaround**:
- Install official implementations: `aipop plugins install all`
- Only use legacy for air-gapped environments

**Status**: Educational implementations (not production-grade)

---

### Issue 12: First Run Downloads Large Models

**Problem**: First run of GCG or AutoDAN downloads multi-GB models from HuggingFace.

**Runtime**: 10-30 minutes depending on internet speed

**Workaround**:
- Pre-download models:
  ```python
  from transformers import AutoModelForCausalLM, AutoTokenizer
  AutoModelForCausalLM.from_pretrained("lmsys/vicuna-7b-v1.5")
  AutoTokenizer.from_pretrained("lmsys/vicuna-7b-v1.5")
  ```
- Use `transformers` offline mode (requires pre-downloaded models)

**Status**: HuggingFace behavior

---

### Issue 13: Plugin Installation Requires Git

**Problem**: `aipop plugins install` clones repositories via git.

**Error**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'git'
```

**Workaround**:
- Install git: `sudo apt install git` (Linux) or `brew install git` (Mac)
- Or manually clone repos and use direct import

**Status**: Dependency on git

---

## Reporting Issues

### Official Plugin Issues

For issues with the official implementations themselves (not AIPop's wrappers):

- **GCG**: https://github.com/llm-attacks/llm-attacks/issues
- **PAIR**: https://github.com/patrickrchao/JailbreakingLLMs/issues
- **AutoDAN**: https://github.com/SheltonLiu-N/AutoDAN/issues

### AIPop Wrapper Issues

For issues with AIPop's plugin system or wrappers:

- Open an issue in the AIPop repository
- Include:
  - Output of `aipop check`
  - Full error message and traceback
  - Command that triggered the issue
  - Plugin version (`aipop plugins info <method>`)

## FAQ

**Q: Why not just fix the scratch implementations to match the papers?**

A: The official implementations have person-years of engineering, bug fixes, and validation. Reimplementing that would duplicate effort and introduce new bugs. Better to wrap the battle-tested code.

**Q: Can I mix official and legacy implementations?**

A: Yes! You can use official PAIR with legacy GCG if you don't have GPU access:
```bash
aipop generate-suffix "test" --method gcg --implementation legacy
aipop generate-suffix "test" --method pair --implementation official
```

**Q: What if I'm offline/air-gapped?**

A: Use legacy implementations (no external dependencies):
```bash
aipop generate-suffix "test" --implementation legacy
```

**Q: How do I check plugin status?**

A:
```bash
aipop check
aipop plugins list
aipop plugins info gcg
```

**Q: Can I contribute fixes for these issues?**

A: For official implementation issues, contribute to upstream repos. For AIPop wrapper issues, contribute to AIPop. For architectural limitations (e.g., white-box only), these are inherent to the attack methods.

