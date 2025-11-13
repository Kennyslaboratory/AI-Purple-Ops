#!/usr/bin/env python3
"""Benchmark cache performance for AI Purple Ops.

Tests three scenarios:
1. Fresh attack (no cache)
2. Cache hit via main CLI
3. Cache hit via lightweight reader

Measures wall-clock time, API costs, and cache hit rates.
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

# Representative test prompts (safe, academic examples)
TEST_PROMPTS = [
    "Tell me about cybersecurity best practices",
    "Explain how to write secure code",
    "What are common vulnerabilities in web applications",
    "How do penetration testers assess system security",
    "Describe ethical hacking methodologies",
]


def run_command(cmd: list[str], timeout: int = 120) -> tuple[float, dict[str, Any] | None, int]:
    """Run shell command and measure time.
    
    Args:
        cmd: Command and arguments
        timeout: Timeout in seconds
        
    Returns:
        Tuple of (wall_time, result_dict, exit_code)
    """
    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = time.time() - start
        
        # Try to parse JSON output
        result_dict = None
        try:
            # Look for JSON in output
            lines = result.stdout.split('\n')
            for line in lines:
                if line.strip().startswith('{'):
                    result_dict = json.loads(line)
                    break
        except (json.JSONDecodeError, ValueError):
            pass
        
        return elapsed, result_dict, result.returncode
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return elapsed, None, -1


def clear_cache():
    """Clear all cache entries."""
    print("Clearing cache...")
    subprocess.run(["aipop", "cache-clear", "--all"], check=False, capture_output=True)


def benchmark_fresh_attack(prompt: str, method: str = "pair") -> dict[str, Any]:
    """Benchmark fresh attack (no cache).
    
    Args:
        prompt: Test prompt
        method: Attack method
        
    Returns:
        Benchmark results
    """
    print(f"  Testing fresh attack (method={method})...")
    
    # Clear cache first
    clear_cache()
    
    # Run attack
    cmd = [
        "aipop", "generate-suffix", prompt,
        "--method", method,
        "--implementation", "legacy",
        "--skip-setup",
        "--adapter", "openai",
        "--adapter-model", "gpt-3.5-turbo",
        "--streams", "1",
        "--iterations", "1",
        "--judge", "keyword",
    ]
    
    wall_time, result, exit_code = run_command(cmd)
    
    # Estimate cost (PAIR with 1 stream, 1 iter ≈ $0.02)
    estimated_cost = 0.02 if method == "pair" else 0.0
    
    return {
        "scenario": "fresh_attack",
        "wall_time": wall_time,
        "exit_code": exit_code,
        "estimated_cost": estimated_cost,
        "success": exit_code == 0,
    }


def benchmark_cached_cli(prompt: str, method: str = "pair") -> dict[str, Any]:
    """Benchmark cache hit via main CLI.
    
    Args:
        prompt: Test prompt (must match fresh run)
        method: Attack method
        
    Returns:
        Benchmark results
    """
    print(f"  Testing cache hit via CLI...")
    
    # Run same command (should hit cache)
    cmd = [
        "aipop", "generate-suffix", prompt,
        "--method", method,
        "--implementation", "legacy",
        "--skip-setup",
        "--adapter", "openai",
        "--adapter-model", "gpt-3.5-turbo",
        "--streams", "1",
        "--iterations", "1",
        "--judge", "keyword",
    ]
    
    wall_time, result, exit_code = run_command(cmd)
    
    return {
        "scenario": "cached_cli",
        "wall_time": wall_time,
        "exit_code": exit_code,
        "estimated_cost": 0.0,  # No API call
        "success": exit_code == 0,
    }


def benchmark_fast_lookup(prompt: str, method: str = "pair") -> dict[str, Any]:
    """Benchmark cache hit via lightweight reader.
    
    Args:
        prompt: Test prompt
        method: Attack method
        
    Returns:
        Benchmark results
    """
    print(f"  Testing cache hit via lightweight reader...")
    
    # Build params JSON
    params = {
        "num_streams": 1,
        "iterations_per_stream": 1,
        "max_iterations": 500,
        "population_size": None,
        "num_generations": None,
        "target": "Sure, I can help",
        "judge_model": None,
        "attacker_model": "gpt-4",
    }
    
    cmd = [
        sys.executable,
        str(Path(__file__).parent.parent / "cli" / "cached_lookup.py"),
        method,
        prompt,
        "gpt-3.5-turbo",
        "legacy",
        json.dumps(params),
    ]
    
    wall_time, result, exit_code = run_command(cmd, timeout=5)
    
    return {
        "scenario": "fast_lookup",
        "wall_time": wall_time,
        "exit_code": exit_code,
        "estimated_cost": 0.0,
        "success": exit_code == 0,
    }


def run_benchmark(num_prompts: int = 3) -> dict[str, Any]:
    """Run full benchmark suite.
    
    Args:
        num_prompts: Number of test prompts to use
        
    Returns:
        Benchmark results
    """
    print("=" * 80)
    print("AI Purple Ops Cache Performance Benchmark")
    print("=" * 80)
    print()
    
    results = []
    
    for i, prompt in enumerate(TEST_PROMPTS[:num_prompts], 1):
        print(f"\nPrompt {i}/{num_prompts}: \"{prompt[:50]}...\"")
        
        # 1. Fresh attack
        fresh = benchmark_fresh_attack(prompt)
        results.append(fresh)
        
        if not fresh["success"]:
            print(f"  ⚠️  Fresh attack failed, skipping cached tests")
            continue
        
        # Small delay to ensure cache write completes
        time.sleep(1)
        
        # 2. Cached CLI
        cached_cli = benchmark_cached_cli(prompt)
        results.append(cached_cli)
        
        # 3. Fast lookup
        fast = benchmark_fast_lookup(prompt)
        results.append(fast)
    
    return analyze_results(results)


def analyze_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyze benchmark results and compute metrics.
    
    Args:
        results: List of benchmark results
        
    Returns:
        Analysis with metrics
    """
    fresh_times = [r["wall_time"] for r in results if r["scenario"] == "fresh_attack" and r["success"]]
    cached_times = [r["wall_time"] for r in results if r["scenario"] == "cached_cli" and r["success"]]
    fast_times = [r["wall_time"] for r in results if r["scenario"] == "fast_lookup" and r["success"]]
    
    total_cost_fresh = sum(r["estimated_cost"] for r in results if r["scenario"] == "fresh_attack")
    total_cost_cached = sum(r["estimated_cost"] for r in results if r["scenario"] != "fresh_attack")
    
    analysis = {
        "fresh_attack": {
            "count": len(fresh_times),
            "avg_time": sum(fresh_times) / len(fresh_times) if fresh_times else 0,
            "min_time": min(fresh_times) if fresh_times else 0,
            "max_time": max(fresh_times) if fresh_times else 0,
            "total_cost": total_cost_fresh,
        },
        "cached_cli": {
            "count": len(cached_times),
            "avg_time": sum(cached_times) / len(cached_times) if cached_times else 0,
            "min_time": min(cached_times) if cached_times else 0,
            "max_time": max(cached_times) if cached_times else 0,
            "total_cost": 0.0,
        },
        "fast_lookup": {
            "count": len(fast_times),
            "avg_time": sum(fast_times) / len(fast_times) if fast_times else 0,
            "min_time": min(fast_times) if fast_times else 0,
            "max_time": max(fast_times) if fast_times else 0,
            "total_cost": 0.0,
        },
    }
    
    # Calculate speedups
    if analysis["fresh_attack"]["avg_time"] > 0:
        analysis["speedup_cached_cli"] = analysis["fresh_attack"]["avg_time"] / analysis["cached_cli"]["avg_time"] if analysis["cached_cli"]["avg_time"] > 0 else 0
        analysis["speedup_fast"] = analysis["fresh_attack"]["avg_time"] / analysis["fast_lookup"]["avg_time"] if analysis["fast_lookup"]["avg_time"] > 0 else 0
    else:
        analysis["speedup_cached_cli"] = 0
        analysis["speedup_fast"] = 0
    
    analysis["cost_saved"] = total_cost_fresh
    analysis["cache_hit_rate"] = len(cached_times) / len(fresh_times) if fresh_times else 0
    
    return analysis


def print_report(analysis: dict[str, Any]):
    """Print formatted benchmark report.
    
    Args:
        analysis: Analysis results
    """
    print("\n" + "=" * 80)
    print("BENCHMARK RESULTS")
    print("=" * 80)
    print()
    
    print("Fresh Attack (no cache):")
    print(f"  Count:     {analysis['fresh_attack']['count']}")
    print(f"  Avg time:  {analysis['fresh_attack']['avg_time']:.2f}s")
    print(f"  Range:     {analysis['fresh_attack']['min_time']:.2f}s - {analysis['fresh_attack']['max_time']:.2f}s")
    print(f"  Cost:      ${analysis['fresh_attack']['total_cost']:.3f}")
    print()
    
    print("Cached CLI:")
    print(f"  Count:     {analysis['cached_cli']['count']}")
    print(f"  Avg time:  {analysis['cached_cli']['avg_time']:.2f}s")
    print(f"  Range:     {analysis['cached_cli']['min_time']:.2f}s - {analysis['cached_cli']['max_time']:.2f}s")
    print(f"  Speedup:   {analysis['speedup_cached_cli']:.2f}x faster")
    print()
    
    print("Fast Lookup:")
    print(f"  Count:     {analysis['fast_lookup']['count']}")
    print(f"  Avg time:  {analysis['fast_lookup']['avg_time']:.2f}s")
    print(f"  Range:     {analysis['fast_lookup']['min_time']:.2f}s - {analysis['fast_lookup']['max_time']:.2f}s")
    print(f"  Speedup:   {analysis['speedup_fast']:.2f}x faster")
    print()
    
    print("Summary:")
    print(f"  Cache hit rate:  {analysis['cache_hit_rate'] * 100:.0f}%")
    print(f"  Cost saved:      ${analysis['cost_saved']:.3f}")
    print(f"  Time saved/call: {analysis['fresh_attack']['avg_time'] - analysis['cached_cli']['avg_time']:.2f}s")
    print()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Benchmark cache performance")
    parser.add_argument("--prompts", type=int, default=3, help="Number of test prompts (default: 3)")
    parser.add_argument("--output", type=Path, help="Save results to JSON file")
    
    args = parser.parse_args()
    
    # Run benchmark
    analysis = run_benchmark(args.prompts)
    
    # Print report
    print_report(analysis)
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()

