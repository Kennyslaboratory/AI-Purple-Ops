# Reviewer Notes & Action Items

This document tracks reviewer feedback and action items for future branches.

## From b02-dev-tooling Code Review

### ✅ P0 Blockers
None. All acceptance criteria met.

### ✅ P1 Items (Addressed in b02)
1. **Scope hygiene** - Trailing newline cleanups
   - Status: Noted for future branches
   - Action: Keep file changes tight to branch plan

2. **Registry expansion uncommitted** - ✅ DONE
   - Committed as separate change: commit ec23358

3. **pip-audit policy** - ✅ DONE
   - Documented in Makefile help text as "non-fatal, informational only"
   - CI target explicitly notes audit not included

4. **ANSI in tests and logs** - Noted for b04
   - Status: Future enhancement
   - Action: Add ANSI-strip helper when writing JUnit/JSON evidence

5. **Document env precedence** - ✅ DONE
   - Added Configuration section to README
   - Documents AIPO_* override behavior

## Action Items for Future Branches

### b03-cli-skeleton
- **Scope Discipline**: Keep file changes tight to branch acceptance criteria
- **Avoid**: Auto-formatter making unrelated trailing newline cleanups
- **Strategy**: Review diffs before commit, stage only planned files

### b04-runner-mock (Reports & Evidence)
- **ANSI Stripping**: Add helper to clean ANSI codes from evidence files
- **Why**: Rich logger outputs ANSI codes that shouldn't be in JUnit XML or JSON reports
- **Implementation**: Simple regex or library like `strip-ansi` or `colorama`
- **Location**: `src/harness/utils/formatting.py` or similar
- **Example**:
  ```python
  import re

  def strip_ansi(text: str) -> str:
      """Remove ANSI escape sequences from text."""
      ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
      return ansi_escape.sub('', text)
  ```

### General Best Practices
- Review `git diff --stat` before committing
- Use `git add -p` for selective staging
- Keep commits atomic and aligned with branch goals
- Document deviations in commit messages

## What We Got Right in b02
✅ Acceptance criteria met: setup, lint, type, sec, tests, smoke
✅ Config precedence is explicit and tested
✅ Self-healing creates output dirs with clean logging
✅ Strict typing and linting across utils
✅ Compliance lane carried forward from b01
✅ Tool registry comprehensive and validated
