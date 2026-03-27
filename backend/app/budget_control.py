"""
Budget Control System
Prevents overspending on Azure resources
"""

from datetime import datetime
from typing import List, Dict, Any, Tuple
import logging
from app.config import settings
from app.models import Operation, BudgetStatus

logger = logging.getLogger(__name__)


class BudgetController:
    """
    Controls budget to ensure costs stay within limits

    Key Responsibilities:
    1. Track current spending
    2. Estimate costs before operations
    3. Approve/deny operations based on budget
    4. Log all operations
    """

    # Azure VM pricing (Southeast Asia region, per hour in USD)
    # Source: https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/
    VM_HOURLY_RATES = {
        "B1s": 0.0104,  # 1 vCPU, 1 GB RAM - Cheapest option
        "B1ms": 0.0207,  # 1 vCPU, 2 GB RAM
        "B2s": 0.0416,  # 2 vCPU, 4 GB RAM
    }

    def __init__(self):
        """Initialize budget controller"""
        self.monthly_limit = settings.MONTHLY_BUDGET_LIMIT
        self.current_spend = 0.0
        self.operations: List[Operation] = []

        logger.info(
            f"Budget Controller initialized with ${self.monthly_limit:.2f} monthly limit"
        )

    def estimate_vm_cost(
        self,
        vm_size: str,
        hours: int = 730  # Average hours per month
    ) -> Dict[str, float]:
        """
        Estimate VM cost

        Args:
            vm_size: Azure VM size (e.g., "B1s")
            hours: Number of hours to estimate (default: 1 month = 730 hours)

        Returns:
            Dict with hourly, daily, and monthly cost estimates
        """
        hourly_rate = self.VM_HOURLY_RATES.get(vm_size, 0.0)

        if hourly_rate == 0.0:
            logger.warning(f"Unknown VM size: {vm_size}, cannot estimate cost")

        return {
            "hourly": round(hourly_rate, 4),
            "daily": round(hourly_rate * 24, 2),
            "monthly": round(hourly_rate * 730, 2),
            "custom_hours": round(hourly_rate * hours, 2)
        }

    def check_and_approve(
        self,
        operation: str,
        estimated_cost: float,
        parameters: Dict[str, Any] = None
    ) -> Tuple[bool, str]:
        """
        Check if operation is within budget and approve/deny

        Args:
            operation: Name of operation (e.g., "create_vm")
            estimated_cost: Estimated cost in USD
            parameters: Operation parameters for logging

        Returns:
            Tuple of (approved: bool, reason: str)
        """
        projected_total = self.current_spend + estimated_cost

        # Check if within budget
        if projected_total > self.monthly_limit:
            reason = (
                f"Budget exceeded: ${projected_total:.2f} > ${self.monthly_limit:.2f}. "
                f"Operation would cost ${estimated_cost:.2f}, "
                f"but only ${self.remaining:.2f} remaining."
            )
            logger.warning(f"❌ Operation denied: {reason}")

            # Log denied operation
            self._log_operation(
                operation=operation,
                estimated_cost=estimated_cost,
                parameters=parameters or {},
                result="denied",
                mode="budget_check"
            )

            return False, reason

        # Operation approved
        reason = (
            f"Approved: ${projected_total:.2f} / ${self.monthly_limit:.2f} "
            f"({self.percentage_used:.1f}% used)"
        )
        logger.info(f"✅ Operation approved: {operation} - {reason}")

        return True, reason

    def record_operation(
        self,
        operation: str,
        estimated_cost: float,
        actual_cost: float = None,
        parameters: Dict[str, Any] = None,
        result: str = "success",
        mode: str = "mock"
    ) -> None:
        """
        Record an operation and update spending

        Args:
            operation: Operation name
            estimated_cost: Estimated cost
            actual_cost: Actual cost (if known)
            parameters: Operation parameters
            result: Operation result
            mode: Execution mode (mock/azure)
        """
        cost_to_record = actual_cost if actual_cost is not None else estimated_cost

        # Update current spend (only for real Azure operations)
        if mode == "azure":
            self.current_spend += cost_to_record
            logger.info(f"💰 Spend updated: +${cost_to_record:.2f} = ${self.current_spend:.2f}")

        # Log operation
        self._log_operation(
            operation=operation,
            estimated_cost=estimated_cost,
            actual_cost=cost_to_record,
            parameters=parameters or {},
            result=result,
            mode=mode
        )

    def _log_operation(
        self,
        operation: str,
        estimated_cost: float,
        parameters: Dict[str, Any],
        result: str,
        mode: str,
        actual_cost: float = 0.0
    ) -> None:
        """Internal: Log operation to history"""
        op = Operation(
            operation=operation,
            timestamp=datetime.now(),
            estimated_cost=estimated_cost,
            actual_cost=actual_cost,
            mode=mode,
            parameters=parameters,
            result=result
        )
        self.operations.append(op)

        logger.debug(f"📝 Logged operation: {op.operation} ({op.mode})")

    @property
    def remaining(self) -> float:
        """Calculate remaining budget"""
        return max(0.0, self.monthly_limit - self.current_spend)

    @property
    def percentage_used(self) -> float:
        """Calculate percentage of budget used"""
        if self.monthly_limit == 0:
            return 0.0
        return (self.current_spend / self.monthly_limit) * 100

    def get_status(self) -> BudgetStatus:
        """
        Get current budget status

        Returns:
            BudgetStatus model with current information
        """
        return BudgetStatus(
            limit=self.monthly_limit,
            current_spend=round(self.current_spend, 2),
            remaining=round(self.remaining, 2),
            percentage_used=round(self.percentage_used, 2),
            operations_count=len(self.operations),
            last_updated=datetime.now().isoformat()
        )

    def get_operations_history(
        self,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent operations history

        Args:
            limit: Number of recent operations to return

        Returns:
            List of operation dictionaries
        """
        recent_ops = self.operations[-limit:]
        return [
            {
                "operation": op.operation,
                "timestamp": op.timestamp.isoformat(),
                "estimated_cost": op.estimated_cost,
                "actual_cost": op.actual_cost,
                "mode": op.mode,
                "result": op.result,
                "parameters": op.parameters
            }
            for op in reversed(recent_ops)
        ]

    def reset_monthly(self) -> None:
        """
        Reset monthly budget (call at start of new month)

        WARNING: Only call this manually for testing
        Production should automate this
        """
        logger.info(f"🔄 Resetting monthly budget. Previous spend: ${self.current_spend:.2f}")
        self.current_spend = 0.0
        # Keep operation history for auditing

    def get_summary(self) -> str:
        """Get human-readable budget summary"""
        status = self.get_status()
        return f"""
💰 Budget Summary:
├─ Limit: ${status.limit:.2f}/month
├─ Used: ${status.current_spend:.2f} ({status.percentage_used:.1f}%)
├─ Remaining: ${status.remaining:.2f}
└─ Operations: {status.operations_count}
"""


# Global budget controller instance
budget_controller = BudgetController()


def get_budget_controller() -> BudgetController:
    """Get the global budget controller instance"""
    return budget_controller


# Example usage
if __name__ == "__main__":
    # Test budget controller
    bc = BudgetController()

    # Estimate VM cost
    cost = bc.estimate_vm_cost("B1s")
    print(f"B1s VM Cost: {cost}")

    # Check if we can create a VM
    approved, reason = bc.check_and_approve(
        operation="create_vm",
        estimated_cost=cost["monthly"],
        parameters={"size": "B1s", "name": "test-vm"}
    )
    print(f"Approved: {approved}, Reason: {reason}")

    # Record operation
    if approved:
        bc.record_operation(
            operation="create_vm",
            estimated_cost=cost["monthly"],
            parameters={"size": "B1s"},
            mode="mock"
        )

    # Get status
    print(bc.get_summary())
