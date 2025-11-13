# ADR 0002: Licensing

## Status
Accepted

## Context
AI Purple Ops is designed as a community-forkable, vendor-neutral backend for AI security testing. We need a license that:
- Allows broad use and modification
- Permits commercial use to encourage adoption
- Maintains attribution and derivative work transparency
- Balances openness with protection against exploitation

## Decision
Use MIT License.

## Rationale

### Why MIT
- **Maximum adoption**: Permissive license removes barriers for enterprise, research, and individual users
- **Simple and clear**: Well-understood terms reduce legal friction
- **Commercial friendly**: Organizations can build on and deploy without complex compliance
- **Community standard**: Widely accepted in security tooling ecosystem

### Alternatives considered

**AGPL-3.0**
- ✅ Stronger copyleft, requires service providers to share modifications
- ❌ More complex compliance, may deter enterprise adoption
- ❌ Incompatible with some commercial toolchains

**Apache 2.0**
- ✅ Patent grant protection
- ✅ Explicit contributor license agreement
- ❌ Slightly more complex than MIT
- ❌ Patent clause can complicate enterprise legal review

**MIT + Commons Clause**
- ✅ Prevents pure resale without contribution
- ❌ Not OSI-approved, creates ambiguity
- ❌ May fragment community and reduce adoption

**SSPL (Server Side Public License)**
- ✅ Requires cloud providers to open their stack
- ❌ Not OSI-approved, controversial in community
- ❌ Major barrier to enterprise adoption

## Consequences

### Positive
- Low friction for anyone to fork, modify, and deploy
- Compatible with most corporate security tool stacks
- Encourages contributions and ecosystem growth
- Simple compliance for researchers and consultants

### Negative
- Anyone can commercialize without contributing back or sharing revenue
- No patent grant (but project doesn't currently involve patentable inventions)
- Derivative works can become proprietary

### Mitigation
- Build strong community through quality, documentation, and support
- Use trademarks to prevent misleading derivative products
- Encourage contribution through clear governance and credit
- Maintain reference implementation as the canonical version

## Notes
If commercial exploitation without contribution becomes problematic, revisit with dual-licensing (MIT for open source, commercial license for proprietary use) or switch to Apache 2.0 for patent protection.

This decision prioritizes maximum accessibility and adoption over revenue capture.
