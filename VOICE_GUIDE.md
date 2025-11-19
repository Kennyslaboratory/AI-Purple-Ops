# AI Purple Ops - Voice & Tone Guide

## Core Principle

Write like a security researcher who ships production code. Direct. Confident. Zero fluff.

## What We Sound Like

**Think:** Super hacker meets Steve Jobs. Technical precision with uncompromising vision.

### Examples of Our Voice

**Good:**
```
The weapon of choice for AI security professionals.
```

**Bad:**
```
🎉 We're super excited to announce our amazing new feature! 🚀✨
```

---

**Good:**
```
94% test pass rate (673/748 tests). The foundation is complete.
```

**Bad:**
```
✅ Amazing news everyone! ✅ We're making great progress! 🔨 Almost there! 🎯
```

---

**Good:**
```
Error classification eliminates false positives. HAR 1.2 export for Burp Suite. DuckDB persistence.
```

**Bad:**
```
🔥 Check out our super cool error thingy that's like totally awesome! 💯
```

## Writing Rules

### DO
- Be direct and factual
- Use concrete metrics (94% pass rate, 673 tests, 2,500 lines)
- State capabilities clearly ("eliminates false positives" not "reduces false positives")
- Use industry terminology (HAR 1.2, token bucket, CVSS v3.1)
- Be confident about what works
- Be honest about what's pending

### DON'T
- Use emoji spam (one per section max, preferably zero)
- Use marketing fluff ("amazing", "super cool", "game-changing")
- Use excessive punctuation (!!!, ???)
- Use "we're excited to announce" or similar corporate speak
- Apologize or hedge ("we think", "hopefully", "maybe")
- Use passive voice ("mistakes were made")

## Status Terminology

Use these precise terms:

- **Production** - Battle-tested, ready for production use
- **Foundation** - Infrastructure complete, integration pending
- **Beta** - Functional with known limitations
- **Planned** - On the roadmap

Never use:
- "Almost done!"
- "Coming soon™"
- "Exciting new feature!"
- "Revolutionary"
- "Best-in-class"

## Technical Writing

### Command Descriptions

**Good:**
```
aipop doctor check    # Run preflight diagnostics
aipop sessions export # Export HAR for Burp Suite
```

**Bad:**
```
aipop doctor check    # 🔍 Amazingly checks your awesome config!
aipop sessions export # ✨ Super cool export feature! 🎉
```

### Documentation Headers

**Good:**
```
# Error Classification System

Prevents false positives by distinguishing infrastructure errors from security findings.
```

**Bad:**
```
# 🎯 Our Amazing Error Classification System! ✨

We're super excited to introduce our revolutionary error classification feature that will totally change your life! 🚀
```

### README Style

**Good:**
```
## Current Status: v1.2.3 - Production Ready

Core testing, diagnostics, and session management are production-ready.
94% test pass rate (673/748 tests).
```

**Bad:**
```
## ✅ CURRENT STATUS: v1.2.3 - 🎉 Foundation Complete! 🚀

**Core Functionality:** Production-ready ✅ ✅ ✅
**Professional Features:** Foundation built, integration in progress 🔨 🔨
```

## Examples from Codebase

### Recently Fixed

**Before:**
```markdown
## ✅ CURRENT STATUS: v1.2.3 - Foundation Complete

**Core Functionality:** Production-ready ✅  
**Professional Features:** Foundation built, integration in progress 🔨
```

**After:**
```markdown
## Current Status: v1.2.3 - Production Ready

Core testing, diagnostics, and session management are production-ready.
94% test pass rate (673/748 tests).
```

---

**Before:**
```python
console.print("\n[bold]🔍 AI Purple Ops Doctor - Configuration Check[/bold]\n")
```

**After:**
```python
console.print("\n[bold]AI Purple Ops Doctor - Configuration Check[/bold]\n")
```

---

**Before:**
```
| **NEW:** Diagnostics (Doctor) | ✅ Production |
```

**After:**
```
| Diagnostics (Doctor) | Production |
```

## CLI Help Text Standards

Keep it terse and professional:

```python
# Good
app = typer.Typer(help="Diagnose configuration and environment issues")

# Bad
app = typer.Typer(help="🔍 Super awesome diagnostic tool that checks everything! ✨")
```

## Commit Message Style

**Good:**
```
feat: add error classification system

- Prevents false positives from API errors
- TestResult with 1:N Finding relationship
- 94% test pass rate
```

**Bad:**
```
🎉 feat: Added AMAZING new error classification! ✅ 

We're super excited to announce this revolutionary feature! 🚀
- Totally awesome TestResult thingy! 💯
- Like, way better false positive handling! 🔥
```

## When in Doubt

Ask: "Would a senior security engineer at Google write this?"

If not, simplify. Remove fluff. Add facts.

---

**Remember:** We're building a weapon for professionals. Act like it.

