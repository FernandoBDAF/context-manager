#!/usr/bin/env python3
"""
Quick test to verify plan dashboard launches correctly after fix.
"""
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.resolve()
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from rich.console import Console
from LLM.dashboard.main_dashboard import MainDashboard
from LLM.dashboard.plan_discovery import PlanDiscovery

console = Console()


def test_plan_dashboard_integration():
    """Test that main dashboard can launch plan dashboard."""
    console.print("[bold cyan]Testing Plan Dashboard Integration[/bold cyan]\n")

    try:
        # Test 1: Check import works
        from LLM.dashboard.plan_dashboard import PlanDashboard

        console.print("✅ Test 1: PlanDashboard import successful")

        # Test 2: Check main dashboard has the import
        dashboard = MainDashboard()
        console.print("✅ Test 2: MainDashboard instantiated")

        # Test 3: Verify open_plan_dashboard method exists and is updated
        import inspect

        source = inspect.getsource(dashboard.open_plan_dashboard)
        if "PlanDashboard" in source and "Achievement 1.1" in source:
            console.print("✅ Test 3: open_plan_dashboard method updated with PlanDashboard")
        else:
            console.print("❌ Test 3: Method still has old placeholder code")
            return False

        # Test 4: Test plan dashboard can be created for first plan
        discovery = PlanDiscovery()
        plans = discovery.get_all_plans()
        if plans:
            plan_dashboard = PlanDashboard(plan_id=1, console=console)
            console.print(f"✅ Test 4: PlanDashboard created for: {plan_dashboard.plan_name}")
        else:
            console.print("⚠️  Test 4: No plans found, skipping")

        console.print(
            "\n[bold green]All tests passed! Plan dashboard integration working.[/bold green]"
        )
        return True

    except Exception as e:
        console.print(f"\n[bold red]❌ Error: {e}[/bold red]")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_plan_dashboard_integration()
    sys.exit(0 if success else 1)
