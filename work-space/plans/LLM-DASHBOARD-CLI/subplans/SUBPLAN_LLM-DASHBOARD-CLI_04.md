# SUBPLAN: Achievement 0.4 - Library Integration & Production Patterns

**PLAN**: LLM-DASHBOARD-CLI  
**Achievement**: 0.4  
**Estimated Time**: 3-4 hours  
**Created**: 2025-11-13  
**Status**: 📋 Design Phase

---

## 🎯 Objective

Integrate production-ready libraries (error handling, logging, caching, metrics, regex compilation) from PROMPT-GENERATOR Achievements 3.1-3.3 into the dashboard codebase, transforming it from a prototype into a production-ready application with structured error handling, observability, and optimized performance.

**Core Purpose**: Apply proven library patterns to the dashboard, ensuring consistency with the prompt generator architecture while achieving >80% cache hit rates, structured error handling, comprehensive logging, and performance metrics—all critical for production deployment.

**Success Definition**:
- All dashboard modules use structured exceptions with context and suggestions
- All output uses structured logging (no print statements remain)
- Cache hit rate >80% for repeated state detection
- Metrics exportable in Prometheus format
- Performance tests validate <500ms dashboard load time for 10 plans

---

## 📦 Deliverables

### 1. Dashboard Exception Classes
**File**: `LLM/dashboard/exceptions.py` (~120 lines, NEW)
**Contents**:
- `DashboardError(ApplicationError)` - Base dashboard exception
- `PlanLoadError(DashboardError)` - Plan loading failures
- `StateDetectionError(DashboardError)` - State detection failures
- `ActionExecutionError(DashboardError)` - Action execution failures
- `InvalidUserInputError(DashboardError)` - Invalid user input

**Pattern**:
```python
from LLM.scripts.generation.exceptions import ApplicationError

class DashboardError(ApplicationError):
    """Base exception for dashboard errors."""
    pass

class PlanLoadError(DashboardError):
    """
    Raised when plan cannot be loaded.
    
    Context fields:
    - plan_path: Path to plan that failed to load
    - reason: Why loading failed
    
    Suggestions:
    - Verify plan directory exists
    - Check PLAN_*.md file is present
    - Ensure proper file permissions
    """
    pass
```

### 2. Structured Logging Integration
**Files**: All dashboard modules modified (~80 lines added total)
**Modules to Update**:
- `base_dashboard.py` - Replace console.print with logger
- `main_dashboard.py` - Add logging for dashboard lifecycle
- `plan_discovery.py` - Log discovery operations
- `state_detector.py` - Log state detection operations
- `utils.py` - Log utility operations

**Pattern**:
```python
from core.libraries.logging import get_logger, set_log_context

logger = get_logger(__name__)

def show(self):
    """Show dashboard with logging."""
    set_log_context(
        dashboard='main',
        action='show'
    )
    
    logger.info("Dashboard opened", extra={
        'plan_count': len(plans),
        'workspace_root': str(self.workspace_root)
    })
    
    # ... logic ...
    
    logger.info("Dashboard closed", extra={
        'duration': timer.elapsed()
    })
```

**Log Configuration**:
- File: `LLM/dashboard/dashboard.log`
- Format: JSON
- Level: INFO
- Rotation: Daily

### 3. Performance Optimization (Caching)
**Files**: `plan_discovery.py`, `state_detector.py` (modified, ~30 lines added total)
**Caching Strategy**:

**A. Plan Discovery Cache**:
```python
from core.libraries.caching import cached
import os

@cached(
    max_size=20,
    ttl=600,  # 10 minutes
    key_func=lambda self: f"plans:{os.path.getmtime(self.plans_root)}",
    name="plan_discovery_cache"
)
def get_all_plans(self) -> List[Path]:
    """Get all plans with directory mtime-based invalidation."""
    # ... existing logic ...
```

**B. State Detection Cache**:
```python
@cached(
    max_size=50,
    ttl=300,  # 5 minutes
    key_func=lambda self, plan_dir: f"{plan_dir}:{os.path.getmtime(plan_dir)}",
    name="plan_state_cache"
)
def get_plan_state(self, plan_dir: Path) -> PlanState:
    """Get plan state with plan directory mtime-based invalidation."""
    # ... existing logic ...
```

**C. Regex Compilation**:
```python
# Module level in utils.py
import re

ACHIEVEMENT_NUM_PATTERN = re.compile(r'(\d+)\.(\d+)')
APPROVED_FILE_PATTERN = re.compile(r'APPROVED_(\d+)\.md')
FIX_FILE_PATTERN = re.compile(r'FIX_(\d+)\.md')
SUBPLAN_FILE_PATTERN = re.compile(r'SUBPLAN_.*_(\d+)\.md')
EXECUTION_FILE_PATTERN = re.compile(r'EXECUTION_TASK_.*_(\d+)_\d+\.md')

# Use in parse_achievement_number()
def parse_achievement_number(filename: str) -> Optional[str]:
    """Parse achievement number using compiled regex."""
    match = ACHIEVEMENT_NUM_PATTERN.search(filename)
    # ...
```

### 4. Metrics Collection
**File**: `LLM/dashboard/metrics.py` (~100 lines, NEW)
**Contents**:
- Dashboard action metrics (Counter)
- Dashboard load time metrics (Histogram)
- Cache hit rate metrics (Counter)
- Plan state metrics (Gauge)

**Pattern**:
```python
from core.libraries.metrics import Counter, Histogram, Gauge, MetricRegistry

# Define metrics
dashboard_actions_total = Counter(
    'dashboard_actions_total',
    'Total dashboard actions executed',
    labels=['action_type', 'status']
)

dashboard_load_duration_seconds = Histogram(
    'dashboard_load_duration_seconds',
    'Dashboard load time in seconds',
    labels=['dashboard_type']
)

cache_operations_total = Counter(
    'cache_operations_total',
    'Total cache operations',
    labels=['cache_name', 'operation', 'result']
)

plan_state_info = Gauge(
    'plan_state_info',
    'Current plan state information',
    labels=['plan_name', 'status']
)

# Register all metrics
def register_dashboard_metrics():
    """Register all dashboard metrics with registry."""
    registry = MetricRegistry.get_instance()
    registry.register(dashboard_actions_total)
    registry.register(dashboard_load_duration_seconds)
    registry.register(cache_operations_total)
    registry.register(plan_state_info)
```

### 5. Error Handling Integration
**Files**: All dashboard modules (modified, ~60 lines added total)
**Updates**:
- Replace `print` error messages with `format_error_with_suggestions`
- Add try-except blocks with structured exceptions
- Add context to all exceptions
- Use color-coded output

**Pattern**:
```python
from LLM.dashboard.exceptions import PlanLoadError
from LLM.scripts.generation.exceptions import format_error_with_suggestions

try:
    plan_file = self.get_plan_file(plan_dir)
    if not plan_file:
        raise PlanLoadError(
            "Plan file not found",
            context={
                'plan_dir': str(plan_dir),
                'expected_pattern': 'PLAN_*.md'
            },
            suggestions=[
                "Verify plan directory exists",
                "Check for PLAN_*.md file in directory",
                "Ensure file permissions are correct"
            ]
        )
except PlanLoadError as e:
    error_output = format_error_with_suggestions(e)
    self.console.print(error_output)
    logger.error("Plan load failed", exc_info=True, extra={
        'plan_dir': str(plan_dir)
    })
```

### 6. Integration Tests
**File**: `tests/LLM/dashboard/test_library_integration.py` (~200 lines, NEW)
**Test Coverage**:
- Exception handling tests (8 tests)
- Logging integration tests (6 tests)
- Caching tests (8 tests)
- Metrics collection tests (6 tests)
- End-to-end integration tests (4 tests)

**Total**: 32 tests

### 7. Performance Tests
**File**: `tests/LLM/dashboard/test_performance.py` (extended, ~80 lines added)
**Test Coverage**:
- Dashboard load time test (<500ms for 10 plans)
- Cache hit rate test (>80% hit rate)
- State detection performance test (<200ms per plan)
- Metrics export performance test (<100ms)

**Total**: 4 performance tests

---

## 🔧 Approach

### Phase 1: Exception Classes & Error Handling (60 min)

**Goal**: Create exception hierarchy and integrate error handling

**Steps**:
1. **Create `LLM/dashboard/exceptions.py`** (20 min):
   - Define `DashboardError` base class
   - Define 4 specific exception classes (PlanLoadError, StateDetectionError, ActionExecutionError, InvalidUserInputError)
   - Add docstrings with context fields and suggestions
   - Import `ApplicationError` from prompt generator

2. **Integrate Error Handling in Modules** (40 min):
   - Update `plan_discovery.py`: Use `PlanLoadError` for missing plans
   - Update `state_detector.py`: Use `StateDetectionError` for detection failures
   - Update `main_dashboard.py`: Use `ActionExecutionError` for action failures
   - Update `main_dashboard.py`: Use `InvalidUserInputError` for invalid input
   - Replace all error `print` statements with `format_error_with_suggestions`

**Output**: Structured exceptions with context and suggestions

---

### Phase 2: Structured Logging Integration (60 min)

**Goal**: Replace all print statements with structured logging

**Steps**:
1. **Update Module Imports** (15 min):
   - Add `from core.libraries.logging import get_logger, set_log_context` to all modules
   - Add `logger = get_logger(__name__)` at module level
   - Configure log file: `LLM/dashboard/dashboard.log`

2. **Replace Print Statements** (45 min):
   - `base_dashboard.py`: Replace `self.print()` with `logger.info()` where appropriate
   - `main_dashboard.py`: Add logging for dashboard lifecycle (open, close, actions)
   - `plan_discovery.py`: Log discovery operations (found X plans)
   - `state_detector.py`: Log state detection operations
   - Keep `self.console.print()` for UI output, use `logger` for diagnostic info

3. **Add Log Context** (10 min):
   - Set context in `MainDashboard.show()` (dashboard='main')
   - Set context in action handlers (action_type='select_plan')

**Output**: All diagnostic output uses structured logging

---

### Phase 3: Performance Optimization (60 min)

**Goal**: Add caching and compile regex patterns

**Steps**:
1. **Add Caching to Discovery** (20 min):
   - Import `@cached` decorator in `plan_discovery.py`
   - Apply to `get_all_plans()` with mtime-based key
   - Max size: 20, TTL: 600 seconds

2. **Add Caching to State Detection** (25 min):
   - Apply `@cached` to `get_plan_state()` in `state_detector.py`
   - Use plan directory mtime for cache invalidation
   - Max size: 50, TTL: 300 seconds

3. **Compile Regex Patterns** (15 min):
   - Move regex compilation to module level in `utils.py`
   - Define 5 compiled patterns (achievement, approved, fix, subplan, execution)
   - Update `parse_achievement_number()` to use compiled pattern

**Output**: Caching with >80% hit rate, compiled regex patterns

---

### Phase 4: Metrics & Testing (60 min)

**Goal**: Add metrics collection and comprehensive tests

**Steps**:
1. **Create Metrics Module** (20 min):
   - Create `LLM/dashboard/metrics.py`
   - Define 4 metrics (actions, load time, cache ops, plan state)
   - Create `register_dashboard_metrics()` function
   - Call registration in `main_dashboard.py` init

2. **Instrument Dashboard Code** (20 min):
   - Add metrics to `MainDashboard.show()` (load time histogram)
   - Add metrics to action handlers (action counter)
   - Add metrics to cache operations (cache hits/misses)

3. **Write Tests** (20 min):
   - Create `test_library_integration.py` (32 tests)
   - Extend `test_performance.py` (4 performance tests)
   - Verify exception handling works
   - Verify logging works (check log file)
   - Verify caching works (cache hit rate)
   - Verify metrics exportable

**Output**: Comprehensive test suite verifying all integrations

---

## 🔄 Execution Strategy

**Type**: Single EXECUTION (Recommended)

**Rationale**:
1. **Cohesive Integration**: All library integrations work together (errors logged, cached, metricsed)
2. **Manageable Scope**: 3-4 hours, can be done in one focused session
3. **Sequential Dependencies**: Each phase builds on previous (exceptions → logging → caching → metrics)
4. **Atomic Deployment**: All libraries needed together for production readiness

**Phase Execution**:
1. Phase 1: Exception Classes & Error Handling (60 min)
2. Phase 2: Structured Logging Integration (60 min)
3. Phase 3: Performance Optimization (60 min)
4. Phase 4: Metrics & Testing (60 min)

**Total**: 3-4 hours (240 min estimated, budget 180-240 min)

---

## 🧪 Testing Strategy

### Unit Testing

**Scope**: Test each library integration in isolation

**Test Files**:
1. `test_library_integration.py` - All library integration tests
2. Extend existing module tests - Verify integration doesn't break existing functionality

**Coverage Target**: >90% for new code

**Key Tests**:
- Exception creation and context propagation
- Logging output and context setting
- Cache hit/miss rates
- Metrics registration and collection
- Regex pattern compilation and usage

### Performance Testing

**Scope**: Verify performance targets met

**Test Cases**:
1. **Dashboard Load Time**:
   - Load main dashboard with 10 plans
   - Measure time from init to first render
   - Target: <500ms

2. **Cache Hit Rate**:
   - Load dashboard twice consecutively
   - Measure cache hits vs misses
   - Target: >80% hit rate

3. **State Detection Performance**:
   - Detect state for 10 plans
   - Measure per-plan time
   - Target: <200ms per plan

4. **Metrics Export**:
   - Export all metrics to Prometheus format
   - Measure export time
   - Target: <100ms

### Integration Testing

**Scope**: Test libraries working together

**Test Cases**:
1. **Error + Logging**:
   - Raise exception
   - Verify logged with context
   - Verify formatted for user

2. **Cache + Metrics**:
   - Trigger cache operations
   - Verify metrics collected
   - Verify cache performance

3. **End-to-End**:
   - Launch dashboard
   - Perform actions
   - Verify all libraries working (logs, metrics, cache)

---

## 📊 Expected Results

### Functional

**Exception Handling**:
- ✅ All dashboard errors use structured exceptions
- ✅ Exceptions include context and suggestions
- ✅ Errors formatted with color coding
- ✅ Errors auto-copied to clipboard

**Logging**:
- ✅ All diagnostic output uses logger
- ✅ Logs written to `dashboard.log` in JSON format
- ✅ Log context propagates across modules
- ✅ No print statements for diagnostic output (UI print OK)

**Caching**:
- ✅ Plan discovery cached (mtime invalidation)
- ✅ State detection cached (mtime invalidation)
- ✅ Cache hit rate >80% for repeated operations
- ✅ Cache invalidates on file changes

**Metrics**:
- ✅ Dashboard actions tracked (Counter)
- ✅ Load time tracked (Histogram)
- ✅ Cache operations tracked (Counter)
- ✅ Plan state tracked (Gauge)
- ✅ Metrics exportable in Prometheus format

**Regex**:
- ✅ Patterns compiled at module level
- ✅ 10-20% performance improvement
- ✅ All pattern usage updated

### Performance

**Targets**:
- Dashboard load time: <500ms for 10 plans ✅
- Cache hit rate: >80% for repeated operations ✅
- State detection: <200ms per plan ✅
- Metrics export: <100ms ✅

**Quality**:
- Test coverage: >90% for new code ✅
- All tests passing ✅
- No linter errors ✅
- Clear documentation ✅

---

## ⚠️ Risks & Mitigations

### Risk 1: Breaking Existing Functionality

**Risk**: Replacing print with logger might break UI output

**Impact**: HIGH - Dashboard unusable if UI breaks

**Mitigation**:
- Keep `self.console.print()` for UI output
- Only replace diagnostic `print()` with `logger`
- Test all UI interactions after changes
- Run full test suite (140 existing tests) to verify no regressions

### Risk 2: Cache Invalidation Complexity

**Risk**: Mtime-based invalidation might miss changes

**Impact**: MEDIUM - Stale data shown in dashboard

**Mitigation**:
- Use directory mtime (changes when files added/removed)
- Test cache invalidation with file modifications
- Keep TTL short (5-10 minutes) as fallback
- Add manual cache clear option if needed

### Risk 3: Performance Overhead from Libraries

**Risk**: Library overhead might slow dashboard

**Impact**: LOW - But defeats purpose of optimization

**Mitigation**:
- Measure performance before and after
- Profile hot paths
- Optimize library usage if needed
- Cache library calls where appropriate

### Risk 4: Metrics Collection Overhead

**Risk**: Metrics collection might add latency

**Impact**: LOW - Metrics are lightweight

**Mitigation**:
- Use efficient metric types (Counter, Gauge)
- Batch metric updates where possible
- Measure metrics overhead (<1ms target)
- Disable metrics if performance issue

---

## 💡 Design Decisions

### Decision 1: Single Module vs Distributed Error Handling

**Chosen**: Single `exceptions.py` module for all dashboard exceptions

**Rationale**:
- Centralizes exception hierarchy
- Easy to import from any module
- Clear documentation in one place
- Follows prompt generator pattern

**Trade-off**: All exceptions in one file, but only ~120 lines

### Decision 2: Replace All Print vs Selective Replacement

**Chosen**: Selective replacement (keep UI print, replace diagnostic)

**Rationale**:
- `console.print()` needed for Rich UI output
- `logger` for diagnostic/debug info
- Clear separation of concerns
- Best of both worlds

**Trade-off**: Need to decide print vs log case-by-case, but clear guidelines

### Decision 3: Aggressive Caching vs Conservative Caching

**Chosen**: Conservative caching with short TTL

**Rationale**:
- Mtime-based invalidation catches most changes
- Short TTL (5-10 min) as safety net
- Better to be correct than fast
- Can increase TTL if needed

**Trade-off**: Might miss some cache benefits, but safer

### Decision 4: Compiled Regex vs Runtime Compilation

**Chosen**: Module-level compiled regex patterns

**Rationale**:
- 10-20% performance gain for repeated matches
- No code complexity increase
- Proven pattern from prompt generator
- Zero runtime cost

**Trade-off**: Slightly more module-level code, but worth performance gain

---

## 🔗 Dependencies

### Requires (from PROMPT-GENERATOR achievements):
- Achievement 3.1: `core/libraries/error_handling/` ✅
- Achievement 3.1: `core/libraries/logging/` ✅
- Achievement 3.2: `core/libraries/caching/` ✅
- Achievement 3.2: `core/libraries/metrics/` ✅
- Achievement 3.2: Compiled regex patterns ✅

### Requires (from LLM-DASHBOARD achievements):
- Achievement 0.1: Base dashboard framework ✅
- Achievement 0.2: Plan discovery and state detection ✅
- Achievement 0.3: Main dashboard implementation ✅

### Enables (for future achievements):
- Achievement 1.1: Plan-specific dashboard (will use same patterns)
- Achievement 1.2: Achievement visualization (will use same patterns)
- Achievement 1.3: Quick actions (will use same patterns)
- All future dashboard features (production-ready foundation)

---

## 📝 Implementation Notes

### Library Import Pattern

```python
# At top of each module
from core.libraries.logging import get_logger, set_log_context
from core.libraries.caching import cached
from core.libraries.metrics import Counter, Histogram
from LLM.dashboard.exceptions import (
    DashboardError,
    PlanLoadError,
    StateDetectionError,
    ActionExecutionError,
    InvalidUserInputError
)

logger = get_logger(__name__)
```

### Print vs Logger Guidelines

**Use `self.console.print()`**:
- UI output (tables, panels, prompts)
- User-facing messages
- Rich formatting needed

**Use `logger.info/debug/error()`**:
- Diagnostic information
- Performance metrics
- Error details
- State changes
- Action tracking

### Cache Key Patterns

```python
# Directory-based cache (uses directory mtime)
f"plans:{os.path.getmtime(self.plans_root)}"

# File-based cache (uses file mtime)
f"{plan_dir}:{os.path.getmtime(plan_dir)}"

# Combination cache (uses both)
f"{plan_dir}:{plan_file}:{os.path.getmtime(plan_file)}"
```

---

## ✅ Definition of Done

**Code Complete**:
- [ ] `LLM/dashboard/exceptions.py` created
- [ ] `LLM/dashboard/metrics.py` created
- [ ] All modules updated with logging
- [ ] Caching applied to discovery and state detection
- [ ] Regex patterns compiled at module level
- [ ] Error handling integrated with format_error_with_suggestions

**Tests Complete**:
- [ ] 32 integration tests written and passing
- [ ] 4 performance tests written and passing
- [ ] 140 existing tests still passing (no regressions)
- [ ] >90% coverage for new code

**Performance Complete**:
- [ ] Dashboard load time <500ms for 10 plans
- [ ] Cache hit rate >80%
- [ ] State detection <200ms per plan
- [ ] Metrics export <100ms

**Quality Complete**:
- [ ] No linter errors
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] Reference docs updated

**Integration Complete**:
- [ ] Works with all 5 libraries
- [ ] No breaking changes to existing functionality
- [ ] Ready for Achievement 1.1
- [ ] Production-ready patterns established

---

**Status**: 📋 Ready for Execution  
**Next Step**: Create `EXECUTION_TASK_LLM-DASHBOARD-CLI_04_01.md` and execute work  
**Executor**: Begin with Phase 1 (Exception Classes & Error Handling)

