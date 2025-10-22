# Roadmap

Goal
- Backend that powers AI Purple Ops UI
- Safety lane and Security lane both enforced
- Batteries included for planning, scoping, threat modeling, eval, emulation, and gates
- **Recipe system for instant workflow deployment**

Phases
1 b01 initial commit
2 b02 dev tooling
3 b03 cli skeleton
4 b04 runner mock and reports
5 b05 oracles and policies
6 b06 gate and evidence **+ recipe engine + 3 reference recipes**
7 b07 redteam rag ui fuzz **+ 6 security recipes**
8 b08 retrievers and simulated tools **+ 5 compliance recipes**
9 b09 ci workflows **+ recipe validation**
10 b10 backend api and compose **+ recipe marketplace**

Each phase is demo ready. Keep pull requests small. Tag v0.NN.0 after merge.

## Recipe System Rollout

**b06**: Recipe engine foundation
- Recipe loader and validator
- Recipe executor (orchestrates existing components)
- 3 reference recipes: content_policy (safety), prompt_injection (security), nist_measure (compliance)
- CLI: `recipe run`, `recipe list`, `recipe validate`

**b07**: Security recipe library
- 6 security-focused recipes (OWASP LLM coverage)
- Recipe testing framework
- Recipe documentation templates

**b08**: Compliance recipe library
- 5 compliance-focused recipes (NIST, EU, FedRAMP, ISO)
- Evidence pack templates for each framework
- Recipe best practices guide

**b09**: Recipe CI/CD integration
- Recipe validation in pre-commit hooks
- Recipe testing in GitHub Actions
- Recipe versioning and compatibility checks

**b10**: Recipe marketplace
- Community recipe contributions
- Recipe sharing/publishing
- Recipe quality standards
