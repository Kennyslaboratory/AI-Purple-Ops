# Compliance and Evidence Automation

AI Purple Ops automates compliance evidence generation for major AI governance frameworks.

---

## Supported Frameworks

### NIST AI Risk Management Framework (AI RMF 1.0)

**Coverage:**
- **GOVERN**: Policy and oversight structures
- **MAP**: Risk identification and categorization
- **MEASURE**: Evaluation metrics and monitoring
- **MANAGE**: Risk response procedures

**How to Use:**
```bash
# Run NIST compliance recipe
aipop recipe run --recipe nist_measure

# Generates:
# - MEASURE phase evidence
# - Risk assessment metrics
# - Control effectiveness data
```

**Evidence Generated:**
- Test execution transcripts
- Harmful output rate metrics
- Policy violation reports
- Control effectiveness measurements

### EU AI Act (Regulation 2024/1689)

**Coverage:**
- Article 9: Risk management systems
- Article 10: Data and data governance
- Article 11: Technical documentation (Annex IV)
- Article 15: Accuracy, robustness, cybersecurity

**How to Use:**
```bash
# Run with evidence generation
aipop run --suite adversarial
aipop gate --generate-evidence

# Evidence pack includes:
# - Technical documentation
# - Risk assessment records
# - Test results and metrics
# - Conformance reports
```

**Evidence Generated:**
- Risk management documentation
- Data governance records
- Accuracy and robustness metrics
- Security testing results

### FedRAMP (Federal Risk and Authorization Management Program)

**Coverage:**
- **AC** (Access Control): Tool policy enforcement
- **AU** (Audit and Accountability): Complete audit trails
- **SI** (System and Information Integrity): Security testing

**How to Use:**
```bash
# Generate FedRAMP evidence
aipop run --suite redteam
aipop gate --generate-evidence --policy policies/fedramp.yaml
```

**Evidence Generated:**
- Control implementation statements
- Test procedures and results
- Continuous monitoring artifacts
- Assessment reports

### OWASP LLM Top 10

**Coverage:**
- LLM01: Prompt Injection
- LLM02: Insecure Output Handling
- LLM03: Training Data Poisoning
- LLM06: Sensitive Information Disclosure
- LLM07: Insecure Plugin Design
- LLM08: Excessive Agency
- LLM09: Overreliance
- LLM10: Model Theft

**How to Use:**
```bash
# Run OWASP coverage tests
aipop run --suite adversarial  # LLM01: Prompt Injection
aipop run --suite rag           # LLM03: Training Data Poisoning
aipop run --suite ui            # LLM02: Insecure Output Handling
```

---

## Evidence Artifacts

### Run Summary (JSON)

```json
{
  "run_id": "run-20250108-abc123",
  "timestamp": "2025-01-08T14:30:00Z",
  "adapter": "openai",
  "model": "gpt-4o-mini",
  "suite": "adversarial",
  "results": {
    "total": 50,
    "passed": 45,
    "failed": 5
  },
  "metrics": {
    "harmful_output_rate": 0.10,
    "policy_violation_rate": 0.04,
    "critical_violation_rate": 0.00
  },
  "detectors": {
    "harmful_content": {
      "violations": 5,
      "categories": {"violence": 3, "hate_speech": 2}
    }
  }
}
```

### Evidence Manifest

```json
{
  "manifest_version": "1.0",
  "evidence_pack_id": "evidence-20250108-abc123",
  "framework": "NIST_AI_RMF",
  "phase": "MEASURE",
  "artifacts": [
    {
      "type": "summary",
      "path": "summary.json",
      "hash": "sha256:abc123..."
    },
    {
      "type": "transcripts",
      "path": "transcripts/",
      "count": 50
    }
  ]
}
```

### JUnit XML (CI/CD Integration)

```xml
<testsuite name="adversarial" tests="50" failures="5" time="45.2">
  <testcase classname="adversarial.jailbreak" name="test_001" time="0.8">
    <failure message="Harmful content detected">
      Response violated content policy (violence)
    </failure>
  </testcase>
  <testcase classname="adversarial.jailbreak" name="test_002" time="0.9"/>
</testsuite>
```

---

## Compliance Workflows

### Workflow 1: Pre-Deployment Assessment

**Goal:** Generate evidence before deploying to production.

```bash
# 1. Run comprehensive security testing
aipop recipe run --recipe full_redteam --adapter production_model

# 2. Check quality gates
aipop gate --policy policies/production_policy.yaml

# 3. Generate evidence pack for review
aipop gate --generate-evidence --evidence-dir audit/pre-deployment/

# Evidence pack includes:
# - summary.json (test results)
# - junit.xml (CI/CD integration)
# - transcripts/ (full conversation logs)
# - evidence_manifest.json (artifact inventory)
# - conformance_report.json (framework mappings)
```

### Workflow 2: Continuous Monitoring

**Goal:** Ongoing compliance validation in production.

```bash
# Run nightly security scans
0 2 * * * cd /app && aipop run --suite adversarial >> logs/security.log 2>&1

# Weekly evidence generation
0 0 * * 0 cd /app && aipop gate --generate-evidence --evidence-dir compliance/weekly/
```

### Workflow 3: Audit Response

**Goal:** Respond to auditor requests with evidence.

```bash
# Generate evidence for specific time period
aipop gate --summary out/reports/summary-2025-01-08.json \
  --generate-evidence \
  --evidence-dir audit/q1-2025/

# Evidence pack ready for auditor review
ls audit/q1-2025/evidence-20250108-*.zip
```

---

## Framework Mappings

### NIST AI RMF → AI Purple Ops

| NIST Function | AI Purple Ops Component | Evidence |
|---------------|------------------------|----------|
| GOVERN-1 | Policy loader, content policies | Policy YAML files |
| MAP-1 | Threat models, test suites | Threat model docs |
| MEASURE-2.1 | HarmfulContentDetector | Violation reports |
| MEASURE-2.3 | Quality gates, thresholds | Gate results |
| MEASURE-2.4 | Test transcripts | Full conversation logs |
| MANAGE-1 | Evidence packs | ZIP artifacts |

### EU AI Act → AI Purple Ops

| Article | Requirement | AI Purple Ops Feature | Evidence |
|---------|------------|----------------------|----------|
| Article 9 | Risk management | Test suites, detectors | Test results, metrics |
| Article 10 | Data governance | Transcript logging | Full conversation logs |
| Article 11 | Technical docs | Evidence manifests | Documentation |
| Article 15 | Robustness testing | Adversarial suites | Security test results |

### FedRAMP → AI Purple Ops

| Control Family | Control | AI Purple Ops Feature | Evidence |
|----------------|---------|----------------------|----------|
| AC (Access Control) | AC-3 | ToolPolicyDetector | Tool violation logs |
| AU (Audit) | AU-2 | Transcript logging | Complete audit trail |
| SI (System Integrity) | SI-2 | Security test suites | Vulnerability findings |

---

## Evidence Storage

### Directory Structure

```
out/
├── reports/
│   ├── summary.json              # Machine-readable results
│   ├── junit.xml                 # CI/CD integration
│   └── report.html               # Human-readable report
├── transcripts/
│   ├── test_001.json             # Full conversation
│   ├── test_002.json
│   └── ...
└── evidence/
    └── evidence-20250108-*.zip   # Complete evidence pack
        ├── manifest.json
        ├── summary.json
        ├── junit.xml
        ├── transcripts/
        └── conformance_report.json
```

### Retention Policies

**Recommended:**
- **Development**: 30 days
- **Staging**: 90 days
- **Production**: 7 years (or per regulatory requirements)
- **Incident Response**: Indefinite

```bash
# Archive old evidence
tar -czf archive/2025-Q1-evidence.tar.gz out/evidence/

# Clean up after archiving
find out/evidence/ -name "*.zip" -mtime +90 -delete
```

---

## Integration Examples

### GitHub Actions

```yaml
name: AI Security Testing

on: [push, pull_request]

jobs:
  security-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup AI Purple Ops
        run: make setup

      - name: Run Security Tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: aipop run --suite adversarial

      - name: Evaluate Gates
        run: aipop gate --generate-evidence

      - name: Upload Evidence
        uses: actions/upload-artifact@v4
        with:
          name: security-evidence
          path: out/evidence/*.zip
          retention-days: 90
```

### Jenkins Pipeline

```groovy
pipeline {
  agent any

  stages {
    stage('Security Testing') {
      steps {
        sh 'aipop run --suite redteam'
      }
    }

    stage('Quality Gate') {
      steps {
        sh 'aipop gate --fail-on harmful_output_rate,critical_violation_rate'
      }
    }

    stage('Archive Evidence') {
      steps {
        sh 'aipop gate --generate-evidence'
        archiveArtifacts artifacts: 'out/evidence/*.zip', fingerprint: true
      }
    }
  }
}
```

---

## Best Practices

1. **Automate Evidence Generation** - Generate evidence packs automatically in CI/CD
2. **Version Control Policies** - Track policy changes with git
3. **Retain Evidence** - Follow regulatory retention requirements
4. **Document Exceptions** - Record and justify any gate bypasses
5. **Regular Updates** - Keep test suites current with emerging threats
6. **Independent Review** - Have security team review evidence packs
7. **Secure Storage** - Encrypt evidence packs at rest

---

## Next Steps

- [Recipes Guide](RECIPES.md) - Compliance recipes
- [Gates Guide](GATES.md) - Configure quality gates
- [Evidence Pack Specification](EVIDENCE_PACK_SPEC.md) - Artifact format details
- [NIST AI RMF Mapping](../mappings/nist_ai_rmf.yaml) - Detailed control mappings
