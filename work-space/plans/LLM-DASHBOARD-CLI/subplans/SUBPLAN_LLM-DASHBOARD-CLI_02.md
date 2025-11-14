# SUBPLAN: Achievement 0.2 - Plan Discovery & State Detection

**PLAN**: LLM-DASHBOARD-CLI  
**Achievement**: 0.2  
**Estimated Time**: 3-4 hours  
**Created**: 2025-11-13  
**Status**: 📋 Design Phase

---

## 🎯 Objective

Implement filesystem-based plan discovery and state detection to enable the dashboard to automatically find all plans, detect their completion status, identify pending work, and compute progress. This is the **foundational data layer** that all dashboard views will consume.

**Core Purpose**: Provide accurate, real-time state information by querying the filesystem (APPROVED files, FIX files, SUBPLAN files, EXECUTION_TASK files) rather than maintaining separate state storage, adhering to the filesystem-first philosophy.

**Success Definition**: A robust plan discovery and state detection system that can accurately detect all plans in `work-space/plans/`, compute their progress, identify the last completed achievement, find next available achievements, and detect pending reviews or fixes—all from filesystem queries with <500ms latency.

---

## 📦 Deliverables

### 1. Plan Discovery Module

**File**: `LLM/dashboard/plan_discovery.py` (~150 lines)

**Contents**:

- `PlanDiscovery` class
- `get_all_plans()` - Find all plan directories
- `get_plan_file()` - Get PLAN_*.md file from directory
- `get_plan_name()` - Extract plan name from directory/file
- `validate_plan_structure()` - Verify plan has required directories
- Error handling for missing/malformed plans

**Key Features**:
- Filters hidden directories (starts with `.`)
- Handles missing PLAN files gracefully
- Returns sorted list of plans (alphabetical)

### 2. State Detection Module

**File**: `LLM/dashboard/state_detector.py` (~250 lines)

**Contents**:

- `StateDetector` class
- `get_plan_state()` - Get complete plan state
- `_get_last_complete()` - Find last APPROVED achievement
- `_get_pending_reviews()` - Find EXECUTION_TASKs awaiting review
- `_get_pending_fixes()` - Find FIX files
- `_get_next_available()` - Compute next executable achievements
- `_calculate_progress()` - Compute completion percentage
- `_parse_achievement_index()` - Extract achievements from PLAN

**Key Features**:
- Filesystem-first (no state persistence)
- Handles missing feedback directories
- Extracts achievement numbers from filenames (APPROVED_31.md → "3.1")
- Computes next achievements based on sequential order

### 3. Data Models

**File**: `LLM/dashboard/models.py` (~120 lines)

**Contents**:

```python
@dataclass
class PlanState:
    """Complete state of a PLAN."""
    name: str
    plan_file: Path
    last_achievement: Optional[str]
    next_achievements: List[str]
    pending_reviews: List[str]
    pending_fixes: List[str]
    total_achievements: int
    completed_achievements: int
    progress_percentage: float
    status: PlanStatus  # Enum: active, complete, needs_attention


@dataclass
class AchievementState:
    """State of a single achievement."""
    achievement_id: str
    title: str
    status: AchievementStatus  # Enum: not_started, in_progress, complete, needs_fix
    has_subplan: bool
    has_execution: bool
    has_approved: bool
    has_fix: bool


class PlanStatus(Enum):
    """Plan-level status."""
    ACTIVE = "active"  # Work in progress
    COMPLETE = "complete"  # All achievements approved
    NEEDS_ATTENTION = "needs_attention"  # Has pending fixes or reviews


class AchievementStatus(Enum):
    """Achievement-level status."""
    NOT_STARTED = "not_started"  # No SUBPLAN file
    IN_PROGRESS = "in_progress"  # SUBPLAN or EXECUTION_TASK exists, no APPROVED
    COMPLETE = "complete"  # APPROVED file exists
    NEEDS_FIX = "needs_fix"  # FIX file exists
```

### 4. Test Suite

**Files** (3 test files):

- `tests/LLM/dashboard/test_plan_discovery.py` (~150 lines, 15 tests)
- `tests/LLM/dashboard/test_state_detector.py` (~200 lines, 20 tests)
- `tests/LLM/dashboard/test_models.py` (~80 lines, 8 tests)

**Coverage**:
- Plan discovery (all plans, single plan, missing plans)
- State detection (complete plans, partial plans, no feedback plans)
- Achievement parsing (various PLAN formats)
- Edge cases (empty directories, malformed files, missing feedback dirs)
- Models (dataclass creation, enum values, serialization)

### 5. Integration Utilities

**Updates to existing files**:

- `LLM/dashboard/utils.py` - Add `parse_achievement_number()` helper
- Integration with existing project structure

---

## 🔧 Approach

### Phase 1: Data Models & Infrastructure (45 min)

**Goal**: Define data structures and establish patterns

**Tasks**:

1. **Create `models.py`**:
   - Define `PlanState` dataclass
   - Define `AchievementState` dataclass
   - Define `PlanStatus` enum
   - Define `AchievementStatus` enum
   - Add docstrings for all fields
   - Add helper methods (e.g., `is_complete()`, `needs_attention()`)

2. **Update `utils.py`**:
   - Add `parse_achievement_number(filename: str) -> str` function
   - Handles formats: `APPROVED_31.md` → `"3.1"`, `SUBPLAN_02.md` → `"0.2"`
   - Add unit tests

**Output**: 
- `models.py` with complete data structures
- `utils.py` with achievement number parsing
- Foundation for Phase 2

**Why First**: Models define the contract for all subsequent modules

### Phase 2: Plan Discovery (45 min)

**Goal**: Implement filesystem traversal and plan detection

**Tasks**:

1. **Create `plan_discovery.py`**:
   - Implement `PlanDiscovery` class
   - `get_all_plans()` - List all plan directories in `work-space/plans/`
   - `get_plan_file()` - Find `PLAN_*.md` file in directory
   - `get_plan_name()` - Extract plan name from path
   - `validate_plan_structure()` - Check for required directories

2. **Error Handling**:
   - Handle missing `work-space/plans/` directory
   - Handle directories without PLAN files
   - Handle multiple PLAN files (take first, log warning)
   - Return empty list gracefully if no plans found

3. **Filtering**:
   - Exclude hidden directories (`.git`, `.cache`)
   - Exclude non-directories
   - Sort results alphabetically

**Output**: 
- `plan_discovery.py` with robust discovery logic
- Handles edge cases gracefully
- Returns consistent, predictable results

**Why Second**: Discovery is needed before state detection can run

### Phase 3: State Detection (60 min)

**Goal**: Implement filesystem-based state computation

**Tasks**:

1. **Create `state_detector.py` - Core Class**:
   - Implement `StateDetector` class
   - `get_plan_state(plan_path: Path) -> PlanState` - Main entry point

2. **Achievement Tracking**:
   - `_get_last_complete()` - Find highest numbered APPROVED file
   - `_get_pending_reviews()` - Find EXECUTION_TASKs without feedback
   - `_get_pending_fixes()` - Find FIX files
   - `_get_next_available()` - Compute next achievements to execute

3. **Progress Calculation**:
   - `_calculate_progress()` - Compute completion percentage
   - `_parse_achievement_index()` - Extract all achievements from PLAN
   - Parse "## 📋 Achievement Index" section
   - Extract achievement numbers using regex (`\d+\.\d+`)

4. **Filesystem Queries**:
   - Check `execution/feedbacks/` for APPROVED and FIX files
   - Check `execution/` for EXECUTION_TASK files
   - Check `subplans/` for SUBPLAN files
   - All queries use `Path.glob()` for efficiency

5. **Status Computation**:
   - Determine `PlanStatus` based on:
     - `COMPLETE`: All achievements have APPROVED files
     - `NEEDS_ATTENTION`: Any FIX files exist
     - `ACTIVE`: Otherwise (work in progress)

**Output**: 
- `state_detector.py` with complete state computation
- Filesystem-first queries (no state persistence)
- Accurate progress calculation
- Robust error handling

**Why Third**: State detection is the core functionality, builds on models and discovery

### Phase 4: Testing & Validation (50 min)

**Goal**: Comprehensive test coverage and validation

**Tasks**:

1. **Test Plan Discovery** (`test_plan_discovery.py`):
   - Test `get_all_plans()` with various scenarios:
     - Multiple plans
     - Single plan
     - No plans (empty directory)
     - Plans with/without PLAN files
   - Test `get_plan_file()`:
     - Valid PLAN file
     - Missing PLAN file
     - Multiple PLAN files
   - Test `validate_plan_structure()`:
     - Complete plan structure
     - Missing directories
   - Test filtering (hidden directories excluded)

2. **Test State Detection** (`test_state_detector.py`):
   - Test `get_plan_state()` with mock filesystem:
     - Complete plan (all achievements approved)
     - Partial plan (some achievements complete)
     - New plan (no achievements complete)
     - Plan with pending fixes
   - Test `_get_last_complete()`:
     - Single APPROVED file
     - Multiple APPROVED files (highest number)
     - No APPROVED files
   - Test `_get_pending_fixes()`:
     - Single FIX file
     - Multiple FIX files
     - No FIX files
   - Test `_parse_achievement_index()`:
     - Standard PLAN format
     - PLAN with priorities
     - Malformed PLAN (graceful failure)
   - Test progress calculation accuracy

3. **Test Models** (`test_models.py`):
   - Test dataclass creation
   - Test enum values
   - Test helper methods
   - Test edge cases (None values, empty lists)

4. **Integration Testing**:
   - Test full flow: discovery → state detection → model creation
   - Use real PLAN from project (e.g., PROMPT-GENERATOR-UX-AND-FOUNDATION)
   - Verify accuracy against known state

5. **Run Tests**:
   ```bash
   pytest tests/LLM/dashboard/ -v
   ```
   - Target: >90% coverage
   - All tests passing

**Output**: 
- 43 tests covering all modules
- >90% code coverage
- Integration test with real data
- All edge cases handled

**Why Last**: Tests validate all functionality and catch edge cases

---

## 🔄 Execution Strategy

### Type: Single Execution (Recommended)

**Rationale**:

1. **Small Scope**: 3-4 hours total, manageable in one session
2. **Interdependent Modules**: Models → Discovery → State Detection flow sequentially
3. **Atomic Delivery**: All components needed together for dashboard (Achievement 0.3)
4. **Clear Phases**: 4 distinct phases that build on each other

**Alternative Considered**: Split into 2 executions (Discovery + State Detection), but overhead of coordination and integration would exceed benefits.

**Execution**: Create single `EXECUTION_TASK_LLM-DASHBOARD-CLI_02_01.md`

---

## 🧪 Testing Strategy

### Unit Testing

**Scope**: Test each module in isolation with mocks

**Test Files**:
1. `test_plan_discovery.py` - Plan discovery logic
2. `test_state_detector.py` - State detection logic
3. `test_models.py` - Data models and enums

**Mocking Strategy**:
- Mock `Path.iterdir()` for plan discovery
- Mock `Path.glob()` for file detection
- Use `tmp_path` fixture for filesystem tests
- Create fake APPROVED/FIX files in test fixtures

**Coverage Target**: >90% line coverage

### Integration Testing

**Scope**: Test full workflow with real project data

**Test Cases**:
1. **Real Plan Test**: Use `PROMPT-GENERATOR-UX-AND-FOUNDATION` plan
   - Verify discovery finds it
   - Verify state detection is accurate
   - Compare with manual inspection
2. **Multi-Plan Test**: Discover and detect state for all plans
   - Verify counts match filesystem
   - Verify no errors

**Validation**:
- Compare computed state with manual filesystem inspection
- Verify achievement index parsing matches PLAN
- Verify progress percentage is accurate

### Performance Testing

**Requirements**:
- Plan discovery: <100ms for 10 plans
- State detection: <200ms per plan
- Full scan (all plans): <2 seconds for 10 plans

**Test Method**:
- Use `time.perf_counter()` to measure
- Run multiple iterations
- Average results
- Fail if >20% over budget

### Edge Case Testing

**Scenarios**:
1. Missing `work-space/plans/` directory
2. Plan directory without PLAN file
3. Plan without `execution/` directory
4. Plan without `feedbacks/` directory
5. PLAN file without Achievement Index
6. Malformed achievement numbers
7. Empty feedback directory
8. Multiple PLAN files in directory

**Expected Behavior**: Graceful degradation, helpful error messages, no crashes

---

## 📊 Expected Results

### Success Criteria

**Functional**:
- ✅ Discovers all plans in `work-space/plans/`
- ✅ Detects last completed achievement accurately
- ✅ Identifies pending reviews and fixes
- ✅ Computes progress percentage correctly
- ✅ Parses Achievement Index from PLAN files
- ✅ Returns consistent, predictable data structures

**Performance**:
- ✅ Plan discovery <100ms for 10 plans
- ✅ State detection <200ms per plan
- ✅ Full scan <2 seconds for 10 plans

**Quality**:
- ✅ >90% test coverage
- ✅ All tests passing
- ✅ No linter errors
- ✅ Comprehensive docstrings
- ✅ Type hints throughout

**Integration**:
- ✅ Works with existing project structure
- ✅ Compatible with `utils.py`
- ✅ Ready for Achievement 0.3 (Main Dashboard)

### Deliverable Metrics

**Files Created**: 6 files (~950 lines total)
- Source: 3 files (~520 lines)
- Tests: 3 files (~430 lines)

**Test Metrics**:
- Total Tests: 43 tests
- Coverage: >90%
- Performance: All under budget

### Integration Points

**For Achievement 0.3 (Main Dashboard)**:
- Use `PlanDiscovery` to get all plans
- Use `StateDetector` to get plan states
- Use `PlanState` model to render dashboard
- Display progress, last achievement, next achievements

**For Achievement 1.1 (Plan Dashboard)**:
- Use `StateDetector` for detailed plan view
- Display achievement-level states
- Show pending reviews and fixes

---

## 🚨 Risks & Mitigations

### Risk 1: PLAN File Format Variations

**Risk**: Different PLANs may have different Achievement Index formats

**Impact**: HIGH - Parser may fail to extract achievements

**Mitigation**:
- Parse multiple format variations:
  - Standard: `- Achievement 1.1: Title`
  - With priorities: `**Priority 1**: ...`
  - With status: `- Achievement 1.1 ✅: Title`
- Use flexible regex patterns
- Test with multiple real PLAN files
- Graceful fallback if parsing fails

### Risk 2: Performance with Large Plan Counts

**Risk**: Filesystem queries may be slow with 50+ plans

**Impact**: MEDIUM - Dashboard load time >2 seconds

**Mitigation**:
- Use `Path.glob()` for efficiency (not `os.walk`)
- Cache results with TTL (Achievement 3.2 - future)
- Parallel state detection (Achievement 2.1 - future)
- Profile and optimize hot paths

### Risk 3: Filesystem Inconsistencies

**Risk**: Missing directories, malformed files, permission errors

**Impact**: MEDIUM - State detection may fail or be inaccurate

**Mitigation**:
- Check directory existence before querying
- Handle `PermissionError` and `FileNotFoundError`
- Return partial data if some components fail
- Log warnings for inconsistencies
- Comprehensive error handling in all methods

### Risk 4: Achievement Number Extraction Errors

**Risk**: Filenames may not follow expected pattern

**Impact**: LOW - Some achievements not detected

**Mitigation**:
- Use robust regex: `r'(\d+)(\d+)'` from `APPROVED_31.md`
- Handle both formats: `31` and `3.1`
- Log warnings for unexpected formats
- Test with various filename patterns

---

## 💡 Design Decisions

### Decision 1: Filesystem-First vs State Database

**Chosen**: Filesystem-First

**Rationale**:
- Aligns with project philosophy (single source of truth)
- No synchronization issues
- Simpler architecture
- Real-time accuracy
- No migration needed

**Trade-offs**:
- Slightly slower than in-memory (but <200ms is acceptable)
- Requires filesystem access on every query
- Mitigation: Caching in future (Achievement 3.2)

### Decision 2: Single vs Multiple PlanState Classes

**Chosen**: Single `PlanState` with comprehensive fields

**Rationale**:
- Single data contract for all consumers
- Easy to serialize/deserialize
- All information in one place
- Simpler API

**Alternative Considered**: Separate `BasicPlanState` and `DetailedPlanState`, but overhead of multiple classes not worth complexity savings.

### Decision 3: Sequential vs Parallel State Detection

**Chosen**: Sequential (for now)

**Rationale**:
- Simpler implementation
- Performance adequate for <10 plans (<2 seconds)
- Parallel can be added later (Achievement 2.1)

**Future Enhancement**: Parallel state detection when plan count >20

### Decision 4: Regex vs Parser for Achievement Index

**Chosen**: Regex with flexible patterns

**Rationale**:
- Faster than full parser
- Sufficient for structured PLAN format
- Handles format variations
- Easy to debug

**Alternative Considered**: Full markdown parser (too heavy for simple extraction)

---

## 📝 Implementation Notes

### Achievement Index Parsing Pattern

The Achievement Index section in PLAN files follows this pattern:

```markdown
## 📋 Achievement Index

**Priority 0: Foundation**

- Achievement 0.1: Rich Dashboard Framework Setup ✅
- Achievement 0.2: Plan Discovery & State Detection
- Achievement 0.3: Main Dashboard Implementation
```

**Extraction Strategy**:
1. Find section starting with `## 📋 Achievement Index`
2. Extract lines matching pattern: `- Achievement \d+\.\d+:`
3. Use regex: `r'Achievement (\d+\.\d+):'`
4. Return list of achievement numbers

### File Detection Patterns

**APPROVED files**: `execution/feedbacks/APPROVED_*.md`
**FIX files**: `execution/feedbacks/FIX_*.md`
**EXECUTION files**: `execution/EXECUTION_TASK_*_01.md` (or _02, _03)
**SUBPLAN files**: `subplans/SUBPLAN_*_01.md`

### Progress Calculation Formula

```python
def _calculate_progress(self, approved_count: int, total_count: int) -> float:
    """Calculate progress percentage."""
    if total_count == 0:
        return 0.0
    return round((approved_count / total_count) * 100, 1)
```

---

## 🔗 Dependencies

### Requires (from previous achievements):
- Achievement 0.1: Rich Dashboard Framework ✅
  - `BaseDashboard` class
  - `ui_components` module
  - `utils` module

### Enables (for future achievements):
- Achievement 0.3: Main Dashboard Implementation
- Achievement 1.1: Plan-Specific Dashboard
- Achievement 1.2: Achievement State Visualization

### External Dependencies:
- Python 3.8+ (Path, dataclasses, typing)
- No new external libraries needed

---

## ✅ Definition of Done

**Code Complete**:
- [ ] `plan_discovery.py` created and functional
- [ ] `state_detector.py` created and functional
- [ ] `models.py` created with all data structures
- [ ] `utils.py` updated with achievement parsing
- [ ] All modules have comprehensive docstrings
- [ ] Type hints present throughout

**Tests Complete**:
- [ ] 43 tests written and passing
- [ ] >90% code coverage achieved
- [ ] Integration test with real PLAN passes
- [ ] All edge cases covered
- [ ] Performance tests pass (<200ms per plan)

**Quality Complete**:
- [ ] No linter errors (ruff/flake8)
- [ ] No type errors (mypy)
- [ ] Code follows project conventions
- [ ] Docstrings complete and helpful

**Integration Complete**:
- [ ] Works with existing project structure
- [ ] Compatible with Achievement 0.1 (dashboard framework)
- [ ] Ready for Achievement 0.3 (main dashboard)
- [ ] Manual testing with real plans successful

**Documentation Complete**:
- [ ] EXECUTION_TASK updated with completion notes
- [ ] Learning summary documented
- [ ] Any issues or surprises noted

---

**Status**: 📋 Ready for Execution  
**Next Step**: Create `EXECUTION_TASK_LLM-DASHBOARD-CLI_02_01.md` and execute work  
**Executor**: Begin with Phase 1 (Data Models & Infrastructure)

