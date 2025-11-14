# SUBPLAN: Achievement 1.2 - Achievement State Visualization

**PLAN**: LLM-DASHBOARD-CLI  
**Achievement**: 1.2  
**Estimated Time**: 3-4 hours  
**Created**: 2025-11-14  
**Status**: 📋 Design Phase

---

## 🎯 Objective

Implement detailed achievement state visualization within the plan dashboard, showing achievement list with status indicators, dependencies, and an overall plan health score. This transforms the dashboard from showing basic counts to showing detailed achievement-level state, enabling users to see exactly which achievements are complete, in progress, or blocked.

**Core Purpose**: Provide comprehensive visualization of all achievements in a plan with clear status indicators, dependency relationships, and an overall health score that encourages plan completion and highlights issues immediately.

**Success Definition**:
- Users can see all achievements in a table with clear status indicators
- Each achievement shows its current state (✅ APPROVED, ⚠️ FIX pending, 🔄 In progress, 📝 SUBPLAN ready, ⏸️ Not started)
- Users can visualize achievement dependencies with Tree display
- Dashboard shows overall plan health score (0-100) with breakdown
- All information is derived from filesystem state (no manual tracking)
- Rendering is fast (<100ms for 20 achievements)

---

## 📦 Deliverables

### 1. Achievement List Rendering

**Function**: `render_achievements()` in `plan_dashboard.py` (~80 lines)

**Purpose**: Display all achievements in a table with status and action columns

**Implementation**:

```python
def render_achievements(self):
    """
    Render achievement list with states.
    
    Shows:
    - Achievement number (e.g., "1.1", "2.3")
    - Achievement title
    - Current status (with emoji)
    - Next action (what to do)
    
    Format:
        Achievements
        ┌───────────┬──────────────────────────────────┬──────────────┬─────────────┐
        │ Number    │ Title                            │ Status       │ Action      │
        ├───────────┼──────────────────────────────────┼──────────────┼─────────────┤
        │ 0.1       │ Rich Dashboard Framework Setup   │ ✅ APPROVED  │ Complete    │
        │ 0.2       │ Plan Discovery & State Detection │ ✅ APPROVED  │ Complete    │
        │ 1.1       │ Plan-Specific Dashboard          │ 🔄 In progress│ Continue    │
        │ 1.2       │ Achievement State Visualization  │ ⏸️ Not started│ Design      │
        └───────────┴──────────────────────────────────┴──────────────┴─────────────┘
    """
    achievements = self._get_all_achievements()
    
    if not achievements:
        self.console.print("[yellow]No achievements found in plan[/yellow]")
        return
    
    table = Table(
        title="📋 Achievements",
        show_header=True,
        header_style="bold cyan",
        border_style="cyan"
    )
    
    table.add_column("Number", style="bold", width=12)
    table.add_column("Title", width=40)
    table.add_column("Status", width=20)
    table.add_column("Action", width=15)
    
    for ach in achievements:
        status_str = self._format_status(ach)
        action_str = self._format_action(ach)
        
        table.add_row(
            ach['number'],
            ach['title'],
            status_str,
            action_str
        )
    
    self.console.print(table)
```

### 2. Status Formatting Functions

**Functions**: `_format_status()`, `_format_action()` in `plan_dashboard.py` (~40 lines)

**Purpose**: Format achievement status with appropriate emoji and text

**Implementation**:

```python
def _format_status(self, achievement: Dict) -> str:
    """
    Format achievement status with emoji.
    
    Status Priority (check in order):
    1. APPROVED (highest priority - completed)
    2. FIX pending (needs attention)
    3. In progress (has EXECUTION, no APPROVED)
    4. SUBPLAN ready (has SUBPLAN, no EXECUTION)
    5. Not started (default)
    
    Args:
        achievement: Achievement dict with 'number' and 'title'
    
    Returns:
        Formatted status string with emoji
    """
    ach_num = achievement['number'].replace('.', '')
    
    # Check for APPROVED (complete)
    approved_file = self.plan_path / 'execution' / 'feedbacks' / f'APPROVED_{ach_num}.md'
    if approved_file.exists():
        return "[green]✅ APPROVED[/green]"
    
    # Check for FIX (needs attention)
    fix_file = self.plan_path / 'execution' / 'feedbacks' / f'FIX_{ach_num}.md'
    if fix_file.exists():
        return "[red]⚠️ FIX pending[/red]"
    
    # Check for EXECUTION (in progress)
    execution_pattern = f'EXECUTION_TASK_*_{ach_num}_*.md'
    execution_dir = self.plan_path / 'execution'
    if execution_dir.exists() and list(execution_dir.glob(execution_pattern)):
        return "[yellow]🔄 In progress[/yellow]"
    
    # Check for SUBPLAN (ready to execute)
    subplan_pattern = f'SUBPLAN_*_{ach_num}.md'
    subplans_dir = self.plan_path / 'subplans'
    if subplans_dir.exists() and list(subplans_dir.glob(subplan_pattern)):
        return "[cyan]📝 SUBPLAN ready[/cyan]"
    
    # Not started
    return "[dim]⏸️ Not started[/dim]"

def _format_action(self, achievement: Dict) -> str:
    """
    Format next action for achievement.
    
    Args:
        achievement: Achievement dict
    
    Returns:
        Formatted action string
    """
    ach_num = achievement['number'].replace('.', '')
    
    # Complete
    approved_file = self.plan_path / 'execution' / 'feedbacks' / f'APPROVED_{ach_num}.md'
    if approved_file.exists():
        return "[dim]Complete[/dim]"
    
    # Fix
    fix_file = self.plan_path / 'execution' / 'feedbacks' / f'FIX_{ach_num}.md'
    if fix_file.exists():
        return "[red]Fix issues[/red]"
    
    # Continue execution
    execution_pattern = f'EXECUTION_TASK_*_{ach_num}_*.md'
    execution_dir = self.plan_path / 'execution'
    if execution_dir.exists() and list(execution_dir.glob(execution_pattern)):
        return "[yellow]Continue[/yellow]"
    
    # Execute (SUBPLAN ready)
    subplan_pattern = f'SUBPLAN_*_{ach_num}.md'
    subplans_dir = self.plan_path / 'subplans'
    if subplans_dir.exists() and list(subplans_dir.glob(subplan_pattern)):
        return "[cyan]Execute[/cyan]"
    
    # Design (need SUBPLAN)
    return "Design"
```

### 3. Plan Health Score

**Functions**: `calculate_health_score()`, `render_health_score()` in `plan_dashboard.py` (~100 lines)

**Purpose**: Calculate and display overall plan health score (0-100) to encourage completion

**Implementation**:

```python
from dataclasses import dataclass

@dataclass
class HealthScore:
    """Plan health score data."""
    score: float  # 0-100
    status: str   # "Excellent", "Good", "Fair", "Needs Attention"
    emoji: str    # "🟢", "🟡", "🟠", "🔴"
    breakdown: Dict[str, float]  # Component scores

def calculate_health_score(self) -> HealthScore:
    """
    Calculate overall plan health score (0-100).
    
    Components (total 100 points):
    - 30 points: Achievement completion rate
    - 20 points: No pending fixes
    - 20 points: No stale executions (>7 days old)
    - 15 points: Test pass rate
    - 15 points: Documentation complete
    
    Returns:
        HealthScore with score, status, emoji, and breakdown
    """
    breakdown = {}
    score = 0
    
    # 30 points: Achievement completion rate
    if self.state.total_achievements > 0:
        completion_rate = self.state.completed_achievements / self.state.total_achievements
        completion_points = 30 * completion_rate
        score += completion_points
        breakdown['completion'] = completion_points
    else:
        breakdown['completion'] = 0
    
    # 20 points: No pending fixes
    stats = self._calculate_stats()
    if stats['reviews_pending'] == 0:
        score += 20
        breakdown['no_fixes'] = 20
    else:
        breakdown['no_fixes'] = 0
    
    # 20 points: No stale executions (>7 days old)
    stale_count = self._count_stale_executions()
    if stale_count == 0:
        score += 20
        breakdown['no_stale'] = 20
    else:
        breakdown['no_stale'] = 0
    
    # 15 points: Test pass rate (placeholder for MVP)
    test_pass_rate = 0  # TODO: Integrate with pytest
    score += 15 * (test_pass_rate / 100) if stats['tests_total'] > 0 else 0
    breakdown['tests'] = 15 * (test_pass_rate / 100) if stats['tests_total'] > 0 else 0
    
    # 15 points: Documentation complete (placeholder for MVP)
    # TODO: Check for README, guides, etc.
    breakdown['docs'] = 0
    
    return HealthScore(
        score=score,
        status=self._get_health_status(score),
        emoji=self._get_health_emoji(score),
        breakdown=breakdown
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

def _count_stale_executions(self) -> int:
    """
    Count EXECUTION files older than 7 days without APPROVED.
    
    Returns:
        Count of stale executions
    """
    from datetime import datetime, timedelta
    
    stale_count = 0
    execution_dir = self.plan_path / 'execution'
    
    if not execution_dir.exists():
        return 0
    
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    for exec_file in execution_dir.glob('EXECUTION_TASK_*_01.md'):
        # Check if APPROVED exists
        ach_num = exec_file.stem.split('_')[-2]  # Extract achievement number
        approved_file = self.plan_path / 'execution' / 'feedbacks' / f'APPROVED_{ach_num}.md'
        
        if not approved_file.exists():
            # Check file age
            mtime = datetime.fromtimestamp(exec_file.stat().st_mtime)
            if mtime < seven_days_ago:
                stale_count += 1
    
    return stale_count

def render_health_score(self):
    """
    Render plan health score.
    
    Shows:
    - Overall score (0-100)
    - Status (Excellent, Good, Fair, Needs Attention)
    - Emoji indicator
    - Breakdown of score components
    """
    health = self.calculate_health_score()
    
    content = Text()
    content.append(f"{health.emoji} Score: {health.score:.0f}/100 - {health.status}\n", 
                  style="bold")
    content.append("\nBreakdown:\n")
    
    # Completion
    if 'completion' in health.breakdown:
        content.append(f"  ✅ Completion: {health.breakdown['completion']:.0f}/30\n")
    
    # No fixes
    if health.breakdown.get('no_fixes', 0) > 0:
        content.append(f"  ✅ No pending fixes: {health.breakdown['no_fixes']:.0f}/20\n")
    else:
        content.append(f"  ⚠️ Has pending fixes: 0/20\n")
    
    # No stale
    if health.breakdown.get('no_stale', 0) > 0:
        content.append(f"  ✅ No stale executions: {health.breakdown['no_stale']:.0f}/20\n")
    else:
        content.append(f"  ⚠️ Has stale executions: 0/20\n")
    
    # Tests (placeholder)
    content.append(f"  ⏸️ Tests: {health.breakdown.get('tests', 0):.0f}/15 (not integrated)\n")
    
    # Docs (placeholder)
    content.append(f"  ⏸️ Docs: {health.breakdown.get('docs', 0):.0f}/15 (not integrated)\n")
    
    border_style = "green" if health.score >= 80 else "yellow" if health.score >= 60 else "red"
    panel = Panel(content, title="🏥 Plan Health", border_style=border_style, padding=(1, 2))
    self.console.print(panel)
```

### 4. Achievement Parsing

**Function**: `_get_all_achievements()` in `plan_dashboard.py` (~60 lines)

**Purpose**: Parse Achievement Index from PLAN file

**Implementation**:

```python
def _get_all_achievements(self) -> List[Dict[str, str]]:
    """
    Parse all achievements from PLAN file.
    
    Parses the "Achievement Index" section and extracts:
    - Achievement number (e.g., "1.1")
    - Achievement title (e.g., "Plan-Specific Dashboard")
    
    Returns:
        List of achievement dicts with 'number' and 'title' keys
    
    Example:
        [
            {'number': '0.1', 'title': 'Rich Dashboard Framework Setup'},
            {'number': '0.2', 'title': 'Plan Discovery & State Detection'},
            ...
        ]
    """
    achievements = []
    
    plan_file = self.state.plan_file
    if not plan_file or not plan_file.exists():
        return []
    
    try:
        content = plan_file.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as e:
        logger.error("Failed to read PLAN file for achievements", exc_info=True, extra={
            'plan_file': str(plan_file)
        })
        return []
    
    # Parse Achievement Index section
    import re
    
    # Look for "## Achievement Index" or "## 📋 Achievement Index"
    index_pattern = re.compile(r'^##\s+(?:📋\s+)?Achievement Index', re.MULTILINE)
    match = index_pattern.search(content)
    
    if not match:
        logger.warning("No Achievement Index found in PLAN", extra={
            'plan_file': str(plan_file)
        })
        return []
    
    # Extract section after Achievement Index
    index_start = match.end()
    # Find next ## heading or end of file
    next_heading = re.search(r'^##\s+', content[index_start:], re.MULTILINE)
    index_end = index_start + next_heading.start() if next_heading else len(content)
    index_section = content[index_start:index_end]
    
    # Parse achievements: "- Achievement X.Y: Title"
    ach_pattern = re.compile(r'-\s+Achievement\s+(\d+\.\d+):\s+(.+?)(?:\n|$)')
    
    for match in ach_pattern.finditer(index_section):
        number = match.group(1)
        title = match.group(2).strip()
        
        achievements.append({
            'number': number,
            'title': title
        })
    
    logger.debug("Achievements parsed", extra={
        'plan_name': self.plan_name,
        'achievement_count': len(achievements)
    })
    
    return achievements
```

### 5. Test Suite

**File**: `tests/LLM/dashboard/test_achievement_visualization.py` (~350 lines, NEW)

**Purpose**: Comprehensive tests for achievement visualization features

**Test Coverage**:

```python
class TestAchievementListRendering:
    """Tests for achievement list rendering."""
    
    def test_render_achievements_empty(self):
        """Test with no achievements."""
    
    def test_render_achievements_with_data(self):
        """Test with multiple achievements."""
    
    def test_get_all_achievements_parsing(self):
        """Test achievement parsing from PLAN file."""
    
    def test_get_all_achievements_no_index(self):
        """Test when Achievement Index section missing."""

class TestStatusFormatting:
    """Tests for status formatting."""
    
    def test_format_status_approved(self):
        """Test approved achievement status."""
    
    def test_format_status_fix_pending(self):
        """Test fix pending status."""
    
    def test_format_status_in_progress(self):
        """Test in progress status."""
    
    def test_format_status_subplan_ready(self):
        """Test SUBPLAN ready status."""
    
    def test_format_status_not_started(self):
        """Test not started status."""
    
    def test_format_action_for_each_status(self):
        """Test action formatting for all statuses."""

class TestHealthScore:
    """Tests for plan health score."""
    
    def test_calculate_health_score_perfect(self):
        """Test health score for perfect plan."""
    
    def test_calculate_health_score_with_fixes(self):
        """Test health score with pending fixes."""
    
    def test_calculate_health_score_with_stale(self):
        """Test health score with stale executions."""
    
    def test_count_stale_executions(self):
        """Test stale execution detection."""
    
    def test_get_health_status_ranges(self):
        """Test health status for different score ranges."""
    
    def test_get_health_emoji_ranges(self):
        """Test health emoji for different score ranges."""
    
    def test_render_health_score(self):
        """Test health score rendering."""
```

---

## 🔧 Approach

### Phase 1: Achievement List Rendering (90 min)

**Goal**: Display all achievements in a table with status indicators

**Steps**:

1. **Implement `_get_all_achievements()`** (40 min):
   - Parse PLAN file for Achievement Index section
   - Use regex to extract achievement numbers and titles
   - Return list of achievement dicts
   - Handle missing Achievement Index gracefully

2. **Implement `render_achievements()`** (30 min):
   - Create Rich Table with 4 columns
   - Iterate through achievements
   - Call status and action formatters
   - Display with cyan border

3. **Implement status and action formatters** (20 min):
   - `_format_status()` - check files in priority order
   - `_format_action()` - suggest next action
   - Use filesystem state (APPROVED, FIX, EXECUTION, SUBPLAN)

**Verification**:
- Can parse Achievement Index from real PLAN
- Table displays correctly with all columns
- Status indicators show correct state
- Action suggestions are appropriate

---

### Phase 2: Plan Health Score (90 min)

**Goal**: Calculate and display overall plan health score (0-100)

**Steps**:

1. **Implement `calculate_health_score()`** (40 min):
   - Calculate completion points (30 max)
   - Check for pending fixes (20 points if none)
   - Count stale executions (20 points if none)
   - Tests placeholder (15 points, not integrated)
   - Docs placeholder (15 points, not integrated)
   - Return HealthScore dataclass

2. **Implement `_count_stale_executions()`** (20 min):
   - Find EXECUTION files without APPROVED
   - Check file modification time
   - Count files older than 7 days
   - Return count

3. **Implement `render_health_score()`** (20 min):
   - Display score with emoji and status
   - Show breakdown of components
   - Use green/yellow/red border based on score
   - Format as Panel

4. **Implement helper methods** (10 min):
   - `_get_health_status()` - map score to status
   - `_get_health_emoji()` - map score to emoji

**Verification**:
- Health score calculation is accurate
- Breakdown shows all components
- Stale execution detection works
- Rendering displays correctly

---

### Phase 3: Integration with Dashboard (30 min)

**Goal**: Integrate new features into plan dashboard

**Steps**:

1. **Update `show()` method** (15 min):
   - Add `render_health_score()` call
   - Add `render_achievements()` call
   - Position appropriately in dashboard layout

2. **Add HealthScore dataclass** (5 min):
   - Import dataclasses
   - Define HealthScore with score, status, emoji, breakdown

3. **Test integration** (10 min):
   - Verify all sections render correctly
   - Check dashboard layout
   - Test with real plan data

**Verification**:
- Dashboard shows health score and achievements
- Layout is clean and readable
- All features work together

---

### Phase 4: Testing (60 min)

**Goal**: Achieve >90% test coverage with comprehensive tests

**Steps**:

1. **Create `test_achievement_visualization.py`** (40 min):
   - Test achievement list rendering
   - Test status formatting (5 statuses)
   - Test action formatting
   - Test health score calculation
   - Test stale execution detection
   - Test helper methods

2. **Run tests and fix issues** (20 min):
   ```bash
   pytest tests/LLM/dashboard/test_achievement_visualization.py -v
   pytest tests/LLM/dashboard/ -v  # Full suite
   ```
   - Fix any test failures
   - Achieve >90% coverage
   - No linter errors

**Verification**:
- All tests pass (25+ tests)
- Coverage >90%
- No linter errors
- No regressions in existing tests

---

## 🔄 Execution Strategy

### Type: Single EXECUTION (Recommended)

**Rationale**:

1. **Cohesive Feature**: All components work together (list, status, health score)
2. **Manageable Scope**: 3-4 hours, can be done in one focused session
3. **Sequential Dependencies**: Each phase builds on previous
4. **Atomic Delivery**: Feature is only useful when complete

**Execution**: Create single `EXECUTION_TASK_LLM-DASHBOARD-CLI_12_01.md`

**Alternative**: Could split into 2 EXECUTIONs (list + status, health score + testing), but overhead not worth it

---

## 🧪 Testing Strategy

### Unit Testing

**Scope**: Test each function in isolation

**Test Files**:
- `test_achievement_visualization.py` - All visualization features

**Coverage Target**: >90% for new code

**Key Tests**:
- Achievement parsing from PLAN file
- Status formatting (5 different statuses)
- Action formatting (6 different actions)
- Health score calculation (various scenarios)
- Stale execution detection
- Rendering methods

### Integration Testing

**Scope**: Test with real plan structure

**Test Cases**:
1. **Full Dashboard with Achievements**:
   - Create plan with multiple achievements
   - Verify table rendering
   - Check status accuracy

2. **Health Score Scenarios**:
   - Perfect plan (100 score)
   - Plan with fixes (reduced score)
   - Plan with stale executions (reduced score)

3. **Edge Cases**:
   - Empty Achievement Index
   - Missing directories
   - Malformed PLAN file

### Manual Testing

**Verification**:
- Test with LLM-DASHBOARD-CLI plan (real data)
- Verify achievements display correctly
- Check health score accuracy
- Test with PARALLEL-EXECUTION-AUTOMATION plan

---

## 📊 Expected Results

### Success Criteria

**Functional**:
- ✅ Achievement list displays in table format
- ✅ Status indicators show correct state (5 statuses)
- ✅ Action suggestions are appropriate
- ✅ Health score calculates correctly (0-100)
- ✅ Health score breakdown shows components
- ✅ Stale execution detection works (>7 days)
- ✅ Handles missing Achievement Index gracefully

**Quality**:
- ✅ Test coverage >90% for new code
- ✅ All tests passing (25+ tests)
- ✅ No linter errors
- ✅ Clear, readable formatting

**User Experience**:
- ✅ Table is easy to read
- ✅ Status indicators are clear
- ✅ Health score is motivating
- ✅ Rendering is fast (<100ms for 20 achievements)

### Deliverable Metrics

**Files Created**: 2 files (~500 lines total)
- Modified: 1 file (~200 new lines)
- New: 1 file (~350 lines)

**Test Metrics**:
- Total Tests: ~25 new tests
- Coverage: >90% for new code
- All tests passing

---

## 🚨 Risks & Mitigations

### Risk 1: Achievement Index Parsing

**Risk**: PLAN files might have inconsistent Achievement Index format

**Impact**: MEDIUM - Can't display achievements

**Mitigation**:
- Support multiple formats ("Achievement X.Y:", "- Achievement X.Y")
- Graceful fallback (show empty if can't parse)
- Test with multiple PLAN file formats
- Log warnings for unparseable formats

### Risk 2: Performance with Large Plans

**Risk**: Plans with 50+ achievements might render slowly

**Impact**: LOW - Dashboard feels sluggish

**Mitigation**:
- Benchmark with large plans
- Use efficient glob patterns
- Cache achievement list if needed
- Target <100ms render time

### Risk 3: Stale Execution False Positives

**Risk**: Active work might be flagged as stale (>7 days)

**Impact**: LOW - Inaccurate health score

**Mitigation**:
- 7 days is reasonable threshold
- Only flag if no APPROVED exists
- Clear in health score breakdown
- Users can ignore if actively working

### Risk 4: Health Score Interpretation

**Risk**: Users might not understand what health score means

**Impact**: MEDIUM - Feature not useful

**Mitigation**:
- Show clear breakdown
- Use familiar emoji indicators (🟢🟡🟠🔴)
- Document components in UI
- Add tooltips or help text (future)

---

## 💡 Design Decisions

### Decision 1: Table vs List for Achievements

**Chosen**: Rich Table with 4 columns

**Rationale**:
- Table provides clear structure
- Columns enable scanning (status, action)
- Rich Table is visually appealing
- Familiar format for users

**Alternative Considered**: Simple list, but less scannable

### Decision 2: Status Priority Order

**Chosen**: APPROVED > FIX > In Progress > SUBPLAN ready > Not started

**Rationale**:
- Highest priority statuses first (APPROVED, FIX)
- Logical progression through workflow
- Matches user mental model
- Easy to implement (cascade if-elif)

**Alternative Considered**: Alphabetical, but less meaningful

### Decision 3: Health Score Components

**Chosen**: 5 components (completion, fixes, stale, tests, docs) totaling 100 points

**Rationale**:
- Completion is most important (30 points)
- Pending fixes are critical (20 points)
- Stale work indicates problems (20 points)
- Tests and docs are important but secondary (15 each)
- Total 100 is intuitive

**Alternative Considered**: Weighted average, but fixed points are clearer

### Decision 4: Stale Threshold

**Chosen**: 7 days without APPROVED

**Rationale**:
- Most achievements complete in 1-3 days
- 7 days suggests abandonment or blocking
- Not too aggressive (2-3 days) or too lenient (14 days)
- Can be adjusted based on feedback

**Alternative Considered**: 14 days, but too lenient

### Decision 5: Single EXECUTION

**Chosen**: One EXECUTION_TASK for all components

**Rationale**:
- 3-4 hours is manageable
- Components are tightly coupled
- Atomic feature delivery
- Less overhead than split

**Alternative Considered**: Split into 2 EXECUTIONs (list, health), but not needed

---

## 📝 Implementation Notes

### Achievement Index Format

**Expected Format** in PLAN file:

```markdown
## Achievement Index

**Priority 0: FOUNDATION**

- Achievement 0.1: Rich Dashboard Framework Setup
- Achievement 0.2: Plan Discovery & State Detection

**Priority 1: PLAN DASHBOARD**

- Achievement 1.1: Plan-Specific Dashboard
- Achievement 1.2: Achievement State Visualization
```

**Parsing Strategy**:
- Find "## Achievement Index" heading
- Extract until next ## heading
- Use regex: `- Achievement (\d+\.\d+): (.+)`
- Support with or without emoji in heading

### File Pattern Conventions

**Status Detection** (filesystem patterns):
- APPROVED: `execution/feedbacks/APPROVED_{number}.md`
- FIX: `execution/feedbacks/FIX_{number}.md`
- EXECUTION: `execution/EXECUTION_TASK_*_{number}_*.md`
- SUBPLAN: `subplans/SUBPLAN_*_{number}.md`

**Achievement Number**: `{major}.{minor}` → filename uses `{major}{minor}` (no dot)
- Example: "1.2" → "APPROVED_12.md"

### Health Score Breakdown Display

**Format**:
```
🏥 Plan Health
🟢 Score: 87/100 - Good

Breakdown:
  ✅ Completion: 26/30 (11/18 achievements)
  ✅ No pending fixes: 20/20
  ⚠️ Has stale executions: 0/20 (2 executions >7 days)
  ⏸️ Tests: 0/15 (not integrated)
  ⏸️ Docs: 0/15 (not integrated)
```

---

## 🔗 Dependencies

### Requires (from previous achievements):

- Achievement 0.2: `StateDetector`, `PlanState` ✅
- Achievement 1.1: `PlanDashboard` base class ✅

### Enables (for future achievements):

- Achievement 1.3: Quick Action Shortcuts (will use achievement list for actions)
- Achievement 2.1: Parallel Execution Detection (will enhance achievement display)

### External Dependencies:

- Python 3.8+ (existing)
- Rich library (from Achievement 0.1)
- No new external libraries needed

---

## ✅ Definition of Done

**Code Complete**:
- [ ] `_get_all_achievements()` implemented (~60 lines)
- [ ] `render_achievements()` implemented (~80 lines)
- [ ] `_format_status()` implemented (~30 lines)
- [ ] `_format_action()` implemented (~30 lines)
- [ ] `calculate_health_score()` implemented (~60 lines)
- [ ] `render_health_score()` implemented (~40 lines)
- [ ] Helper methods implemented (~30 lines)
- [ ] `test_achievement_visualization.py` created (~350 lines)

**Tests Complete**:
- [ ] 25+ tests written and passing
- [ ] >90% coverage for new code
- [ ] Achievement parsing tested
- [ ] Status formatting tested (all 5 statuses)
- [ ] Health score tested (various scenarios)

**Quality Complete**:
- [ ] No linter errors
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] Error messages clear

**Integration Complete**:
- [ ] Integrated into plan_dashboard.py
- [ ] Renders correctly in dashboard
- [ ] No performance issues
- [ ] Works with real PLAN files

---

**Status**: 📋 Ready for Execution  
**Next Step**: Create `EXECUTION_TASK_LLM-DASHBOARD-CLI_12_01.md` and execute work  
**Executor**: Begin with Phase 1 (Achievement List Rendering)

