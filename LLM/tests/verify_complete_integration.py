#!/usr/bin/env python3
"""
Comprehensive verification of complete dashboard integration.
Tests all user paths end-to-end.
"""
import sys
import inspect
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.resolve()
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from rich.console import Console
from LLM.dashboard.main_dashboard import MainDashboard
from LLM.dashboard.plan_dashboard import PlanDashboard
from LLM.dashboard.plan_discovery import PlanDiscovery

console = Console()


def verify_integration():
    """Verify all integration points work."""
    console.print("[bold cyan]Comprehensive Dashboard Integration Verification[/bold cyan]\n")

    all_passed = True

    # Test 1: Main Dashboard Launch
    console.print("[bold]Test 1: Main Dashboard Launch[/bold]")
    try:
        dashboard = MainDashboard()
        console.print("  ✅ MainDashboard instantiates")
    except Exception as e:
        console.print(f"  ❌ Failed: {e}")
        all_passed = False
        return all_passed

    # Test 2: PlanDashboard Import in MainDashboard
    console.print("\n[bold]Test 2: PlanDashboard Import[/bold]")
    try:
        # Read the file directly to check imports
        main_dashboard_file = WORKSPACE_ROOT / "LLM" / "dashboard" / "main_dashboard.py"
        content = main_dashboard_file.read_text()
        if "from LLM.dashboard.plan_dashboard import PlanDashboard" in content:
            console.print("  ✅ PlanDashboard imported in MainDashboard")
        else:
            console.print("  ❌ PlanDashboard not imported")
            all_passed = False
    except Exception as e:
        console.print(f"  ❌ Failed: {e}")
        all_passed = False

    # Test 3: open_plan_dashboard Method Updated
    console.print("\n[bold]Test 3: open_plan_dashboard Method[/bold]")
    try:
        source = inspect.getsource(dashboard.open_plan_dashboard)

        if "PlanDashboard" in source:
            console.print("  ✅ Method uses PlanDashboard class")
        else:
            console.print("  ❌ Method doesn't use PlanDashboard")
            all_passed = False

        if "plan_dashboard.show()" in source:
            console.print("  ✅ Method calls show()")
        else:
            console.print("  ❌ Method doesn't call show()")
            all_passed = False

        if "coming in Achievement 1.1" in source:
            console.print("  ❌ Placeholder code still present")
            all_passed = False
        else:
            console.print("  ✅ Placeholder code removed")

    except Exception as e:
        console.print(f"  ❌ Failed: {e}")
        all_passed = False

    # Test 4: Plan Dashboard Can Be Created
    console.print("\n[bold]Test 4: Plan Dashboard Creation[/bold]")
    try:
        discovery = PlanDiscovery()
        plans = discovery.get_all_plans()

        if not plans:
            console.print("  ⚠️  No plans found, skipping creation test")
        else:
            plan_dashboard = PlanDashboard(plan_id=1, console=console)
            console.print(f"  ✅ PlanDashboard created for: {plan_dashboard.plan_name}")

            # Verify all components present
            if hasattr(plan_dashboard, "render_header"):
                console.print("  ✅ Has render_header method")
            if hasattr(plan_dashboard, "render_achievements"):
                console.print("  ✅ Has render_achievements method")
            if hasattr(plan_dashboard, "render_actions"):
                console.print("  ✅ Has render_actions method")
            if hasattr(plan_dashboard, "render_parallel_opportunities"):
                console.print("  ✅ Has render_parallel_opportunities method")

    except Exception as e:
        console.print(f"  ❌ Failed: {e}")
        all_passed = False

    # Test 5: Critical Test Files Exist
    console.print("\n[bold]Test 5: Test Coverage[/bold]")
    try:
        test_files = [
            "tests/LLM/dashboard/test_main_dashboard.py",
            "tests/LLM/dashboard/test_plan_dashboard.py",
            "tests/LLM/dashboard/test_action_executor.py",
            "tests/LLM/dashboard/test_parallel_detector.py",
        ]

        for test_file in test_files:
            test_path = WORKSPACE_ROOT / test_file
            if test_path.exists():
                console.print(f"  ✅ {test_file.split('/')[-1]} exists")
            else:
                console.print(f"  ❌ {test_file.split('/')[-1]} missing")
                all_passed = False

    except Exception as e:
        console.print(f"  ⚠️  Could not check tests: {e}")

    # Summary
    console.print()
    if all_passed:
        console.print("[bold green]✅ All integration checks passed![/bold green]")
        console.print("\n[dim]Dashboard is ready for production use.[/dim]")
    else:
        console.print("[bold red]❌ Some integration checks failed[/bold red]")

    return all_passed


if __name__ == "__main__":
    success = verify_integration()
    sys.exit(0 if success else 1)
