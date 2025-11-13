# Orchestrators Guide

## What Are Orchestrators?

Orchestrators control how prompts are sent to AI models, managing conversation state, context injection, and attack strategy coordination. They sit between the Runner and Adapter, providing intelligent orchestration capabilities.

## When to Use Orchestrators

- **Multi-turn conversations**: Maintain context across multiple exchanges
- **Attack chaining**: Coordinate complex multi-step attacks
- **State management**: Track conversation history and context
- **Custom workflows**: Implement specialized testing strategies

## Configuration Hierarchy

Orchestrators support flexible configuration with clear priority:

1. **Test case metadata** (highest priority)
   - Per-test overrides via `orchestrator_config` in test metadata
   - Allows fine-grained control per test case

2. **CLI options**
   - `--orch-opts debug,verbose`: Enable debug/verbose modes
   - Override config files

3. **Config files**
   - `--orch-config`: Custom config file path
   - Default: `configs/orchestrators/{orchestrator_name}.yaml`

4. **Default values** (lowest priority)
   - Built-in defaults for all settings

## Programmatic API

### Basic Usage

```python
from harness.orchestrators.simple import SimpleOrchestrator
from harness.core.orchestrator_config import OrchestratorConfig
from harness.adapters.openai import OpenAIAdapter
from harness.core.models import TestCase

# Create orchestrator with config
config = OrchestratorConfig(debug=True, verbose=True)
orchestrator = SimpleOrchestrator(config=config)

# Use directly
adapter = OpenAIAdapter(model="gpt-4o-mini")
test_case = TestCase(id="test1", prompt="Hello", metadata={})
response = orchestrator.execute_prompt("Hello", test_case, adapter)

# Get debug info
debug_info = orchestrator.get_debug_info()
print(debug_info)
```

### With Runner

```python
from harness.runners.mock import MockRunner

runner = MockRunner(
    adapter=adapter,
    orchestrator=orchestrator
)

result = runner.execute(test_case)
```

### Per-Test Configuration

```python
test_case = TestCase(
    id="test1",
    prompt="Hello",
    metadata={
        "orchestrator_config": {
            "debug": True,
            "custom_params": {"special_mode": "enabled"}
        }
    }
)

# Test metadata config overrides instance config
response = orchestrator.execute_prompt("Hello", test_case, adapter)
```

## Mutation Engine Integration

Orchestrators can optionally use mutation engines to automatically generate and test mutated versions of prompts. This enables intelligent attack generation and adaptive testing strategies.

### Enabling Mutations in Orchestrator

Configure mutations via orchestrator custom parameters:

```python
from harness.core.orchestrator_config import OrchestratorConfig

config = OrchestratorConfig(
    custom_params={
        "enable_mutations": True,
        "mutation_config": "configs/mutation/default.yaml"
    }
)
orchestrator = SimpleOrchestrator(config=config)
```

### Per-Test Mutation Configuration

Control mutations per test case via metadata:

```python
test_case = TestCase(
    id="test1",
    prompt="Attack prompt",
    metadata={
        "optimization_target": "asr",  # asr, stealth, or balanced
        "orchestrator_config": {
            "custom_params": {
                "enable_mutations": True
            }
        }
    }
)
```

The orchestrator will automatically:
1. Generate mutations using enabled strategies
2. Try mutations in order (best first based on RL feedback)
3. Record results for learning
4. Fall back to original prompt if all mutations fail

See [Mutation Engine Guide](MUTATION_ENGINE.md) for complete details.

## Implementing Custom Orchestrators

All orchestrators must implement the `Orchestrator` protocol:

```python
from typing import Protocol, Any
from harness.core.models import TestCase, ModelResponse
from harness.core.adapters import Adapter

class Orchestrator(Protocol):
    def execute_prompt(
        self,
        prompt: str,
        test_case: TestCase,
        adapter: Adapter,
        config_override: dict[str, Any] | None = None
    ) -> ModelResponse:
        ...
    
    def reset_state(self) -> None:
        ...
    
    def get_debug_info(self) -> dict[str, Any]:
        ...
```

### Example Custom Orchestrator

```python
from harness.core.orchestrator_config import OrchestratorConfig
from harness.core.models import TestCase, ModelResponse
from harness.core.adapters import Adapter

class CustomOrchestrator:
    def __init__(self, config: OrchestratorConfig | None = None):
        self.config = config or OrchestratorConfig()
        self._state = {}
    
    def execute_prompt(
        self,
        prompt: str,
        test_case: TestCase,
        adapter: Adapter,
        config_override: dict[str, Any] | None = None
    ) -> ModelResponse:
        # Custom logic here
        response_text = adapter.invoke(prompt)
        return ModelResponse(text=response_text, meta={"orchestrator": "custom"})
    
    def reset_state(self) -> None:
        self._state.clear()
    
    def get_debug_info(self) -> dict[str, Any]:
        return {"orchestrator_type": "custom", "state": self._state}
```

## PyRIT Orchestrator (Multi-Turn Conversations)

**New in b08.3**: The PyRIT orchestrator provides multi-turn conversation support with persistent memory using PyRIT's proven DuckDB architecture.

### When to Use PyRIT Orchestrator

- **Multi-turn attacks**: Test multi-step jailbreaks and conversation hijacking
- **Stateful testing**: Maintain context across multiple prompts
- **Conversation persistence**: Store and resume conversations
- **Advanced attacks**: Implement delayed payloads, context confusion, multi-turn traps

### CLI Usage

```bash
# Basic multi-turn testing (5 turns)
aipop run --suite adversarial --orchestrator pyrit --max-turns 5

# Single turn (backward compatible with simple)
aipop run --suite adversarial --orchestrator pyrit --max-turns 1

# With custom config
aipop run --suite adversarial --orchestrator pyrit --orch-config configs/orchestrators/pyrit.yaml

# Continue previous conversation
aipop run --suite adversarial --orchestrator pyrit --conversation-id abc123

# Debug mode
aipop run --suite adversarial --orchestrator pyrit --max-turns 5 --orch-opts debug,verbose
```

### Configuration

Default config: `configs/orchestrators/pyrit.yaml`

```yaml
name: pyrit
description: Multi-turn orchestrator with conversation memory

# Conversation settings
max_turns: 10
conversation_timeout_seconds: 300
enable_branching: true
persist_history: true

# Memory settings
db_path: out/conversations.duckdb
auto_save: true
history_limit: 100

# Mutation settings (integrates with b08.2)
enable_mutations: false
mutation_config: configs/mutation/default.yaml

# Debug settings
debug: false
verbose: false

# Custom parameters
custom_params:
  strategy: "multi_turn"
  context_window: 5
  state_tracking: true
```

### Programmatic API

```python
from harness.orchestrators.pyrit import PyRITOrchestrator
from harness.core.orchestrator_config import OrchestratorConfig
from harness.runners.mock import MockRunner
from harness.adapters.openai import OpenAIAdapter

# Create PyRIT orchestrator
config = OrchestratorConfig(
    orchestrator_type="pyrit",
    debug=True,
    custom_params={
        "max_turns": 5,
        "db_path": "out/conversations.duckdb",
        "context_window": 3,
    }
)
orchestrator = PyRITOrchestrator(config=config)

# Use with runner
adapter = OpenAIAdapter(model="gpt-4o-mini")
runner = MockRunner(adapter=adapter, orchestrator=orchestrator)

# Execute test (will run 5 turns automatically)
result = runner.execute(test_case)

# Access multi-turn results
print(f"Total turns: {result.metadata['total_turns']}")
for turn in result.metadata['turn_results']:
    print(f"Turn {turn['turn']}: {turn['response'][:50]}...")

# Conversation management
history = orchestrator.get_conversation_history()
orchestrator.reset_conversation()  # Start new conversation
orchestrator.branch_conversation(turn_id=3)  # Branch from turn 3
```

### Key Features

**Multi-Turn Execution**
- Automatically executes multiple turns for each test case
- Maintains conversation state across turns
- Aggregates results from all turns
- Stores full conversation history in transcripts

**DuckDB Persistence**
- Uses PyRIT's proven DuckDB schema
- Stores conversations for later analysis
- Resume conversations by ID
- Query conversation history

**Conversation Management**
- Reset: Start new conversation
- Branch: Create new conversation from specific turn
- Continue: Resume previous conversation by ID
- Context window: Include N previous turns in context

**Integration with Mutations**
- Optional mutation injection per turn
- Uses mutation engine from b08.2
- Tracks which mutations succeed across turns

### Performance

- **Single-turn**: <500ms overhead vs no orchestrator
- **Multi-turn (5 turns)**: ~2s per test case
- **Memory**: <100MB for 1000 conversations
- **Throughput**: 10-20 test cases/minute

### Architecture Pattern for PyRIT/Garak Integration

The orchestrator pattern allows wrapping external tools:

```
Runner
  └─> Orchestrator (Protocol)
       ├─> SimpleOrchestrator (single-turn, backward compatible)
       ├─> PyRITOrchestrator (multi-turn with DuckDB memory) ← NEW in b08.3
       └─> GarakOrchestrator (future: wrapper around Garak)
```

The PyRIT orchestrator (b08.3) wraps PyRIT's memory architecture while maintaining our configuration system and debug capabilities.

## Debugging

Enable debug mode to see exactly what's happening:

```bash
# Debug mode only
aipop run --suite redteam --orchestrator simple --orch-opts debug

# Debug + verbose for maximum visibility
aipop run --suite redteam --orchestrator simple --orch-opts debug,verbose
```

Debug output includes:
- Configuration resolution (which config was used)
- Execution history (last 5 operations)
- State information
- Error logs

Programmatically:

```python
orchestrator = SimpleOrchestrator(config=OrchestratorConfig(debug=True))
# ... execute tests ...
debug_info = orchestrator.get_debug_info()
print(json.dumps(debug_info, indent=2))
```

## Best Practices

1. **Start simple**: Use `SimpleOrchestrator` for basic needs
2. **Use config files**: Keep orchestrator configs in version control
3. **Per-test overrides**: Use test metadata for test-specific needs
4. **Debug mode**: Enable when troubleshooting
5. **Programmatic API**: Use Python API for automation and scripting
6. **Custom orchestrators**: Implement protocol for specialized workflows

