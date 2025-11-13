"""Example: Using orchestrators programmatically for advanced workflows."""

from harness.adapters.openai import OpenAIAdapter
from harness.core.models import TestCase
from harness.core.orchestrator_config import OrchestratorConfig
from harness.orchestrators.simple import SimpleOrchestrator
from harness.runners.mock import MockRunner

# Example 1: Create orchestrator with custom config
config = OrchestratorConfig(debug=True, verbose=True, custom_params={"max_retries": 5, "timeout": 30.0})
orchestrator = SimpleOrchestrator(config=config)

# Example 2: Use orchestrator directly (escape hatch)
adapter = OpenAIAdapter(model="gpt-4o-mini")
test_case = TestCase(
    id="custom_test",
    prompt="Test prompt",
    metadata={
        "orchestrator_config": {
            "debug": True,
            "custom_params": {"special_mode": "enabled"},
        }
    },
)

response = orchestrator.execute_prompt(
    test_case.prompt,
    test_case,
    adapter,
    config_override={"verbose": True},  # Per-call override
)

print(f"Response: {response.text}")
print(f"Debug info: {orchestrator.get_debug_info()}")

# Example 3: Use with runner for batch testing
runner = MockRunner(adapter=adapter, orchestrator=orchestrator)

results = list(
    runner.execute_many(
        [
            TestCase(id="test1", prompt="Prompt 1", metadata={}),
            TestCase(
                id="test2",
                prompt="Prompt 2",
                metadata={"orchestrator_config": {"debug": True}},  # Override for this test
            ),
        ]
    )
)

# Example 4: Dynamic config based on test characteristics
def create_orchestrator_for_test(test_type: str):
    """Create orchestrator with config based on test type."""
    if test_type == "sensitive":
        config = OrchestratorConfig(debug=True, verbose=True)
    else:
        config = OrchestratorConfig()
    return SimpleOrchestrator(config=config)

