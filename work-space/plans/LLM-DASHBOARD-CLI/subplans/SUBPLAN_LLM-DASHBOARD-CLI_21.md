# SUBPLAN: Achievement 2.1 - Parallel Execution Detection & UI

**PLAN**: LLM-DASHBOARD-CLI  
**Achievement**: 2.1  
**Estimated Time**: 4-5 hours  
**Created**: 2025-11-14  
**Status**: 📋 Design Phase

---

## 🎯 Objective

Integrate parallel execution detection and UI into the dashboard by leveraging the parallel execution tools from PARALLEL-EXECUTION-AUTOMATION (batch_subplan.py, batch_execution.py, parallel.json schema). This enables users to discover and execute parallel achievements directly from the dashboard, with automatic detection of parallel opportunities and time savings calculations.

**Core Purpose**: Transform the dashboard from sequential-only execution to parallel-aware execution, automatically detecting and highlighting parallel opportunities based on parallel.json files, and providing one-key shortcuts to batch create SUBPLANs and EXECUTIONs for parallel groups.

**Success Definition**:
- Dashboard detects parallel.json files in plans
- Shows parallel opportunities with time savings estimates
- Provides one-key action to batch create SUBPLANs and EXECUTIONs
- Integrates seamlessly with existing batch_subplan.py and batch_execution.py
- All information is derived from parallel.json (no manual tracking)
- Tested with PARALLEL-EXECUTION-AUTOMATION plan as real-world case

**Integration Note**: This achievement integrates with PARALLEL-EXECUTION-AUTOMATION tools (see `EXECUTION_ANALYSIS_DASHBOARD-PARALLEL-INTEGRATION-STRATEGY.md`). All prerequisites verified ready.

---

## 📦 Deliverables

### 1. Parallel Detector Module

**File**: `LLM/dashboard/parallel_detector.py` (~250 lines, NEW)

**Purpose**: Detect parallel execution opportunities from parallel.json files

**Key Components**:

```python
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional
import json

from LLM.scripts.generation.batch_subplan import filter_by_dependency_level


@dataclass
class ParallelGroup:
    """Parallel execution group."""
    level: int  # Dependency level (0, 1, 2, etc.)
    achievements: List[Dict[str, str]]  # Achievement dicts from parallel.json
    estimated_time: float  # Max time among achievements
    sequential_time: float  # Sum of times
    savings: float  # Time savings
    savings_pct: float  # Savings percentage


class ParallelDetector:
    """
    Detect parallel execution opportunities from parallel.json.
    
    Leverages tools from PARALLEL-EXECUTION-AUTOMATION:
    - filter_by_dependency_level() from batch_subplan.py
    - parallel.json schema from Achievement 1.2
    
    Example:
        >>> detector = ParallelDetector()
        >>> groups = detector.detect_parallel_opportunities(plan_path)
        >>> if groups:
        ...     print(f"Found {len(groups)} parallel groups")
    """
    
    def __init__(self):
        """Initialize parallel detector."""
        pass
    
    def detect_parallel_opportunities(self, plan_path: Path) -> List[ParallelGroup]:
        """
        Detect parallel execution opportunities.
        
        Args:
            plan_path: Path to plan directory
        
        Returns:
            List of ParallelGroup objects
        
        Algorithm:
        1. Check for parallel.json file
        2. Load and parse parallel.json
        3. Use filter_by_dependency_level() to group by level
        4. Calculate time savings for each level
        5. Return parallel groups
        """
        # Check for parallel.json
        parallel_json_file = plan_path / "parallel.json"
        if not parallel_json_file.exists():
            return []
        
        try:
            parallel_data = json.loads(parallel_json_file.read_text())
        except (json.JSONDecodeError, OSError) as e:
            logger.error("Failed to parse parallel.json", exc_info=True)
            return []
        
        achievements = parallel_data.get("achievements", [])
        if not achievements:
            return []
        
        # Group by dependency level (use existing tool)
        groups = []
        level = 0
        while True:
            level_achievements = filter_by_dependency_level(achievements, level=level)
            
            if not level_achievements:
                break  # No more levels
            
            # Filter to incomplete only (no APPROVED files)
            incomplete = self._filter_incomplete(level_achievements, plan_path)
            
            if len(incomplete) > 1:  # Only groups with 2+ achievements
                group = self._build_parallel_group(level, incomplete)
                groups.append(group)
            
            level += 1
        
        return groups
    
    def _filter_incomplete(self, achievements: List[Dict], plan_path: Path) -> List[Dict]:
        """Filter to achievements without APPROVED files."""
        incomplete = []
        feedbacks_dir = plan_path / "execution" / "feedbacks"
        
        for ach in achievements:
            ach_id = ach["achievement_id"]
            ach_num = ach_id.replace('.', '')
            approved_file = feedbacks_dir / f"APPROVED_{ach_num}.md"
            
            if not approved_file.exists():
                incomplete.append(ach)
        
        return incomplete
    
    def _build_parallel_group(self, level: int, achievements: List[Dict]) -> ParallelGroup:
        """Build ParallelGroup with time calculations."""
        # Get estimated times
        times = [ach.get("estimated_hours", 3) for ach in achievements]
        
        estimated_time = max(times)  # Parallel time = max
        sequential_time = sum(times)  # Sequential time = sum
        savings = sequential_time - estimated_time
        savings_pct = (savings / sequential_time * 100) if sequential_time > 0 else 0
        
        return ParallelGroup(
            level=level,
            achievements=achievements,
            estimated_time=estimated_time,
            sequential_time=sequential_time,
            savings=savings,
            savings_pct=savings_pct
        )
```

### 2. Parallel UI Rendering

**Function**: `render_parallel_opportunities()` in `plan_dashboard.py` (~60 lines)

**Purpose**: Display parallel groups with time savings

**Implementation**:

```python
def render_parallel_opportunities(self):
    """
    Render parallel execution opportunities.
    
    Shows:
    - Parallel groups by dependency level
    - Achievements in each group
    - Time savings (parallel vs sequential)
    - Action option to execute parallel group
    """
    from LLM.dashboard.parallel_detector import ParallelDetector
    
    if not hasattr(self, 'parallel_detector'):
        self.parallel_detector = ParallelDetector()
    
    groups = self.parallel_detector.detect_parallel_opportunities(self.plan_path)
    
    if not groups:
        return  # Don't show section if no parallel opportunities
    
    content = Text()
    content.append("🔀 Parallel Execution Opportunities\n\n", style="bold magenta")
    
    for i, group in enumerate(groups, 1):
        content.append(f"Level {group.level} Group (", style="bold")
        content.append(f"{len(group.achievements)} achievements", style="bold cyan")
        content.append("):\n", style="bold")
        
        for ach in group.achievements:
            content.append(f"  ├─ {ach['achievement_id']}: {ach.get('description', 'No description')}\n")
        
        content.append(f"  └─ Time: {group.estimated_time:.1f}h parallel vs {group.sequential_time:.1f}h sequential\n")
        content.append(f"     ", style="green")
        content.append(f"Savings: {group.savings:.1f}h ({group.savings_pct:.0f}%)\n", style="green bold")
        
        if i < len(groups):
            content.append("\n")
    
    panel = Panel(content, border_style="magenta", padding=(1, 2))
    self.console.print(panel)
    self.console.print()
```

### 3. Parallel Execution Action

**Function**: `_action_execute_parallel()` in `plan_dashboard.py` (~80 lines)

**Purpose**: Enable parallel execution from dashboard

**Implementation**:

```python
def _action_execute_parallel(self):
    """
    Execute parallel group action.
    
    Workflow:
    1. Detect parallel groups
    2. Show groups with time savings
    3. Ask user to select group
    4. Batch create SUBPLANs for group
    5. Batch create EXECUTIONs for group
    6. Show execution instructions
    """
    from LLM.dashboard.parallel_detector import ParallelDetector
    from LLM.scripts.generation.batch_subplan import batch_create_subplans
    from LLM.scripts.generation.batch_execution import batch_create_executions
    
    if not hasattr(self, 'parallel_detector'):
        self.parallel_detector = ParallelDetector()
    
    groups = self.parallel_detector.detect_parallel_opportunities(self.plan_path)
    
    if not groups:
        self.console.print("[yellow]No parallel execution opportunities found[/yellow]")
        self.console.print("[dim]Tip: Create parallel.json file to enable parallel execution[/dim]")
        self.console.print("\nPress any key to continue...")
        self.get_user_input("")
        return
    
    # Show groups
    self.clear()
    self.render_parallel_opportunities()
    
    # Prompt for group selection
    group_choices = [str(i) for i in range(1, len(groups) + 1)]
    group_choices.append('b')
    
    choice = Prompt.ask(
        f"\nSelect group to execute (1-{len(groups)}) or 'b' to cancel",
        console=self.console,
        choices=group_choices,
        default='b'
    )
    
    if choice == 'b':
        return
    
    group_idx = int(choice) - 1
    group = groups[group_idx]
    
    # Batch create SUBPLANs
    self.console.print(f"\n[cyan]Creating SUBPLANs for Level {group.level} achievements...[/cyan]")
    subplan_result = batch_create_subplans(
        plan_path=self.plan_path,
        dry_run=False
    )
    
    # Batch create EXECUTIONs
    self.console.print(f"\n[cyan]Creating EXECUTIONs for Level {group.level} achievements...[/cyan]")
    execution_result = batch_create_executions(
        plan_path=self.plan_path,
        dry_run=False
    )
    
    # Show results
    self.console.print("\n" + "="*80)
    self.console.print(subplan_result)
    self.console.print(execution_result)
    self.console.print("="*80)
    
    # Show execution instructions
    self._show_parallel_execution_instructions(group)
    
    self.console.print("\nPress any key to continue...")
    self.get_user_input("")

def _show_parallel_execution_instructions(self, group: ParallelGroup):
    """Show instructions for executing parallel group."""
    content = Text()
    content.append("\n🔀 Parallel Execution Instructions\n\n", style="bold magenta")
    content.append("Option A: Multiple Terminals (Recommended)\n\n", style="bold")
    
    for i, ach in enumerate(group.achievements, 1):
        ach_id = ach["achievement_id"]
        content.append(f"Terminal {i}:\n", style="bold")
        content.append(f"  python LLM/scripts/generation/generate_prompt.py @{self.plan_name} continue @EXECUTION_TASK_*_{ach_id.replace('.', '')}_01.md\n", style="cyan")
        content.append("\n")
    
    content.append("Option B: Sequential (if parallel not feasible)\n\n", style="bold dim")
    content.append("  Execute each EXECUTION_TASK one at a time\n", style="dim")
    
    panel = Panel(content, title="Next Steps", border_style="magenta", padding=(1, 2))
    self.console.print(panel)
```

### 4. Action Menu Enhancement

**Changes**: Update `_get_available_actions()` in `plan_dashboard.py` (~20 lines)

**Purpose**: Add parallel execution action to menu

**Implementation**:

```python
def _get_available_actions(self) -> List[Action]:
    """Get list of available actions based on plan state."""
    # Check for parallel opportunities
    has_parallel = self._has_parallel_opportunities()
    
    # Execute Next only enabled if next achievements exist
    has_next = len(self.state.next_achievements) > 0
    
    actions = [
        Action('1', '▶️', 'Execute Next Achievement', enabled=has_next),
        Action('2', '🔀', 'Execute Parallel Group', enabled=has_parallel),  # NEW
        Action('3', '📝', 'Create SUBPLAN', enabled=True),
        Action('4', '🔄', 'Create EXECUTION', enabled=True),
        Action('5', '📚', 'View Documentation', enabled=True),
        Action('6', '🔙', 'Back to Plans', enabled=True),
    ]
    return actions

def _has_parallel_opportunities(self) -> bool:
    """Check if plan has parallel opportunities."""
    parallel_json = self.plan_path / "parallel.json"
    return parallel_json.exists()
```

### 5. Test Suite

**File**: `tests/LLM/dashboard/test_parallel_detector.py` (~350 lines, NEW)

**Purpose**: Comprehensive tests for parallel detection

**Test Coverage**:

```python
class TestParallelDetector:
    """Tests for ParallelDetector class."""
    
    def test_detect_no_parallel_json(self):
        """Test when no parallel.json exists."""
    
    def test_detect_with_parallel_json(self):
        """Test with valid parallel.json."""
    
    def test_detect_invalid_json(self):
        """Test with invalid JSON."""
    
    def test_filter_incomplete_achievements(self):
        """Test filtering to incomplete achievements."""
    
    def test_build_parallel_group_calculations(self):
        """Test time savings calculations."""

class TestParallelUI:
    """Tests for parallel UI rendering."""
    
    def test_render_parallel_opportunities_none(self):
        """Test when no parallel opportunities."""
    
    def test_render_parallel_opportunities_with_groups(self):
        """Test rendering parallel groups."""
    
    def test_has_parallel_opportunities_true(self):
        """Test parallel.json detection."""
    
    def test_has_parallel_opportunities_false(self):
        """Test no parallel.json."""

class TestParallelAction:
    """Tests for parallel execution action."""
    
    def test_action_execute_parallel_no_opportunities(self):
        """Test action when no parallel opportunities."""
    
    def test_action_execute_parallel_cancelled(self):
        """Test action when user cancels."""
    
    def test_action_execute_parallel_success(self):
        """Test successful parallel execution."""

class TestIntegration:
    """Integration tests with real parallel.json."""
    
    def test_integration_with_parallel_automation_plan(self):
        """Test with PARALLEL-EXECUTION-AUTOMATION plan structure."""
```

---

## 🔧 Approach

### Phase 1: Parallel Detector Module (120 min)

**Goal**: Create parallel_detector.py with integration to batch tools

**Steps**:

1. **Create `LLM/dashboard/parallel_detector.py`** (60 min):
   - Define ParallelGroup dataclass
   - Define ParallelDetector class
   - Implement `detect_parallel_opportunities()`
   - Implement `_filter_incomplete()` - Filter to achievements without APPROVED
   - Implement `_build_parallel_group()` - Calculate time savings
   - Add logging

2. **Import and integrate with batch_subplan** (30 min):
   - Import `filter_by_dependency_level()` from batch_subplan.py
   - Use to group achievements by dependency level
   - Test integration

3. **Handle edge cases** (30 min):
   - Missing parallel.json
   - Invalid JSON
   - Empty achievements list
   - All achievements complete

**Verification**:
- Can detect parallel.json files
- Can parse and group achievements
- Time calculations are correct
- Handles edge cases gracefully

---

### Phase 2: Dashboard UI Integration (90 min)

**Goal**: Add parallel UI to plan dashboard

**Steps**:

1. **Implement `render_parallel_opportunities()`** (40 min):
   - Create ParallelDetector instance
   - Detect parallel groups
   - Render with Rich Panel (magenta border)
   - Show time savings

2. **Update `show()` method** (10 min):
   - Add `render_parallel_opportunities()` call
   - Position after health score, before stats

3. **Enhance action menu** (20 min):
   - Add `_has_parallel_opportunities()` helper
   - Update `_get_available_actions()` to include parallel action
   - Change action numbers (Execute Parallel is now action 2)

4. **Implement `_action_execute_parallel()`** (20 min):
   - Detect groups
   - Prompt for group selection
   - Call batch_create_subplans()
   - Call batch_create_executions()
   - Show results and instructions

**Verification**:
- Parallel opportunities display correctly
- Action menu includes parallel option
- Option only enabled when parallel.json exists

---

### Phase 3: Parallel Execution Instructions (30 min)

**Goal**: Provide clear instructions for executing parallel groups

**Steps**:

1. **Implement `_show_parallel_execution_instructions()`** (20 min):
   - Show terminal commands for each achievement
   - Format with Rich
   - Provide Option A (multiple terminals) and Option B (sequential)

2. **Test instructions** (10 min):
   - Verify commands are correct
   - Test formatting

**Verification**:
- Instructions are clear
- Commands are copy-pasteable
- Both options shown

---

### Phase 4: Testing & Integration (120 min)

**Goal**: Achieve >90% test coverage and test with real data

**Steps**:

1. **Create `test_parallel_detector.py`** (60 min):
   - Test parallel detection
   - Test UI rendering
   - Test action execution
   - Test integration

2. **Test with PARALLEL-EXECUTION-AUTOMATION** (30 min):
   - Use real parallel.json from PARALLEL-EXECUTION-AUTOMATION plan
   - Verify detection works
   - Verify UI displays correctly
   - Verify batch creation integration

3. **Run full test suite** (30 min):
   ```bash
   pytest tests/LLM/dashboard/test_parallel_detector.py -v
   pytest tests/LLM/dashboard/ -v
   ```
   - Fix any failures
   - Ensure >90% coverage
   - No linter errors
   - No regressions

**Verification**:
- All tests pass (15+ tests)
- Integration with real parallel.json works
- No regressions in existing tests

---

## 🔄 Execution Strategy

### Type: Single EXECUTION (Recommended)

**Rationale**:

1. **Cohesive Feature**: All components work together (detector, UI, action)
2. **Manageable Scope**: 4-5 hours, can be done in one session
3. **Sequential Dependencies**: UI needs detector, action needs both
4. **Integration Testing**: Needs real parallel.json to validate

**Execution**: Create single `EXECUTION_TASK_LLM-DASHBOARD-CLI_21_01.md`

**Alternative**: Could split into 2 EXECUTIONs (detector, UI + action), but testing requires both

---

## 🧪 Testing Strategy

### Unit Testing

**Scope**: Test each component in isolation

**Test Files**:
- `test_parallel_detector.py` - Parallel detection and UI

**Coverage Target**: >90% for new code

**Key Tests**:
- Parallel.json detection and parsing
- Grouping by dependency level
- Time savings calculations
- Incomplete achievement filtering
- UI rendering
- Action execution
- Integration with batch tools

### Integration Testing

**Scope**: Test with real parallel.json

**Test Cases**:
1. **PARALLEL-EXECUTION-AUTOMATION Plan**:
   - Use actual parallel.json
   - Verify detection works
   - Test batch creation integration

2. **Edge Cases**:
   - No parallel.json (no opportunities shown)
   - All achievements complete (no groups)
   - Invalid JSON (graceful error)

### Manual Testing

**Verification**:
- Open LLM-DASHBOARD-CLI dashboard
- Navigate to PARALLEL-EXECUTION-AUTOMATION plan
- Verify parallel opportunities display
- Test parallel execution action
- Verify batch creation works

---

## 📊 Expected Results

### Success Criteria

**Functional**:
- ✅ Detects parallel.json files
- ✅ Parses and groups achievements by level
- ✅ Calculates time savings correctly
- ✅ Displays parallel opportunities in UI
- ✅ Parallel action creates SUBPLANs and EXECUTIONs
- ✅ Shows execution instructions
- ✅ Only shows when parallel.json exists

**Quality**:
- ✅ Test coverage >90% for new code
- ✅ All tests passing (15+ tests)
- ✅ No linter errors
- ✅ Integration tested with real data

**User Experience**:
- ✅ Parallel opportunities are discoverable
- ✅ Time savings are motivating
- ✅ One-key parallel execution
- ✅ Clear instructions provided

### Deliverable Metrics

**Files Created**: 2 files (~600 lines total)
- New: 2 files (~600 lines)

**Test Metrics**:
- Total Tests: ~15 new tests
- Coverage: >90% for new code
- All tests passing

---

## 🚨 Risks & Mitigations

### Risk 1: parallel.json Format Changes

**Risk**: parallel.json format might differ from expected schema

**Impact**: MEDIUM - Can't parse parallel opportunities

**Mitigation**:
- Use validated schema from PARALLEL-EXECUTION-AUTOMATION 1.2
- Handle parsing errors gracefully
- Validate JSON structure before using
- Test with real parallel.json files

### Risk 2: Batch Tool Integration

**Risk**: batch_subplan.py or batch_execution.py might have changed

**Impact**: HIGH - Integration breaks

**Mitigation**:
- Verify tools exist and are importable
- Test integration thoroughly
- Use try-except for imports
- Refer to integration analysis document

### Risk 3: Missing parallel.json

**Risk**: Most plans don't have parallel.json yet

**Impact**: LOW - Feature not available for most plans

**Mitigation**:
- Only show parallel section if parallel.json exists
- Don't clutter UI when not available
- Provide tip to create parallel.json
- Enable action only when available

### Risk 4: Time Estimation Accuracy

**Risk**: Time savings calculations might be inaccurate

**Impact**: LOW - Misleading estimates

**Mitigation**:
- Use estimated_hours from parallel.json
- Fallback to 3 hours if not specified
- Show as estimates, not guarantees
- Document calculation method

---

## 💡 Design Decisions

### Decision 1: Use Existing filter_by_dependency_level

**Chosen**: Import and reuse from batch_subplan.py

**Rationale**:
- Already implemented and tested (31 tests)
- Consistent grouping logic
- No duplication
- Validates integration approach

**Alternative Considered**: Reimplement, but would duplicate code

### Decision 2: Only Show When parallel.json Exists

**Chosen**: Don't show parallel section if no parallel.json

**Rationale**:
- Most plans don't have parallel.json yet
- Reduces UI clutter
- Feature is opt-in
- Clear when not available

**Alternative Considered**: Always show section with message, but clutters UI

### Decision 3: Integrate with Batch Tools

**Chosen**: Call batch_create_subplans() and batch_create_executions()

**Rationale**:
- Reuses tested, production-ready tools
- Consistent with command-line workflow
- Prerequisite validation automatic (from batch_execution)
- No code duplication

**Alternative Considered**: Reimplement batch logic, but violates DRY

### Decision 4: Action Menu Position

**Chosen**: Parallel execution as action 2 (after Execute Next)

**Rationale**:
- Logical progression (single → parallel)
- High visibility (near top)
- Only enabled when available
- Doesn't disrupt existing actions

**Alternative Considered**: Last action, but less discoverable

### Decision 5: Single EXECUTION

**Chosen**: One EXECUTION_TASK for all components

**Rationale**:
- 4-5 hours is manageable
- Components are tightly coupled
- Integration testing needs all parts
- Atomic feature delivery

**Alternative Considered**: Split into 2, but testing requires both

---

## 📝 Implementation Notes

### parallel.json Schema

**Expected Format** (from PARALLEL-EXECUTION-AUTOMATION 1.2):

```json
{
  "plan": "PLAN_NAME",
  "version": "1.0",
  "achievements": [
    {
      "achievement_id": "3.1",
      "description": "Achievement title",
      "dependencies": [],
      "estimated_hours": 2.5
    },
    {
      "achievement_id": "3.2",
      "description": "Achievement title",
      "dependencies": ["3.1"],
      "estimated_hours": 3.0
    }
  ]
}
```

### Integration with Batch Tools

**Import Pattern**:
```python
from LLM.scripts.generation.batch_subplan import (
    filter_by_dependency_level,
    batch_create_subplans
)
from LLM.scripts.generation.batch_execution import (
    batch_create_executions
)
```

**Usage**:
```python
# Group by level
level_0 = filter_by_dependency_level(achievements, level=0)

# Batch create
subplan_result = batch_create_subplans(plan_path, dry_run=False)
execution_result = batch_create_executions(plan_path, dry_run=False)
```

### Action Menu Update

**Before** (Achievements 1.1-1.3):
```
1. ▶️ Execute Next Achievement
2. 📝 Create SUBPLAN
3. 🔄 Create EXECUTION
4. 📚 View Documentation
5. 🔙 Back to Plans
```

**After** (Achievement 2.1):
```
1. ▶️ Execute Next Achievement
2. 🔀 Execute Parallel Group  ← NEW
3. 📝 Create SUBPLAN
4. 🔄 Create EXECUTION
5. 📚 View Documentation
6. 🔙 Back to Plans
```

---

## 🔗 Dependencies

### Requires (from previous achievements):

- Achievement 1.1-1.3: Plan dashboard complete ✅
- Achievement 0.2: State detection ✅
- PARALLEL-EXECUTION-AUTOMATION 2.2: batch_subplan.py ✅
- PARALLEL-EXECUTION-AUTOMATION 2.3: batch_execution.py ✅
- PARALLEL-EXECUTION-AUTOMATION 1.2: parallel.json schema ✅

### Enables (for future achievements):

- Achievement 2.2: Interactive Workflow Execution (will enhance parallel execution)
- Achievement 2.3: Real-Time State Updates (will show parallel execution status)

### External Dependencies:

- Python 3.8+ (existing)
- Rich library (from Achievement 0.1)
- No new external libraries needed

---

## ✅ Definition of Done

**Code Complete**:
- [ ] `parallel_detector.py` created (~250 lines)
- [ ] `render_parallel_opportunities()` implemented (~60 lines)
- [ ] `_action_execute_parallel()` implemented (~80 lines)
- [ ] `_show_parallel_execution_instructions()` implemented (~40 lines)
- [ ] `_has_parallel_opportunities()` implemented (~10 lines)
- [ ] Action menu updated (6 actions instead of 5)
- [ ] `test_parallel_detector.py` created (~350 lines)

**Tests Complete**:
- [ ] 15+ tests written and passing
- [ ] >90% coverage for new code
- [ ] Integration with batch tools tested
- [ ] Tested with real parallel.json

**Quality Complete**:
- [ ] No linter errors
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] Error messages clear

**Integration Complete**:
- [ ] Imports from batch_subplan.py work
- [ ] Imports from batch_execution.py work
- [ ] Tested with PARALLEL-EXECUTION-AUTOMATION plan
- [ ] No breaking changes

---

**Status**: 📋 Ready for Execution  
**Next Step**: Create `EXECUTION_TASK_LLM-DASHBOARD-CLI_21_01.md` and execute work  
**Executor**: Begin with Phase 1 (Parallel Detector Module)  
**Reference**: `EXECUTION_ANALYSIS_DASHBOARD-PARALLEL-INTEGRATION-STRATEGY.md`

