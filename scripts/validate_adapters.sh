#!/usr/bin/env bash
# Validate adapters script
# Tests adapter loading and basic functionality

set -euo pipefail

echo "🔌 AI Purple Ops - Adapter Validation"
echo "======================================"
echo ""

# Check Python environment
if ! command -v python &> /dev/null; then
    echo "❌ Python not found"
    exit 1
fi

echo "1. Listing available adapters..."
python -m cli.harness adapter list || echo "⚠️  Adapter list command failed"

echo ""
echo "2. Testing mock adapter (should always work)..."
python -m cli.harness adapter test --name mock || echo "⚠️  Mock adapter test failed"

echo ""
echo "3. Checking adapter registry..."
python -c "
from harness.adapters.registry import AdapterRegistry
adapters = AdapterRegistry.list_adapters()
print(f'✅ Found {len(adapters)} registered adapters: {', '.join(adapters)}')
"

echo ""
echo "4. Testing recipe executor with mock adapter..."
python -c "
from harness.executors.recipe_executor import execute_recipe
from harness.loaders.recipe_loader import RecipeConfig
import tempfile
from pathlib import Path

# Create minimal test recipe
recipe = RecipeConfig(
    version=1,
    metadata={'name': 'Test', 'lane': 'safety'},
    config={'adapter': 'mock', 'seed': 42},
    execution={'suites': ['normal']},
    outputs=None,
    gate=None,
)

# Create temp suite
with tempfile.TemporaryDirectory() as tmpdir:
    suite_dir = Path(tmpdir) / 'suites' / 'normal'
    suite_dir.mkdir(parents=True)
    (suite_dir / 'test.yaml').write_text('id: test\ncases:\n  - id: t1\n    prompt: \"test\"\n    expected: pass\n')

    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmpdir)
        result = execute_recipe(recipe, output_dir=tmpdir)
        if result.success:
            print('✅ Recipe execution with mock adapter successful')
        else:
            print(f'⚠️  Recipe execution failed: {result.error}')
    finally:
        os.chdir(old_cwd)
" || echo "⚠️  Recipe executor test failed"

echo ""
echo "5. Checking for optional adapter dependencies..."
python -c "
optional_deps = {
    'transformers': 'local adapters (HuggingFace)',
    'openai': 'cloud adapters (OpenAI)',
    'anthropic': 'cloud adapters (Anthropic)',
    'boto3': 'cloud adapters (AWS Bedrock)',
    'llama_cpp': 'local adapters (llama.cpp)',
}

missing = []
for dep, desc in optional_deps.items():
    try:
        __import__(dep)
        print(f'✅ {dep} installed ({desc})')
    except ImportError:
        print(f'⚠️  {dep} not installed ({desc}) - optional')
        missing.append(dep)

if missing:
    print(f'\n💡 Install optional dependencies: pip install ai-purple-ops[all-adapters]')
"

echo ""
echo "✅ Adapter validation complete!"
echo ""
echo "Next steps:"
echo "  - Run 'python -m cli.harness adapter init' to create a custom adapter"
echo "  - Run 'python -m cli.harness adapter test --name <adapter>' to test an adapter"
echo "  - See docs/ADAPTERS_QUICKSTART.md for more information"
