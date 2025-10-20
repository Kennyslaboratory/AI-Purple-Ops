from __future__ import annotations

from harness.utils.logging import log
from harness.utils.preflight import preflight


def main() -> None:
    log.info("Developer smoke test starting")
    preflight()
    log.ok("Developer smoke test passed")


if __name__ == "__main__":
    main()
