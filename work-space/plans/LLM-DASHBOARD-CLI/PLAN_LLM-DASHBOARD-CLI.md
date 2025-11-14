# PLAN: LLM Methodology Dashboard CLI

**Type**: PLAN  
**Status**: 🚀 Ready to Execute (Enhanced)  
**Priority**: CRITICAL - UX Quick Win  
**Created**: 2025-11-13  
**Enhanced**: 2025-11-13 (Gap Analysis Applied)  
**Goal**: Transform LLM-METHODOLOGY workflow from verbose commands to intuitive dashboard-driven CLI with Rich library, providing instant visibility into plan states and one-key shortcuts for common operations  
**Estimated Effort**: 40-48 hours (was 12-18 hours, revised after gap analysis)

**Parent North Stars**:

- `NORTH_STAR_LLM-METHODOLOGY.md` - LLM methodology excellence vision
- `NORTH_STAR_UNIVERSAL-METHODOLOGY-CLI.md` - Universal CLI platform vision

**Gap Analysis**:

- `work-space/analyses/EXECUTION_ANALYSIS_LLM-DASHBOARD-CLI-PLAN-REVIEW.md` - Comprehensive plan review identifying 8 critical gaps and 6 improvement opportunities. This PLAN has been enhanced to address critical gaps and integrate opportunities 1-2.

---

## 📖 Context for LLM Execution

**What This Plan Is**: Quick-win UX transformation that replaces verbose command-line arguments with an intuitive dashboard interface, addressing the two worst user pain points: command verbosity and lack of state visibility.

**Why Critical**:

**Current Pain Points**:

1. **Verbose Commands**: `python LLM/scripts/generation/generate_prompt.py @PLAN_NAME --achievement 2.3 --interactive` (80+ characters)
2. **No State Visibility**: Users can't see what's ready to execute, what's waiting for review, what needs fixes
3. **Context Switching**: Must manually track plan states across multiple files
4. **Discovery Friction**: Hard to find available plans, achievements, parallel opportunities

**Proposed Solution**:

```bash
# Simple entry point
python LLM/main.py

# Dashboard shows:
┌─ LLM Methodology Dashboard ─────────────────────────────────┐
│                                                              │
│  Active Plans (3)                                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 1. PROMPT-GENERATOR-UX-AND-FOUNDATION                  │ │
│  │    ├─ Last: 3.1 (✅ APPROVED)                          │ │
│  │    ├─ Next: 3.2, 3.3 (🔀 2 parallel available)        │ │
│  │    └─ Status: 🟢 Ready to execute                     │ │
│  │                                                        │ │
│  │ 2. GRAPHRAG-OBSERVABILITY-VALIDATION                   │ │
│  │    ├─ Last: 2.3 (✅ APPROVED)                          │ │
│  │    ├─ Next: 3.1 (⏸️ Waiting for execution)            │ │
│  │    └─ Status: 🟡 Execution in progress                │ │
│  │                                                        │ │
│  │ 3. STAGE-DOMAIN-REFACTOR                               │ │
│  │    ├─ Last: 1.2 (⚠️ FIX_12 waiting)                   │ │
│  │    ├─ Next: Fix 1.2 issues                            │ │
│  │    └─ Status: 🔴 Needs attention                      │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Enter plan number (1-3) or 'q' to quit: _                  │
└──────────────────────────────────────────────────────────────┘

# Direct plan access
python LLM/main.py --plan 1

# Plan-specific dashboard
┌─ PROMPT-GENERATOR-UX-AND-FOUNDATION ─────────────────────────┐
│                                                              │
│  📊 Plan Status                                              │
│  ├─ Progress: 11/18 achievements (61%)                       │
│  ├─ Last Complete: 3.1 (✅ APPROVED_31.md)                   │
│  ├─ Priority: 3 (Polish - Production Ready)                  │
│  └─ Estimated Remaining: 6-10 hours                          │
│                                                              │
│  🎯 Available Actions                                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 1. ▶️  Execute Next (3.2 - Performance Optimization)   │ │
│  │ 2. 🔀 Execute Parallel (3.2 + 3.3 available)           │ │
│  │ 3. 📝 Create SUBPLAN (for 3.2)                         │ │
│  │ 4. ✅ Review Achievement (3.1 complete)                │ │
│  │ 5. 📊 View Achievement Details                         │ │
│  │ 6. 🔙 Back to Plans                                    │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ⚡ Quick Stats                                              │
│  ├─ SUBPLANs: 11 created, 0 waiting                         │
│  ├─ EXECUTIONs: 11 complete, 0 active                       │
│  ├─ Reviews: 11 approved, 0 fixes pending                   │
│  └─ Tests: 346/375 passing (92.3%)                          │
│                                                              │
│  Enter action (1-6): _                                       │
└──────────────────────────────────────────────────────────────┘
```

**Impact**:

- **80% faster workflow**: One key instead of 80+ character commands
- **100% visibility**: Instant state overview, no manual tracking
- **Zero context switching**: Dashboard shows everything in one view
- **Parallel execution discovery**: Highlights parallel opportunities automatically

---

## 📋 Achievement Index

**All Achievements in This Plan** (for sequence reference):

**Priority 0: FOUNDATION (CRITICAL - Core Infrastructure)**

- Achievement 0.1: Rich Dashboard Framework Setup
- Achievement 0.2: Plan Discovery & State Detection
- Achievement 0.3: Main Dashboard Implementation
- Achievement 0.4: Library Integration & Production Patterns (NEW - Gap Fix #1)

**Priority 1: PLAN DASHBOARD (HIGH - Core UX)**

- Achievement 1.1: Plan-Specific Dashboard
- Achievement 1.2: Achievement State Visualization
- Achievement 1.3: Quick Action Shortcuts

**Priority 2: ADVANCED FEATURES (MEDIUM - Power User)**

- Achievement 2.1: Parallel Execution Detection & UI
- Achievement 2.2: Interactive Workflow Execution
- Achievement 2.3: Real-Time State Updates

**Priority 3: POLISH (LOW - Nice to Have)**

- Achievement 3.1: Color Themes & Customization
- Achievement 3.2: Keyboard Shortcuts & Navigation
- Achievement 3.3: Help System & Documentation

**Purpose**:

- Quick reference for achievement sequence
- Enables scripts to detect all achievements without parsing full PLAN
- Shows progress at a glance (✅ = completed via APPROVED feedback)
- Helps detect completion via feedback files (APPROVED_XX.md in execution/feedbacks/)

---

## 🎯 Goal

**Transform LLM-METHODOLOGY workflow from verbose CLI to intuitive dashboard**:

**Primary Goals**:

1. **Eliminate Command Verbosity**: Replace 80+ character commands with single-key actions
2. **Provide State Visibility**: Show all plan states, achievements, reviews in one view
3. **Enable Quick Actions**: One-key shortcuts for common operations (next, parallel, review)
4. **Discover Parallel Opportunities**: Automatically detect and highlight parallel execution options

**Secondary Goals**:

1. **Reduce Context Switching**: All information in dashboard, no file hunting
2. **Improve Discoverability**: Show available plans, achievements, actions
3. **Enhance User Confidence**: Clear status indicators (✅ ⚠️ 🔴 🟢)
4. **Enable Power Users**: Keyboard shortcuts, batch operations

**Result**: **80% faster workflow** with **100% state visibility** and **zero friction** for common operations.

---

## 📖 Problem Statement

**Current State**: Verbose commands, no visibility, manual tracking

**Pain Point 1: Command Verbosity** (80+ characters)

```bash
# Current workflow
python LLM/scripts/generation/generate_prompt.py @PROMPT-GENERATOR-UX-AND-FOUNDATION --achievement 3.2 --interactive

# Problems:
- 80+ characters to type
- Must remember exact paths
- Must know achievement numbers
- Must specify flags every time
```

**Pain Point 2: No State Visibility**

```bash
# Current workflow to check state
ls work-space/plans/PROMPT-GENERATOR-UX-AND-FOUNDATION/execution/feedbacks/
grep "Achievement" work-space/plans/PROMPT-GENERATOR-UX-AND-FOUNDATION/PLAN_*.md
python LLM/scripts/generation/generate_prompt.py @PROMPT-GENERATOR --next

# Problems:
- Must manually check multiple files
- No overview of all plans
- Can't see parallel opportunities
- No indication of what needs attention
```

**Pain Point 3: Context Switching**

```bash
# Current workflow
1. Check PLAN file for achievement index
2. Check execution/feedbacks/ for completion status
3. Check subplans/ for SUBPLAN existence
4. Check execution/ for EXECUTION_TASK status
5. Run generate_prompt.py to see next action

# Problems:
- 5+ file reads to understand state
- Easy to miss FIX files
- Hard to track parallel opportunities
- Cognitive overhead
```

**Proposed Solution**: Single dashboard entry point with Rich library

```bash
# New workflow
python LLM/main.py
# Shows all plans, states, actions in one view
# Press 1 to select plan
# Press 1 to execute next
# Done in 2 keystrokes vs 80+ characters
```

---

## 🎯 Success Metrics

**Quantitative**:

| Metric                       | Before | After | Target |
| ---------------------------- | ------ | ----- | ------ |
| Command Length (avg)         | 80 ch  | 2 ch  | -97%   |
| Time to Execute Next         | 30s    | 3s    | -90%   |
| Files to Check for State     | 5+     | 0     | -100%  |
| Parallel Discovery Time      | 5 min  | 0s    | -100%  |
| Context Switches per Action  | 3-5    | 0     | -100%  |
| User Confidence (subjective) | 3/10   | 9/10  | +200%  |

**Qualitative**:

- ✅ Users can see all plan states at a glance
- ✅ Users can execute next achievement in 2 keystrokes
- ✅ Users know when parallel execution is available
- ✅ Users see FIX files immediately
- ✅ Users don't need to remember commands

---

## 🏗️ Technical Architecture

### Core Components

**1. Main Entry Point** (`LLM/main.py`):

```python
"""
LLM Methodology Dashboard - Main Entry Point

Usage:
    python LLM/main.py              # Open main dashboard
    python LLM/main.py --plan 1     # Open plan 1 dashboard
    python LLM/main.py --plan @NAME # Open plan by name
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from LLM.dashboard.main_dashboard import MainDashboard
from LLM.dashboard.plan_dashboard import PlanDashboard

def main():
    console = Console()

    # Parse arguments
    args = parse_args()

    if args.plan:
        # Direct to plan dashboard
        dashboard = PlanDashboard(args.plan, console)
        dashboard.show()
    else:
        # Show main dashboard
        dashboard = MainDashboard(console)
        dashboard.show()

if __name__ == "__main__":
    main()
```

**2. Dashboard Framework** (`LLM/dashboard/`):

```
LLM/dashboard/
├── __init__.py
├── main_dashboard.py       # Main dashboard (plan list)
├── plan_dashboard.py       # Plan-specific dashboard
├── state_detector.py       # Detect plan/achievement states
├── action_executor.py      # Execute user actions
├── parallel_detector.py    # Detect parallel opportunities
└── ui_components.py        # Reusable Rich UI components
```

**3. State Detection** (`LLM/dashboard/state_detector.py`):

```python
class StateDetector:
    """Detect plan and achievement states from filesystem."""

    def get_plan_state(self, plan_path: Path) -> PlanState:
        """Get complete plan state."""
        return PlanState(
            last_achievement=self._get_last_complete(),
            next_achievements=self._get_next_available(),
            parallel_opportunities=self._detect_parallel(),
            pending_reviews=self._get_pending_reviews(),
            pending_fixes=self._get_pending_fixes(),
            subplans_waiting=self._get_subplans_waiting(),
            executions_active=self._get_active_executions(),
        )

    def _get_last_complete(self) -> Optional[str]:
        """Get last completed achievement from APPROVED files."""
        feedbacks_dir = self.plan_path / "execution" / "feedbacks"
        approved_files = sorted(feedbacks_dir.glob("APPROVED_*.md"))
        if approved_files:
            # Extract achievement number from filename
            return self._extract_achievement_num(approved_files[-1])
        return None

    def _detect_parallel(self) -> List[str]:
        """Detect parallel execution opportunities."""
        # Use parallel execution framework from case study
        # Check achievement dependencies
        # Return list of achievements that can run in parallel
        pass
```

**4. Action Executor** (`LLM/dashboard/action_executor.py`):

```python
class ActionExecutor:
    """Execute user actions from dashboard."""

    def execute_next(self, plan_path: Path):
        """Execute next achievement."""
        # Call generate_prompt.py with --next
        subprocess.run([
            "python", "LLM/scripts/generation/generate_prompt.py",
            f"@{plan_path.name}", "--next", "--interactive"
        ])

    def execute_parallel(self, plan_path: Path, achievements: List[str]):
        """Execute multiple achievements in parallel."""
        # Launch multiple generate_prompt.py instances
        # Or provide instructions for parallel execution
        pass

    def create_subplan(self, plan_path: Path, achievement: str):
        """Create SUBPLAN for achievement."""
        subprocess.run([
            "python", "LLM/scripts/generation/generate_subplan_prompt.py",
            f"@{plan_path.name}", "--achievement", achievement
        ])
```

**5. UI Components** (`LLM/dashboard/ui_components.py`):

```python
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

def create_plan_table(plans: List[PlanState]) -> Table:
    """Create Rich table for plan list."""
    table = Table(title="Active Plans", show_header=True)
    table.add_column("#", style="cyan", width=3)
    table.add_column("Plan", style="bold")
    table.add_column("Last", style="green")
    table.add_column("Next", style="yellow")
    table.add_column("Status", style="magenta")

    for i, plan in enumerate(plans, 1):
        table.add_row(
            str(i),
            plan.name,
            plan.last_achievement or "None",
            plan.next_achievements_str,
            plan.status_emoji
        )

    return table

def create_action_menu(actions: List[Action]) -> Panel:
    """Create Rich panel for action menu."""
    content = "\n".join([
        f"{i}. {action.emoji} {action.label}"
        for i, action in enumerate(actions, 1)
    ])
    return Panel(content, title="Available Actions", border_style="blue")
```

---

## 🧪 Testing Strategy (Gap Fix #2)

**Coverage Target**: >80% code coverage across all dashboard modules

**Test-Driven Development Workflow**:

- Write tests FIRST for each achievement
- Red → Green → Refactor cycle
- Update tests when design changes
- Run tests on every commit

**Test Levels**:

### 1. Unit Tests (per module)

**Location**: `tests/LLM/dashboard/`

**Files**:

- `test_plan_discovery.py` - Test plan finding and parsing
- `test_state_detector.py` - Test state detection logic
- `test_action_executor.py` - Test action execution (mocked)
- `test_ui_components.py` - Test Rich component creation
- `test_parallel_detector.py` - Test parallel opportunity detection

**Strategy**:

- Mock filesystem operations (no real file I/O in unit tests)
- Use pytest fixtures for common test data
- Test edge cases (missing files, malformed data, empty directories)
- Validate error handling (exceptions raised correctly)

### 2. Integration Tests

**Location**: `tests/LLM/dashboard/test_dashboard_integration.py`

**Tests**:

- Dashboard + generate_prompt.py integration
- Dashboard + state detection integration
- End-to-end user workflows (next, parallel, review)
- Real filesystem operations with temporary directories

**Strategy**:

- Create temporary plan structures for testing
- Verify subprocess calls to generate_prompt.py
- Test actual file creation (APPROVED_XX.md, etc.)
- Validate error propagation across modules

### 3. Performance Tests

**Location**: `tests/LLM/dashboard/test_dashboard_performance.py`

**Tests**:

- Dashboard load time <500ms for 10 plans
- State detection <100ms per plan
- Cache hit rate >80%
- Total scan time <1s for 50 plans

**Strategy**:

- Create realistic plan structures (multiple sizes)
- Measure actual timing with `time.perf_counter()`
- Validate caching effectiveness
- Profile hot paths if performance targets not met

### 4. User Acceptance Tests

**Manual Testing Checklist**:

- ✅ Dashboard displays all active plans
- ✅ Plan selection works (keyboard input)
- ✅ Next achievement execution launches correctly
- ✅ Parallel opportunities detected and displayed
- ✅ FIX files detected and highlighted
- ✅ Error messages are clear and actionable
- ✅ Performance feels responsive (<1s interactions)

**Test Scenarios**:

- New user: First dashboard open, select plan, execute next
- Power user: Navigate quickly, use shortcuts, batch operations
- Error scenarios: Missing files, invalid input, subprocess failures
- Edge cases: Empty plans, no achievements, 50+ plans

---

## 🚨 Error Handling Strategy (Gap Fix #4)

**Approach**: Structured exceptions with actionable suggestions (from Achievement 3.1 patterns)

**Error Categories**:

### 1. Recoverable Errors (show warning, continue)

**Examples**:

- Plan file not found → Skip plan, log warning, show in dashboard with "⚠️ Not Found"
- State detection fails → Show "Unknown" state, allow manual refresh
- Achievement Index missing → Warn user, allow manual achievement entry
- Cache read error → Clear cache, reload from filesystem

**Handling**:

```python
try:
    plan_state = state_detector.get_plan_state(plan_path)
except PlanNotFoundError:
    logger.warning(f"Plan not found: {plan_path}")
    plan_state = PlanState(name=plan_path.name, status="not_found")
    # Continue with other plans
```

### 2. User-Facing Errors (show formatted error, re-prompt)

**Examples**:

- Invalid user input → Show error, re-prompt with valid options
- Action execution fails → Show command output, error, suggestions
- Subprocess failure → Show error with subprocess stderr, suggest fixes
- File permission error → Show error, suggest chmod commands

**Handling**:

```python
from LLM.scripts.generation.exceptions import (
    format_error_with_suggestions,
    InvalidInputError
)

try:
    action = executor.execute_action(user_input)
except InvalidInputError as e:
    error_output = format_error_with_suggestions(e, use_colors=True)
    console.print(error_output)
    console.print("\n📋 Error copied to clipboard")
    # Don't clear screen, let user see error
    # Re-prompt for input
```

### 3. Fatal Errors (show error, exit gracefully)

**Examples**:

- Rich library import fails → Show error, suggest `pip install rich`
- Workspace not found → Show error, suggest running from project root
- Python version incompatible → Show error, suggest Python 3.8+

**Handling**:

```python
try:
    from rich.console import Console
except ImportError:
    print("ERROR: Rich library not found")
    print("Install: pip install rich>=13.0.0")
    sys.exit(1)
```

**Error Display**:

- Use `format_error_with_suggestions` from Achievement 3.1
- Color-coded: 🔴 errors (red), 💡 suggestions (yellow), ℹ️ details (blue)
- Auto-copy error to clipboard for easy reporting
- Preserve dashboard state (don't clear screen on recoverable errors)

**Error Logging**:

- Log all errors with structured logging (from Achievement 3.1)
- Include context: `dashboard_type`, `plan`, `action`, `user_input`
- Log to file: `LLM/dashboard/dashboard.log`
- Rotate logs (keep last 10MB or 7 days)

**Custom Exceptions** (to be created in `LLM/dashboard/exceptions.py`):

```python
from LLM.scripts.generation.exceptions import ApplicationError

class DashboardError(ApplicationError):
    """Base exception for dashboard errors."""
    pass

class PlanLoadError(DashboardError):
    """Raised when plan cannot be loaded."""
    pass

class StateDetectionError(DashboardError):
    """Raised when state detection fails."""
    pass

class ActionExecutionError(DashboardError):
    """Raised when action execution fails."""
    pass
```

---

## ⚡ Performance Requirements (Gap Fix #6)

**Overall Target**: Dashboard feels instant (<1s for common operations)

**Dashboard Load Time**:

- **Target**: <500ms for up to 10 plans
- **Target**: <1s for up to 50 plans
- **Target**: <3s for up to 100 plans
- **Mitigation**: Cache discovery results, lazy load state, parallel processing

**State Detection Performance**:

- **Target**: <100ms per plan (cached)
- **Target**: <1s total for 10 plans (parallel)
- **Target**: <5s total for 50 plans (parallel)
- **Mitigation**: Parallel state detection, aggressive caching, compiled regex

**Action Execution Latency**:

- **Target**: <100ms to launch subprocess
- **Target**: <200ms to show "⏳ Executing..." message
- **Target**: <3s for user to see action result
- **Mitigation**: Background execution, async subprocess, immediate UI feedback

**Caching Requirements**:

- **Target**: >80% cache hit rate (from Achievement 3.2)
- **TTL**: 5 minutes (balance freshness vs performance)
- **Max size**: 50 plans cached, 100 state objects
- **Invalidation**: Mtime-based (automatic on file changes)

**UI Responsiveness**:

- **Target**: <50ms for keyboard input registration
- **Target**: <100ms for screen refresh
- **Target**: <500ms for state updates after action
- **Mitigation**: Rich library async rendering, efficient re-rendering

**Validation Strategy**:

- Performance tests in `test_dashboard_performance.py`
- Benchmark with realistic plan counts (1, 10, 50, 100 plans)
- Profile using `cProfile` or `py-spy` to identify bottlenecks
- Monitor cache hit rates in production logs
- User feedback on "feels fast" vs "feels slow"

**Performance Budget**:

```
User Action: "Open dashboard"
├─ Load Rich (50ms)
├─ Discover plans (100ms, cached)
├─ Detect state for 10 plans (500ms, parallel)
├─ Render dashboard (100ms)
└─ Total: 750ms ✅ (<1s target)

User Action: "Select plan"
├─ Load plan details (50ms, cached)
├─ Detect plan state (80ms, cached)
├─ Render plan dashboard (50ms)
└─ Total: 180ms ✅ (<500ms target)

User Action: "Execute next"
├─ Launch subprocess (50ms)
├─ Show executing message (50ms)
└─ Total: 100ms ✅ (<200ms target)
```

**Degradation Strategy** (if performance targets not met):

- Show loading spinner for operations >1s
- Lazy load: Show plan list first, load states on demand
- Progressive rendering: Show cached data first, update with fresh data
- User control: "Quick mode" (cached only) vs "Fresh mode" (force refresh)

---

## 🔗 Library Integration (Gap Fix #1)

**Purpose**: Integrate production-ready libraries from Achievements 3.1-3.3 for consistency, observability, and performance.

**Libraries to Integrate**:

### 1. Error Handling Library

**From**: `core/libraries/error_handling/` (Achievement 3.1)

**Integration**:

```python
from core.libraries.error_handling import ApplicationError
from LLM.scripts.generation.exceptions import format_error_with_suggestions

# Create dashboard-specific exceptions
class DashboardError(ApplicationError):
    """Base exception for all dashboard errors."""
    pass

# Use structured error handling
try:
    plan_state = detect_state(plan_path)
except PlanNotFoundError as e:
    error_msg = format_error_with_suggestions(e, use_colors=True)
    console.print(error_msg)
```

**Benefits**: Consistent error experience, color-coded output, actionable suggestions

### 2. Structured Logging Library

**From**: `core/libraries/logging/` (Achievement 3.1)

**Integration**:

```python
from core.libraries.logging import get_logger, set_log_context

logger = get_logger(__name__)

def show_dashboard(plan_name):
    set_log_context(
        dashboard='main',
        plan=plan_name,
        user_action='show_dashboard'
    )

    logger.info("Dashboard opened", extra={'plan_count': len(plans)})
    # ... dashboard logic ...
    logger.info("Dashboard closed", extra={'duration': timer.elapsed()})
```

**Benefits**: Searchable logs, context propagation, JSON output for analysis

### 3. Caching Library

**From**: `core/libraries/caching/` (Achievement 3.2)

**Integration**:

```python
from core.libraries.caching import cached
import os

@cached(
    max_size=50,
    ttl=300,
    key_func=lambda self, plan_path: f"{plan_path}:{os.path.getmtime(plan_path)}",
    name="plan_state_cache"
)
def get_plan_state(self, plan_path):
    """Get plan state with mtime-based cache invalidation."""
    # ... state detection logic ...
```

**Benefits**: 582x speedup for cached operations, automatic invalidation, >80% hit rate

### 4. Metrics Library

**From**: `core/libraries/metrics/` (Achievement 3.2)

**Integration**:

```python
from core.libraries.metrics import Counter, Histogram, Timer, MetricRegistry

# Define metrics
dashboard_actions = Counter(
    'dashboard_actions_total',
    description='User actions in dashboard',
    labels=['action_type', 'status']
)

dashboard_load_time = Histogram(
    'dashboard_load_duration_seconds',
    description='Dashboard load time',
    labels=['dashboard_type']
)

# Register metrics
registry = MetricRegistry.get_instance()
registry.register(dashboard_actions)
registry.register(dashboard_load_time)

# Use metrics
with Timer() as timer:
    render_dashboard()

dashboard_load_time.observe(timer.elapsed(), labels={'dashboard_type': 'main'})
dashboard_actions.inc(labels={'action_type': 'show_dashboard', 'status': 'success'})
```

**Benefits**: Prometheus-compatible metrics, performance monitoring, usage analytics

### 5. Compiled Regex Patterns

**From**: Achievement 3.2 patterns

**Integration**:

```python
import re

# Module-level compilation (10-20% performance gain)
ACHIEVEMENT_NUM_PATTERN = re.compile(r'(\d+)\.(\d+)')
APPROVED_FILE_PATTERN = re.compile(r'APPROVED_(\d+)\.md')
FIX_FILE_PATTERN = re.compile(r'FIX_(\d+)\.md')

def extract_achievement_num(filename):
    """Extract achievement number from filename."""
    match = APPROVED_FILE_PATTERN.match(filename)
    if match:
        num = match.group(1)
        return f"{num[0]}.{num[1:]}"
    return None
```

**Benefits**: Faster pattern matching, consistent patterns across modules

**References**:

- `LLM/scripts/generation/LIBRARY_INTEGRATION_GUIDE.md` - Complete patterns and examples
- `LLM/docs/ERROR_HANDLING_PATTERNS.md` - Error handling details
- `LLM/docs/PERFORMANCE_OPTIMIZATION_GUIDE.md` - Caching and metrics details

---

## 📋 Achievements

### Priority 0: FOUNDATION (CRITICAL - Core Infrastructure)

**Achievement 0.1**: Rich Dashboard Framework Setup

**Purpose**: Set up Rich library and basic dashboard framework

**What**:

1. **Install Rich Library**:

   - Add `rich>=13.0.0` to requirements.txt
   - Install and verify

2. **Create Dashboard Structure**:

   ```
   LLM/
   ├── main.py                    # Entry point
   └── dashboard/
       ├── __init__.py
       ├── base_dashboard.py      # Base dashboard class
       ├── ui_components.py       # Reusable UI components
       └── utils.py               # Helper functions
   ```

3. **Base Dashboard Class**:

   ```python
   class BaseDashboard:
       """Base class for all dashboards."""

       def __init__(self, console: Console):
           self.console = console

       def show(self):
           """Show dashboard."""
           raise NotImplementedError

       def clear(self):
           """Clear screen."""
           self.console.clear()

       def render_panel(self, content, title, **kwargs):
           """Render Rich panel."""
           return Panel(content, title=title, **kwargs)
   ```

4. **Basic UI Components**:
   - Panel wrapper
   - Table wrapper
   - Prompt wrapper
   - Status indicators (✅ ⚠️ 🔴 🟢)

**Deliverables**:

- `requirements.txt` updated with Rich
- `LLM/main.py` entry point
- `LLM/dashboard/` structure created
- `base_dashboard.py` with core functionality
- `ui_components.py` with reusable components
- Tests for UI components

**Effort**: 2-3 hours

---

**Achievement 0.2**: Plan Discovery & State Detection

**Purpose**: Detect all plans and their states from filesystem

**What**:

1. **Plan Discovery**:

   ```python
   class PlanDiscovery:
       """Discover all plans in work-space/plans/."""

       def get_all_plans(self) -> List[Path]:
           """Get all plan directories."""
           plans_dir = Path("work-space/plans")
           return [
               p for p in plans_dir.iterdir()
               if p.is_dir() and not p.name.startswith(".")
           ]

       def get_plan_file(self, plan_dir: Path) -> Optional[Path]:
           """Get PLAN_*.md file in directory."""
           plan_files = list(plan_dir.glob("PLAN_*.md"))
           return plan_files[0] if plan_files else None
   ```

2. **State Detection**:

   ```python
   class StateDetector:
       """Detect plan and achievement states."""

       def get_plan_state(self, plan_path: Path) -> PlanState:
           """Get complete plan state."""
           return PlanState(
               name=self._extract_name(plan_path),
               last_achievement=self._get_last_complete(plan_path),
               next_achievements=self._get_next_available(plan_path),
               pending_reviews=self._get_pending_reviews(plan_path),
               pending_fixes=self._get_pending_fixes(plan_path),
               progress=self._calculate_progress(plan_path),
           )

       def _get_last_complete(self, plan_path: Path) -> Optional[str]:
           """Get last completed achievement from APPROVED files."""
           feedbacks_dir = plan_path / "execution" / "feedbacks"
           if not feedbacks_dir.exists():
               return None

           approved_files = sorted(feedbacks_dir.glob("APPROVED_*.md"))
           if approved_files:
               # Extract achievement number from APPROVED_31.md -> "3.1"
               filename = approved_files[-1].stem
               num = filename.replace("APPROVED_", "")
               return f"{num[0]}.{num[1:]}"
           return None

       def _get_pending_fixes(self, plan_path: Path) -> List[str]:
           """Get achievements with pending FIX files."""
           feedbacks_dir = plan_path / "execution" / "feedbacks"
           if not feedbacks_dir.exists():
               return []

           fix_files = feedbacks_dir.glob("FIX_*.md")
           return [self._extract_achievement_num(f) for f in fix_files]
   ```

3. **Achievement Index Parser**:
   ```python
   def parse_achievement_index(plan_file: Path) -> List[str]:
       """Parse Achievement Index from PLAN file."""
       # Read PLAN file
       # Find "## 📋 Achievement Index" section
       # Extract all achievement numbers (X.Y format)
       # Return list of achievement numbers
       pass
   ```

**Deliverables**:

- `LLM/dashboard/plan_discovery.py`
- `LLM/dashboard/state_detector.py`
- `LLM/dashboard/models.py` (PlanState, AchievementState dataclasses)
- Tests for discovery and state detection
- Integration with existing `utils.py` functions

**Effort**: 3-4 hours

---

**Achievement 0.3**: Main Dashboard Implementation

**Purpose**: Implement main dashboard showing all plans

**What**:

1. **Main Dashboard Class**:

   ```python
   class MainDashboard(BaseDashboard):
       """Main dashboard showing all plans."""

       def __init__(self, console: Console):
           super().__init__(console)
           self.discovery = PlanDiscovery()
           self.state_detector = StateDetector()

       def show(self):
           """Show main dashboard."""
           while True:
               self.clear()
               self.render_header()
               self.render_plans()
               self.render_prompt()

               choice = self.get_user_input()
               if choice == 'q':
                   break
               elif choice.isdigit():
                   self.open_plan_dashboard(int(choice))

       def render_plans(self):
           """Render plan list table."""
           plans = self.discovery.get_all_plans()
           plan_states = [
               self.state_detector.get_plan_state(p)
               for p in plans
           ]

           table = create_plan_table(plan_states)
           self.console.print(table)
   ```

2. **Plan Table Rendering**:

   ```python
   def create_plan_table(plan_states: List[PlanState]) -> Table:
       """Create Rich table for plan list."""
       table = Table(
           title="Active Plans",
           show_header=True,
           header_style="bold cyan"
       )

       table.add_column("#", style="cyan", width=3)
       table.add_column("Plan", style="bold", width=40)
       table.add_column("Last", style="green", width=15)
       table.add_column("Next", style="yellow", width=20)
       table.add_column("Status", style="magenta", width=15)

       for i, plan in enumerate(plan_states, 1):
           status_emoji = get_status_emoji(plan)
           next_str = format_next_achievements(plan.next_achievements)

           table.add_row(
               str(i),
               plan.name,
               plan.last_achievement or "None",
               next_str,
               status_emoji
           )

       return table
   ```

3. **Status Indicators**:
   ```python
   def get_status_emoji(plan: PlanState) -> str:
       """Get status emoji for plan."""
       if plan.pending_fixes:
           return "🔴 Needs attention"
       elif plan.executions_active:
           return "🟡 In progress"
       elif plan.next_achievements:
           return "🟢 Ready to execute"
       else:
           return "⚪ No next action"
   ```

**Deliverables**:

- `LLM/dashboard/main_dashboard.py`
- `LLM/main.py` integration
- Rich table rendering for plans
- Status indicators and emojis
- User input handling
- Tests for main dashboard

**Effort**: 2-3 hours

---

**Achievement 0.4**: Library Integration & Production Patterns (NEW - Gap Fix #1)

**Purpose**: Integrate production-ready libraries from Achievements 3.1-3.3 for consistency, observability, and performance

**What**:

1. **Error Handling Integration**:

   ```python
   # LLM/dashboard/exceptions.py
   from LLM.scripts.generation.exceptions import ApplicationError

   class DashboardError(ApplicationError):
       """Base exception for dashboard errors."""
       pass

   class PlanLoadError(DashboardError):
       """Raised when plan cannot be loaded."""
       pass

   class StateDetectionError(DashboardError):
       """Raised when state detection fails."""
       pass

   class ActionExecutionError(DashboardError):
       """Raised when action execution fails."""
       pass

   class InvalidUserInputError(DashboardError):
       """Raised when user input is invalid."""
       pass
   ```

   - Use `format_error_with_suggestions` for all user-facing errors
   - Color-coded error output (red errors, yellow suggestions)
   - Auto-copy errors to clipboard
   - Structured exceptions with context and suggestions

2. **Structured Logging Integration**:

   ```python
   # All dashboard modules
   from core.libraries.logging import get_logger, set_log_context

   logger = get_logger(__name__)

   def show_dashboard(plan_name):
       set_log_context(
           dashboard='main',
           plan=plan_name,
           user_action='show_dashboard'
       )

       logger.info("Dashboard opened", extra={'plan_count': len(plans)})
       # ... logic ...
       logger.info("Dashboard closed", extra={'duration': timer.elapsed()})
   ```

   - Replace all `print` statements with structured logging
   - Log to file: `LLM/dashboard/dashboard.log`
   - JSON log format for easy searching
   - Context propagation across all modules

3. **Performance Optimization (Caching)**:

   ```python
   from core.libraries.caching import cached
   import os

   @cached(
       max_size=50,
       ttl=300,
       key_func=lambda self, plan_path: f"{plan_path}:{os.path.getmtime(plan_path)}",
       name="plan_state_cache"
   )
   def get_plan_state(self, plan_path):
       """Get plan state with mtime-based cache invalidation."""
       # ... state detection ...
   ```

   - Cache plan discovery results
   - Cache state detection (mtime-based invalidation)
   - Compile regex patterns at module level
   - Target: >80% cache hit rate

4. **Metrics Collection**:

   ```python
   from core.libraries.metrics import Counter, Histogram, Timer, MetricRegistry

   # Define metrics
   dashboard_actions = Counter(
       'dashboard_actions_total',
       labels=['action_type', 'status']
   )

   dashboard_load_time = Histogram(
       'dashboard_load_duration_seconds',
       labels=['dashboard_type']
   )

   # Register
   registry = MetricRegistry.get_instance()
   registry.register(dashboard_actions)
   registry.register(dashboard_load_time)
   ```

   - Track all user actions
   - Monitor dashboard performance
   - Collect cache hit rates
   - Export Prometheus-compatible metrics

5. **Compiled Regex Patterns**:

   ```python
   import re

   # Module level (10-20% performance gain)
   ACHIEVEMENT_NUM_PATTERN = re.compile(r'(\d+)\.(\d+)')
   APPROVED_FILE_PATTERN = re.compile(r'APPROVED_(\d+)\.md')
   FIX_FILE_PATTERN = re.compile(r'FIX_(\d+)\.md')
   SUBPLAN_FILE_PATTERN = re.compile(r'SUBPLAN_.*_(\d+)\.md')
   ```

**Deliverables**:

- `LLM/dashboard/exceptions.py` - Custom dashboard exceptions
- All modules use structured logging (get_logger, set_log_context)
- State detection cached (>80% hit rate target)
- Metrics defined and registered
- Compiled regex patterns at module level
- Integration tests for library usage
- Performance tests validate caching

**Success Criteria**:

- All errors use structured exceptions with suggestions
- All output uses structured logging (no print statements)
- Cache hit rate >80% for repeated operations
- Metrics exportable in Prometheus format
- Performance tests pass (<500ms dashboard load for 10 plans)

**References**:

- `LLM/scripts/generation/LIBRARY_INTEGRATION_GUIDE.md` - Complete patterns
- `LLM/docs/ERROR_HANDLING_PATTERNS.md` - Error handling details
- `LLM/docs/PERFORMANCE_OPTIMIZATION_GUIDE.md` - Caching and metrics

**Effort**: 3-4 hours

---

### Priority 1: PLAN DASHBOARD (HIGH - Core UX)

**Achievement 1.1**: Plan-Specific Dashboard

**Purpose**: Implement plan-specific dashboard with detailed information

**What**:

1. **Plan Dashboard Class**:

   ```python
   class PlanDashboard(BaseDashboard):
       """Plan-specific dashboard."""

       def __init__(self, plan_id: Union[int, str], console: Console):
           super().__init__(console)
           self.plan_path = self._resolve_plan(plan_id)
           self.state = StateDetector().get_plan_state(self.plan_path)

       def show(self):
           """Show plan dashboard."""
           while True:
               self.clear()
               self.render_header()
               self.render_status()
               self.render_actions()
               self.render_stats()

               choice = self.get_user_input()
               if choice == '6':  # Back
                   break
               else:
                   self.handle_action(choice)
   ```

2. **Status Section**:

   ```python
   def render_status(self):
       """Render plan status section."""
       content = Text()
       content.append("📊 Plan Status\n", style="bold cyan")
       content.append(f"├─ Progress: {self.state.progress_str}\n")
       content.append(f"├─ Last Complete: {self.state.last_achievement}\n")
       content.append(f"├─ Priority: {self.state.current_priority}\n")
       content.append(f"└─ Estimated Remaining: {self.state.estimated_hours}h\n")

       panel = Panel(content, border_style="cyan")
       self.console.print(panel)
   ```

3. **Quick Stats Section**:

   ```python
   def render_stats(self):
       """Render quick stats section."""
       stats = self.state.get_stats()

       content = Text()
       content.append("⚡ Quick Stats\n", style="bold yellow")
       content.append(f"├─ SUBPLANs: {stats.subplans_created} created, {stats.subplans_waiting} waiting\n")
       content.append(f"├─ EXECUTIONs: {stats.executions_complete} complete, {stats.executions_active} active\n")
       content.append(f"├─ Reviews: {stats.reviews_approved} approved, {stats.reviews_pending} pending\n")
       content.append(f"└─ Tests: {stats.tests_passing}/{stats.tests_total} passing ({stats.tests_percentage}%)\n")

       panel = Panel(content, border_style="yellow")
       self.console.print(panel)
   ```

**Deliverables**:

- `LLM/dashboard/plan_dashboard.py`
- Plan resolution (by number or @name)
- Status section rendering
- Stats section rendering
- Navigation between dashboards
- Tests for plan dashboard

**Effort**: 3-4 hours

---

**Achievement 1.2**: Achievement State Visualization

**Purpose**: Show detailed achievement states and dependencies

**What**:

1. **Achievement List Rendering**:

   ```python
   def render_achievements(self):
       """Render achievement list with states."""
       achievements = self.state.get_all_achievements()

       table = Table(
           title="Achievements",
           show_header=True,
           header_style="bold cyan"
       )

       table.add_column("Achievement", style="bold", width=15)
       table.add_column("Title", width=40)
       table.add_column("Status", width=20)
       table.add_column("Action", width=20)

       for ach in achievements:
           status_str = self._format_status(ach)
           action_str = self._format_action(ach)

           table.add_row(
               ach.number,
               ach.title,
               status_str,
               action_str
           )

       self.console.print(table)
   ```

2. **Status Formatting**:

   ```python
   def _format_status(self, achievement: Achievement) -> str:
       """Format achievement status."""
       if achievement.approved:
           return "✅ APPROVED"
       elif achievement.fix_pending:
           return "⚠️ FIX pending"
       elif achievement.execution_active:
           return "🔄 In progress"
       elif achievement.subplan_exists:
           return "📝 SUBPLAN ready"
       else:
           return "⏸️ Not started"
   ```

3. **Dependency Visualization**:

   ```python
   def render_dependencies(self, achievement: str):
       """Show achievement dependencies."""
       deps = self.state.get_dependencies(achievement)

       tree = Tree(f"[bold]{achievement}[/bold]")

       if deps.depends_on:
           depends_node = tree.add("[yellow]Depends On[/yellow]")
           for dep in deps.depends_on:
               depends_node.add(f"[cyan]{dep}[/cyan]")

       if deps.blocks:
           blocks_node = tree.add("[red]Blocks[/red]")
           for blocked in deps.blocks:
               blocks_node.add(f"[magenta]{blocked}[/magenta]")

       self.console.print(tree)
   ```

4. **Plan Health Score** (NEW - Opportunity #2):

   ```python
   def calculate_health_score(self, plan_state: PlanState) -> HealthScore:
       """Calculate overall plan health score (0-100)."""
       score = 0

       # 30 points: Achievement completion rate
       if plan_state.total_achievements > 0:
           completion_rate = len(plan_state.approved) / plan_state.total_achievements
           score += 30 * completion_rate

       # 20 points: No pending fixes
       if not plan_state.pending_fixes:
           score += 20

       # 20 points: No stale executions (>7 days old)
       if not plan_state.stale_executions:
           score += 20

       # 15 points: Test pass rate
       if plan_state.test_pass_rate:
           score += 15 * (plan_state.test_pass_rate / 100)

       # 15 points: Documentation complete
       if plan_state.documentation_complete:
           score += 15

       return HealthScore(
           score=score,
           status=self._get_health_status(score),
           emoji=self._get_health_emoji(score)
       )

   def _get_health_status(self, score: float) -> str:
       """Get health status from score."""
       if score >= 95:
           return "Excellent"
       elif score >= 80:
           return "Good"
       elif score >= 60:
           return "Fair"
       else:
           return "Needs Attention"

   def _get_health_emoji(self, score: float) -> str:
       """Get health emoji from score."""
       if score >= 95:
           return "🟢"
       elif score >= 80:
           return "🟡"
       elif score >= 60:
           return "🟠"
       else:
           return "🔴"

   def render_health_score(self, health: HealthScore):
       """Render health score in dashboard."""
       panel = Panel(
           f"{health.emoji} Score: {health.score:.0f}/100 - {health.status}",
           title="Plan Health",
           border_style="green" if health.score >= 80 else "yellow"
       )
       self.console.print(panel)
   ```

   **Display in Dashboard**:

   ```
   ┌─ Plan Health ────────────────────┐
   │ 🟢 Score: 87/100 - Good          │
   │                                  │
   │ Breakdown:                       │
   │ ✅ Completion: 26/30 (11/18 achv)│
   │ ✅ No pending fixes: 20/20       │
   │ ⚠️ Stale execution: 0/20         │
   │ ✅ Tests: 14/15 (92%)            │
   │ ✅ Docs complete: 15/15          │
   └──────────────────────────────────┘
   ```

   **Benefits**:

   - Quick visual health indicator
   - Encourages completing stale work
   - Highlights problems immediately
   - Gamifies plan completeness

**Deliverables**:

- Achievement list rendering
- Status formatting with emojis
- Dependency visualization
- Progress bar for plan completion
- Plan Health Score calculation and display (NEW - Opportunity #2)
- Tests for achievement visualization
- Tests for health score calculation

**Effort**: 3-4 hours (was 2-3 hours, +1 hour for health score)

---

**Achievement 1.3**: Quick Action Shortcuts

**Purpose**: Implement one-key shortcuts for common actions

**What**:

1. **Action Menu**:

   ```python
   def render_actions(self):
       """Render action menu."""
       actions = self._get_available_actions()

       content = Text()
       content.append("🎯 Available Actions\n", style="bold green")

       for i, action in enumerate(actions, 1):
           content.append(f"{i}. {action.emoji} {action.label}\n")

       panel = Panel(content, border_style="green")
       self.console.print(panel)
   ```

2. **Action Executor Integration**:

   ```python
   def handle_action(self, choice: str):
       """Handle user action choice."""
       actions = {
           '1': self.execute_next,
           '2': self.execute_parallel,
           '3': self.create_subplan,
           '4': self.create_execution,
           '5': self.review_achievement,
       }

       action = actions.get(choice)
       if action:
           action()
       else:
           self.console.print("[red]Invalid choice[/red]")

   def execute_next(self):
       """Execute next achievement."""
       executor = ActionExecutor(self.plan_path)
       executor.execute_next()
   ```

3. **Command Building**:

   ```python
   class ActionExecutor:
       """Execute user actions."""

       def execute_next(self):
           """Execute next achievement."""
           cmd = [
               "python",
               "LLM/scripts/generation/generate_prompt.py",
               f"@{self.plan_path.name}",
               "--next",
               "--interactive"
           ]

           subprocess.run(cmd)

       def create_subplan(self, achievement: str):
           """Create SUBPLAN for achievement."""
           cmd = [
               "python",
               "LLM/scripts/generation/generate_subplan_prompt.py",
               f"@{self.plan_path.name}",
               "--achievement", achievement
           ]

           subprocess.run(cmd)
   ```

4. **Documentation Quick Access** (NEW - Opportunity #1):

   ```python
   def render_actions_with_docs(self):
       """Render action menu with documentation links."""
       actions = [
           Action('1', '▶️', 'Execute Next Achievement'),
           Action('2', '🔀', 'Execute Parallel'),
           Action('3', '📝', 'Create SUBPLAN'),
           Action('4', '✅', 'Review Achievement'),
           Action('5', '📚', 'View Documentation'),  # NEW
           Action('6', '🔙', 'Back to Plans'),
       ]

       # ... render actions ...

   def open_documentation(self):
       """Open documentation menu."""
       docs = [
           ('1', 'Library Integration Guide', 'LLM/scripts/generation/LIBRARY_INTEGRATION_GUIDE.md'),
           ('2', 'Error Handling Patterns', 'LLM/docs/ERROR_HANDLING_PATTERNS.md'),
           ('3', 'Performance Optimization', 'LLM/docs/PERFORMANCE_OPTIMIZATION_GUIDE.md'),
           ('4', 'SUBPLAN Workflow Guide', 'LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md'),
           ('5', 'Main README', 'LLM/scripts/generation/README.md'),
           ('6', 'Troubleshooting', 'LLM/scripts/generation/TROUBLESHOOTING.md'),
       ]

       # Render docs menu
       content = Text()
       content.append("📚 Documentation\n\n", style="bold cyan")
       for num, title, _ in docs:
           content.append(f"{num}. {title}\n")

       panel = Panel(content, title="Available Documentation", border_style="cyan")
       self.console.print(panel)

       choice = Prompt.ask("Select document (1-6) or 'b' for back")

       if choice.isdigit() and 1 <= int(choice) <= 6:
           doc_path = docs[int(choice)-1][2]
           self.open_document(doc_path)

   def open_document(self, doc_path: str):
       """Open document in pager or browser."""
       import subprocess

       # Try to open in less (pager)
       try:
           subprocess.run(['less', doc_path])
       except FileNotFoundError:
           # Fallback: print first 50 lines
           with open(doc_path, 'r') as f:
               lines = f.readlines()[:50]
               self.console.print(''.join(lines))
               self.console.print(f"\n[cyan]Full doc: {doc_path}[/cyan]")
   ```

   **Benefits**:

   - Documentation discoverable from dashboard
   - No need to remember doc paths
   - Quick access to patterns and guides
   - Reduces support burden

   **Integrated Docs** (from Achievement 3.3):

   - LIBRARY_INTEGRATION_GUIDE.md - Library patterns
   - ERROR_HANDLING_PATTERNS.md - Error handling
   - PERFORMANCE_OPTIMIZATION_GUIDE.md - Caching/metrics
   - SUBPLAN-WORKFLOW-GUIDE.md - Workflow guide
   - README.md - Quick start
   - TROUBLESHOOTING.md - Common issues

**Deliverables**:

- `LLM/dashboard/action_executor.py`
- Action menu rendering
- One-key action handling
- Command building and execution
- Documentation quick access menu (NEW - Opportunity #1)
- Error handling for actions
- Tests for action executor
- Tests for documentation access

**Effort**: 3-4 hours (was 2-3 hours, +1 hour for doc integration)

---

### Priority 2: ADVANCED FEATURES (MEDIUM - Power User)

**Achievement 2.1**: Parallel Execution Detection & UI

**Purpose**: Detect and highlight parallel execution opportunities

**What**:

1. **Parallel Detector**:

   ```python
   class ParallelDetector:
       """Detect parallel execution opportunities."""

       def detect_parallel_achievements(
           self,
           plan_path: Path
       ) -> List[ParallelGroup]:
           """Detect achievements that can run in parallel."""
           # Use 3-tier framework from case study
           # Check achievement dependencies
           # Apply independence criteria
           return self._find_parallel_groups()

       def _check_independence(
           self,
           ach1: Achievement,
           ach2: Achievement
       ) -> bool:
           """Check if two achievements are independent."""
           # Check file overlap
           # Check dependencies
           # Check test conflicts
           return (
               not self._has_file_overlap(ach1, ach2) and
               not self._has_dependencies(ach1, ach2) and
               not self._has_test_conflicts(ach1, ach2)
           )
   ```

2. **Parallel UI Rendering**:

   ```python
   def render_parallel_opportunities(self):
       """Render parallel execution opportunities."""
       parallel_groups = self.parallel_detector.detect_parallel_achievements(
           self.plan_path
       )

       if not parallel_groups:
           return

       content = Text()
       content.append("🔀 Parallel Execution Opportunities\n", style="bold magenta")

       for group in parallel_groups:
           content.append(f"\nGroup {group.id}:\n", style="bold")
           for ach in group.achievements:
               content.append(f"  ├─ {ach.number}: {ach.title}\n")
           content.append(f"  └─ Estimated: {group.max_time}h (vs {group.sequential_time}h sequential)\n")
           content.append(f"     Savings: {group.savings}h ({group.savings_pct}%)\n", style="green")

       panel = Panel(content, border_style="magenta")
       self.console.print(panel)
   ```

3. **Parallel Execution Action**:

   ```python
   def execute_parallel(self):
       """Execute parallel achievements."""
       parallel_groups = self.parallel_detector.detect_parallel_achievements(
           self.plan_path
       )

       if not parallel_groups:
           self.console.print("[yellow]No parallel opportunities available[/yellow]")
           return

       # Show parallel groups
       self.render_parallel_opportunities()

       # Prompt user to select group
       group_choice = Prompt.ask("Select group to execute", choices=[str(i) for i in range(1, len(parallel_groups)+1)])

       # Provide instructions for parallel execution
       group = parallel_groups[int(group_choice)-1]
       self._show_parallel_instructions(group)
   ```

4. **Parallel Detection Algorithm** (NEW - Gap Fix #3):

   **Specific Implementation**:

   ```python
   def detect_parallel_achievements(self, plan_path: Path) -> List[ParallelGroup]:
       """Detect parallel execution opportunities with dependency analysis."""

       # Step 1: Parse Achievement Index
       achievements = self._parse_achievement_index(plan_path)

       # Step 2: Filter to incomplete achievements only
       incomplete = [
           ach for ach in achievements
           if not self._is_approved(ach.number, plan_path)
       ]

       # Step 3: Build dependency graph
       dep_graph = self._build_dependency_graph(achievements)

       # Step 4: Find independent pairs
       parallel_groups = []
       checked = set()

       for i, ach1 in enumerate(incomplete):
           for ach2 in incomplete[i+1:]:
               pair_key = tuple(sorted([ach1.number, ach2.number]))
               if pair_key in checked:
                   continue
               checked.add(pair_key)

               if self._are_independent(ach1, ach2, dep_graph):
                   parallel_groups.append(
                       ParallelGroup(
                           achievements=[ach1, ach2],
                           confidence='HIGH' if self._no_file_overlap(ach1, ach2) else 'MEDIUM'
                       )
                   )

       return parallel_groups

   def _are_independent(self, ach1, ach2, dep_graph) -> bool:
       """Check if two achievements are independent."""
       # 1. No direct dependency
       if ach2.number in dep_graph.get(ach1.number, []):
           return False
       if ach1.number in dep_graph.get(ach2.number, []):
           return False

       # 2. No transitive dependency
       if self._has_transitive_dependency(ach1, ach2, dep_graph):
           return False

       # 3. No file overlap (if determinable)
       if self._has_file_overlap(ach1, ach2):
           return False  # Conservative: assume conflict

       return True

   def _build_dependency_graph(self, achievements) -> Dict[str, List[str]]:
       """Build dependency graph from achievements."""
       graph = {}

       for ach in achievements:
           # Parse achievement section for "Depends on: X.Y" or similar
           deps = self._extract_dependencies(ach)
           if deps:
               graph[ach.number] = deps

       return graph

   def _extract_dependencies(self, achievement) -> List[str]:
       """Extract dependencies from achievement text."""
       # Look for patterns:
       # - "Depends on: 1.1, 1.2"
       # - "Requires: Achievement 1.1"
       # - "After: 1.1"

       # For MVP: Return [] (assume no dependencies unless explicitly marked)
       # Future: Parse achievement text for dependency markers
       return []

   def _show_parallel_instructions(self, group: ParallelGroup):
       """Show instructions for parallel execution."""
       content = Text()
       content.append("🔀 Parallel Execution Instructions\n\n", style="bold magenta")
       content.append("Option A: Multiple Terminals (Recommended)\n", style="bold")

       for i, ach in enumerate(group.achievements, 1):
           content.append(f"\nTerminal {i}:\n")
           content.append(f"  python LLM/scripts/generation/generate_prompt.py @{self.plan_name} {ach.number}\n", style="cyan")

       content.append("\n\nOption B: Background Execution (Advanced)\n", style="bold")
       content.append("  # Not yet implemented, use Option A\n", style="dim")

       panel = Panel(content, title="Parallel Execution", border_style="magenta")
       self.console.print(panel)
   ```

   **Dependencies**:

   - Parse "Depends on:" fields from achievements (if present)
   - Build dependency graph (directed acyclic graph)
   - Detect transitive dependencies
   - Conservative approach: Assume conflict if unclear

   **MVP Simplification**:

   - For first version: Detect based on achievement numbers only
   - Assume achievements in same priority level are independent
   - Assume cross-priority dependencies exist
   - Example: 3.2 and 3.3 (same priority 3) → parallel OK
   - Example: 2.5 and 3.1 (different priorities) → not parallel

   **Future Enhancement**:

   - Parse achievement descriptions for explicit dependencies
   - Analyze file modifications for conflicts
   - Check test data overlaps
   - Use ML to suggest parallel opportunities

**Deliverables**:

- `LLM/dashboard/parallel_detector.py`
- Parallel opportunity detection with algorithm (NEW - Gap Fix #3)
- Dependency graph building
- Independence checking logic
- Parallel UI rendering
- Parallel execution instructions
- Integration with case study framework
- Tests for parallel detection
- Tests for dependency graph

**Effort**: 4-5 hours (was 3-4 hours, +1 hour for algorithm)

---

**Achievement 2.2**: Interactive Workflow Execution

**Purpose**: Execute workflows interactively from dashboard

**What**:

1. **Workflow Executor**:

   ```python
   class WorkflowExecutor:
       """Execute workflows interactively."""

       def execute_workflow(self, workflow_type: str):
           """Execute workflow with user prompts."""
           if workflow_type == "next":
               self._execute_next_workflow()
           elif workflow_type == "subplan":
               self._execute_subplan_workflow()
           elif workflow_type == "execution":
               self._execute_execution_workflow()

       def _execute_next_workflow(self):
           """Execute next achievement workflow."""
           # Detect workflow state
           state = self.workflow_detector.detect_workflow_state()

           # Show workflow options
           self.console.print(f"[cyan]Workflow: {state.workflow}[/cyan]")

           # Execute appropriate script
           if state.workflow == "create_subplan":
               self._create_subplan(state.achievement)
           elif state.workflow == "create_execution":
               self._create_execution(state.achievement)
           elif state.workflow == "continue_execution":
               self._continue_execution(state.execution_path)
   ```

2. **Progress Tracking**:

   ```python
   def track_execution_progress(self, execution_path: Path):
       """Track execution progress in real-time."""
       with Progress() as progress:
           task = progress.add_task(
               f"[cyan]Executing {execution_path.name}...",
               total=100
           )

           # Monitor execution file for updates
           # Update progress bar based on phase completion
           # Show live status
   ```

3. **Result Display**:
   ```python
   def display_execution_result(self, result: ExecutionResult):
       """Display execution result."""
       if result.success:
           self.console.print(Panel(
               f"[green]✅ Execution complete![/green]\n\n"
               f"Deliverables: {len(result.deliverables)}\n"
               f"Tests: {result.tests_passing}/{result.tests_total} passing\n"
               f"Duration: {result.duration}",
               title="Success",
               border_style="green"
           ))
       else:
           self.console.print(Panel(
               f"[red]❌ Execution failed[/red]\n\n"
               f"Error: {result.error}\n"
               f"See: {result.log_file}",
               title="Error",
               border_style="red"
           ))
   ```

**Deliverables**:

- `LLM/dashboard/workflow_executor.py`
- Interactive workflow execution
- Progress tracking with Rich Progress
- Result display with panels
- Error handling and recovery
- Tests for workflow executor

**Effort**: 3-4 hours

---

**Achievement 2.3**: Real-Time State Updates

**Purpose**: Update dashboard state in real-time

**What**:

1. **State Watcher**:

   ```python
   class StateWatcher:
       """Watch filesystem for state changes."""

       def watch(self, plan_path: Path, callback: Callable):
           """Watch for state changes."""
           # Use watchdog library or polling
           # Monitor execution/feedbacks/ for new APPROVED/FIX files
           # Monitor execution/ for new EXECUTION_TASK files
           # Call callback when changes detected
   ```

2. **Live Dashboard**:

   ```python
   def show_live(self):
       """Show dashboard with live updates."""
       with Live(self.render(), refresh_per_second=1) as live:
           watcher = StateWatcher(self.plan_path)

           def on_state_change():
               self.state = self.state_detector.get_plan_state(self.plan_path)
               live.update(self.render())

           watcher.watch(on_state_change)
   ```

3. **Auto-Refresh**:

   ```python
   def render_with_refresh(self):
       """Render dashboard with auto-refresh indicator."""
       content = self.render_content()

       footer = Text()
       footer.append(f"Last updated: {datetime.now().strftime('%H:%M:%S')}", style="dim")
       footer.append(" | ", style="dim")
       footer.append("Press 'r' to refresh manually", style="dim")

       return Group(content, footer)
   ```

4. **State Consistency & Cache Invalidation** (NEW - Gap Fix #5):

   ```python
   def handle_state_refresh(self):
       """Handle manual state refresh with cache invalidation."""
       # Clear all caches
       self.state_detector.get_plan_state.cache.clear()
       self.discovery.get_all_plans.cache.clear()

       # Reload state from filesystem
       self.state = self.state_detector.get_plan_state(self.plan_path)

       # Show refresh indicator
       self.console.print("[green]✓ State refreshed from filesystem[/green]")

       logger.info("State refreshed", extra={
           'plan': self.plan_name,
           'cache_cleared': True
       })

   def auto_refresh_after_action(self):
       """Auto-refresh state after any action execution."""
       # Action execution may change filesystem state
       # Automatically refresh to show current state

       time.sleep(0.5)  # Give filesystem time to settle
       self.handle_state_refresh()  # Clear cache and reload

   def detect_multi_instance(self) -> bool:
       """Detect if another dashboard instance is running."""
       lock_file = Path("LLM/dashboard/.dashboard.lock")

       if lock_file.exists():
           # Check if process still alive
           try:
               with open(lock_file, 'r') as f:
                   pid = int(f.read().strip())

               # Check if PID exists (Unix)
               import os, signal
               os.kill(pid, 0)  # Raises if process doesn't exist

               # Process exists
               return True
           except (ValueError, ProcessLookupError, PermissionError):
               # Stale lock file, remove it
               lock_file.unlink()
               return False

       return False

   def create_lock_file(self):
       """Create lock file for this dashboard instance."""
       import os
       lock_file = Path("LLM/dashboard/.dashboard.lock")
       lock_file.parent.mkdir(parents=True, exist_ok=True)
       lock_file.write_text(str(os.getpid()))

   def cleanup_lock_file(self):
       """Remove lock file on dashboard exit."""
       lock_file = Path("LLM/dashboard/.dashboard.lock")
       if lock_file.exists():
           lock_file.unlink()
   ```

   **Refresh Triggers**:

   - After any action execution (auto)
   - User presses 'r' (manual)
   - Dashboard regains focus (if detectable)
   - Every 30s in live mode (optional)

   **Cache Invalidation**:

   - Mtime-based cache keys (Achievement 3.2 pattern)
   - Automatic invalidation on file changes
   - Manual cache clear option ('c' key)

   **Multi-Instance Handling**:

   - Show warning if another instance detected
   - Allow override with confirmation
   - Clean up lock file on exit (atexit handler)

   **UI Indicators**:

   - Show last refresh time in footer
   - Show "🔄 Refreshing..." during refresh
   - Show "⚠️ Stale data (5m+)" if cache old

**Deliverables**:

- `LLM/dashboard/state_watcher.py`
- Real-time state updates
- Live dashboard with Rich Live
- Auto-refresh with timestamp
- Manual refresh option ('r' key)
- State consistency mechanisms (NEW - Gap Fix #5)
- Cache invalidation strategy
- Multi-instance detection
- Tests for state watcher
- Tests for cache invalidation

**Effort**: 3-4 hours (was 2-3 hours, +1 hour for state consistency)

---

### Priority 3: POLISH (LOW - Nice to Have)

**Achievement 3.1**: Color Themes & Customization

**Purpose**: Add color themes and user customization

**What**:

1. **Theme System**:

   ```python
   class Theme:
       """Dashboard color theme."""

       def __init__(self, name: str):
           self.name = name
           self.colors = self._load_colors()

       def _load_colors(self) -> Dict[str, str]:
           """Load theme colors."""
           themes = {
               "default": {
                   "primary": "cyan",
                   "success": "green",
                   "warning": "yellow",
                   "error": "red",
                   "info": "blue",
               },
               "dark": {
                   "primary": "bright_cyan",
                   "success": "bright_green",
                   "warning": "bright_yellow",
                   "error": "bright_red",
                   "info": "bright_blue",
               },
               "light": {
                   "primary": "blue",
                   "success": "green",
                   "warning": "yellow",
                   "error": "red",
                   "info": "cyan",
               }
           }
           return themes.get(self.name, themes["default"])
   ```

2. **Configuration File**:

   ```yaml
   # LLM/dashboard/config.yaml
   theme: default
   refresh_interval: 1
   show_stats: true
   show_parallel: true
   auto_copy_commands: true
   ```

3. **Customization UI**:

   ```python
   def show_settings(self):
       """Show settings menu."""
       settings = self.config.load()

       menu = [
           f"1. Theme: {settings.theme}",
           f"2. Refresh Interval: {settings.refresh_interval}s",
           f"3. Show Stats: {settings.show_stats}",
           f"4. Show Parallel: {settings.show_parallel}",
           f"5. Auto-Copy Commands: {settings.auto_copy_commands}",
           "6. Back",
       ]

       # Show menu and handle choices
   ```

**Deliverables**:

- Theme system with 3 themes
- Configuration file (YAML)
- Settings menu
- Theme preview
- Tests for themes

**Effort**: 2-3 hours

---

**Achievement 3.2**: Keyboard Shortcuts & Navigation

**Purpose**: Add keyboard shortcuts for power users

**What**:

1. **Keyboard Handler**:

   ```python
   class KeyboardHandler:
       """Handle keyboard shortcuts."""

       def __init__(self):
           self.shortcuts = {
               'n': 'execute_next',
               'p': 'execute_parallel',
               's': 'create_subplan',
               'e': 'create_execution',
               'r': 'refresh',
               'q': 'quit',
               'h': 'help',
           }

       def handle_key(self, key: str) -> Optional[str]:
           """Handle keyboard shortcut."""
           return self.shortcuts.get(key)
   ```

2. **Help Screen**:

   ```python
   def show_help(self):
       """Show keyboard shortcuts help."""
       shortcuts = Table(title="Keyboard Shortcuts")
       shortcuts.add_column("Key", style="cyan")
       shortcuts.add_column("Action", style="yellow")

       shortcuts.add_row("n", "Execute next achievement")
       shortcuts.add_row("p", "Execute parallel achievements")
       shortcuts.add_row("s", "Create SUBPLAN")
       shortcuts.add_row("e", "Create EXECUTION")
       shortcuts.add_row("r", "Refresh dashboard")
       shortcuts.add_row("q", "Quit")
       shortcuts.add_row("h", "Show this help")

       self.console.print(Panel(shortcuts, border_style="blue"))
   ```

3. **Navigation History**:

   ```python
   class NavigationHistory:
       """Track navigation history."""

       def __init__(self):
           self.history = []

       def push(self, dashboard: str):
           """Push dashboard to history."""
           self.history.append(dashboard)

       def back(self) -> Optional[str]:
           """Go back to previous dashboard."""
           if len(self.history) > 1:
               self.history.pop()
               return self.history[-1]
           return None
   ```

4. **Enhanced Navigation & Action History** (NEW - Gap Fix #7):

   ```python
   class ActionHistory:
       """Track recent user actions."""

       def __init__(self, max_size=10):
           self.actions = []
           self.max_size = max_size

       def add(self, action: str, plan: str, timestamp: datetime):
           """Add action to history."""
           self.actions.append({
               'action': action,
               'plan': plan,
               'timestamp': timestamp
           })

           # Keep only last N actions
           if len(self.actions) > self.max_size:
               self.actions.pop(0)

       def get_recent(self, count=5) -> List[Dict]:
           """Get recent actions."""
           return self.actions[-count:]

   def render_breadcrumb(self):
       """Render breadcrumb navigation."""
       breadcrumb = Text()
       breadcrumb.append("📍 ", style="dim")

       for i, item in enumerate(self.history):
           if i > 0:
               breadcrumb.append(" → ", style="dim")
           breadcrumb.append(item, style="cyan" if i == len(self.history)-1 else "dim")

       self.console.print(breadcrumb)

   def render_recent_actions(self):
       """Render recent action history."""
       recent = self.action_history.get_recent(3)

       if not recent:
           return

       content = Text()
       content.append("Recent Actions:\n", style="dim")
       for action in recent:
           time_str = action['timestamp'].strftime('%H:%M')
           content.append(f"  {time_str} - {action['action']} ({action['plan']})\n", style="dim")

       self.console.print(content)

   def handle_navigation(self, key: str):
       """Handle navigation keys."""
       if key == 'b' or key == '\x1b':  # 'b' or ESC
           # Go back to previous dashboard
           prev = self.nav_history.back()
           if prev:
               return prev
           else:
               self.console.print("[yellow]Already at top level[/yellow]")

       elif key == 'r':
           # Refresh current dashboard
           self.refresh_state()

       elif key == 'h':
           # Show help
           self.show_help()
   ```

   **Navigation Improvements**:

   - **Back Navigation**: 'b' key or ESC to go back
   - **Breadcrumb Trail**: Main → Plan → Action Result
   - **Action History**: Show last 3 actions
   - **Quick Repeat**: Re-run recent actions

   **UI Enhancements**:

   ```
   📍 Main → PROMPT-GENERATOR → Execute Next

   Recent Actions:
     12:34 - Executed 3.2 (PROMPT-GENERATOR)
     12:35 - Created SUBPLAN 3.3 (PROMPT-GENERATOR)
     12:36 - Refreshed State (PROMPT-GENERATOR)
   ```

   **Benefits**:

   - Easy to go back without quitting
   - Context awareness (breadcrumbs)
   - Action audit trail
   - Confidence in navigation

**Deliverables**:

- Keyboard shortcut system
- Help screen
- Navigation history
- Breadcrumb trail
- Action history tracking (NEW - Gap Fix #7)
- Back navigation ('b' or ESC key)
- Breadcrumb rendering
- Recent actions display
- Tests for keyboard handling
- Tests for navigation history

**Effort**: 3-4 hours (was 2-3 hours, +1 hour for enhanced navigation)

---

**Achievement 3.3**: Help System & Documentation

**Purpose**: Add comprehensive help system

**What**:

1. **Contextual Help**:

   ```python
   def show_contextual_help(self, context: str):
       """Show help for current context."""
       help_text = self.help_system.get_help(context)

       panel = Panel(
           help_text,
           title=f"Help: {context}",
           border_style="blue"
       )

       self.console.print(panel)
   ```

2. **Interactive Tutorial**:

   ```python
   def run_tutorial(self):
       """Run interactive tutorial."""
       steps = [
           ("Welcome", "Welcome to LLM Dashboard! Let's take a quick tour."),
           ("Main Dashboard", "This is the main dashboard. It shows all your plans."),
           ("Plan Dashboard", "Select a plan to see its detailed dashboard."),
           ("Actions", "Use numbered shortcuts to execute actions."),
           ("Keyboard", "Press 'h' anytime to see keyboard shortcuts."),
       ]

       for title, text in steps:
           self.console.print(Panel(text, title=title, border_style="cyan"))
           Prompt.ask("Press Enter to continue")
   ```

3. **Documentation Generator**:

   ```python
   def generate_docs(self):
       """Generate markdown documentation."""
       docs = []

       docs.append("# LLM Dashboard CLI\n")
       docs.append("## Main Dashboard\n")
       docs.append(self._document_main_dashboard())
       docs.append("## Plan Dashboard\n")
       docs.append(self._document_plan_dashboard())
       docs.append("## Keyboard Shortcuts\n")
       docs.append(self._document_shortcuts())

       return "\n".join(docs)
   ```

4. **Comprehensive Documentation** (ENHANCED - Gap Fix #8):

   **User Documentation** (`LLM/dashboard/USER_GUIDE.md`, ~400 lines):

   ```markdown
   # LLM Dashboard User Guide

   ## Quick Start (5 Minutes)

   1. Open dashboard: `python LLM/main.py`
   2. Select plan by number
   3. Press 1 to execute next achievement
   4. Done!

   ## All Actions Explained

   - Execute Next (key: 'n' or '1')
   - Execute Parallel (key: 'p' or '2')
   - Create SUBPLAN (key: 's' or '3')
   - Review Achievement (key: '4')
   - View Documentation (key: '5')

   ## Common Workflows

   1. Sequential work: Execute next → Approve → Execute next
   2. Parallel work: Detect parallel → Execute in parallel
   3. Fix workflow: See FIX indicator → Address fixes
   4. Review workflow: See completed → Review → Approve

   ## Troubleshooting

   - Dashboard won't load → Check Rich library installed
   - No plans shown → Check work-space/plans/ exists
   - Slow performance → Check cache hit rate
   - Stale state → Press 'r' to refresh
   ```

   **Developer Documentation** (`LLM/dashboard/DEVELOPER_GUIDE.md`, ~300 lines):

   ```markdown
   # LLM Dashboard Developer Guide

   ## Architecture Overview

   - Main entry: LLM/main.py
   - Dashboard modules: LLM/dashboard/
   - Integration: LLM/scripts/generation/

   ## Adding New Dashboard Types

   1. Inherit from BaseDashboard
   2. Implement show() method
   3. Use ui_components for rendering
   4. Follow error handling patterns

   ## Testing Guidelines

   - Unit tests: Mock filesystem
   - Integration tests: Real files in tmp_path
   - Performance tests: Benchmark with timing

   ## Library Integration Patterns

   - Error handling: Use DashboardError subclasses
   - Logging: Use get_logger(**name**)
   - Caching: Use @cached with mtime keys
   - Metrics: Register all metrics
   ```

   **Inline Help Enhancements**:

   - Press 'h' shows help overlay with all shortcuts
   - Context-sensitive help per screen
   - Quick reference card (press '?')
   - Link to full docs (press 'd' for docs menu)

   **Examples & Workflows**:

   - Common workflow examples in USER_GUIDE.md
   - Screenshot mockups (ASCII art)
   - Video demo script (for recording)
   - FAQ section

   **Integration with Achievement 3.3** (PROMPT-GENERATOR):

   - Link to LIBRARY_INTEGRATION_GUIDE.md
   - Link to README.md (generate_prompt.py guide)
   - Link to TROUBLESHOOTING.md
   - Consistent documentation structure

**Deliverables**:

- Contextual help system
- Interactive tutorial
- Documentation generator
- USER_GUIDE.md (~400 lines, NEW - Gap Fix #8)
- DEVELOPER_GUIDE.md (~300 lines, NEW - Gap Fix #8)
- README.md for dashboard (enhanced)
- Inline help overlays
- FAQ section
- Tests for help system

**Effort**: 3-4 hours (was 2-3 hours, +1-2 hours for comprehensive documentation)

---

## 📊 Testing Strategy

### Test Coverage Requirements

**Target**: >90% coverage for all dashboard code

**Test Types**:

1. **Unit Tests**:

   - State detection logic
   - Parallel detection algorithm
   - Action executor commands
   - UI component rendering

2. **Integration Tests**:

   - Dashboard navigation flow
   - Action execution end-to-end
   - State updates after actions
   - Error handling

3. **UI Tests**:
   - Rich component rendering
   - Table formatting
   - Panel layouts
   - Color themes

### Test Files

```
tests/LLM/dashboard/
├── test_main_dashboard.py
├── test_plan_dashboard.py
├── test_state_detector.py
├── test_parallel_detector.py
├── test_action_executor.py
├── test_workflow_executor.py
├── test_ui_components.py
└── test_integration.py
```

---

## 📁 File Structure

```
LLM/
├── main.py                           # Entry point (100 lines)
├── dashboard/
│   ├── __init__.py
│   ├── base_dashboard.py             # Base class (150 lines)
│   ├── main_dashboard.py             # Main dashboard (250 lines)
│   ├── plan_dashboard.py             # Plan dashboard (350 lines)
│   ├── state_detector.py             # State detection (300 lines)
│   ├── parallel_detector.py          # Parallel detection (250 lines)
│   ├── action_executor.py            # Action execution (200 lines)
│   ├── workflow_executor.py          # Workflow execution (250 lines)
│   ├── state_watcher.py              # Real-time updates (150 lines)
│   ├── ui_components.py              # Reusable UI (300 lines)
│   ├── models.py                     # Data models (200 lines)
│   ├── utils.py                      # Helpers (150 lines)
│   ├── config.py                     # Configuration (100 lines)
│   └── themes.py                     # Color themes (100 lines)
├── docs/
│   └── DASHBOARD_GUIDE.md            # User guide (500 lines)
└── scripts/
    └── generation/
        └── (existing scripts)

tests/LLM/dashboard/
├── test_main_dashboard.py            # Main dashboard tests (200 lines)
├── test_plan_dashboard.py            # Plan dashboard tests (250 lines)
├── test_state_detector.py            # State detection tests (200 lines)
├── test_parallel_detector.py         # Parallel detection tests (200 lines)
├── test_action_executor.py           # Action executor tests (150 lines)
├── test_workflow_executor.py         # Workflow executor tests (200 lines)
├── test_ui_components.py             # UI component tests (150 lines)
└── test_integration.py               # Integration tests (250 lines)

Total: ~4,500 lines (3,000 production, 1,500 tests)
```

---

## 🚀 Implementation Roadmap

### Phase 1: Foundation (Priority 0) - 7-10 hours

**Week 1**:

- Achievement 0.1: Rich Framework Setup (2-3h)
- Achievement 0.2: State Detection (3-4h)
- Achievement 0.3: Main Dashboard (2-3h)

**Deliverable**: Working main dashboard showing all plans

### Phase 2: Core UX (Priority 1) - 7-10 hours

**Week 2**:

- Achievement 1.1: Plan Dashboard (3-4h)
- Achievement 1.2: Achievement Visualization (2-3h)
- Achievement 1.3: Quick Actions (2-3h)

**Deliverable**: Full plan dashboard with one-key actions

### Phase 3: Advanced Features (Priority 2) - 8-11 hours

**Week 3**:

- Achievement 2.1: Parallel Detection (3-4h)
- Achievement 2.2: Interactive Workflows (3-4h)
- Achievement 2.3: Real-Time Updates (2-3h)

**Deliverable**: Parallel execution and live updates

### Phase 4: Polish (Priority 3) - 6-9 hours

**Week 4**:

- Achievement 3.1: Themes (2-3h)
- Achievement 3.2: Keyboard Shortcuts (2-3h)
- Achievement 3.3: Help System (2-3h)

**Deliverable**: Production-ready dashboard with full features

**Total Effort**: 28-40 hours (3-4 weeks)

---

## 📊 Success Criteria

### Must Have (Priority 0-1)

- [ ] Main dashboard shows all plans with states
- [ ] Plan dashboard shows detailed information
- [ ] One-key shortcuts for common actions (next, parallel, review)
- [ ] State detection from filesystem (APPROVED, FIX, SUBPLAN, EXECUTION)
- [ ] Action execution (generate_prompt.py, generate_subplan_prompt.py)
- [ ] Tests passing (>90% coverage)

### Should Have (Priority 2)

- [ ] Parallel execution detection and UI
- [ ] Interactive workflow execution
- [ ] Real-time state updates
- [ ] Progress tracking for executions

### Nice to Have (Priority 3)

- [ ] Color themes
- [ ] Keyboard shortcuts
- [ ] Help system and tutorial
- [ ] Documentation generator

---

## 🎯 Key Decisions

### Decision 1: Rich Library vs Custom UI

**Chosen**: Rich library

**Rationale**:

- Production-grade terminal UI
- Excellent documentation
- Active maintenance
- Rich feature set (tables, panels, progress, live)
- Python-native (no external dependencies)

**Alternatives Considered**:

- Textual (too heavy for quick win)
- Curses (too low-level)
- Custom (reinventing wheel)

---

### Decision 2: State Detection Strategy

**Chosen**: Filesystem-first (APPROVED files, FIX files)

**Rationale**:

- Consistent with Achievement 2.5 (Feedback System)
- Single source of truth
- No markdown parsing needed
- Fast and reliable

**Alternatives Considered**:

- Parse PLAN markdown (slow, unreliable)
- Database (overkill)
- Cache files (stale data risk)

---

### Decision 3: Action Execution Strategy

**Chosen**: Subprocess calls to existing scripts

**Rationale**:

- Reuse existing, tested scripts
- No code duplication
- Backward compatible
- Easy to maintain

**Alternatives Considered**:

- Import and call functions (tight coupling)
- Rewrite logic (duplication)
- REST API (overkill)

---

### Decision 4: Parallel Detection Strategy

**Chosen**: Use 3-tier framework from case study

**Rationale**:

- Already designed and documented
- Proven criteria (independence, testability, mergeability)
- Quantitative impact analysis available
- Clear decision tree

**Alternatives Considered**:

- Manual parallel specification (error-prone)
- Simple heuristics (inaccurate)
- No parallel detection (missed opportunities)

---

## 📚 References

**Methodology Documents**:

- `LLM-METHODOLOGY.md` - Core methodology
- `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` - Workflow patterns
- `LLM/docs/FEEDBACK_SYSTEM_GUIDE.md` - State tracking

**Case Studies**:

- `work-space/case-studies/EXECUTION_CASE-STUDY_PARALLEL-EXECUTION-PATTERNS-EVOLUTION.md` - Parallel execution framework

**Related Plans**:

- `PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md` - UX improvements
- `GRAMMAPLAN_UNIVERSAL-CLI-CORE-FOUNDATION.md` - North Star vision

**External Libraries**:

- Rich: https://rich.readthedocs.io/
- Click: https://click.palletsprojects.com/ (if needed for CLI args)

---

## 🎓 Expected Learnings

### Technical Learnings

1. **Rich Library Mastery**: Deep understanding of Rich components
2. **Terminal UI Patterns**: Best practices for CLI dashboards
3. **State Management**: Efficient filesystem state detection
4. **Subprocess Management**: Clean subprocess execution patterns

### Process Learnings

1. **UX Design for CLI**: Principles for intuitive terminal interfaces
2. **Quick Win Strategy**: Delivering high-impact features fast
3. **Incremental Enhancement**: Building features in priority order
4. **User-Centered Design**: Solving actual pain points first

### Strategic Learnings

1. **Dashboard as Platform**: Foundation for future CLI tools
2. **State Visibility Value**: Impact of instant state overview
3. **Shortcut Power**: One-key actions vs verbose commands
4. **Parallel Discovery**: Automated detection vs manual tracking

---

## 🚨 Risks & Mitigation

### Risk 1: Rich Library Learning Curve

**Risk**: Team unfamiliar with Rich library

**Mitigation**:

- Start with simple components (Panel, Table)
- Reference Rich documentation extensively
- Create reusable UI components early
- Test each component independently

---

### Risk 2: State Detection Performance

**Risk**: Filesystem scanning may be slow for many plans

**Mitigation**:

- Cache state detection results
- Use async I/O for parallel scanning
- Implement incremental updates
- Profile and optimize hot paths

---

### Risk 3: Subprocess Execution Complexity

**Risk**: Managing subprocess execution and output

**Mitigation**:

- Use subprocess.run() with proper error handling
- Capture stdout/stderr for display
- Implement timeout mechanisms
- Test subprocess execution thoroughly

---

### Risk 4: Backward Compatibility

**Risk**: Dashboard may break existing workflows

**Mitigation**:

- Keep existing scripts functional
- Dashboard is additive, not replacement
- Provide fallback to command-line
- Document migration path

---

## 📝 Notes

**Quick Win Focus**: This plan prioritizes immediate UX improvements (Priority 0-1) over advanced features (Priority 2-3). Goal is to deliver 80% of value in 40% of time.

**Incremental Delivery**: Each priority level delivers standalone value. Can stop after Priority 1 and still have massive UX improvement.

**Foundation for Future**: Dashboard architecture designed to support future CLI tools (testing, validation, metrics, etc.).

**User-Centered Design**: Every feature addresses actual user pain points identified in problem statement.

---

## 💡 Future Opportunities (For Consideration)

**Source**: `work-space/analyses/EXECUTION_ANALYSIS_LLM-DASHBOARD-CLI-PLAN-REVIEW.md`

These opportunities were identified in gap analysis but deferred for future consideration. They are **NOT** required for initial implementation but may be valuable additions later.

### Opportunity 3: Export/Report Generation 📄

**Priority**: LOW-MEDIUM  
**Effort**: +2-3 hours

**What**:

- Plain text export (copy-pasteable for Slack/email)
- JSON export (machine-readable, API-friendly)
- Markdown report (GitHub-friendly)
- HTML static dashboard (share via web)

**Benefits**:

- Collaboration: Share plan state easily
- Integration: Machine-readable format for tools
- Documentation: Static reports for archival

**When to Implement**: If users request sharing/reporting features

---

### Opportunity 4: Search/Filter Functionality 🔍

**Priority**: MEDIUM  
**Effort**: +2-3 hours

**What**:

- Plan search (fuzzy matching, press '/')
- Status filters (show only: Ready, In Progress, Needs Attention)
- Achievement filters (complete, incomplete, has SUBPLAN)
- Quick jump (type plan number directly)

**Benefits**:

- Power users with many plans (>10)
- Quick navigation
- Focused views

**When to Implement**: When users have >10 active plans

---

### Opportunity 5: Batch Operations ⚡

**Priority**: LOW-MEDIUM  
**Effort**: +3-4 hours

**What**:

- Multi-select plans (space bar to select)
- Batch actions (create SUBPLANs for all, review all)
- Execution queue (queue multiple actions)
- Progress tracking for batch operations

**Benefits**:

- 10x faster for bulk operations
- Power user feature
- Reduces repetitive tasks

**When to Implement**: If power users request bulk operations

---

### Opportunity 6: Git Integration 🔗

**Priority**: LOW  
**Effort**: +4-5 hours

**What**:

- Git status indicator (uncommitted changes, push needed)
- Quick git actions (commit, push, view diff)
- Change detection (files modified since last commit)
- Auto-commit on achievement completion (optional)

**Benefits**:

- Reduces context switching
- Encourages frequent commits
- Version control visibility

**When to Implement**: If version control integration becomes pain point

---

**Implementation Priority** (if pursuing):

1. Search/Filter (Opportunity 4) - Most useful for power users
2. Export/Report (Opportunity 3) - Enables collaboration
3. Batch Operations (Opportunity 5) - Nice-to-have for power users
4. Git Integration (Opportunity 6) - Lowest priority, can use terminal

**Note**: These opportunities are documented for future consideration. They should NOT be implemented in initial version unless user pain points emerge during usage.

**Reference**: See full analysis in `EXECUTION_ANALYSIS_LLM-DASHBOARD-CLI-PLAN-REVIEW.md` for detailed rationale, implementation suggestions, and effort estimates.

---

**Status**: 🚀 Ready to Execute (Enhanced with Gap Fixes)  
**Priority**: CRITICAL - UX Quick Win  
**Estimated Effort**: 40-48 hours (was 12-18 hours, revised after gap analysis)  
**Expected Impact**: 80% faster workflow, 100% state visibility, zero friction
