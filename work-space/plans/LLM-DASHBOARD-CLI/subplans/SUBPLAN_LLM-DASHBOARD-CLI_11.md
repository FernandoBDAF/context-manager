# SUBPLAN: Achievement 1.1 - Plan-Specific Dashboard

**PLAN**: LLM-DASHBOARD-CLI  
**Achievement**: 1.1  
**Estimated Time**: 3-4 hours  
**Created**: 2025-11-14  
**Status**: 📋 Design Phase

---

## 🎯 Objective

Implement a plan-specific dashboard that shows detailed information for a single plan, including status, quick stats, and available actions. This dashboard provides the second level of navigation after the main dashboard, allowing users to dive deep into a specific plan's state and perform plan-specific actions.

**Core Purpose**: Create an interactive, detailed view of a single plan that shows progress, statistics, and actionable next steps, replacing the need to manually check multiple files and directories to understand plan state.

**Success Definition**:
- Users can navigate to a plan-specific dashboard from the main dashboard
- Dashboard shows comprehensive plan status (progress, last achievement, priority, remaining time)
- Dashboard shows quick stats (SUBPLANs, EXECUTIONs, reviews, tests)
- Users can navigate back to main dashboard
- All information is derived from filesystem state (no manual tracking)
- Dashboard is interactive and responsive

---

## 📦 Deliverables

### 1. Plan Dashboard Class

**File**: `LLM/dashboard/plan_dashboard.py` (~350 lines, NEW)

**Purpose**: Main class for plan-specific dashboard with status, stats, and navigation

**Key Components**:

```python
class PlanDashboard(BaseDashboard):
    """
    Plan-specific dashboard showing detailed information for a single plan.
    
    Shows:
    - Plan header (name, description)
    - Status section (progress, last achievement, priority, remaining time)
    - Quick stats (SUBPLANs, EXECUTIONs, reviews, tests)
    - Navigation (back to main dashboard)
    
    Example:
        >>> dashboard = PlanDashboard(plan_id=1, console=console)
        >>> dashboard.show()  # Interactive loop
    """
    
    def __init__(self, plan_id: Union[int, str], console: Console):
        """
        Initialize plan dashboard.
        
        Args:
            plan_id: Plan number (e.g., 1) or plan name (e.g., "@LLM-DASHBOARD-CLI")
            console: Rich Console instance
        """
        super().__init__(console)
        self.plan_path = self._resolve_plan(plan_id)
        self.state = StateDetector().get_plan_state(self.plan_path)
        self.plan_name = self.plan_path.name
    
    def show(self):
        """
        Show plan dashboard in interactive loop.
        
        Loop:
        1. Clear screen
        2. Render all sections
        3. Get user input
        4. Handle action or exit
        """
        while True:
            self.clear()
            self.render_header()
            self.render_status()
            self.render_stats()
            self.console.print()  # Spacing
            self.console.print("[dim]Press 'b' to go back to main dashboard[/dim]")
            
            choice = self.get_user_input("\nEnter action: ")
            if choice.lower() in ['b', 'back', '6']:
                break
    
    def _resolve_plan(self, plan_id: Union[int, str]) -> Path:
        """
        Resolve plan ID to plan directory path.
        
        Args:
            plan_id: Either:
                - Integer (1, 2, 3) - plan number from main dashboard
                - String with @ ("@LLM-DASHBOARD-CLI") - plan name
                - String without @ ("LLM-DASHBOARD-CLI") - plan name
        
        Returns:
            Path to plan directory
        
        Raises:
            ValueError: If plan not found
        
        Example:
            >>> self._resolve_plan(1)
            Path('work-space/plans/LLM-DASHBOARD-CLI')
            >>> self._resolve_plan("@LLM-DASHBOARD-CLI")
            Path('work-space/plans/LLM-DASHBOARD-CLI')
        """
        discovery = PlanDiscovery()
        plans = discovery.get_all_plans()
        
        # Handle integer (plan number from list)
        if isinstance(plan_id, int):
            if 1 <= plan_id <= len(plans):
                return plans[plan_id - 1]
            raise ValueError(f"Plan number {plan_id} out of range (1-{len(plans)})")
        
        # Handle string (plan name)
        plan_name = plan_id.lstrip('@').strip()
        
        # Find matching plan directory
        for plan_path in plans:
            if plan_path.name == plan_name:
                return plan_path
        
        raise ValueError(f"Plan not found: {plan_name}")
```

### 2. Status Section Rendering

**Function**: `render_status()` in `plan_dashboard.py`

**Purpose**: Display plan status with progress, last achievement, priority, and remaining time

**Implementation**:

```python
def render_status(self):
    """
    Render plan status section.
    
    Shows:
    - Progress (X/Y achievements, percentage)
    - Last completed achievement (with APPROVED file reference)
    - Current priority level
    - Estimated remaining hours
    
    Format:
        📊 Plan Status
        ├─ Progress: 11/18 achievements (61%)
        ├─ Last Complete: 3.1 (✅ APPROVED_31.md)
        ├─ Priority: 3 (Polish - Production Ready)
        └─ Estimated Remaining: 6-10 hours
    """
    content = Text()
    content.append("📊 Plan Status\n", style="bold cyan")
    
    # Progress
    progress_pct = (self.state.completed_achievements / self.state.total_achievements * 100) if self.state.total_achievements > 0 else 0
    content.append(f"├─ Progress: {self.state.completed_achievements}/{self.state.total_achievements} achievements ({progress_pct:.0f}%)\n")
    
    # Last complete achievement
    if self.state.last_achievement:
        content.append(f"├─ Last Complete: {self.state.last_achievement} (✅ APPROVED_{self.state.last_achievement.replace('.', '')}.md)\n")
    else:
        content.append("├─ Last Complete: None (new plan)\n")
    
    # Current priority
    priority_desc = self._get_priority_description(self.state.current_priority)
    content.append(f"├─ Priority: {self.state.current_priority} ({priority_desc})\n")
    
    # Estimated remaining time
    remaining_hours = self._estimate_remaining_hours()
    content.append(f"└─ Estimated Remaining: {remaining_hours} hours\n")
    
    panel = Panel(content, border_style="cyan", padding=(1, 2))
    self.console.print(panel)

def _get_priority_description(self, priority: int) -> str:
    """Get human-readable priority description."""
    descriptions = {
        0: "Foundation - Core Infrastructure",
        1: "Plan Dashboard - Core UX",
        2: "Advanced Features - Power User",
        3: "Polish - Production Ready"
    }
    return descriptions.get(priority, f"Priority {priority}")

def _estimate_remaining_hours(self) -> str:
    """
    Estimate remaining hours based on pending achievements.
    
    Logic:
    - Get all achievements from PLAN Achievement Index
    - Count achievements without APPROVED files
    - Multiply by average effort (assume 3-4 hours per achievement)
    - Return range (e.g., "6-10 hours")
    """
    pending = self.state.total_achievements - self.state.completed_achievements
    min_hours = pending * 3
    max_hours = pending * 4
    
    if pending == 0:
        return "0 (complete!)"
    elif pending == 1:
        return f"{min_hours}-{max_hours}"
    else:
        return f"{min_hours}-{max_hours}"
```

### 3. Quick Stats Section Rendering

**Function**: `render_stats()` in `plan_dashboard.py`

**Purpose**: Display quick statistics about plan artifacts (SUBPLANs, EXECUTIONs, reviews, tests)

**Implementation**:

```python
def render_stats(self):
    """
    Render quick stats section.
    
    Shows:
    - SUBPLANs: Created vs waiting
    - EXECUTIONs: Complete vs active
    - Reviews: Approved vs pending fixes
    - Tests: Passing/total (percentage)
    
    Format:
        ⚡ Quick Stats
        ├─ SUBPLANs: 11 created, 0 waiting
        ├─ EXECUTIONs: 11 complete, 0 active
        ├─ Reviews: 11 approved, 0 fixes pending
        └─ Tests: 346/375 passing (92.3%)
    """
    stats = self._calculate_stats()
    
    content = Text()
    content.append("⚡ Quick Stats\n", style="bold yellow")
    
    # SUBPLANs
    content.append(f"├─ SUBPLANs: {stats['subplans_created']} created, {stats['subplans_waiting']} waiting\n")
    
    # EXECUTIONs
    content.append(f"├─ EXECUTIONs: {stats['executions_complete']} complete, {stats['executions_active']} active\n")
    
    # Reviews
    content.append(f"├─ Reviews: {stats['reviews_approved']} approved, {stats['reviews_pending']} fixes pending\n")
    
    # Tests
    test_pct = (stats['tests_passing'] / stats['tests_total'] * 100) if stats['tests_total'] > 0 else 0
    content.append(f"└─ Tests: {stats['tests_passing']}/{stats['tests_total']} passing ({test_pct:.1f}%)\n")
    
    panel = Panel(content, border_style="yellow", padding=(1, 2))
    self.console.print(panel)

def _calculate_stats(self) -> Dict[str, int]:
    """
    Calculate statistics from filesystem state.
    
    Returns:
        Dictionary with:
        - subplans_created: Count of SUBPLAN_*.md files in subplans/
        - subplans_waiting: Count of achievements without SUBPLANs
        - executions_complete: Count of EXECUTION_TASK_*_01.md files with APPROVED
        - executions_active: Count of EXECUTION_TASK_*_01.md files without APPROVED
        - reviews_approved: Count of APPROVED_*.md files
        - reviews_pending: Count of FIX_*.md files
        - tests_passing: From pytest (or 0 if not available)
        - tests_total: From pytest (or 0 if not available)
    """
    stats = {
        'subplans_created': 0,
        'subplans_waiting': 0,
        'executions_complete': 0,
        'executions_active': 0,
        'reviews_approved': 0,
        'reviews_pending': 0,
        'tests_passing': 0,
        'tests_total': 0
    }
    
    # Count SUBPLANs
    subplans_dir = self.plan_path / 'subplans'
    if subplans_dir.exists():
        stats['subplans_created'] = len(list(subplans_dir.glob('SUBPLAN_*.md')))
    
    # Count achievements waiting for SUBPLANs
    total_achievements = self.state.total_achievements
    stats['subplans_waiting'] = max(0, total_achievements - stats['subplans_created'])
    
    # Count APPROVED reviews
    feedbacks_dir = self.plan_path / 'execution' / 'feedbacks'
    if feedbacks_dir.exists():
        stats['reviews_approved'] = len(list(feedbacks_dir.glob('APPROVED_*.md')))
        stats['reviews_pending'] = len(list(feedbacks_dir.glob('FIX_*.md')))
    
    # Count EXECUTIONs
    execution_dir = self.plan_path / 'execution'
    if execution_dir.exists():
        execution_files = list(execution_dir.glob('EXECUTION_TASK_*_01.md'))
        stats['executions_active'] = len(execution_files)
        stats['executions_complete'] = stats['reviews_approved']  # APPROVED implies EXECUTION complete
    
    # Tests (placeholder - would integrate with pytest in real implementation)
    # For MVP: Set to 0 (will be implemented in future achievement)
    stats['tests_passing'] = 0
    stats['tests_total'] = 0
    
    return stats
```

### 4. Test Suite

**File**: `tests/LLM/dashboard/test_plan_dashboard.py` (~400 lines, NEW)

**Purpose**: Comprehensive tests for plan dashboard functionality

**Test Coverage**:

```python
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from rich.console import Console

from LLM.dashboard.plan_dashboard import PlanDashboard


class TestPlanDashboard:
    """Tests for PlanDashboard class."""
    
    def test_init_with_plan_number(self, tmp_path):
        """Test initialization with plan number."""
        # Create plan structure
        plan_dir = tmp_path / "plans" / "TEST-PLAN"
        plan_dir.mkdir(parents=True)
        (plan_dir / "PLAN_TEST-PLAN.md").write_text("# Test Plan")
        
        console = Console()
        dashboard = PlanDashboard(plan_id=1, console=console)
        
        assert dashboard.plan_path == plan_dir
        assert dashboard.plan_name == "TEST-PLAN"
    
    def test_init_with_plan_name(self, tmp_path):
        """Test initialization with plan name."""
        # Create plan structure
        plan_dir = tmp_path / "plans" / "TEST-PLAN"
        plan_dir.mkdir(parents=True)
        (plan_dir / "PLAN_TEST-PLAN.md").write_text("# Test Plan")
        
        console = Console()
        dashboard = PlanDashboard(plan_id="@TEST-PLAN", console=console)
        
        assert dashboard.plan_path == plan_dir
        assert dashboard.plan_name == "TEST-PLAN"
    
    def test_resolve_plan_invalid_number(self, tmp_path):
        """Test plan resolution with invalid number."""
        console = Console()
        
        with pytest.raises(ValueError, match="out of range"):
            PlanDashboard(plan_id=999, console=console)
    
    def test_resolve_plan_not_found(self, tmp_path):
        """Test plan resolution with non-existent name."""
        console = Console()
        
        with pytest.raises(ValueError, match="Plan not found"):
            PlanDashboard(plan_id="@NONEXISTENT", console=console)


class TestStatusRendering:
    """Tests for status section rendering."""
    
    def test_render_status_basic(self, tmp_path):
        """Test basic status rendering."""
        # Setup plan with known state
        plan_dir = tmp_path / "plans" / "TEST-PLAN"
        plan_dir.mkdir(parents=True)
        
        console = Console()
        dashboard = PlanDashboard(plan_id="@TEST-PLAN", console=console)
        
        # Mock state
        dashboard.state.completed_achievements = 5
        dashboard.state.total_achievements = 10
        dashboard.state.last_achievement = "2.3"
        dashboard.state.current_priority = 2
        
        # Should not raise
        dashboard.render_status()
    
    def test_get_priority_description(self, tmp_path):
        """Test priority description mapping."""
        console = Console()
        dashboard = PlanDashboard(plan_id=1, console=console)
        
        assert "Foundation" in dashboard._get_priority_description(0)
        assert "Plan Dashboard" in dashboard._get_priority_description(1)
        assert "Advanced Features" in dashboard._get_priority_description(2)
        assert "Polish" in dashboard._get_priority_description(3)
    
    def test_estimate_remaining_hours(self, tmp_path):
        """Test remaining hours estimation."""
        console = Console()
        dashboard = PlanDashboard(plan_id=1, console=console)
        
        # Mock state
        dashboard.state.total_achievements = 10
        dashboard.state.completed_achievements = 7
        
        remaining = dashboard._estimate_remaining_hours()
        
        # Should estimate 3 pending * 3-4 hours = 9-12 hours
        assert "9-12" in remaining or "9" in remaining


class TestStatsCalculation:
    """Tests for stats calculation."""
    
    def test_calculate_stats_empty_plan(self, tmp_path):
        """Test stats calculation for empty plan."""
        plan_dir = tmp_path / "plans" / "TEST-PLAN"
        plan_dir.mkdir(parents=True)
        
        console = Console()
        dashboard = PlanDashboard(plan_id="@TEST-PLAN", console=console)
        dashboard.plan_path = plan_dir
        
        stats = dashboard._calculate_stats()
        
        assert stats['subplans_created'] == 0
        assert stats['reviews_approved'] == 0
        assert stats['reviews_pending'] == 0
    
    def test_calculate_stats_with_artifacts(self, tmp_path):
        """Test stats calculation with artifacts."""
        plan_dir = tmp_path / "plans" / "TEST-PLAN"
        plan_dir.mkdir(parents=True)
        
        # Create artifacts
        subplans_dir = plan_dir / "subplans"
        subplans_dir.mkdir()
        (subplans_dir / "SUBPLAN_TEST-PLAN_11.md").write_text("# SUBPLAN")
        (subplans_dir / "SUBPLAN_TEST-PLAN_12.md").write_text("# SUBPLAN")
        
        feedbacks_dir = plan_dir / "execution" / "feedbacks"
        feedbacks_dir.mkdir(parents=True)
        (feedbacks_dir / "APPROVED_11.md").write_text("# APPROVED")
        (feedbacks_dir / "APPROVED_12.md").write_text("# APPROVED")
        (feedbacks_dir / "FIX_13.md").write_text("# FIX")
        
        console = Console()
        dashboard = PlanDashboard(plan_id="@TEST-PLAN", console=console)
        dashboard.plan_path = plan_dir
        
        stats = dashboard._calculate_stats()
        
        assert stats['subplans_created'] == 2
        assert stats['reviews_approved'] == 2
        assert stats['reviews_pending'] == 1


class TestNavigation:
    """Tests for dashboard navigation."""
    
    def test_show_exits_on_back(self, tmp_path):
        """Test that show() exits when user presses 'b'."""
        plan_dir = tmp_path / "plans" / "TEST-PLAN"
        plan_dir.mkdir(parents=True)
        
        console = Console()
        dashboard = PlanDashboard(plan_id="@TEST-PLAN", console=console)
        
        # Mock user input
        with patch.object(dashboard, 'get_user_input', return_value='b'):
            dashboard.show()  # Should exit without error
    
    def test_show_exits_on_6(self, tmp_path):
        """Test that show() exits when user presses '6'."""
        plan_dir = tmp_path / "plans" / "TEST-PLAN"
        plan_dir.mkdir(parents=True)
        
        console = Console()
        dashboard = PlanDashboard(plan_id="@TEST-PLAN", console=console)
        
        # Mock user input
        with patch.object(dashboard, 'get_user_input', return_value='6'):
            dashboard.show()  # Should exit without error
```

---

## 🔧 Approach

### Phase 1: Plan Dashboard Class (90 min)

**Goal**: Implement core PlanDashboard class with plan resolution and basic structure

**Steps**:

1. **Create `LLM/dashboard/plan_dashboard.py`** (30 min):
   - Define `PlanDashboard` class inheriting from `BaseDashboard`
   - Implement `__init__()` with plan_id parameter
   - Implement `_resolve_plan()` to handle both numbers and names
   - Implement `show()` with interactive loop

2. **Implement plan resolution** (30 min):
   - Handle integer plan IDs (1, 2, 3)
   - Handle string plan names ("@LLM-DASHBOARD-CLI" or "LLM-DASHBOARD-CLI")
   - Use `PlanDiscovery` to get all plans
   - Match plan by index or name
   - Raise clear errors for invalid plans

3. **Implement basic rendering** (30 min):
   - `render_header()` - plan name and description
   - `clear()` - clear screen between renders
   - `get_user_input()` - get user choice
   - Basic navigation (back to main dashboard)

**Verification**:
- Can create dashboard with plan number
- Can create dashboard with plan name
- Plan resolution handles edge cases
- Navigation loop works correctly

---

### Phase 2: Status Section (60 min)

**Goal**: Implement status section showing progress, last achievement, priority, remaining time

**Steps**:

1. **Implement `render_status()`** (30 min):
   - Calculate progress percentage from state
   - Format last achievement with APPROVED file reference
   - Get priority description
   - Estimate remaining hours
   - Create Panel with Rich formatting

2. **Implement helper methods** (30 min):
   - `_get_priority_description()` - map priority number to description
   - `_estimate_remaining_hours()` - calculate based on pending achievements
   - Format status information clearly
   - Test with different plan states

**Verification**:
- Status section displays correct progress
- Last achievement formatted correctly
- Priority description is clear
- Remaining hours estimation reasonable

---

### Phase 3: Quick Stats Section (60 min)

**Goal**: Implement quick stats showing SUBPLANs, EXECUTIONs, reviews, tests

**Steps**:

1. **Implement `_calculate_stats()`** (40 min):
   - Count SUBPLAN files in subplans/ directory
   - Calculate SUBPLANs waiting (total achievements - created)
   - Count APPROVED files in execution/feedbacks/
   - Count FIX files for pending reviews
   - Count EXECUTION_TASK files
   - Handle missing directories gracefully

2. **Implement `render_stats()`** (20 min):
   - Format stats with Rich Text
   - Calculate test percentage
   - Create Panel with yellow border
   - Display in clear hierarchical format

**Verification**:
- Stats calculation handles missing directories
- Counts are accurate for test data
- Formatting is clear and readable
- Tests placeholder shows 0/0 (will implement later)

---

### Phase 4: Testing (60 min)

**Goal**: Achieve >90% test coverage with comprehensive tests

**Steps**:

1. **Create `tests/LLM/dashboard/test_plan_dashboard.py`** (40 min):
   - Test plan resolution (by number, by name, errors)
   - Test status rendering
   - Test stats calculation (empty, with artifacts)
   - Test navigation (back, exit)
   - Test helper methods

2. **Run tests and fix issues** (20 min):
   ```bash
   pytest tests/LLM/dashboard/test_plan_dashboard.py -v
   ```
   - Fix any test failures
   - Achieve >90% coverage
   - No linter errors

**Verification**:
- All tests pass (20+ tests)
- Coverage >90%
- No linter errors
- All edge cases covered

---

## 🔄 Execution Strategy

### Type: Single EXECUTION (Recommended)

**Rationale**:

1. **Cohesive Feature**: All components work together (resolution, status, stats)
2. **Manageable Scope**: 3-4 hours, can be done in one focused session
3. **Sequential Dependencies**: Status needs resolution, stats need status
4. **Atomic Delivery**: Feature is only useful when complete

**Execution**: Create single `EXECUTION_TASK_LLM-DASHBOARD-CLI_11_01.md`

**Alternative**: Could split into 2 EXECUTIONs (class + rendering, stats + testing), but overhead not worth it for 3-4 hour task

---

## 🧪 Testing Strategy

### Unit Testing

**Scope**: Test each component in isolation

**Test Files**:
- `test_plan_dashboard.py` - All dashboard functionality

**Coverage Target**: >90% for new code

**Key Tests**:
- Plan resolution (by number, by name, errors)
- Status rendering (progress, last achievement, priority, hours)
- Stats calculation (empty plan, with artifacts, missing directories)
- Navigation (back, exit, invalid input)
- Helper methods (priority description, hours estimation)

### Integration Testing

**Scope**: Test with real plan structure

**Test Cases**:
1. **Full Dashboard Workflow**:
   - Create plan with artifacts
   - Initialize dashboard
   - Render all sections
   - Verify output

2. **Navigation Workflow**:
   - Open dashboard
   - Navigate sections
   - Return to main dashboard

3. **Edge Cases**:
   - Empty plan (no artifacts)
   - Plan with FIX files
   - Invalid plan IDs

### Manual Testing

**Verification**:
- Test with LLM-DASHBOARD-CLI plan (real data)
- Test plan resolution with various inputs
- Verify stats accuracy
- Check formatting and colors
- Test navigation flow

---

## 📊 Expected Results

### Success Criteria

**Functional**:
- ✅ Can open plan dashboard by number or name
- ✅ Status section shows accurate information
- ✅ Stats section shows accurate counts
- ✅ Navigation back to main dashboard works
- ✅ Handles missing directories gracefully
- ✅ Clear error messages for invalid plans

**Quality**:
- ✅ Test coverage >90% for new code
- ✅ All tests passing (20+ tests)
- ✅ No linter errors
- ✅ Clear, readable formatting
- ✅ Consistent with BaseDashboard pattern

**User Experience**:
- ✅ Dashboard loads quickly (<100ms)
- ✅ Information is clear and actionable
- ✅ Navigation is intuitive
- ✅ Status updates reflect filesystem immediately

### Deliverable Metrics

**Files Created**: 2 files (~750 lines total)
- New: 2 files (~750 lines)

**Test Metrics**:
- Total Tests: ~20 new tests
- Coverage: >90% for new code
- All tests passing

---

## 🚨 Risks & Mitigations

### Risk 1: Plan Resolution Ambiguity

**Risk**: Users might provide ambiguous plan identifiers (partial names, wrong numbers)

**Impact**: MEDIUM - Confusing error messages

**Mitigation**:
- Clear error messages with suggestions
- List available plans in error
- Accept multiple formats (@name, name, number)
- Test all resolution paths

### Risk 2: Stats Calculation Performance

**Risk**: Counting files in large plan directories might be slow

**Impact**: LOW - Dashboard feels sluggish

**Mitigation**:
- Use glob patterns efficiently
- Cache stats for 1-2 seconds if needed
- Benchmark with large plans
- Optimize if >100ms

### Risk 3: Missing Directories

**Risk**: Plan might not have subplans/, execution/, or feedbacks/ directories yet

**Impact**: LOW - Stats calculation crashes

**Mitigation**:
- Check directory existence before accessing
- Return 0 for missing directories
- Graceful degradation
- Test with empty plan structure

### Risk 4: State Detection Dependency

**Risk**: PlanDashboard depends on StateDetector which might not be fully implemented

**Impact**: MEDIUM - Dashboard shows incorrect state

**Mitigation**:
- Review StateDetector implementation (from Achievement 0.2)
- Add tests for state detection integration
- Mock state detector in unit tests
- Ensure PlanState has all required fields

---

## 💡 Design Decisions

### Decision 1: Plan Resolution Strategy

**Chosen**: Support both numbers and names, with `_resolve_plan()` helper

**Rationale**:
- Users might prefer numbers (quick) or names (explicit)
- Numbers are convenient for main dashboard navigation
- Names are convenient for direct CLI access
- Single method handles all cases

**Alternative Considered**: Only support numbers, but names are more flexible

### Decision 2: Stats Calculation Source

**Chosen**: Derive all stats from filesystem (no database, no manual tracking)

**Rationale**:
- Consistent with Achievement 0.2 (filesystem-first state tracking)
- No additional dependencies
- Always reflects current state
- No synchronization issues

**Alternative Considered**: Cache in database, but adds complexity

### Decision 3: Test Stats Placeholder

**Chosen**: Show 0/0 for tests in MVP (implement in future achievement)

**Rationale**:
- Test integration is complex (pytest parsing)
- Not critical for MVP (other stats more important)
- Clear that feature is coming (shows 0/0, not hidden)
- Can be added in Achievement 2.3 or 3.1

**Alternative Considered**: Implement now, but adds 1-2 hours to scope

### Decision 4: Interactive Loop in show()

**Chosen**: Simple while loop with 'b' to go back

**Rationale**:
- Consistent with main dashboard pattern
- Simple to understand and test
- Can extend with actions in Achievement 1.3
- Keyboard shortcut ('b') is intuitive

**Alternative Considered**: More complex menu system, but not needed yet

### Decision 5: Single EXECUTION

**Chosen**: One EXECUTION_TASK for all components

**Rationale**:
- 3-4 hours is manageable in one session
- Components are tightly coupled
- Splitting would add overhead (2 SUBPLANs, 2 EXECUTIONs, 2 reviews)
- Atomic feature delivery

**Alternative Considered**: Split into 2 EXECUTIONs (class, rendering), but overhead not worth it

---

## 📝 Implementation Notes

### PlanState Requirements

**Assumption**: `PlanState` from Achievement 0.2 has these fields:
- `completed_achievements: int`
- `total_achievements: int`
- `last_achievement: Optional[str]`
- `current_priority: int`
- `next_achievements: List[AchievementState]`

**If Missing**: Add fields to `PlanState` in `models.py`

### BaseDashboard Interface

**Assumption**: `BaseDashboard` from Achievement 0.1 provides:
- `console: Console` - Rich console instance
- `clear()` - Clear screen method
- `get_user_input(prompt: str) -> str` - Get user input method

**If Missing**: Add methods to `BaseDashboard` class

### Rich Formatting Conventions

**Panels**:
- Status: Cyan border (`border_style="cyan"`)
- Stats: Yellow border (`border_style="yellow"`)
- Padding: `padding=(1, 2)` for all panels

**Text Styles**:
- Headers: `style="bold cyan"` or `style="bold yellow"`
- Values: No style (default)
- Help text: `style="dim"`

---

## 🔗 Dependencies

### Requires (from previous achievements):

- Achievement 0.1: `BaseDashboard` class ✅
- Achievement 0.2: `PlanDiscovery`, `StateDetector`, `PlanState` ✅
- Achievement 0.3: Main dashboard (for navigation reference) ✅

### Enables (for future achievements):

- Achievement 1.2: Achievement State Visualization (builds on plan dashboard)
- Achievement 1.3: Quick Action Shortcuts (adds actions to plan dashboard)

### External Dependencies:

- Python 3.8+ (existing)
- Rich library (from Achievement 0.1)
- No new external libraries needed

---

## ✅ Definition of Done

**Code Complete**:
- [ ] `plan_dashboard.py` created (~350 lines)
- [ ] `test_plan_dashboard.py` created (~400 lines)
- [ ] All classes and methods implemented
- [ ] Plan resolution working (numbers and names)
- [ ] Status section rendering
- [ ] Stats section rendering
- [ ] Navigation working

**Tests Complete**:
- [ ] 20+ tests written and passing
- [ ] >90% coverage for new code
- [ ] Integration tests pass
- [ ] Edge cases tested

**Quality Complete**:
- [ ] No linter errors
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] Error messages clear and actionable

**Integration Complete**:
- [ ] Works with existing BaseDashboard
- [ ] Integrates with PlanDiscovery
- [ ] Uses StateDetector correctly
- [ ] Can navigate from main dashboard (manual test)

---

**Status**: 📋 Ready for Execution  
**Next Step**: Create `EXECUTION_TASK_LLM-DASHBOARD-CLI_11_01.md` and execute work  
**Executor**: Begin with Phase 1 (Plan Dashboard Class)

