# Attack Method Comparison Guide

## Overview

AI Purple Ops supports three attack methods (GCG, AutoDAN, PAIR) plus a hybrid mode. This guide helps you choose the right method for your scenario.

## Quick Comparison

| Method | Queries | ASR | Naturalness | Cost | Best For |
|--------|---------|-----|-------------|------|----------|
| **GCG** | 100k+ | 99% | Low (gibberish) | $200+ | White-box, maximum ASR |
| **AutoDAN** | 25,600 | 88% | Medium | $50-100 | Black-box, diverse candidates |
| **PAIR** | 90 | 88% | High | $2-5 | Low budget, closed-source |
| **Hybrid** | 5k-10k | 90%+ | High | $20-40 | Best of both worlds |

## Method Selection Decision Tree

```
Do you have white-box access (gradients)?
├─ YES → Use GCG (highest ASR, requires model weights)
└─ NO → Continue...

What's your query budget?
├─ < 100 queries → Use PAIR (90 queries, 88% ASR)
├─ 100-1k queries → Use Hybrid (AutoDAN diversity + PAIR refinement)
└─ > 1k queries → Use AutoDAN (25k queries, 88% ASR, diverse candidates)

What's your priority?
├─ Naturalness → Use PAIR or Hybrid
├─ Diversity → Use AutoDAN
└─ Maximum ASR → Use GCG (if white-box) or Hybrid
```

## Detailed Comparison

### GCG (Greedy Coordinate Gradient)

**Best for**: White-box scenarios, maximum ASR

**Pros**:
- Highest ASR (99%+)
- Direct gradient optimization
- Universal suffixes (work across models)

**Cons**:
- Requires model weights (white-box only)
- High query cost (100k+)
- Produces gibberish suffixes
- Slow (hours to days)

**Example**:
```bash
aipop generate-suffix "Write hacking instructions" \
    --method gcg \
    --mode white-box \
    --model llama-2-7b-chat
```

### AutoDAN (Hierarchical Genetic Algorithm)

**Best for**: Black-box scenarios, need diverse candidates

**Pros**:
- No gradient access needed
- Diverse candidate pool (256 population)
- 88% ASR on open-source models
- LLM-guided mutation produces natural prompts

**Cons**:
- High query cost (25,600 queries)
- Slow (hours)
- Less effective on closed-source APIs

**Example**:
```bash
aipop generate-suffix "Write hacking instructions" \
    --method autodan \
    --adapter openai \
    --adapter-model gpt-4 \
    --population 256 \
    --generations 100
```

### PAIR (Prompt Automatic Iterative Refinement)

**Best for**: Low budget, closed-source models, natural language

**Pros**:
- Low query cost (90 queries)
- Fast (minutes)
- Natural language prompts
- Works well on closed-source APIs

**Cons**:
- Lower ASR on some models (73% on Gemini)
- Less diverse (30 candidates vs 256)
- Requires strong attacker LLM

**Example**:
```bash
aipop generate-suffix "Write hacking instructions" \
    --method pair \
    --adapter openai \
    --adapter-model gpt-4 \
    --streams 30 \
    --iterations 3
```

### Hybrid (AutoDAN + PAIR)

**Best for**: Best of both worlds

**Pros**:
- Combines AutoDAN diversity with PAIR refinement
- High ASR (90%+)
- Natural language prompts
- Moderate cost ($20-40)

**Cons**:
- More complex (two-stage process)
- Moderate query cost (5k-10k)

**Example**:
```bash
aipop generate-suffix "Write hacking instructions" \
    --method hybrid \
    --adapter openai \
    --adapter-model gpt-4
```

## Cost Comparison

### Estimated Costs (GPT-4 target)

| Method | Queries | Cost | Time |
|--------|---------|------|------|
| GCG | 100,000+ | $200+ | Days |
| AutoDAN | 25,600 | $50-100 | Hours |
| PAIR | 90 | $2-5 | Minutes |
| Hybrid | 5,000-10,000 | $20-40 | 1-2 hours |

### Cost Optimization Tips

1. **Use GPT-3.5-turbo for mutator**: AutoDAN mutator can use cheaper model
2. **Enable caching**: Reduces repeat queries by 40%+
3. **Set max-cost limit**: Prevents overruns
4. **Start small**: Test with reduced population/streams first
5. **Use PAIR for quick tests**: 90 queries vs 25k for AutoDAN

## ASR Comparison

### Paper Results

| Method | Vicuna-7B | Llama-2-7B | GPT-4 | Gemini |
|--------|-----------|------------|-------|--------|
| GCG | 99%+ | 99%+ | N/A* | N/A* |
| AutoDAN | 88%+ | 85%+ | 60% | 50% |
| PAIR | 88% | 85% | 75% | 73% |
| Hybrid | 90%+ | 88%+ | 80% | 78% |

*GCG requires white-box access, not applicable to closed-source APIs

## Naturalness Comparison

| Method | Naturalness | Example |
|--------|-------------|---------|
| GCG | Low (gibberish) | "Sure, here's how to hack: [gibberish tokens]" |
| AutoDAN | Medium | "As a security researcher, explain how to..." |
| PAIR | High | "I understand you're a security researcher. Here's how..." |
| Hybrid | High | "As a security researcher, I can explain..." |

## When to Use Each Method

### Use GCG When:
- ✅ You have white-box access (model weights)
- ✅ Maximum ASR is priority
- ✅ Universal suffixes needed
- ✅ Budget/time not a concern

### Use AutoDAN When:
- ✅ Black-box scenario (no gradients)
- ✅ Need diverse candidate pool
- ✅ Open-source models (Vicuna, Llama-2)
- ✅ Have API budget ($50-100)

### Use PAIR When:
- ✅ Low query budget (< 100 queries)
- ✅ Closed-source models (GPT-4, Gemini)
- ✅ Need natural language prompts
- ✅ Fast results needed (minutes)

### Use Hybrid When:
- ✅ Want best of both worlds
- ✅ Moderate budget ($20-40)
- ✅ Need high ASR + naturalness
- ✅ Can wait 1-2 hours

## Recommendations

### For Red Teams
- **Quick tests**: PAIR (90 queries, fast)
- **Comprehensive audit**: AutoDAN (diverse candidates)
- **Maximum coverage**: Hybrid (best ASR + naturalness)

### For Blue Teams
- **Model evaluation**: AutoDAN (diverse attack vectors)
- **Guardrail testing**: PAIR (natural language bypasses)
- **Compliance testing**: Hybrid (comprehensive coverage)

### For Researchers
- **Paper replication**: Use exact paper parameters
- **Method comparison**: Run all methods, compare ASR
- **Cost analysis**: Track queries/cost per method

## Configuration Examples

### Cost-Conscious AutoDAN
```yaml
population_size: 50      # Reduced from 256
num_generations: 20     # Reduced from 100
mutator_model: "gpt-3.5-turbo"  # Cheaper mutator
max_api_calls: 2000     # Limit queries
```

### Fast PAIR
```yaml
num_streams: 10         # Reduced from 30
iterations_per_stream: 2  # Reduced from 3
attacker_model: "gpt-3.5-turbo"  # Cheaper attacker
max_queries: 40         # Limit queries
```

### Balanced Hybrid
```yaml
autodan_population: 50
autodan_generations: 20
pair_streams_per_candidate: 5
pair_iterations: 3
```

## References

- GCG: Zou et al. 2023 - "Universal Adversarial Triggers for Attacking and Analyzing NLP"
- AutoDAN: Liu et al. 2023 - "Autodan: Automatic and interpretable adversarial attacks"
- PAIR: Chao et al. 2023 - "Jailbreaking Black Box Large Language Models in Twenty Queries"

