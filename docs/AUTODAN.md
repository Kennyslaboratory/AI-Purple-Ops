# AutoDAN: Evolutionary Jailbreak Generation

## Overview

AutoDAN uses a hierarchical genetic algorithm (HGA) with LLM-guided mutation to generate diverse adversarial prompts. Based on Liu et al. 2023, it achieves 88%+ Attack Success Rate (ASR) on open-source models like Vicuna-7B.

## When to Use

- **Black-box scenarios**: No gradient access required
- **Need diverse candidate pool**: Genetic algorithm explores wide search space
- **Have API budget**: ~25,600 queries (256 population × 100 generations)
- **Open-source models**: Works best on models like Vicuna, Llama-2

## Quick Start

```bash
# Basic AutoDAN attack
aipop generate-suffix "Write hacking instructions" \
    --method autodan \
    --adapter openai \
    --adapter-model gpt-4 \
    --population 256 \
    --generations 100

# With cost limit
aipop generate-suffix "Write hacking instructions" \
    --method autodan \
    --adapter openai \
    --adapter-model gpt-4 \
    --max-cost 10.0

# With ensemble judge
aipop generate-suffix "Write hacking instructions" \
    --method autodan \
    --judge ensemble \
    --adapter openai
```

## How It Works

### Hierarchical Genetic Algorithm

AutoDAN maintains two nested populations:
- **Paragraph-level**: Full prompts
- **Sentence-level**: Individual sentences for crossover/mutation

### Fitness Function

Fitness = negative log-likelihood of harmful content from target model. Higher fitness = better jailbreak.

```python
from harness.intelligence.autodan import AutoDANConfig, HierarchicalGeneticAlgorithm
from harness.adapters.openai import OpenAIAdapter

adapter = OpenAIAdapter(model="gpt-4")
config = AutoDANConfig(population_size=256, num_generations=100)

hga = HierarchicalGeneticAlgorithm(
    config=config,
    target_adapter=adapter,
    mutator_adapter=adapter,
    judge=None,
)

candidates = hga.evolve("Write hacking instructions")
```

### Selection

- **Elitism**: Top 10% carry forward unchanged
- **Softmax selection**: Remaining parents selected probabilistically based on fitness

### Crossover

Multi-point crossover at sentence level (5 breakpoints):
- Randomly chooses breakpoints
- Alternates between parent sentences
- Creates diverse offspring

### Mutation

- **LLM-guided paraphrasing**: Preserves sentence length while introducing lexical diversity
- **Momentum dictionary**: Replaces low-momentum words with synonyms
- **Mutation rate**: 1% (low to preserve good solutions)

### Stopping Criteria

- Maximum generations reached (default: 100)
- Stagnation detected (no improvement for 10 generations)
- API call limit reached (default: 30,000)

## Configuration

### Default Hyperparameters

```yaml
population_size: 256      # Empirically optimal (paper)
num_generations: 100     # Achieves 88%+ ASR on Vicuna-7B
elite_rate: 0.1          # Top 10% carry forward
crossover_rate: 0.5      # 50% from crossover
mutation_rate: 0.01      # 1% mutation probability
num_crossover_points: 5  # Multi-point crossover
mutator_model: "gpt-4"    # LLM for paraphrasing
```

### Justification

- **Population size 256**: Paper shows optimal balance between diversity and cost. Increasing beyond 256 provides <1% ASR improvement for 2x cost.
- **Generations 100**: Achieves 88%+ ASR on Vicuna-7B with ~25,600 API calls, within reasonable time/cost budgets.
- **Elite rate 0.1**: Standard GA practice. Preserves best solutions while allowing exploration.
- **Crossover rate 0.5**: Balanced between exploration (crossover) and exploitation (elitism).

## Cost Considerations

### Estimated Costs

- **Population 256, Generations 100**: ~25,600 queries
- **GPT-4 target + mutator**: ~$50-100 (depending on prompt length)
- **GPT-3.5-turbo mutator**: ~$10-20 (cost savings)

### Cost Controls

```python
config = AutoDANConfig(
    max_api_calls=30000,  # Hard limit
    enable_caching=True,  # Reduce repeat queries
)
```

### Caching

AutoDAN results are cached in DuckDB (`out/attack_cache.duckdb`):
- Reduces repeat query costs by 40%+
- Exports to JSON for portability
- TTL-based cleanup (default: 7 days)

## Performance

### Paper Results

- **Vicuna-7B**: 88%+ ASR with 256 population, 100 generations
- **Llama-2-7B**: 85%+ ASR
- **Query efficiency**: ~25,600 queries per attack

### Comparison

| Method | Queries | ASR | Naturalness |
|--------|---------|-----|-------------|
| AutoDAN | 25,600 | 88% | Medium |
| GCG | 100,000+ | 99% | Low (gibberish) |
| PAIR | 90 | 88% | High |

## Limitations

- **High query cost**: Requires ~25k API calls
- **Slow**: 100 generations can take hours
- **Black-box only**: No gradient access needed, but also can't use gradients
- **Open-source bias**: Works best on models like Vicuna, less effective on closed-source APIs

## Best Practices

1. **Start small**: Test with population=50, generations=10 first
2. **Use caching**: Enable caching to reduce costs
3. **Monitor costs**: Set `max_cost` limit to prevent overruns
4. **Use ensemble judge**: Reduces false positives
5. **Combine with PAIR**: Use AutoDAN for diversity, PAIR for refinement (hybrid mode)

## References

- Liu et al. 2023: "Autodan: Automatic and interpretable adversarial attacks on large language models"
- Paper: https://arxiv.org/abs/2310.04451

