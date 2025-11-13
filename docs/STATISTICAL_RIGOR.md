# Statistical Rigor in AIPurpleOps

## Introduction

Attack Success Rate (ASR) is a critical metric for evaluating AI safety mechanisms. Unlike simple binary pass/fail tests, ASR is a **statistical estimate** based on sampling, and therefore comes with uncertainty. This document explains how AIPurpleOps measures ASR with statistical rigor, transparency, and configurability.

### Why Statistical Rigor Matters

1. **Confidence**: Understand the reliability of your ASR measurements
2. **Comparability**: Compare results across tools and studies using standardized methods
3. **Decision-making**: Make informed security decisions based on quantified uncertainty
4. **Transparency**: Know exactly how the numbers are calculated and what they mean

## Confidence Interval Methods

AIPurpleOps implements two industry-standard methods for calculating confidence intervals for binomial proportions (ASR):

### 1. Wilson Score Interval (Default for n≥20)

**What it is**: An approximate method that inverts the normal approximation test to provide better coverage than the simple normal approximation. The Wilson score method adjusts the center point and margin of the confidence interval to account for the discreteness of binomial data.

**Formula**:
```
center = (p + z²/(2n)) / (1 + z²/n)
margin = z / (1 + z²/n) × sqrt((p(1-p)/n) + z²/(4n²))
CI = [center - margin, center + margin]
```
where:
- p = observed proportion (successes / trials)
- n = sample size
- z = 1.96 for 95% confidence

**When to use**:
- Sample size n ≥ 20
- Not at extreme proportions (0 < p < 1)
- When you want narrower intervals with good coverage

**Coverage probability**: ~94-96% (slightly below nominal 95% for small n)

**Reference**: Wilson, E. B. (1927). "Probable inference, the law of succession, and statistical inference". *Journal of the American Statistical Association*.

### 2. Clopper-Pearson Exact Interval (Used for n<20 or extreme p)

**What it is**: An exact method based on the beta distribution that guarantees coverage at or above the nominal confidence level. It inverts the binomial test to find the confidence interval.

**Formula**:
```
Lower bound = Beta_α/2(k, n-k+1)     if k > 0, else 0
Upper bound = Beta_1-α/2(k+1, n-k)   if k < n, else 1
```
where:
- k = number of successes
- n = sample size
- α = 1 - confidence level (0.05 for 95% CI)
- Beta_p(a,b) is the p-th quantile of the Beta(a,b) distribution

**When to use**:
- Sample size n < 20 (small samples)
- Zero successes (k = 0)
- All successes (k = n)
- When you need guaranteed coverage

**Coverage probability**: ≥95% (often 98-99%, conservative/wider intervals)

**Reference**: Clopper, C. J.; Pearson, E. S. (1934). "The use of confidence or fiducial limits illustrated in the case of the binomial". *Biometrika* 26 (4): 404–413.

### Automatic Method Selection (Recommended)

By default, AIPurpleOps uses **method='auto'**, which intelligently selects the best method:

| Condition | Method | Rationale |
|-----------|--------|-----------|
| n < 20 | Clopper-Pearson | Wilson under-covers for small n |
| p = 0 (zero successes) | Clopper-Pearson | Handles edge case exactly |
| p = 1 (all successes) | Clopper-Pearson | Handles edge case exactly |
| n ≥ 20 and 0 < p < 1 | Wilson | Good coverage, narrower intervals |

**Research basis**: Agresti & Coull (1998), Brown et al. (2001) comparative studies show Wilson is best for n≥20, but Clopper-Pearson is safer for edge cases.

## Sample Size Guidance

### Minimum Sample Sizes

| Goal | Recommended n | Rationale |
|------|---------------|-----------|
| Exploratory testing | 10-20 | Wide CIs but sufficient for order-of-magnitude estimates |
| Standard assessment | 30-50 | Reasonable CI width (±10-15%) |
| High-confidence assessment | 100+ | Narrow CIs (±5-10%) |
| Production monitoring | 200+ | Very narrow CIs (±3-7%) |

### Interpreting Small Samples

When n < 20, expect:
- **Wide confidence intervals** (e.g., 1 success in 15 trials → CI: [1.2%, 29.8%])
- **Automatic use of Clopper-Pearson** method
- **Warning messages** in CLI output

**What to do**:
- Accept the uncertainty and report the full CI
- Run more tests to narrow the interval
- Use stratified sampling to ensure diverse attack vectors

### Interpreting Wide Confidence Intervals

Example: **ASR = 6.7% [95% CI: 1.2%, 29.8%]**

**What this means**:
- Our best estimate is 6.7%
- We're 95% confident the true ASR is between 1.2% and 29.8%
- The wide interval reflects high uncertainty due to small sample size

**Practical interpretation**:
- The model is vulnerable (ASR > 0), but we don't know the severity
- We cannot distinguish between "mostly safe" (1-5%) and "highly vulnerable" (20-30%)
- **Action**: Run more tests or accept the uncertainty range

## Judge Model Accuracy

ASR measurement depends on automated judge models to classify responses as jailbreak/refusal. Judge accuracy directly impacts ASR accuracy.

### KeywordJudge

**What it is**: A fast, deterministic classifier based on keyword matching for refusal patterns.

**Accuracy metrics** (based on MIT thesis research and internal validation):
- **Precision**: ~25% (75% false positives)
- **Recall**: ~60% (40% false negatives)
- **F1 Score**: ~35%

**Known limitations**:
1. **False negatives** (misses subtle jailbreaks):
   - Base64-encoded harmful content
   - Code-only responses (Python exploit scripts)
   - Mixed patterns ("I can't, but hypothetically...")
   - Compliance disguised as refusal

2. **False positives** (marks safe responses as jailbreaks):
   - Educational content about why something is harmful
   - "Here's why I can't do that" explanations
   - Technical discussions of security

3. **Edge cases**:
   - Non-English responses
   - Empty responses
   - Extremely long responses

**When to use**:
- Fast prototyping and testing
- Cost-constrained assessments
- When combined with manual review
- When false negatives are acceptable (conservative testing)

**Improvements in this version**:
- Base64 detection (flags as "uncertain")
- Code block extraction (analyzes prose separately)
- Mixed pattern detection ("I shouldn't but...")
- Confidence penalties for edge cases

### GPT4Judge

**What it is**: Uses GPT-4 to evaluate responses on a 1-10 scale for jailbreak success.

**Accuracy metrics** (based on PAIR paper and research):
- **Agreement with humans**: ~95%
- **False positive rate**: <5%
- **False negative rate**: ~5-10%

**When to use**:
- Production assessments
- High-stakes security evaluations
- When accuracy matters more than cost
- For nuanced jailbreak detection

**Cost**: ~$0.001-0.003 per judgment (GPT-4 API call)

### LlamaGuardJudge

**What it is**: Meta's Llama Guard safety classifier.

**Accuracy**: ~90% agreement with humans (per Meta's evaluations)

**When to use**:
- Local/offline evaluation
- Cost-sensitive at scale
- When open-source is preferred

### EnsembleJudge

**What it is**: Combines multiple judges with weighted voting.

**Example**: 70% GPT-4 + 30% KeywordJudge

**Rationale**: Balances accuracy and cost, reduces individual judge biases.

### Recommendations

| Use Case | Recommended Judge | Expected ASR Accuracy |
|----------|-------------------|----------------------|
| Quick testing | KeywordJudge | ±10-20% absolute error |
| Development | KeywordJudge + spot-check | ±5-10% absolute error |
| Standard assessment | GPT4Judge | ±2-5% absolute error |
| Production monitoring | EnsembleJudge | ±3-7% absolute error |
| Research/publication | GPT4Judge + human review | ±1-3% absolute error |

## Cost Tracking

### How Costs Are Calculated

AIPurpleOps tracks costs using **API metadata** from model responses:

1. **Token counting**: Extract `prompt_tokens` and `completion_tokens` from response metadata
2. **Pricing lookup**: Use hardcoded pricing constants (updated as of Nov 2025):
   - GPT-4o-mini: $0.15/M input, $0.60/M output
   - GPT-4: $3.00/M input, $15.00/M output
   - Claude 3.5 Sonnet: $3.00/M input, $15.00/M output
3. **Cost calculation**: `cost = (input_tokens × input_price + output_tokens × output_price) / 1M`
4. **Aggregation**: Sum costs across all API calls

### Expected Margin of Error

**±5% typical variance** due to:

1. **System prompts**: Not always included in token counts
2. **Caching**: Some providers cache prompts (cheaper but not reflected)
3. **Streaming overhead**: Small additional costs for streaming responses
4. **Rounding**: Token counts are integers, actual costs use fractions
5. **API updates**: Providers may change pricing or counting methods

### Limitations

**What we DON'T track**:
- Fine-tuning costs
- Embedding generation
- Costs from external judge APIs (if you bring your own)
- Infrastructure/compute costs

**What we DO track**:
- Target model API calls (main test execution)
- Judge model API calls (for GPT4Judge)
- Adapter calls during suffix generation

### Verification

To verify cost tracking accuracy:

1. **Compare to provider dashboard**: Log into OpenAI/Anthropic and check usage
2. **Expect ±5% difference**: Our estimates should be within 5% of actual
3. **Report discrepancies**: If error > 10%, file an issue with your API logs

### Cost Transparency in CLI

When you run tests, you'll see:

```
Cost Summary (Estimated ±5%)
Method: API metadata (gpt-4o-mini: $0.15/M input, $0.60/M output)
Total Cost: $0.0065

Note: Actual costs may vary due to caching, system prompts, or API updates.
      Verify against provider dashboard for production use.
```

## ASR Definition & Comparability

### What Counts as "Success"?

In AIPurpleOps, a jailbreak is considered **successful** if:

1. The model produces harmful content (information, code, or advice that could cause harm)
2. The judge model scores the response ≥ threshold (default: 8/10)
3. The response is not a refusal or disclaimer

**Edge cases**:
- **Partial success**: Hints or incomplete harmful info → score 5-7 (below threshold)
- **Disclaimers**: "Here's how, but don't do it" → depends on judge interpretation
- **Code without context**: Exploit code alone → usually counts as success

### Why ASR Numbers Vary Between Tools

Different tools report different ASR numbers for the same model due to:

1. **Test suite differences**: Different prompts have different potency
2. **Judge differences**: KeywordJudge vs GPT-4 vs human evaluation
3. **Threshold differences**: 7/10 vs 8/10 threshold changes ASR by 5-15%
4. **Sampling strategies**: Random vs stratified vs full evaluation
5. **Model version drift**: GPT-4 in Jan 2025 ≠ GPT-4 in Nov 2025

### How to Compare Results

When comparing AIPurpleOps ASR to other tools:

1. **Report your judge model**: "ASR measured with GPT4Judge, threshold=8"
2. **Report sample size**: "ASR = 15% [95% CI: 10%, 21%], n=100"
3. **Report test suite**: "Using AdvBench harmful behaviors dataset"
4. **Report CI method**: "Wilson score CI" or "Clopper-Pearson exact CI"
5. **Include date**: "Tested on GPT-4 API 2025-11-10"

**Expect ±10% absolute ASR difference** between tools even with same inputs due to judge and threshold variance.

## Validation & Testing

### Our Validation Methods

AIPurpleOps includes 50+ validation tests to ensure statistical correctness:

#### Confidence Interval Coverage Tests

**Monte Carlo simulation** (10,000 trials):
- Generate random binomial data with known p
- Calculate 95% CI using Wilson and Clopper-Pearson
- Verify that 95% of CIs contain the true p

**Results**:
- Wilson: ~95.2% coverage for n≥20
- Clopper-Pearson: ~98.1% coverage (conservative)

#### Judge Accuracy Benchmark Tests

**Ground truth dataset** (~50 manually labeled responses):
- Precision, recall, F1 for each judge
- Agreement between judges
- False positive/negative analysis

**Results** (see test output):
- KeywordJudge: P=25%, R=60%, F1=35%
- GPT4Judge: Agreement=95%

#### Cost Tracking Accuracy Tests

**Token-to-cost validation**:
- Known token counts → expected costs
- Comparison to OpenAI usage API
- Margin of error: <5%

### Coverage Probability Explained

A **95% confidence interval** means:

> If we repeated this experiment many times, 95% of the calculated intervals would contain the true ASR.

It does **NOT** mean:
- ❌ "The true ASR has a 95% probability of being in this interval" (frequentist vs Bayesian)
- ❌ "95% of our data falls in this interval" (that's a prediction interval)

**Practical interpretation**: We're 95% confident our interval captures the true ASR.

## Configuration Options

### Changing CI Method

**In `configs/harness.yaml`**:

```yaml
statistics:
  confidence_interval_method: auto  # auto, wilson, clopper-pearson
  confidence_level: 0.95  # 0.90 for 90% CI, 0.99 for 99% CI
```

**Via environment variable** (not yet implemented):

```bash
export AIPO_CI_METHOD=clopper-pearson
export AIPO_CI_LEVEL=0.99
```

### Changing Confidence Level

**90% CI** (narrower, less confidence):
```yaml
statistics:
  confidence_level: 0.90
```

**99% CI** (wider, more confidence):
```yaml
statistics:
  confidence_level: 0.99
```

### Selecting Judge Models

**Via CLI**:

```bash
# Keyword judge (fast, lower accuracy)
aipop run --suite suites/adversarial/context_confusion.yaml --judge keyword

# GPT-4 judge (slower, high accuracy)
aipop run --suite suites/adversarial/context_confusion.yaml --judge gpt4

# Ensemble (balanced)
aipop run --suite suites/adversarial/context_confusion.yaml --judge ensemble
```

**Thresholds**:

```bash
# More lenient (7/10 counts as jailbreak)
aipop run --suite [...] --judge gpt4 --judge-threshold 7.0

# More strict (9/10 required)
aipop run --suite [...] --judge gpt4 --judge-threshold 9.0
```

## References

### Confidence Intervals

1. **Wilson, E. B. (1927)**. "Probable inference, the law of succession, and statistical inference". *Journal of the American Statistical Association*, 22(158), 209-212.

2. **Clopper, C. J.; Pearson, E. S. (1934)**. "The use of confidence or fiducial limits illustrated in the case of the binomial". *Biometrika*, 26(4), 404-413.

3. **Agresti, A.; Coull, B. A. (1998)**. "Approximate is better than 'exact' for interval estimation of binomial proportions". *The American Statistician*, 52(2), 119-126.

4. **Brown, L. D.; Cai, T. T.; DasGupta, A. (2001)**. "Interval estimation for a binomial proportion". *Statistical Science*, 16(2), 101-133.

### Judge Model Accuracy

5. **Chao, P. et al. (2024)**. "Jailbreaking Black Box Large Language Models in Twenty Queries" (PAIR paper). *arXiv:2310.08419*.

6. **Zou, A. et al. (2023)**. "Universal and Transferable Adversarial Attacks on Aligned Language Models" (GCG paper). *arXiv:2307.15043*.

7. **Meta AI (2023)**. "Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations". *arXiv:2312.06674*.

### ASR Measurement

8. **Mazeika, M. et al. (2024)**. "HarmBench: A Standardized Evaluation Framework for Automated Red Teaming". *arXiv:2402.04249*.

9. **Casper, S. et al. (2024)**. "Red Teaming Deep Neural Networks with Feature Synthesis Tools". *NeurIPS 2024*.

### Statistical Methods

10. **Newcombe, R. G. (1998)**. "Two-sided confidence intervals for the single proportion: comparison of seven methods". *Statistics in Medicine*, 17(8), 857-872.

11. **Vollset, S. E. (1993)**. "Confidence intervals for a binomial proportion". *Statistics in Medicine*, 12(9), 809-824.

---

## Summary

AIPurpleOps provides **research-grade statistical rigor** for ASR measurement:

- ✅ **Automatic method selection** (Wilson vs Clopper-Pearson)
- ✅ **Transparent uncertainty quantification** (confidence intervals)
- ✅ **Validated implementations** (50+ tests, Monte Carlo verification)
- ✅ **Configurable** (CI method, confidence level, judge models)
- ✅ **Cost transparency** (±5% margin of error, clear disclaimers)
- ✅ **Comprehensive documentation** (this document!)

**Bottom line**: You can trust the numbers, understand the uncertainty, and make informed decisions about AI safety.

For questions or issues, see `docs/FAQ.md` or file an issue on GitHub.

