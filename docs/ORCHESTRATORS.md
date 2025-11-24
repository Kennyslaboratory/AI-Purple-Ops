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

## Using Bleeding-Edge PyRIT Features

**New in v1.2.4**: AI Purple Ops doesn't block access to PyRIT internals. Three ways to use bleeding-edge PyRIT features without waiting for AI Purple Ops updates:

### 1. Direct Memory Access (Recommended)

```python
from harness.orchestrators.pyrit import PyRITOrchestrator

orchestrator = PyRITOrchestrator(config=config)

# Access raw PyRIT memory for bleeding-edge features
raw_memory = orchestrator.get_raw_memory()

# Use brand new PyRIT feature released today
from pyrit.scorer import BrandNewScorer  # Hypothetical PyRIT v0.10+ feature
scorer = BrandNewScorer()
raw_memory.add_scorer(scorer)  # Works immediately
```

### 2. Auto-Passthrough

```python
# Unknown methods automatically forward to PyRIT memory
orchestrator = PyRITOrchestrator(config=config)

# PyRIT adds new method tomorrow - it just works
orchestrator.new_pyrit_method()  # Auto-forwards to memory.new_pyrit_method()
```

### 3. Mix Raw PyRIT + AI Purple Ops

```python
from pyrit.orchestrator import PromptSendingOrchestrator

# Use AI Purple Ops wrapper for most work
ai_purple_ops_orch = PyRITOrchestrator(config=config)

# Use raw PyRIT for bleeding-edge feature
raw_pyrit_orch = PromptSendingOrchestrator(
    memory=ai_purple_ops_orch.memory  # Share same DuckDB
)

# Both orchestrators use same conversation database
```

### Installing Latest PyRIT

```bash
# Stable (tested, recommended for production)
pip install -e ".[stable]"

# Bleeding-edge (latest PyRIT, for power users)
pip install -e ".[bleeding-edge]"
pip install --upgrade pyrit

# Development (flexible)
pip install -e ".[dev]"
```

**When to use bleeding-edge:**
- You need PyRIT features released this week
- You're contributing to PyRIT development
- You want to test compatibility with upcoming PyRIT versions

**Trade-offs:**
- ✅ Access to latest PyRIT features immediately
- ✅ Zero waiting for AI Purple Ops updates
- ⚠️ Potential breaking changes from PyRIT
- ⚠️ Features may not be documented in AI Purple Ops yet

## Troubleshooting PyRIT Integration

### Common Issues and Solutions

#### DuckDB Connection Issues

**Error:** `Could not initialize DuckDB at out/conversations.duckdb`

**Possible Causes:**
- File permissions on `out/` directory
- DuckDB already locked by another process
- Corrupted database file

**Solutions:**
```bash
# Check file permissions
ls -la out/conversations.duckdb

# Ensure out/ directory exists and is writable
mkdir -p out/
chmod 755 out/

# If database is corrupted, remove and recreate
rm out/conversations.duckdb
aipop run --suite test --orchestrator pyrit  # Creates new DB
```

**Graceful Fallback:** If DuckDB initialization fails, PyRIT orchestrator automatically falls back to in-memory storage. Conversations will work but won't be persisted.

---

#### PyRIT Version Mismatch

**Error:** `AttributeError: 'DuckDBMemory' object has no attribute 'some_method'`

**Cause:** PyRIT version incompatibility. AI Purple Ops requires `pyrit>=0.4.0`.

**Solutions:**
```bash
# Check installed PyRIT version
pip show pyrit

# Upgrade to latest compatible version
pip install --upgrade "pyrit>=0.4.0,<1"

# Verify installation
python -c "from pyrit.memory import DuckDBMemory; print('PyRIT OK')"
```

**Version Detection:** PyRIT orchestrator uses auto-passthrough (`__getattr__`) for bleeding-edge features. If a method doesn't exist, you'll get a clear error message.

---

#### Memory Initialization Failure

**Warning:** `Warning: Could not initialize DuckDB at <path>: <error>`  
**Warning:** `Falling back to in-memory conversation storage`

**Impact:** Orchestrator continues to work, but conversations are not persisted to disk.

**When This Happens:**
- DuckDB installation issues
- File system permissions
- Disk space issues

**Verification:**
```bash
# Check if database exists after run
ls -lh out/conversations.duckdb

# If file doesn't exist, persistence is disabled
# Conversations work but won't be saved

# To replay conversations, persistence must be enabled
aipop replay-conversation <id>  # Will fail if persistence was disabled
```

**Solution:** Fix DuckDB installation and re-run with persistence enabled.

---

#### Conversation Not Found

**Error:** `Conversation '<id>' not found in database`

**Possible Causes:**
1. Conversation ID is incorrect (typo)
2. Database was reset or deleted
3. Conversation not yet created

**Solutions:**
```bash
# List all available conversations
aipop list-conversations

# Check specific database path
aipop list-conversations --db-path /custom/path/conversations.duckdb

# Replay with correct ID
aipop replay-conversation <correct-id>
```

---

#### Multi-Turn Performance Issues

**Issue:** Multi-turn attacks running slower than expected

**Causes:**
- DuckDB writes on every turn (I/O overhead)
- Large context windows (>10 turns)
- Complex mutation strategies

**Optimizations:**
```yaml
# configs/orchestrators/pyrit.yaml

# Reduce context window for faster execution
custom_params:
  context_window: 3  # Default: 5

# Disable mutations for baseline testing
enable_mutations: false

# Reduce max_turns for testing
max_turns: 3  # Default: 10
```

**Performance Expectations:**
- Single-turn: <500ms overhead
- 5-turn conversation: ~2-3s total
- 10-turn conversation: ~4-5s total

---

#### Bleeding-Edge Feature Access

**Issue:** Need to use new PyRIT feature not yet wrapped by AI Purple Ops

**Solution:** Use escape hatches

**Method 1: `get_raw_memory()`**
```python
from harness.orchestrators.pyrit import PyRITOrchestrator

orchestrator = PyRITOrchestrator(config=config)
raw_memory = orchestrator.get_raw_memory()

# Use any PyRIT feature directly
from pyrit.scorer import NewScorer  # New in PyRIT v0.10
scorer = NewScorer()
raw_memory.add_scorer(scorer)  # Works immediately
```

**Method 2: `__getattr__` auto-passthrough**
```python
# PyRIT v0.10 adds new method tomorrow
orchestrator.brand_new_pyrit_method()  # Auto-forwards to memory

# If method doesn't exist, you get clear error:
# AttributeError: 'PyRITOrchestrator' object has no attribute 'X'. 
# Not found in PyRIT memory either.
```

---

#### Debug Mode

**Enable comprehensive debugging:**

```bash
# CLI debug mode
aipop run --suite test --orchestrator pyrit --orch-opts debug,verbose

# Shows:
# - Configuration resolution
# - Execution history (last 5 operations)
# - Conversation state
# - DuckDB writes
# - Error logs
```

**Programmatic debug:**
```python
from harness.core.orchestrator_config import OrchestratorConfig

config = OrchestratorConfig(debug=True, verbose=True)
orchestrator = PyRITOrchestrator(config=config)

# After execution
debug_info = orchestrator.get_debug_info()
print(json.dumps(debug_info, indent=2))
```

---

#### Database Schema Issues

**Error:** `DuckDB schema version mismatch`

**Cause:** PyRIT updated their schema, existing database incompatible

**Solutions:**
```bash
# Backup existing database
cp out/conversations.duckdb out/conversations.duckdb.backup

# Option 1: Delete and recreate
rm out/conversations.duckdb

# Option 2: Use Alembic migrations (if available)
alembic upgrade head

# Verify
aipop run --suite test --orchestrator pyrit
```

---

#### Getting Help

**Still having issues?**

1. **Check logs:** Enable debug mode (`--orch-opts debug,verbose`)
2. **Verify installation:** `pip show pyrit` and `pip show ai-purple-ops`
3. **Test basic functionality:** `aipop run --suite test --orchestrator pyrit --adapter mock`
4. **Check DuckDB:** `ls -lh out/conversations.duckdb`
5. **Review PyRIT docs:** https://github.com/Azure/PyRIT

**Report issues:** https://github.com/Kennyslaboratory/AI-Purple-Ops/issues

Include:
- AI Purple Ops version (`aipop --version`)
- PyRIT version (`pip show pyrit`)
- Full error message
- Debug output (`--orch-opts debug`)

---

## Best Practices

1. **Start simple**: Use `SimpleOrchestrator` for basic needs
2. **Use config files**: Keep orchestrator configs in version control
3. **Per-test overrides**: Use test metadata for test-specific needs
4. **Debug mode**: Enable when troubleshooting
5. **Programmatic API**: Use Python API for automation and scripting
6. **Custom orchestrators**: Implement protocol for specialized workflows
7. **Bleeding-edge features**: Use escape hatches (`get_raw_memory()`) for new PyRIT features

