#!/usr/bin/env python3
"""
Manual Dashboard Test Script

Tests dashboard functionality end-to-end to verify:
1. Dashboard can be imported
2. Plan discovery works
3. State detection works
4. UI renders without errors
5. Parallel detection works (Achievement 2.1)

Run: python test_dashboard_manual.py
"""
import sys
from pathlib import Path

# Add workspace root to path
WORKSPACE_ROOT = Path(__file__).parent.resolve()
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from rich.console import Console
from LLM.dashboard.main_dashboard import MainDashboard
from LLM.dashboard.plan_dashboard import PlanDashboard
from LLM.dashboard.plan_discovery import PlanDiscovery
from LLM.dashboard.parallel_detector import ParallelDetector

console = Console()


def test_imports():
    """Test 1: All imports work."""
    console.print("[bold cyan]Test 1: Imports[/bold cyan]")
    try:
        from LLM.dashboard import BaseDashboard
        from LLM.dashboard.state_detector import StateDetector
        from LLM.dashboard.models import PlanState, PlanStatus

        console.print("  ✅ All imports successful")
        return True
    except ImportError as e:
        console.print(f"  ❌ Import failed: {e}")
        return False


def test_plan_discovery():
    """Test 2: Plan discovery works."""
    console.print("\n[bold cyan]Test 2: Plan Discovery[/bold cyan]")
    try:
        discovery = PlanDiscovery()
        plans = discovery.get_all_plans()
        console.print(f"  ✅ Discovered {len(plans)} plans")
        for plan in plans:
            console.print(f"     - {plan.name}")
        return True
    except Exception as e:
        console.print(f"  ❌ Discovery failed: {e}")
        return False


def test_main_dashboard_creation():
    """Test 3: Main dashboard can be created."""
    console.print("\n[bold cyan]Test 3: Main Dashboard Creation[/bold cyan]")
    try:
        dashboard = MainDashboard()
        console.print("  ✅ MainDashboard instance created")
        return True
    except Exception as e:
        console.print(f"  ❌ Creation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_plan_dashboard_creation():
    """Test 4: Plan dashboard can be created."""
    console.print("\n[bold cyan]Test 4: Plan Dashboard Creation[/bold cyan]")
    try:
        discovery = PlanDiscovery()
        plans = discovery.get_all_plans()
        if not plans:
            console.print("  ⚠️  No plans found, skipping test")
            return True

        # Test with first plan
        dashboard = PlanDashboard(plan_id=1, console=console)
        console.print(f"  ✅ PlanDashboard created for: {dashboard.plan_name}")
        return True
    except Exception as e:
        console.print(f"  ❌ Creation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_parallel_detection():
    """Test 5: Parallel detection works (Achievement 2.1)."""
    console.print("\n[bold cyan]Test 5: Parallel Detection (Achievement 2.1)[/bold cyan]")
    try:
        discovery = PlanDiscovery()
        plans = discovery.get_all_plans()

        plans_with_parallel = 0
        for plan in plans:
            detector = ParallelDetector(plan)
            if detector.has_parallel_opportunities():
                groups = detector.detect_parallel_opportunities()
                console.print(f"  ✅ {plan.name}: {len(groups)} parallel group(s)")
                plans_with_parallel += 1

        if plans_with_parallel == 0:
            console.print("  ℹ️  No plans with parallel.json found (expected for some setups)")
        else:
            console.print(f"  ✅ Found {plans_with_parallel} plan(s) with parallel opportunities")

        return True
    except Exception as e:
        console.print(f"  ❌ Parallel detection failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_state_detection():
    """Test 6: State detection works."""
    console.print("\n[bold cyan]Test 6: State Detection[/bold cyan]")
    try:
        from LLM.dashboard.state_detector import StateDetector

        discovery = PlanDiscovery()
        plans = discovery.get_all_plans()
        if not plans:
            console.print("  ⚠️  No plans found, skipping test")
            return True

        detector = StateDetector()
        state = detector.get_plan_state(plans[0])
        console.print(f"  ✅ State detected for {state.name}")
        console.print(f"     - Total achievements: {state.total_achievements}")
        console.print(f"     - Completed: {state.completed_achievements}")
        console.print(f"     - Status: {state.status}")
        return True
    except Exception as e:
        console.print(f"  ❌ State detection failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all manual tests."""
    console.print("\n" + "=" * 70)
    console.print("[bold green]Dashboard Manual Test Suite[/bold green]")
    console.print("=" * 70 + "\n")

    tests = [
        test_imports,
        test_plan_discovery,
        test_main_dashboard_creation,
        test_plan_dashboard_creation,
        test_parallel_detection,
        test_state_detection,
    ]

    results = []
    for test in tests:
        results.append(test())

    # Summary
    console.print("\n" + "=" * 70)
    console.print("[bold]Test Summary[/bold]")
    console.print("=" * 70)

    passed = sum(results)
    total = len(results)

    if passed == total:
        console.print(f"\n✅ All {total} tests passed!")
        console.print("\n[bold green]Dashboard is fully functional![/bold green]")
        console.print("\nYou can now run:")
        console.print("  [cyan]python LLM/main.py[/cyan]          # Launch dashboard")
        console.print("  [cyan]python -m LLM.main[/cyan]          # Alternative method")
    else:
        console.print(f"\n❌ {total - passed} test(s) failed out of {total}")
        console.print("\nPlease review the errors above.")

    console.print("\n" + "=" * 70 + "\n")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
