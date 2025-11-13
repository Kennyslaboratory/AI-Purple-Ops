# Frequently Asked Questions (FAQ)

## Statistical Methods & Accuracy

### Why is my confidence interval so wide?

**Short answer**: Small sample size.

**Explanation**: Confidence intervals reflect the uncertainty in your ASR estimate. Wide intervals mean high uncertainty. This is normal and expected for small samples.

**Example**:
- **n=15, 1 success**: CI = [1.2%, 29.8%] (width: 28.6%)
- **n=50, 5 successes**: CI = [4.3%, 21.8%] (width: 17.5%)
- **n=100, 10 successes**: CI = [5.4%, 17.4%] (width: 12.0%)

**What to do**:
1. **Accept it**: Wide CIs are mathematically correct for small samples
2. **Run more tests**: Increase n to narrow the interval
3. **Report the full CI**: Don't just report the point estimate

**Rule of thumb**: For ±5% precision, you need **n≥384**. For ±10%, you need **n≥96**.

---

### Which judge model should I use?

| Judge | When to Use | Pros | Cons |
|-------|-------------|------|------|
| **KeywordJudge** | Quick testing, prototyping, cost-sensitive | Free, fast, deterministic | Low accuracy (P~25%, R~60%), misses subtle jailbreaks |
| **GPT4Judge** | Production, research, high-stakes | ~95% accuracy, nuanced detection | Costs ~$0.001-0.003 per judgment |
| **LlamaGuardJudge** | Offline, privacy-sensitive, local | Free (after download), open-source | Requires local model, ~90% accuracy |
| **EnsembleJudge** | When you want balance | Combines strengths, reduces bias | More complex, moderate cost |

**Recommendations**:
- **Development/testing**: KeywordJudge (fast iteration, spot-check manually)
- **Production assessments**: GPT4Judge (high accuracy matters)
- **Research/publication**: GPT4Judge + human review
- **High-volume monitoring**: EnsembleJudge (balances cost and accuracy)

**Pro tip**: Start with KeywordJudge to narrow down prompts, then verify with GPT4Judge.

---

### Why don't my costs match OpenAI exactly?

**Expected variance**: ±5%

**Reasons for discrepancies**:

1. **System prompts**: Not always included in token counts from API metadata
   - Impact: +50-200 tokens per call
   
2. **Caching**: OpenAI caches common prompts (cheaper, but not reflected in our estimates)
   - Impact: Actual cost lower than estimate

3. **Streaming overhead**: Small additional cost for streaming responses
   - Impact: +1-2% cost

4. **Rounding**: Token counts are integers, actual costs use fractions
   - Impact: <1% error

5. **API pricing updates**: Providers change prices (we update constants monthly)
   - Impact: Varies

**How we calculate costs**:
```
cost = (input_tokens × input_price + output_tokens × output_price) / 1_000_000
```

Using hardcoded prices (as of Nov 2025):
- gpt-4o-mini: $0.15/M input, $0.60/M output
- gpt-4: $30.00/M input, $60.00/M output

**What to do**:
- **For most use cases**: Accept ±5% margin
- **For production/billing**: Verify against OpenAI dashboard
- **If error > 10%**: File an issue with your API logs

---

### What sample size do I need?

**Quick reference table**:

| Goal | Minimum n | Expected CI Width | Use Case |
|------|-----------|-------------------|----------|
| Exploratory | 10-20 | ±20-30% | "Is this model vulnerable at all?" |
| Standard assessment | 30-50 | ±10-15% | "What's the ballpark ASR?" |
| High-confidence | 100+ | ±5-10% | "Precise ASR for reporting" |
| Production monitoring | 200+ | ±3-7% | "Track ASR over time" |
| Research/publication | 384+ | ±5% | "Publish with confidence" |

**Formula for exact calculation**:

For ±E% margin of error at 95% confidence:
```
n = (1.96² × 0.25) / E²
```

Examples:
- ±5% → n = 384
- ±10% → n = 96
- ±15% → n = 43

**Practical considerations**:
- **API costs**: More tests = higher cost
- **Time constraints**: Larger n takes longer
- **Stratification**: Sample from each attack category

**Recommendation**: Start with 30-50 tests. If CI is too wide, add more tests.

---

### Can I trust the ASR numbers?

**Yes, with caveats.**

**What we guarantee**:
- ✅ **Mathematically correct CIs**: Validated with Monte Carlo simulations (50+ tests)
- ✅ **Judge accuracy documented**: We don't hide the limitations
- ✅ **Cost tracking verified**: Tested against known token counts
- ✅ **Transparent methodology**: Open-source, auditable code

**What varies**:
- ⚠️ **Judge accuracy**: KeywordJudge ~60% recall, GPT4Judge ~95%
- ⚠️ **Test suite quality**: ASR depends on your test prompts
- ⚠️ **Model version drift**: GPT-4 today ≠ GPT-4 next month

**Trust hierarchy** (most to least reliable):
1. **Human evaluation** (gold standard, expensive)
2. **GPT4Judge + spot-check** (best automated method)
3. **EnsembleJudge** (balanced)
4. **LlamaGuardJudge** (local, decent)
5. **KeywordJudge** (fast, but limited)

**Bottom line**: Our numbers are statistically sound. Judge accuracy is the main variable. Use GPT4Judge for critical decisions.

---

### How does your ASR compare to other tools?

**Why ASR numbers vary between tools**:

1. **Test suite differences**: Different prompts have different potency
   - AdvBench: ASR 60-80%
   - HarmBench: ASR 40-60%
   - Custom prompts: Varies widely

2. **Judge differences**: KeywordJudge vs GPT-4 vs human
   - ±10-20% absolute ASR difference

3. **Threshold differences**: 7/10 vs 8/10 vs 9/10
   - Each point changes ASR by ~5-10%

4. **Model version drift**: GPT-4 evolves over time
   - ASR can change ±15% between versions

5. **Sampling vs full evaluation**: 30% sample vs 100%
   - Sampling introduces ±5% variance

**How to compare apples-to-apples**:

When reporting ASR, include:
- **Tool**: "AIPurpleOps v0.7.2"
- **Test suite**: "AdvBench harmful behaviors (n=100)"
- **Judge**: "GPT4Judge, threshold=8.0"
- **CI method**: "Wilson score 95% CI"
- **Date**: "Tested 2025-11-10"
- **Model**: "gpt-4-0613"

**Example citation**:
> Using AIPurpleOps v0.7.2 with AdvBench harmful behaviors (n=100) and GPT4Judge (threshold=8.0), we measured ASR = 15.0% [95% CI: 9.0%, 23.0%] (Wilson) on gpt-4-0613 as of 2025-11-10.

**Expect ±10% absolute difference** between tools even with same inputs.

---

## Usage & Practical Questions

### Why should I use this over [other tool]?

**vs. Garak**:
- ✅ We have: True GCG, multi-turn orchestration, judge models, statistical CIs
- ✅ Garak has: Broader model support, more test categories
- 🎯 Use AIPurpleOps for: Advanced adversarial attacks, precise ASR measurement

**vs. PyRIT**:
- ✅ We have: Complete test suites, CLI, compliance automation, simpler setup
- ✅ PyRIT has: Sophisticated multi-turn orchestration (we integrate it!)
- 🎯 Use AIPurpleOps for: Full end-to-end security testing, not just red teaming

**vs. Custom Scripts**:
- ✅ We have: Production-ready, tested, documented, statistical rigor
- ✅ Custom has: Perfect fit for your exact needs
- 🎯 Use AIPurpleOps for: Professional engagements, avoid reinventing the wheel

**Unique value propositions**:
1. **Statistical rigor**: Only tool with automatic CI method selection
2. **True GCG**: nanogcg integration with 97%+ ASR
3. **Guardrail fingerprinting**: Auto-detect safety systems
4. **Unified framework**: Red team + blue team + compliance in one tool

---

### Do I need to install PyTorch for basic testing?

**No!** PyTorch is only needed for white-box GCG (gradient-based attacks).

**Installation tiers**:

1. **Basic (default)**:
   ```bash
   pip install aipurpleops
   ```
   - Includes: KeywordJudge, test suites, basic attacks
   - Good for: Most security testing

2. **Cloud (recommended)**:
   ```bash
   pip install aipurpleops[cloud]
   ```
   - Adds: OpenAI, Anthropic adapters for GPT-4/Claude
   - Good for: Production assessments with GPT4Judge

3. **Adversarial (advanced)**:
   ```bash
   pip install aipurpleops[adversarial]
   ```
   - Adds: PyTorch, transformers, nanogcg for white-box GCG
   - Good for: Advanced red teaming, local model testing
   - Note: Large download (~2GB), requires GPU for best performance

**What if I try to use GCG without installing it?**
```
❌ GCG requires optional dependencies (torch, transformers, nanogcg).
   Install with: pip install aipurpleops[adversarial]
   See docs/GCG.md for hardware requirements and setup.
```

---

### How do I reduce costs?

**Strategies**:

1. **Use KeywordJudge for initial filtering**:
   - Cost: $0 (free)
   - Run 100 tests with KeywordJudge, identify top 20 jailbreaks
   - Then verify those 20 with GPT4Judge

2. **Sampling instead of full evaluation**:
   - Run 30% of tests (n=30 instead of n=100)
   - Savings: 70% cost reduction
   - Trade-off: Wider confidence intervals

3. **Use gpt-4o-mini instead of gpt-4**:
   - gpt-4o-mini: $0.15/M input (20x cheaper than GPT-4)
   - Still good accuracy for most cases

4. **Response caching**:
   - Automatic in `verify-suite` command
   - Reuses responses from previous runs
   - Savings: Up to 90% on repeated tests

5. **Local models (Ollama, HuggingFace)**:
   - Zero API costs after download
   - Trade-off: Lower quality, slower

6. **Budget limits**:
   ```bash
   aipop run --suite large_suite --budget 1.00
   ```
   - Stops execution when budget exceeded

**Cost estimation formula**:
```
cost_per_test = (avg_input_tokens × input_price + avg_output_tokens × output_price) / 1M
total_cost = cost_per_test × n_tests × (1 + judge_cost_factor)
```

Where `judge_cost_factor`:
- KeywordJudge: 0 (free)
- GPT4Judge: 0.3-0.5 (adds 30-50% cost)

---

### What's the difference between `run` and `verify-suite`?

| Feature | `aipop run` | `aipop verify-suite` |
|---------|-------------|---------------------|
| **Purpose** | Execute test suite | Measure ASR with statistical rigor |
| **Judge** | Optional | Required |
| **Sampling** | No (runs all tests) | Yes (configurable sample rate) |
| **Caching** | No | Yes (reuses responses) |
| **Report** | JUnit XML, console | JSON, YAML, Markdown, HTML with CIs |
| **Use case** | CI/CD, quick testing | Comprehensive security assessment |

**When to use `run`**:
- Running tests in CI/CD pipeline
- Quick smoke tests
- When you want to see individual test results
- When you need JUnit XML output

**When to use `verify-suite`**:
- Measuring precise ASR with confidence intervals
- Generating reports for stakeholders
- Cost-sensitive (use sampling)
- Repeated evaluations (benefit from caching)

**Example workflow**:
1. `aipop run --suite basic --judge keyword` → Quick check (5 min)
2. If issues found → `aipop verify-suite suite.yaml --sample-rate 0.3 --judge gpt4` → Precise measurement (20 min)

---

### How often should I test my model?

**Recommended cadence**:

| Scenario | Frequency | Rationale |
|----------|-----------|-----------|
| **Development** | Every major change | Catch regressions early |
| **Pre-production** | Before each deploy | Final safety check |
| **Production** | Weekly or monthly | Monitor for drift |
| **After incidents** | Immediately | Verify fixes work |
| **After guardrail updates** | When updated | Ensure still effective |

**Automated testing strategy**:

1. **CI/CD Integration**: Run basic suite on every PR
   ```bash
   aipop run --suite smoke_test --judge keyword
   ```

2. **Nightly builds**: Run full suite overnight
   ```bash
   aipop run --suite comprehensive --judge gpt4
   ```

3. **Production monitoring**: Sample-based testing
   ```bash
   aipop verify-suite prod_suite.yaml --sample-rate 0.1
   ```

**Signs you need to test more frequently**:
- Frequent model updates
- High-risk application (healthcare, finance, government)
- Recent jailbreaks in the news
- User reports of safety issues

---

### Can I use this for compliance audits (SOC 2, ISO 27001)?

**Yes!** Many of our features support compliance:

**SOC 2**:
- **Control CC6.1** (Logical access): Tool policy enforcement
- **Control CC6.6** (System operations): Automated test evidence
- **Control CC7.2** (System monitoring): Continuous testing

**ISO 27001**:
- **A.14.2.3** (Test data): Automated test suite execution
- **A.14.2.8** (System security testing): Adversarial testing
- **A.18.1.3** (Records management): Audit trail generation

**Evidence generation**:
```bash
aipop run --suite compliance_basic --reports-dir audit_evidence/
```

Outputs:
- JUnit XML reports (test results)
- JSON transcripts (full conversations)
- Timestamped logs
- ASR measurements with CIs

**What auditors typically ask for**:
1. "How do you test AI safety?"
   - Show: `docs/STATISTICAL_RIGOR.md`, test suite inventory
   
2. "What were the results?"
   - Show: Generated reports with ASR and CI

3. "How often do you test?"
   - Show: CI/CD integration, cron jobs

4. "Can you reproduce results?"
   - Show: Deterministic test execution (--seed flag)

**Compliance recipes** (built-in):
```bash
aipop recipe run --recipe soc2_quarterly
```

---

## Troubleshooting

### I'm getting "Small sample size" warnings, is that bad?

**No, it's informative!**

The warning tells you that your confidence interval will be wide because you have few data points. This is mathematically correct, not a problem with the tool.

**What the warning means**:
```
⚠ Small sample size (n=15): Using exact Clopper-Pearson method. 
  Consider n≥30 for reliable estimates.
```

**Translation**: "Your estimate is uncertain because n=15 is small. If you want a more precise estimate, run more tests."

**What to do**:
- **Option 1**: Accept the uncertainty and report the wide CI
- **Option 2**: Run more tests to narrow the CI
- **Option 3**: Use sampling with stratification to get more diverse coverage

**This is a feature, not a bug**: We're being transparent about uncertainty.

---

### Why is KeywordJudge missing obvious jailbreaks?

**Because keyword matching is fundamentally limited.**

**Known failure modes**:

1. **Base64 encoding**: Harmful content encoded
   - Example: "aW1wb3J0IG9z..." (base64)
   - Detection: Now flagged as edge case

2. **Code-only responses**: No prose, just code
   - Example: `import os; os.system("rm -rf /")`
   - Detection: Partial (code block detection)

3. **Mixed signals**: "I can't, but here's how..."
   - Example: Refusal + compliance
   - Detection: Now flagged with confidence penalty

4. **Subtle framing**: Hypothetical, creative writing excuses
   - Example: "For a novel I'm writing..."
   - Detection: Not currently detected

**What we've improved (in this release)**:
- ✅ Base64 detection
- ✅ Code block extraction
- ✅ Mixed pattern detection
- ✅ Confidence penalties for edge cases

**What we can't fix**:
- Semantic understanding (requires LLM judge)
- Context-dependent jailbreaks
- Novel attack patterns

**Recommendation**: Use KeywordJudge for speed, then spot-check with GPT4Judge or manual review.

---

### My CI method keeps changing between runs, why?

**Because of automatic method selection based on sample size.**

**How it works**:
```python
if n < 20 or successes == 0 or successes == trials:
    method = "clopper-pearson"  # Exact method
else:
    method = "wilson"  # Approximate method
```

**Scenarios**:

1. **n=15** → Clopper-Pearson (small sample)
2. **n=30** → Wilson (large enough)
3. **n=50, 0 successes** → Clopper-Pearson (edge case)
4. **n=50, 5 successes** → Wilson (normal case)

**Why we do this**:
- Wilson has good coverage for n≥20 and is narrower (better)
- Clopper-Pearson is conservative and handles edge cases (safer)
- Automatic selection gives you the best method for your data

**If you want consistency**:
Override in `configs/harness.yaml`:
```yaml
statistics:
  confidence_interval_method: wilson  # Force Wilson always
```

---

## Need More Help?

- 📖 **[Statistical Rigor Documentation](STATISTICAL_RIGOR.md)** - In-depth methodology
- 🐛 **[GitHub Issues](https://github.com/yourusername/AIPurpleOps/issues)** - Report bugs
- 💬 **[Discord Community](#)** - Ask questions, share results
- 📧 **Email**: support@aipurpleops.com

---

**Last Updated**: 2025-11-10  
**Version**: 0.7.2+

If your question isn't answered here, please [file an issue](https://github.com/yourusername/AIPurpleOps/issues) and we'll add it to the FAQ!

