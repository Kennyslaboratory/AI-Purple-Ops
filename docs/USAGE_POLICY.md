# Usage Policy

## Authorized Use Only

This AI Security Harness includes offensive security testing capabilities. Use is restricted to:

1. **Authorized test environments only**
   - Dedicated lab tenants
   - Isolated sandboxes
   - Explicitly approved staging environments

2. **Prohibited targets**
   - Production systems without written authorization
   - Third-party systems without explicit permission
   - Any system where you do not have legal authority to test

3. **Required approvals**
   - Security team sign-off for any red-team exercise
   - Legal review for tests involving customer data or production-adjacent systems
   - Incident response team notification before running adversarial batteries

## Scope and Blast Radius

- Define scope and boundaries before each test
- Use ring-based rollouts (canary → pilot → broad)
- Implement kill switches for any automated agents
- Log all tool calls and model interactions

## Data Handling

- No real PII, credentials, or secrets in test corpora
- Use synthetic data and fixtures
- Redact sensitive information in reports and logs
- Follow your organization's data governance policies

## Incident Response

If testing causes an incident:
1. Immediately freeze automations and revoke keys
2. Notify security team per SECURITY_CONTACTS.md
3. Scope impact and roll back changes
4. Add regression test to prevent recurrence
5. Update threat model and controls

## Compliance

Users are responsible for ensuring compliance with:
- Applicable laws and regulations (GDPR, CCPA, etc.)
- Organizational security policies
- Industry standards (SOC 2, ISO 27001, etc.)
- Contractual obligations with customers and partners

## Enforcement

Violations of this policy may result in:
- Immediate access revocation
- Escalation to security and legal teams
- Disciplinary action per organizational policy

For questions or to report misuse, see [SECURITY_CONTACTS.md](../SECURITY_CONTACTS.md).
