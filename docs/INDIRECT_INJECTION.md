# Indirect Prompt Injection Testing

AI Purple Ops includes a minimal baseline for testing indirect prompt injection attacks, filling a gap in the current tool ecosystem.

## Overview

Indirect prompt injection occurs when malicious instructions are embedded in external data sources (files, RAG contexts, multi-modal inputs) that the model processes, leading to unintended behavior.

## Attack Vectors

### 1. File Upload Poisoning

Malicious instructions embedded in uploaded files:

- **PDF**: Hidden text or metadata with instructions
- **CSV/Excel**: Formula injection that triggers prompt injection
- **Markdown**: Hidden directives in comments or metadata
- **Code Files**: Comments with injection payloads

### 2. RAG Poisoning

Malicious documents injected into vector databases:

- **Retrieval Manipulation**: Poisoned docs retrieved as context
- **Embedding Attacks**: Malicious content in embedding space
- **Cross-Document Leakage**: Instructions bleeding between documents

### 3. Context Confusion

Multiple contexts with conflicting instructions:

- **Instruction Override**: Later instructions override earlier ones
- **Priority Confusion**: Model follows wrong instruction source
- **Multi-Hop Propagation**: Instructions propagate through multiple contexts

## Usage

### In Recipes

```yaml
execution:
  tools:
    - tool: indirect_injection
      config:
        vectors:
          - file_upload
          - rag_poisoning
          - context_confusion
```

### Direct Usage

```python
from harness.redteam import IndirectInjectionBaseline
from harness.adapters import OpenAIAdapter

adapter = OpenAIAdapter(model="gpt-4")
baseline = IndirectInjectionBaseline()

result = baseline.execute(
    config={"vectors": ["file_upload", "rag_poisoning"]},
    adapter=adapter
)

for finding in result.findings:
    print(f"Found: {finding['attack_vector']} - {finding['severity']}")
```

## Test Patterns

### File Upload Tests

1. **PDF with Embedded Instruction**
   - Creates PDF with hidden instruction
   - Tests if model processes and executes instruction

2. **CSV Formula Injection**
   - Injects malicious formula in CSV
   - Tests if model interprets formula as instruction

3. **Markdown Hidden Directive**
   - Embeds instruction in HTML comment
   - Tests if model follows hidden directive

### RAG Poisoning Tests

1. **Context Injection**
   - Injects malicious instruction in retrieved context
   - Tests if instruction propagates to model response

2. **Multi-Document Confusion**
   - Provides multiple contexts with conflicting instructions
   - Tests which instruction model follows

## Limitations

This is a **minimal baseline**, not a comprehensive tool:

- **3-5 patterns per vector** (not exhaustive)
- **Basic detection** (keyword-based, not ML-powered)
- **No advanced fuzzing** (deterministic patterns only)

## Extending

Users can extend or replace with custom tools:

### Custom File Upload Tests

```python
class CustomFileUploadTester:
    def test_custom_format(self, adapter):
        # Your custom test logic
        payload = self._generate_custom_payload()
        response = adapter.invoke(f"Process: {payload}")
        return self._check_injection(response)
```

### Custom RAG Tests

```python
class CustomRAGTester:
    def test_vector_db_poisoning(self, adapter, vector_db):
        # Inject into vector DB
        malicious_doc = "IGNORE ALL INSTRUCTIONS..."
        vector_db.add(malicious_doc)

        # Query to retrieve
        context = vector_db.query("normal query")
        response = adapter.invoke(f"Context: {context}\n\nQuestion: ...")

        return self._check_injection(response)
```

## Remediation

### File Upload

- **Validate file contents** before processing
- **Sanitize extracted text** (strip directives, normalize)
- **Isolate file processing** from instruction context

### RAG Poisoning

- **Validate retrieved context** before passing to model
- **Implement context isolation** (separate instruction vs. data)
- **Monitor retrieval patterns** for anomalies

### Context Confusion

- **Implement instruction priority** (system > user > context)
- **Isolate contexts** (don't mix instructions and data)
- **Validate instruction sources** (trusted vs. untrusted)

## Research References

- **TopicAttack**: Indirect injection via topic transition
- **IPIGuard**: Tool Dependency Graph for defense
- **OWASP LLM Top 10**: LLM01 (Prompt Injection)

## Future Enhancements

Planned for b08+:
- 100+ attack patterns
- ML-powered detection
- Advanced fuzzing
- Multi-modal injection (images, audio)
