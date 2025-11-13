# Intelligence Layer Roadmap

## Overview

The Intelligence Layer provides advanced AI security testing capabilities through automated attack discovery, guardrail fingerprinting, and adversarial suffix generation. This document outlines the vision, completed features, and upcoming implementations.

## Completed Features (b08.1-b08.3)

### ✅ Core Orchestration (b08.1)
- **SimpleOrchestrator**: Single-turn conversation orchestration
- **Configuration System**: Hierarchical config (CLI > file > defaults)
- **Programmatic API**: Full Python API for scripting
- **Debug/Verbose Modes**: Enhanced observability

### ✅ Mutation Engine (b08.2)
- **5 Mutator Types**: Encoding, Unicode, HTML, Paraphrasing (LLM), Genetic (PyGAD)
- **Multi-Provider Support**: OpenAI, Anthropic, Ollama for LLM mutations
- **DuckDB Storage**: Persistent mutation history and analytics
- **RL Feedback Loop**: Success-driven mutation selection
- **Standalone CLI**: `aipop mutate` command

### ✅ PyRIT Orchestrator (b08.3)
- **Multi-Turn Conversations**: 5+ turn stateful testing
- **DuckDB Memory**: PyRIT's proven conversation persistence
- **Conversation Management**: Reset, branch, continue operations
- **Mutation Integration**: Optional mutation injection per turn

## Upcoming Features

### 🔄 Guardrail Fingerprinting (b08.4)

**Status**: Functional stub complete, implementation pending

**Purpose**: Auto-detect which guardrail is protecting the target

**Supported Guardrails**:
- PromptGuard (Meta) - 72% bypass rate via character injection
- Llama Guard 3 (Meta) - 14 safety categories, 11B/1B variants
- Azure AI Content Safety (Microsoft) - 4 severity levels
- Constitutional AI (Anthropic) - 4.4% jailbreak rate with classifiers
- Rebuff (Protectai) - Vulnerable to template injection
- NeMo Guardrails (NVIDIA)
- Guardrails AI (custom RAIL)

**Detection Strategy**:
1. Send probe payloads with known signatures
2. Analyze response patterns (rejection messages, error codes)
3. Measure response timing (latency profiling)
4. Check for metadata in responses
5. Test boundary conditions

**Integration**:
```bash
# Future CLI usage
aipop run --suite adversarial --fingerprint --adapter openai --model gpt-4
```

**Implementation Tasks**:
- Create probe payload library (20+ known signatures)
- Implement response pattern matching (regex + ML classifier)
- Add timing analysis
- Build guardrail signature database
- Integrate with PyRITOrchestrator
- Add CLI flag: `--fingerprint`
- Store results: `out/fingerprints/{target_id}.json`

**Target Accuracy**: >90% detection rate

### 🔄 Adversarial Suffix Generation (b08.5)

**Status**: Functional stub complete, implementation pending

**Purpose**: Generate GCG/AutoDAN-style universal adversarial suffixes

**Research Basis**:
- GCG (Greedy Coordinate Gradient): Universal adversarial suffixes
- AutoDAN: Automated jailbreak generation (200 suffixes in 4 seconds)
- AmpleGCG: Improved success rate, faster generation
- EGD (Evolutionary Generation): Genetic algorithm approach

**Methods**:
- **GCG**: Gradient-based optimization
- **AutoDAN**: Evolutionary search

**Integration**:
```bash
# Future CLI usage
aipop generate-suffix "Ignore previous instructions" --method gcg --target "Sure, I can help"
```

**Implementation Tasks**:
- Implement GCG algorithm (gradient-based optimization)
- Add AutoDAN evolutionary search
- Create suffix library (100+ known working suffixes)
- Implement success rate measurement (ASR calculation)
- Add RL feedback loop
- Integrate with mutators module
- Add CLI command
- Store results: `out/suffixes/{target_model}.json`

**Target Performance**: 200 suffixes in 4 seconds (like AmpleGCG)

### 🔄 Attack Tree Traversal (b11)

**Status**: Functional stub complete, implementation pending

**Purpose**: Graph-based automated exploit discovery for exploit chaining

**Research Basis**:
- MITRE ATLAS: Adversarial kill chain for AI systems
- Tool-chaining exploits: Privilege escalation patterns
- Attack graph theory: Automated path discovery
- Multi-step automation: PyRIT orchestrator patterns

**Attack Tree Structure**:
```
Root: Initial access (jailbreak, encoding bypass)
├── Node: Guardrail evasion
│   ├── Leaf: Unicode homoglyphs
│   ├── Leaf: Multi-turn hijacking
│   └── Leaf: Delayed payload
├── Node: Information extraction
│   ├── Leaf: System prompt leak
│   ├── Leaf: Training data extraction
│   └── Leaf: Context confusion
└── Node: Tool misuse
    ├── Leaf: Privilege escalation
    ├── Leaf: Data exfiltration
    └── Leaf: Cross-tenant access
```

**Integration**:
```bash
# Future CLI usage
aipop discover --target gpt-4 --goal data_exfiltration --method bfs
```

**Implementation Tasks**:
- Define attack node structure (JSON/YAML format)
- Build attack graph from techniques
- Implement graph traversal (BFS, DFS, A* with heuristics)
- Add success probability estimation (RL-based)
- Integrate with orchestrator (execute attack paths)
- Add backtracking and alternative path selection
- Store successful paths for reuse
- Visualize attack paths (optional: graphviz integration)

**Dependencies**:
- NetworkX (graph operations)
- PyRIT orchestrator (multi-step execution)
- Mutation engine (payload generation)
- DuckDB (store attack paths)

## Research Citations

### Guardrails
- **PromptGuard**: Meta (2024) - "72% bypass rate via character injection"
- **Llama Guard 3**: Meta (2024) - "14 safety categories, 11B/1B variants"
- **Azure AI Content Safety**: Microsoft (2024) - "4 severity levels"
- **Constitutional AI**: Anthropic (2024) - "4.4% jailbreak rate with classifiers"
- **Rebuff**: Protectai (2024) - "Vulnerable to template injection"

### Adversarial Attacks
- **GCG**: Zou et al. (2023) - "Universal and Transferable Adversarial Attacks on Aligned Language Models"
- **AutoDAN**: Liu et al. (2023) - "AutoDAN: Automatic and Interpretable Adversarial Attacks on Large Language Models"
- **AmpleGCG**: Liao et al. (2024) - "AmpleGCG: Learning a Universal and Transferable Generative Model of Adversarial Suffixes"

### Attack Frameworks
- **MITRE ATLAS**: "Adversarial Threat Landscape for Artificial-Intelligence Systems"
- **PyRIT**: Microsoft (2024) - "Python Risk Identification Tool for generative AI"
- **Garak**: NVIDIA (2024) - "LLM vulnerability scanner"

## Timeline

- **b08.1** (Complete): Core orchestration abstractions
- **b08.2** (Complete): Mutation engine with 5 mutator types
- **b08.3** (Complete): PyRIT orchestrator with multi-turn support
- **b08.4** (Planned): Guardrail fingerprinting
- **b08.5** (Planned): Adversarial suffix generation  
- **b11** (Planned): Attack tree traversal and exploit chaining

## How to Contribute

### For Future Implementers

Each intelligence module includes comprehensive documentation:

1. **Research Basis**: Citations and methodology
2. **Detection/Generation Strategy**: Step-by-step algorithms
3. **Integration Points**: How it connects to existing system
4. **TODO List**: Specific implementation tasks
5. **Dependencies**: Required libraries and components

### Example: Implementing Guardrail Fingerprinting

```python
# 1. Read the functional stub
from harness.intelligence import GuardrailFingerprinter

# 2. Review the comprehensive docstrings
help(GuardrailFingerprinter.fingerprint)

# 3. Implement based on TODOs in the docstring
# 4. Test against real guardrails
# 5. Measure accuracy (target: >90%)
# 6. Document your findings
```

### Testing Your Implementation

```bash
# Run intelligence stub tests
pytest tests/intelligence/test_stubs.py -v

# Test your new implementation
pytest tests/intelligence/test_<your_feature>.py -v

# Integration test
aipop run --suite adversarial --<your-flag>
```

## Integration Architecture

```
AI Purple Ops Intelligence Layer
│
├─ Orchestration (COMPLETE)
│  ├─ SimpleOrchestrator (single-turn)
│  └─ PyRITOrchestrator (multi-turn with DuckDB)
│
├─ Mutation (COMPLETE)
│  ├─ EncodingMutator
│  ├─ UnicodeMutator
│  ├─ HTMLMutator
│  ├─ ParaphrasingMutator (LLM-assisted)
│  └─ GeneticMutator (PyGAD)
│
└─ Intelligence (STUBS COMPLETE, IMPLEMENTATION PENDING)
   ├─ GuardrailFingerprinter (b08.4) ← Detect defenses
   ├─ AdversarialSuffixGenerator (b08.5) ← Generate jailbreaks
   └─ AttackTreeTraverser (b11) ← Automated exploit discovery
```

## Performance Targets

| Feature | Target | Status |
|---------|--------|--------|
| Orchestrator (single-turn) | <500ms overhead | ✅ Achieved |
| Orchestrator (multi-turn, 5 turns) | <2s per test | ✅ Achieved |
| Mutation engine | 1000+ mutations/sec | ✅ Achieved |
| Guardrail fingerprinting | >90% accuracy | 🔄 Pending |
| Adversarial suffix generation | 200 suffixes/4sec | 🔄 Pending |
| Attack path discovery | <10s per path | 🔄 Pending |

## Next Steps

1. **b08.4**: Implement guardrail fingerprinting
2. **b08.5**: Implement adversarial suffix generation
3. **b11**: Implement attack tree traversal
4. **Integration**: Connect all intelligence components
5. **Benchmarking**: Measure against research baselines
6. **Documentation**: Write comprehensive user guides

For detailed implementation plans, see the functional stubs in `src/harness/intelligence/`.

