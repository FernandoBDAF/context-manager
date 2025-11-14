# SUBPLAN: Achievement 0.3 - Main Dashboard Implementation

**PLAN**: LLM-DASHBOARD-CLI  
**Achievement**: 0.3  
**Estimated Time**: 2-3 hours  
**Created**: 2025-11-13  
**Status**: 📋 Design Phase

---

## 🎯 Objective

Implement the main dashboard that displays all plans with their current states, providing users with a single-view overview of the entire LLM Methodology workspace. This dashboard serves as the primary entry point for the CLI, replacing verbose command-line arguments with an intuitive, interactive interface.

**Core Purpose**: Create the main entry point for the dashboard CLI that shows all discovered plans in a Rich-formatted table, displays their current status, and allows users to select a plan for detailed viewing.

**Success Definition**:

- Main dashboard displays all plans from `work-space/plans/` in a formatted table
- Each plan shows: name, last completed achievement, next available achievements, and status
- Status indicators use emojis for instant recognition (🔴 🟡 🟢 ⚪)
- User can select a plan by number or quit with 'q'
- Dashboard integrated into `LLM/main.py` entry point
- All components tested with >90% coverage
- Interactive loop works correctly with clear/refresh

---

## 📦 Deliverables

### 1. Main Dashboard Module

**File**: `LLM/dashboard/main_dashboard.py` (~200 lines)
**Contents**:

- `MainDashboard` class extending `BaseDashboard`
- `show()` method: Interactive loop (render → prompt → handle input)
- `render_header()`: Display dashboard title and navigation help
- `render_plans()`: Display plans table using state detector
- `render_prompt()`: Show user input prompt
- `get_user_input()`: Handle user input (plan selection, quit)
- `open_plan_dashboard()`: Placeholder for Achievement 1.1 (show message)

**Key Methods**:

```python
class MainDashboard(BaseDashboard):
    def __init__(self, console: Optional[Console] = None, workspace_root: Optional[Path] = None):
        """Initialize with console and workspace root."""

    def show(self):
        """Main interactive loop: clear → render → prompt → handle input."""

    def render_header(self):
        """Render dashboard header with title and help text."""

    def render_plans(self):
        """Render plans table using PlanDiscovery and StateDetector."""

    def render_prompt(self):
        """Display user input prompt."""

    def get_user_input(self) -> str:
        """Get and validate user input."""

    def open_plan_dashboard(self, plan_index: int):
        """Open plan-specific dashboard (placeholder for 1.1)."""
```

### 2. Table Rendering Helpers

**File**: `LLM/dashboard/main_dashboard.py` (within same file, ~80 lines)
**Contents**:

- `create_plan_table(plan_states: List[PlanState]) -> Table`: Create Rich table for plans
- `get_status_emoji(plan: PlanState) -> str`: Return status emoji based on plan state
- `format_next_achievements(next_achievements: List[str]) -> str`: Format next achievements for display

**Key Functions**:

```python
def create_plan_table(plan_states: List[PlanState]) -> Table:
    """
    Create Rich table with columns:
    - # (index)
    - Plan (name)
    - Last (last completed achievement)
    - Next (next available achievements)
    - Status (emoji + text)
    """

def get_status_emoji(plan: PlanState) -> str:
    """
    Return status based on priority:
    1. 🔴 Needs attention (pending fixes)
    2. 🟡 In progress (active executions)
    3. 🟢 Ready to execute (next achievements available)
    4. ⚪ No next action (complete or blocked)
    """

def format_next_achievements(next_achievements: List[str]) -> str:
    """
    Format next achievements for display:
    - Empty list: "None"
    - 1 achievement: "2.1"
    - 2+ achievements: "2.1, 2.2"
    - 3+ achievements: "2.1, 2.2 (+2 more)"
    """
```

### 3. Main Entry Point Integration

**File**: `LLM/main.py` (modified, ~20 lines added)
**Contents**:

- Import `MainDashboard`
- Add `--dashboard` flag (default behavior)
- Route to dashboard when no other args provided
- Keep existing `--version` flag

**Integration Pattern**:

```python
# LLM/main.py
from LLM.dashboard.main_dashboard import MainDashboard

def main():
    parser = argparse.ArgumentParser(...)
    parser.add_argument('--dashboard', action='store_true', default=True,
                       help='Launch dashboard (default)')
    # ... existing args ...

    args = parser.parse_args()

    if args.dashboard or len(sys.argv) == 1:
        # Launch dashboard (default)
        dashboard = MainDashboard()
        dashboard.show()
    else:
        # Handle other commands (existing logic)
        ...
```

### 4. Test Files

**File**: `tests/LLM/dashboard/test_main_dashboard.py` (~250 lines, 25 tests)
**Contents**:

**Test Classes**:

- `TestMainDashboard`: Main dashboard class tests (10 tests)
- `TestTableRendering`: Table creation and formatting tests (8 tests)
- `TestStatusIndicators`: Status emoji and formatting tests (7 tests)

**Key Tests**:

1. `test_init_with_defaults()` - Initialize with default console/workspace
2. `test_init_with_custom_values()` - Initialize with custom console/workspace
3. `test_render_header()` - Header rendering
4. `test_render_plans_empty()` - No plans found scenario
5. `test_render_plans_with_data()` - Plans table rendering
6. `test_render_prompt()` - User prompt rendering
7. `test_get_user_input_quit()` - 'q' to quit
8. `test_get_user_input_valid_number()` - Valid plan selection
9. `test_get_user_input_invalid_number()` - Invalid plan selection
10. `test_open_plan_dashboard_placeholder()` - Placeholder message for 1.1
11. `test_create_plan_table_empty()` - Empty plans list
12. `test_create_plan_table_single_plan()` - Single plan in table
13. `test_create_plan_table_multiple_plans()` - Multiple plans in table
14. `test_table_columns()` - Correct columns created
15. `test_get_status_emoji_needs_attention()` - 🔴 for pending fixes
16. `test_get_status_emoji_in_progress()` - 🟡 for active executions
17. `test_get_status_emoji_ready_to_execute()` - 🟢 for next achievements
18. `test_get_status_emoji_no_next_action()` - ⚪ for complete/blocked
19. `test_format_next_achievements_empty()` - "None" for empty list
20. `test_format_next_achievements_single()` - "2.1" for single achievement
21. `test_format_next_achievements_multiple()` - "2.1, 2.2" for 2 achievements
22. `test_format_next_achievements_many()` - "2.1, 2.2 (+2 more)" for 4+ achievements
23. `test_main_integration()` - Integration test with real PlanDiscovery/StateDetector
24. `test_show_loop_quit()` - Interactive loop quits on 'q'
25. `test_show_loop_select_plan()` - Interactive loop handles plan selection

**Total Estimated Lines**: ~550 lines (code + tests)
**Total Estimated Tests**: 25 tests

---

## 🔧 Approach

### Phase 1: Core Dashboard Implementation (50 min)

**Goal**: Implement MainDashboard class with interactive loop

**Tasks**:

1. **Create `LLM/dashboard/main_dashboard.py`**:

   - Define `MainDashboard` class extending `BaseDashboard`
   - Implement `__init__()` with console and workspace_root
   - Implement `show()` main loop (while True: clear → render → input → handle)
   - Implement `render_header()` using `self.render_panel()`
   - Implement `render_plans()` to display plans table
   - Implement `render_prompt()` using Rich prompt
   - Implement `get_user_input()` with validation
   - Implement `open_plan_dashboard()` as placeholder (prints message for 1.1)

2. **Use Existing Components**:
   - Import `PlanDiscovery` from Achievement 0.2
   - Import `StateDetector` from Achievement 0.2
   - Import `BaseDashboard` from Achievement 0.1
   - Import `ui_components` helpers (create_table, format_status, etc.)

**Verification**:

- Class instantiates without errors
- Interactive loop starts and renders header
- Can quit with 'q'

---

### Phase 2: Table Rendering (40 min)

**Goal**: Implement plan table rendering with status indicators

**Tasks**:

1. **Implement `create_plan_table()` function**:

   - Create Rich Table with title "Active Plans"
   - Add 5 columns: #, Plan, Last, Next, Status
   - Iterate over plan_states and add rows
   - Handle empty plans list gracefully

2. **Implement `get_status_emoji()` function**:

   - Check `plan.pending_fixes` → "🔴 Needs attention"
   - Check `plan.next_achievements` and active executions → "🟡 In progress"
   - Check `plan.next_achievements` → "🟢 Ready to execute"
   - Default → "⚪ No next action"

3. **Implement `format_next_achievements()` function**:
   - Empty list → "None"
   - 1 achievement → "2.1"
   - 2 achievements → "2.1, 2.2"
   - 3+ achievements → "2.1, 2.2 (+X more)"

**Verification**:

- Table renders with correct columns
- Status emojis appear correctly
- Next achievements formatted properly

---

### Phase 3: Main Entry Point Integration (30 min)

**Goal**: Integrate dashboard into LLM/main.py

**Tasks**:

1. **Update `LLM/main.py`**:

   - Import `MainDashboard` from `LLM.dashboard.main_dashboard`
   - Add `--dashboard` argument (default=True)
   - Add dashboard routing logic (if args.dashboard or no args: launch dashboard)
   - Keep existing `--version` flag functional

2. **Test Integration**:
   - Run `python LLM/main.py` (should launch dashboard)
   - Run `python LLM/main.py --dashboard` (should launch dashboard)
   - Run `python LLM/main.py --version` (should print version, not dashboard)
   - Verify dashboard shows discovered plans

**Verification**:

- Dashboard launches on `python LLM/main.py`
- Dashboard shows all plans with correct states
- Can navigate and quit

---

### Phase 4: Testing & Validation (40 min)

**Goal**: Achieve >90% test coverage

**Tasks**:

1. **Create `tests/LLM/dashboard/test_main_dashboard.py`**:

   - Write tests for `MainDashboard` class (10 tests)
   - Write tests for table rendering (8 tests)
   - Write tests for status indicators (7 tests)
   - Use mocks for `PlanDiscovery` and `StateDetector` to isolate tests
   - Use `unittest.mock.patch` for user input and console rendering

2. **Run Tests**:

   ```bash
   pytest tests/LLM/dashboard/test_main_dashboard.py -v
   ```

3. **Manual Integration Test**:
   - Run `python LLM/main.py`
   - Verify dashboard displays all plans
   - Verify status emojis correct
   - Verify can select plan (shows placeholder message)
   - Verify can quit with 'q'

**Verification**:

- All tests pass (25/25)
- Coverage >90%
- No linter errors
- Manual integration successful

---

## 🔄 Execution Strategy

**Type**: Single EXECUTION (all components interdependent)

**Rationale**:

- Main dashboard, table rendering, and main.py integration are tightly coupled
- Total effort is 2-3 hours, suitable for a single focused execution
- All components needed together for the dashboard to be functional
- Testing requires all pieces working together

**Phase Execution**:

1. Phase 1: Core Dashboard Implementation (50 min)
2. Phase 2: Table Rendering (40 min)
3. Phase 3: Main Entry Point Integration (30 min)
4. Phase 4: Testing & Validation (40 min)

**Total**: 2-3 hours (160 min estimated, budget 180 min)

---

## 🧪 Testing Strategy

**Unit Tests**:

- **Scope**: Each method in `MainDashboard` class, table rendering functions, status helpers
- **Framework**: `pytest`
- **Mocks**: Use `unittest.mock` to mock:
  - `PlanDiscovery.get_all_plans()` → return test plan paths
  - `StateDetector.get_plan_state()` → return test `PlanState` objects
  - `Console.print()` → verify rendering calls
  - `Prompt.ask()` → simulate user input
- **Coverage**: Target >90% line coverage for `main_dashboard.py`
- **Edge Cases**: Empty plans list, invalid user input, no next achievements, various status combinations

**Integration Tests (Manual)**:

- After unit tests pass, manually verify:
  - Dashboard launches with `python LLM/main.py`
  - All real plans from `work-space/plans/` are displayed
  - Status emojis match actual plan states
  - Can select a plan (shows placeholder message)
  - Can quit with 'q'
  - Dashboard refreshes correctly on each iteration

**Interactive Tests**:

- Test user experience:
  - Table is readable and well-formatted
  - Status indicators are clear
  - Navigation help is visible
  - Prompt is clear
  - Error messages for invalid input are helpful

---

## 📈 Expected Results

**Functional**:

- `MainDashboard` displays all plans in a Rich table
- Each plan shows:
  - Plan name
  - Last completed achievement (from `APPROVED_*.md`)
  - Next available achievements (from state detection)
  - Status emoji (🔴 🟡 🟢 ⚪)
- User can:
  - Select a plan by entering its number
  - Quit the dashboard by entering 'q'
  - See a placeholder message when selecting a plan (Achievement 1.1 not yet implemented)
- Dashboard integrates seamlessly into `LLM/main.py` as the default behavior

**Visual**:

```
┌─ LLM Methodology Dashboard ─────────────────────────────────┐
│                                                              │
│  Active Plans (3)                                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ #  Plan                                Last    Next      │ │
│  │ 1  PROMPT-GENERATOR-UX-AND-FOUNDATION  3.1     3.2, 3.3 │ │
│  │    Status: 🟢 Ready to execute                          │ │
│  │                                                          │ │
│  │ 2  LLM-DASHBOARD-CLI                   0.2     0.3      │ │
│  │    Status: 🟢 Ready to execute                          │ │
│  │                                                          │ │
│  │ 3  PARALLEL-EXECUTION-AUTOMATION       1.3     2.1      │ │
│  │    Status: 🔴 Needs attention (1 fix)                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Select plan (1-3) or 'q' to quit: _                        │
└──────────────────────────────────────────────────────────────┘
```

**Performance**:

- Dashboard load time: <500ms for up to 10 plans
- Plan state detection: <200ms per plan (from Achievement 0.2)
- Interactive loop: <100ms per iteration
- Total: <2 seconds from launch to first render

**Quality**:

- All unit tests pass with >90% coverage
- Code is clean, well-documented with docstrings and type hints
- No linter errors
- User experience is smooth and intuitive

---

## ⚠️ Risks and Mitigations

### Risk 1: Performance with Many Plans

- **Description**: If there are 20+ plans, state detection could slow down the dashboard (20 plans × 200ms = 4 seconds)
- **Mitigation**:
  - Acceptable for Achievement 0.3 (most users have <10 plans)
  - Defer optimization to Achievement 0.4 (caching) or Achievement 2.3 (async loading)
  - Document performance characteristics in docstrings

### Risk 2: Interactive Loop Complexity

- **Description**: The `show()` method's interactive loop (clear → render → input → handle) could be error-prone
- **Mitigation**:
  - Use try-except blocks for input handling
  - Test thoroughly with unit tests and mocks
  - Implement graceful error handling (e.g., invalid input → show message, re-prompt)
  - Follow pattern from Rich library examples

### Risk 3: Status Logic Accuracy

- **Description**: Status emoji logic (pending_fixes, active executions, next_achievements) must match user expectations
- **Mitigation**:
  - Follow clear priority order: fixes > in-progress > ready > none
  - Test all status combinations with unit tests
  - Verify against real plans during manual integration testing
  - Document status logic clearly in docstrings

### Risk 4: Main.py Integration Conflicts

- **Description**: Modifying `LLM/main.py` could conflict with existing command-line argument handling
- **Mitigation**:
  - Keep changes minimal (add dashboard flag, route to dashboard)
  - Preserve existing flags (--version)
  - Test that existing functionality still works
  - Use `len(sys.argv) == 1` to detect no args → launch dashboard

---

## 💡 Design Decisions

### 1. Single File vs Multiple Files

- **Decision**: Single file `main_dashboard.py` for all dashboard logic
- **Rationale**:
  - ~200 lines is manageable in one file
  - Helper functions (create_plan_table, get_status_emoji) are tightly coupled to MainDashboard
  - Simpler imports and testing
  - Can refactor later if file grows too large

### 2. Interactive Loop Pattern

- **Decision**: Use `while True: clear → render → input → handle` pattern
- **Rationale**:
  - Standard pattern for terminal dashboards
  - Clear separation of concerns (render vs input handling)
  - Easy to test with mocks
  - Follows Rich library examples

### 3. Status Priority Order

- **Decision**: Fixes > In Progress > Ready > None
- **Rationale**:
  - Most urgent issues shown first (fixes need immediate attention)
  - Active work shown next (in progress)
  - Ready to execute shown next (actionable)
  - No action shown last (complete or blocked)
  - Matches user mental model

### 4. Placeholder for Plan Selection

- **Decision**: Show message "Plan dashboard coming in Achievement 1.1" instead of implementing
- **Rationale**:
  - Achievement 0.3 scope is main dashboard only
  - Achievement 1.1 will implement plan-specific dashboard
  - Placeholder keeps user informed and prevents confusion
  - Follows incremental development approach

### 5. Default Behavior in main.py

- **Decision**: Dashboard is default when no args provided
- **Rationale**:
  - New users get dashboard immediately (better UX)
  - Existing users can still use command-line args (backward compatible)
  - `--dashboard` flag is explicit but unnecessary (default=True)
  - Aligns with goal of reducing command verbosity

---

## 🔗 Integration Points

**Requires**:

- **Achievement 0.1 (Rich Dashboard Framework)**: `BaseDashboard`, `ui_components`, `utils`
- **Achievement 0.2 (Plan Discovery & State Detection)**: `PlanDiscovery`, `StateDetector`, `PlanState`, `AchievementState`

**Enables**:

- **Achievement 1.1 (Plan-Specific Dashboard)**: `open_plan_dashboard()` will be implemented to call plan-specific dashboard instead of showing placeholder message

**Blocks**:

- Achievement 1.1 cannot start until Achievement 0.3 is complete (plan selection logic needed)

---

## 📋 Next Steps After Design

1. **Execute Achievement 0.3**: Implement the code as described in the `EXECUTION_TASK_LLM-DASHBOARD-CLI_03_01.md` file.
2. **Request Review**: After execution, create a feedback request for Achievement 0.3.
3. **Create APPROVED_03.md**: After review approval.
4. **Design Achievement 0.4**: Proceed to design "Library Integration & Production Patterns" only after Achievement 0.3 is fully executed and approved.

---

## 📊 Success Criteria

**Achievement 0.3 is complete when**:

- [x] SUBPLAN created (this document)
- [ ] EXECUTION_TASK created (EXECUTION_TASK_LLM-DASHBOARD-CLI_03_01.md)
- [ ] `LLM/dashboard/main_dashboard.py` created (~200 lines)
- [ ] `LLM/main.py` integrated (~20 lines added)
- [ ] `tests/LLM/dashboard/test_main_dashboard.py` created (~250 lines, 25 tests)
- [ ] All tests pass (25/25)
- [ ] Test coverage >90%
- [ ] No linter errors
- [ ] Manual integration test successful
- [ ] Dashboard launches on `python LLM/main.py`
- [ ] Dashboard shows all plans with correct states
- [ ] User can select plan or quit
- [ ] APPROVED_03.md created (after review)

---

**SUBPLAN Status**: 📋 Design Phase Complete  
**Next**: Create EXECUTION_TASK_LLM-DASHBOARD-CLI_03_01.md  
**Reference**: EXECUTION_TASK-TEMPLATE.md for structure
