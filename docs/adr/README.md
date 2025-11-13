# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for AI Purple Ops.

## What are ADRs?

ADRs document significant architectural decisions, their context, and their consequences. They help future contributors understand why things are the way they are.

## Format

Each ADR is a short markdown file with:
- **Title**: Decision being made
- **Context**: What problem are we solving?
- **Decision**: What did we decide?
- **Consequences**: What are the tradeoffs?

## Existing ADRs

- [ADR 0001: Context and Scope](0001-context-and-scope.md)
- [ADR 0002: Licensing](0002-licensing.md)

## Governance Principles

1. **Safety First**: Defaults choose safety and clarity over convenience
2. **Vendor Neutrality**: Adapters isolate vendors and infrastructure
3. **Evidence-Driven**: All claims must be testable and verifiable
4. **Simple Over Clever**: Code should be obvious, not clever
