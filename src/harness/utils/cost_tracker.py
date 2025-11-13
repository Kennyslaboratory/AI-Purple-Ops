"""Cost tracking utility for per-operation cost monitoring."""

from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class CostOperation:
    """Represents a single cost operation."""

    operation: str
    tokens: int
    model: str
    cost: float
    timestamp: datetime = field(default_factory=datetime.now)


class CostTracker:
    """Track token usage and cost per operation.

    Provides per-operation cost visibility and budget warnings.
    """

    def __init__(self):
        """Initialize cost tracker."""
        self.operations: list[CostOperation] = []

    def track(
        self,
        operation: str,
        tokens: int,
        model: str,
        cost: float,
    ) -> None:
        """Track a cost operation.

        Args:
            operation: Operation name (e.g., "generate-suffix", "verify-suite", "run")
            tokens: Token count (prompt + completion)
            model: Model identifier
            cost: Cost in USD
        """
        self.operations.append(
            CostOperation(
                operation=operation,
                tokens=tokens,
                model=model,
                cost=cost,
            )
        )

    def get_summary(self) -> dict[str, Any]:
        """Get cost summary statistics.

        Returns:
            Dictionary with total cost, operation breakdown, and model breakdown
        """
        if not self.operations:
            return {
                "total_cost": 0.0,
                "total_tokens": 0,
                "operation_breakdown": {},
                "model_breakdown": {},
                "operation_count": 0,
            }

        total_cost = sum(op.cost for op in self.operations)
        total_tokens = sum(op.tokens for op in self.operations)

        # Breakdown by operation
        operation_breakdown: dict[str, dict[str, Any]] = defaultdict(
            lambda: {"cost": 0.0, "tokens": 0, "count": 0}
        )
        for op in self.operations:
            operation_breakdown[op.operation]["cost"] += op.cost
            operation_breakdown[op.operation]["tokens"] += op.tokens
            operation_breakdown[op.operation]["count"] += 1

        # Breakdown by model
        model_breakdown: dict[str, dict[str, Any]] = defaultdict(
            lambda: {"cost": 0.0, "tokens": 0, "count": 0}
        )
        for op in self.operations:
            model_breakdown[op.model]["cost"] += op.cost
            model_breakdown[op.model]["tokens"] += op.tokens
            model_breakdown[op.model]["count"] += 1

        return {
            "total_cost": total_cost,
            "total_tokens": total_tokens,
            "operation_breakdown": dict(operation_breakdown),
            "model_breakdown": dict(model_breakdown),
            "operation_count": len(self.operations),
        }

    def warn_if_over_budget(self, budget: float) -> bool:
        """Warn if total cost exceeds budget.

        Args:
            budget: Budget limit in USD

        Returns:
            True if over budget, False otherwise
        """
        summary = self.get_summary()
        total_cost = summary["total_cost"]

        if total_cost > budget:
            logger.warning(
                f"⚠️  Over budget: ${total_cost:.2f} / ${budget:.2f} "
                f"({total_cost / budget * 100:.1f}%)"
            )
            return True
        return False

    def reset(self) -> None:
        """Reset all tracked operations."""
        self.operations.clear()

    def get_operation_cost(self, operation: str) -> float:
        """Get total cost for a specific operation.

        Args:
            operation: Operation name

        Returns:
            Total cost for the operation
        """
        return sum(op.cost for op in self.operations if op.operation == operation)

    def get_model_cost(self, model: str) -> float:
        """Get total cost for a specific model.

        Args:
            model: Model identifier

        Returns:
            Total cost for the model
        """
        return sum(op.cost for op in self.operations if op.model == model)

    def estimate_autodan_cost(
        self,
        population_size: int,
        num_generations: int,
        model: str,
        mutator_model: str | None = None,
    ) -> dict[str, Any]:
        """Estimate AutoDAN cost before running.

        Args:
            population_size: Population size (N)
            num_generations: Number of generations (G)
            model: Target model identifier
            mutator_model: Mutator model identifier (if different from target)

        Returns:
            Dictionary with cost estimates and warnings
        """
        # Estimate queries: population_size * num_generations (fitness evaluation)
        # Plus mutation queries: population_size * num_generations * mutation_rate
        fitness_queries = population_size * num_generations
        mutation_queries = int(population_size * num_generations * 0.01)  # 1% mutation rate
        total_queries = fitness_queries + mutation_queries

        # Get cost per query (simplified - assumes average tokens)
        cost_per_query = self._get_model_cost_per_query(model)
        mutator_cost_per_query = (
            self._get_model_cost_per_query(mutator_model) if mutator_model else cost_per_query
        )

        fitness_cost = fitness_queries * cost_per_query
        mutation_cost = mutation_queries * mutator_cost_per_query
        total_cost = fitness_cost + mutation_cost

        return {
            "estimated_queries": total_queries,
            "fitness_queries": fitness_queries,
            "mutation_queries": mutation_queries,
            "estimated_cost_usd": total_cost,
            "fitness_cost": fitness_cost,
            "mutation_cost": mutation_cost,
            "warning": total_cost > 10.0,  # Warn if >$10
            "model": model,
            "mutator_model": mutator_model or model,
        }

    def estimate_pair_cost(
        self,
        num_streams: int,
        iterations_per_stream: int,
        attacker_model: str,
        target_model: str,
    ) -> dict[str, Any]:
        """Estimate PAIR cost before running.

        Args:
            num_streams: Number of parallel streams (N)
            iterations_per_stream: Iterations per stream (K)
            attacker_model: Attacker LLM identifier
            target_model: Target model identifier

        Returns:
            Dictionary with cost estimates and warnings
        """
        # PAIR uses N * K queries (attacker + target per iteration)
        queries_per_stream = iterations_per_stream * 2  # Attacker + target
        total_queries = num_streams * queries_per_stream

        attacker_cost_per_query = self._get_model_cost_per_query(attacker_model)
        target_cost_per_query = self._get_model_cost_per_query(target_model)

        attacker_queries = num_streams * iterations_per_stream
        target_queries = num_streams * iterations_per_stream

        attacker_cost = attacker_queries * attacker_cost_per_query
        target_cost = target_queries * target_cost_per_query
        total_cost = attacker_cost + target_cost

        return {
            "estimated_queries": total_queries,
            "attacker_queries": attacker_queries,
            "target_queries": target_queries,
            "estimated_cost_usd": total_cost,
            "attacker_cost": attacker_cost,
            "target_cost": target_cost,
            "warning": total_cost > 5.0,  # Warn if >$5 (PAIR is cheaper)
            "attacker_model": attacker_model,
            "target_model": target_model,
        }

    def _get_model_cost_per_query(self, model: str) -> float:
        """Get estimated cost per query for a model.

        Args:
            model: Model identifier

        Returns:
            Estimated cost per query in USD
        """
        # Simplified cost estimation (can be enhanced with actual pricing)
        # Assumes average 100 tokens input + 200 tokens output
        pricing = {
            "gpt-4": 0.03 / 1000 * 100 + 0.06 / 1000 * 200,  # $0.03/1k input, $0.06/1k output
            "gpt-4o-mini": 0.15 / 1000 * 100 + 0.60 / 1000 * 200,
            "gpt-3.5-turbo": 0.50 / 1000 * 100 + 1.50 / 1000 * 200,
            "claude-3-5-sonnet-20241022": 3.00 / 1000 * 100 + 15.00 / 1000 * 200,
            "claude-3-5-haiku-20241022": 0.80 / 1000 * 100 + 4.00 / 1000 * 200,
        }

        return pricing.get(model.lower(), 0.01)  # Default $0.01 per query

