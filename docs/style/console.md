# Console Style Guide

We print with SQLMap-tier clarity. Prefix tokens:

- [*] info   - high-level narration
- [+] ok     - success
- [!] warn   - risky or degraded but continuing
- [x] error  - fatal
- [>] step   - important phase transition
- [~] try    - attempt / retry
- [-] skip   - intentionally skipped

All actions:
- are idempotent where practical
- log before and after steps
- emit a single-line outcome summary
