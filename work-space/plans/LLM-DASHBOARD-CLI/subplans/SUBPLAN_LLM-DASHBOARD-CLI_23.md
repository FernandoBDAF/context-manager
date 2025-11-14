# SUBPLAN: Real-Time State Updates

**Type**: SUBPLAN  
**Mother Plan**: PLAN_LLM-DASHBOARD-CLI.md  
**Plan**: LLM-DASHBOARD-CLI  
**Achievement Addressed**: Achievement 2.3 (Real-Time State Updates)  
**Achievement**: 2.3  
**Status**: Not Started  
**Created**: 2025-11-14 22:30 UTC  
**Estimated Effort**: 3-4 hours

**Metadata Tags**: `#dashboard #real-time-updates #state-watcher #cache-invalidation #multi-instance`

**File Location**: `work-space/plans/LLM-DASHBOARD-CLI/subplans/SUBPLAN_LLM-DASHBOARD-CLI_23.md`

**Size**: 200-600 lines (within target range)

---

## 🎯 Objective

Create a real-time state monitoring system for the dashboard that automatically detects filesystem changes and updates the display without manual refresh. This implements Achievement 2.3 (Real-Time State Updates) and includes state consistency mechanisms (Gap Fix #5) to ensure the dashboard always shows current state, handles multiple dashboard instances safely, and provides both automatic and manual refresh capabilities with clear UI indicators.

---

## 📋 What Needs to Be Created

### Files to Create

1. **`LLM/dashboard/state_watcher.py`** (300-400 lines)
   - `StateWatcher` class for monitoring filesystem changes
   - File watcher using polling (simple) or watchdog library (advanced)
   - Callback mechanism for state change notifications
   - Watch execution/feedbacks/ and execution/ directories
   - Debouncing to avoid excessive callbacks

2. **`tests/LLM/dashboard/test_state_watcher.py`** (300-400 lines)
   - Unit tests for StateWatcher
   - Tests for file change detection
   - Tests for callback invocation
   - Tests for debouncing
   - Mock filesystem operations

3. **`tests/LLM/dashboard/test_state_consistency.py`** (200-300 lines)
   - Tests for cache invalidation
   - Tests for manual refresh
   - Tests for auto-refresh after actions
   - Tests for multi-instance detection
   - Tests for lock file management

### Files to Modify

1. **`LLM/dashboard/plan_dashboard.py`** (significant changes)
   - Add `StateWatcher` integration
   - Add `show_live()` method with Rich Live display
   - Add `handle_state_refresh()` for manual refresh
   - Add `auto_refresh_after_action()` called after each action
   - Add multi-instance detection (`detect_multi_instance()`, `create_lock_file()`, `cleanup_lock_file()`)
   - Add 'r' key handler for manual refresh
   - Add 'c' key handler for cache clear
   - Update `show()` to use live display mode
   - Add footer with last updated timestamp
   - Add atexit handler for lock file cleanup

2. **`LLM/dashboard/base_dashboard.py`** (minor changes)
   - Add timestamp tracking for last refresh
   - Add method to check cache staleness
   - Add utility methods for refresh indicators

3. **`LLM/dashboard/state_detector.py`** (if using caching)
   - Verify cache implementation
   - Ensure mtime-based cache keys
   - Add cache.clear() method if not present

### Functions/Classes to Add

**StateWatcher Class**:

```python
class StateWatcher:
    """Watch filesystem for state changes."""
    
    def __init__(self, plan_path: Path, callback: Callable):
        """Initialize watcher."""
        
    def start(self):
        """Start watching for changes."""
        
    def stop(self):
        """Stop watching."""
        
    def _poll_for_changes(self):
        """Poll directories for changes."""
        
    def _debounce_callback(self):
        """Debounce multiple rapid changes."""
```

**PlanDashboard Additions**:

```python
def show_live(self):
    """Show dashboard with live updates."""
    
def handle_state_refresh(self):
    """Manual refresh with cache invalidation."""
    
def auto_refresh_after_action(self):
    """Auto-refresh after action execution."""
    
def detect_multi_instance(self) -> bool:
    """Detect if another dashboard running."""
    
def create_lock_file(self):
    """Create lock file for this instance."""
    
def cleanup_lock_file(self):
    """Remove lock file on exit."""
    
def render_with_timestamp(self):
    """Render dashboard with refresh timestamp."""
```

### Tests Required

**Test File 1**: `tests/LLM/dashboard/test_state_watcher.py`

**Test Cases**:

1. **Initialization Tests** (3 tests)
   - Test StateWatcher initialization
   - Test callback registration
   - Test directory validation

2. **File Change Detection** (8 tests)
   - Test detects new APPROVED file
   - Test detects new FIX file
   - Test detects new EXECUTION_TASK file
   - Test detects file deletion
   - Test detects file modification
   - Test ignores non-relevant files
   - Test watches correct directories
   - Test recursive directory watching

3. **Callback Tests** (5 tests)
   - Test callback invoked on change
   - Test callback receives correct data
   - Test multiple callbacks
   - Test callback error handling
   - Test callback debouncing

4. **Polling Tests** (4 tests)
   - Test polling interval
   - Test stop/start polling
   - Test polling performance
   - Test cleanup on stop

**Test File 2**: `tests/LLM/dashboard/test_state_consistency.py`

**Test Cases**:

1. **Cache Invalidation** (6 tests)
   - Test manual cache clear
   - Test auto-clear after action
   - Test mtime-based invalidation
   - Test cache.clear() method exists
   - Test all caches cleared
   - Test state reload after clear

2. **Manual Refresh** (4 tests)
   - Test 'r' key triggers refresh
   - Test refresh indicator displayed
   - Test state updated after refresh
   - Test timestamp updated

3. **Auto-Refresh** (5 tests)
   - Test auto-refresh after execute_next
   - Test auto-refresh after create_subplan
   - Test auto-refresh after create_execution
   - Test filesystem settle delay
   - Test refresh only when needed

4. **Multi-Instance Detection** (7 tests)
   - Test lock file creation
   - Test lock file detection
   - Test stale lock file cleanup
   - Test process existence check
   - Test lock file cleanup on exit
   - Test warning on multi-instance
   - Test atexit handler registration

**Total**: ~40 comprehensive tests

---

## 📝 Approach

**Strategy**: Build a lightweight state monitoring system using filesystem polling (simpler than watchdog library) with automatic and manual refresh capabilities, cache invalidation, and multi-instance safety.

**Method**:

1. **Create StateWatcher (Simple Polling)** (1 hour)
   - Use simple polling instead of watchdog library (fewer dependencies)
   - Poll execution/feedbacks/ and execution/ directories every 2 seconds
   - Track file mtimes to detect changes
   - Debounce callbacks (wait 500ms after last change)
   - Thread-based polling for non-blocking operation

2. **Add Manual Refresh to PlanDashboard** (45 min)
   - Implement `handle_state_refresh()` with cache clearing
   - Add 'r' key handler in `get_user_input()`
   - Show "🔄 Refreshing..." indicator
   - Update last_refresh_time timestamp
   - Log refresh events with structured logging

3. **Add Auto-Refresh After Actions** (30 min)
   - Implement `auto_refresh_after_action()`
   - Call after each action method completes
   - Add 500ms delay for filesystem settle
   - Clear caches and reload state
   - Update timestamp

4. **Implement Multi-Instance Detection** (1 hour)
   - Create lock file with PID on dashboard start
   - Check for existing lock file on start
   - Validate PID is still running
   - Clean up stale lock files
   - Register atexit handler for cleanup
   - Show warning if another instance detected
   - Allow override with user confirmation

5. **Add Live Display Mode (Optional)** (45 min)
   - Integrate StateWatcher with Rich Live
   - Update display on state changes
   - Add footer with timestamp
   - Handle keyboard interrupts gracefully
   - **Decision**: Make this optional/future enhancement (complex)

6. **Add Refresh Indicators** (30 min)
   - Show last updated timestamp in footer
   - Show "🔄 Refreshing..." during refresh
   - Show "⚠️ Stale data (5m+)" if no refresh in 5 minutes
   - Use Rich styling for indicators

7. **Write Comprehensive Tests** (1.5 hours)
   - Write ~40 tests covering all functionality
   - Mock filesystem operations
   - Mock time.sleep for faster tests
   - Test error conditions and edge cases
   - Verify cache invalidation

8. **Integration and Polish** (30 min)
   - Ensure all pieces work together
   - Test multi-instance handling
   - Test auto-refresh flow
   - Fix any integration issues
   - Update documentation

**Key Considerations**:

- **Simplicity vs Features**: Simple polling is easier than watchdog library
  - **Decision**: Use polling (no external dependencies, easier to test)
  
- **Live Display Complexity**: Rich Live is powerful but adds complexity
  - **Decision**: Defer live display to future enhancement, focus on refresh mechanisms
  
- **Refresh Frequency**: Balance between responsiveness and performance
  - **Decision**: Poll every 2 seconds, debounce callbacks by 500ms
  
- **Cache Strategy**: Need to ensure cache invalidation works
  - **Decision**: Manual clear + mtime-based keys (if caching implemented)

**Trade-offs**:

- **Polling vs Watchdog**: 
  - Polling: Simpler, no dependencies, slight delay (2s)
  - Watchdog: Instant, complex, external dependency
  - **Decision**: Use polling for simplicity

- **Live Mode vs Refresh Mode**:
  - Live: Always updating, complex keyboard handling
  - Refresh: Simpler, user-triggered or auto-triggered
  - **Decision**: Refresh mode only (simpler, sufficient)

**Risks to Watch For**:

- **Race Conditions**: Multiple threads accessing state
  - **Mitigation**: Use threading locks, debounce callbacks
  
- **Lock File Cleanup**: Stale lock files if crash
  - **Mitigation**: Check PID validity, clean up stale locks
  
- **Cache Invalidation**: If caching not implemented, need to verify
  - **Mitigation**: Check state_detector for cache, add if needed
  
- **Performance**: Polling every 2s might impact performance
  - **Mitigation**: Monitor CPU usage, adjust interval if needed

---

## 🔄 Execution Strategy

**Execution Count**: Single

**Rationale**: Single clear approach, cohesive implementation

- **Clear Requirements**: Achievement 2.3 has well-defined deliverables
- **Cohesive Feature**: All components work together for state consistency
- **No Alternatives**: Polling is chosen approach, no A/B testing needed
- **Sequential Implementation**: Each component builds on previous

**EXECUTION_TASK**: `EXECUTION_TASK_LLM-DASHBOARD-CLI_23_01.md`

**Implementation Flow**:

1. StateWatcher (polling) → 2. Manual refresh → 3. Auto-refresh → 4. Multi-instance → 5. Indicators → 6. Tests

---

## 🧪 Tests Required

### Test File 1

- **Path**: `tests/LLM/dashboard/test_state_watcher.py`
- **Test Cases**: ~20 tests covering initialization, file detection, callbacks, polling
- **Approach**: Mock filesystem, use temporary directories, mock time.sleep

### Test File 2

- **Path**: `tests/LLM/dashboard/test_state_consistency.py`
- **Test Cases**: ~22 tests covering cache, refresh, multi-instance
- **Approach**: Mock cache operations, mock lock files, verify cleanup

### Coverage Requirements

- **Target Coverage**: >90% for new code
- **Required Test Types**:
  - Unit tests for StateWatcher class
  - Integration tests for refresh flows
  - Edge case tests for lock file handling
  - Mock tests for filesystem operations

### Test-First Requirement

- [ ] Tests written before implementation (TDD workflow)
- [ ] Initial test run shows all failing (red)
- [ ] Tests define success criteria
- [ ] Implementation makes tests pass (green)

---

## ✅ Expected Results

### Functional Changes

**After this SUBPLAN is complete, users will have**:

1. **Automatic State Updates**:
   - State refreshes automatically after any action
   - No need to restart dashboard to see changes
   - Cache cleared and state reloaded from filesystem

2. **Manual Refresh Option**:
   - Press 'r' to manually refresh state
   - Clears all caches and reloads from filesystem
   - Shows "🔄 Refreshing..." indicator
   - Updates "Last updated" timestamp

3. **Multi-Instance Safety**:
   - Dashboard checks for other running instances on start
   - Shows warning if another instance detected
   - Allows override with user confirmation
   - Cleans up lock file on normal exit
   - Detects and removes stale lock files

4. **State Consistency**:
   - Dashboard always shows current filesystem state
   - Cache invalidation prevents stale data
   - Timestamp shows when state was last updated
   - Warning if data is stale (5+ minutes old)

5. **Clear UI Feedback**:
   - Footer shows "Last updated: HH:MM:SS"
   - "🔄 Refreshing..." during refresh
   - "⚠️ Stale data (5m+)" warning if old
   - "✓ State refreshed from filesystem" on manual refresh

### Performance Changes

- **Polling overhead**: ~0.1% CPU for 2-second polling
- **Refresh time**: <100ms to clear cache and reload state
- **User experience**: Perceived instant updates after actions

### Observable Outcomes

**Success Indicators**:

1. **User executes action and state updates**:
   ```
   User presses '1' (Execute Next)
   → Workflow executes
   → Auto-refresh triggered (500ms delay)
   → State reloaded from filesystem
   → Dashboard shows updated state
   → Timestamp updated in footer
   ```

2. **User manually refreshes**:
   ```
   User presses 'r'
   → "🔄 Refreshing..." displayed
   → Caches cleared
   → State reloaded
   → "✓ State refreshed from filesystem" shown
   → Timestamp updated
   ```

3. **Multi-instance detection**:
   ```
   Terminal 1: python LLM/main.py (running)
   Terminal 2: python LLM/main.py (new)
   
   → Dashboard detects existing instance
   → Shows warning:
     "⚠️ Another dashboard instance is already running (PID: 12345)
      Continue anyway? [y/N]"
   → User can choose to continue or exit
   ```

4. **Tests verify all functionality**:
   ```bash
   $ python -m pytest tests/LLM/dashboard/test_state_watcher.py -v
   $ python -m pytest tests/LLM/dashboard/test_state_consistency.py -v
   
   ========== 42 passed in 1.23s ==========
   ```

---

## 🔍 Conflict Analysis with Other Subplans

**Review Existing Subplans**:

From PLAN tracking:
- ✅ SUBPLAN_11 (Achievement 1.1) - Complete
- ✅ SUBPLAN_12 (Achievement 1.2) - Complete
- ✅ SUBPLAN_13 (Achievement 1.3) - Complete
- ✅ SUBPLAN_21 (Achievement 2.1) - Complete
- ✅ SUBPLAN_22 (Achievement 2.2) - Complete
- 🆕 SUBPLAN_23 (Achievement 2.3) - This SUBPLAN

**Check for Conflicts**:

- **Overlap**: None - This adds new real-time update functionality
- **Conflicts**: None - Extends existing dashboard without replacing anything
- **Dependencies**: 
  - ✅ Achievement 2.2 complete (actions to auto-refresh after)
  - ✅ All dashboard achievements complete (ready for real-time updates)
- **Integration**:
  - Integrates with Achievement 2.2 (auto-refresh after workflow execution)
  - Integrates with Achievement 1.1 (PlanDashboard gets refresh methods)

**Analysis**:

- **No conflicts detected**: This achievement adds state monitoring and refresh capabilities
- **Depends on Achievement 2.2**: Auto-refresh called after each action execution
- **Extends PlanDashboard**: Adds new methods for refresh and multi-instance handling
- **Backward compatible**: Existing functionality unchanged, new features are additive

**Result**: Safe to proceed - No conflicts, dependencies met, clean extension

---

## 🔗 Dependencies

### Other Subplans

- **Depends on SUBPLAN_22** (Achievement 2.2 - Interactive Workflow Execution): ✅ Complete
  - Provides action methods to call auto-refresh after
  - Workflow execution triggers state changes that need refresh

- **Depends on SUBPLAN_11** (Achievement 1.1 - Plan-Specific Dashboard): ✅ Complete
  - Provides `PlanDashboard` class to extend with refresh methods

### External Dependencies

**Python Libraries** (standard library only):
- `threading`: For background polling
- `time`: For delays and timestamps
- `os`: For PID checking
- `signal`: For process validation (Unix)
- `atexit`: For lock file cleanup
- `pathlib`: For file path handling
- `datetime`: For timestamps

**Dashboard Infrastructure** (already exists):
- `rich.live.Live`: For live display (if implementing)
- `rich.text.Text`: For footer text
- `rich.group.Group`: For combining renderable
- `LLM/dashboard/base_dashboard.py`: Base class
- `LLM/dashboard/state_detector.py`: State detection
- `LLM/dashboard/plan_dashboard.py`: Integration point

**No new external dependencies required** (no watchdog library needed)

### Prerequisite Knowledge

- **Threading**: Background polling with thread safety
- **Rich Live Display**: Rich Live context manager (if implementing)
- **Cache Management**: Understanding of cache invalidation strategies
- **Process Management**: PID checking and lock files on Unix systems

**Documentation to Review**:
- Rich Live documentation (if implementing live mode)
- Python threading documentation
- Unix process management (os.kill, PID validation)

---

## 🔄 Execution Task Reference

**Execution Tasks**:

- `EXECUTION_TASK_LLM-DASHBOARD-CLI_23_01.md` - Implement real-time state updates (3-4 hours)

**Status**: Planning

---

## 📊 Success Criteria

**This Subplan is Complete When**:

- [ ] `StateWatcher` class created with polling mechanism
- [ ] Manual refresh implemented (`handle_state_refresh()`, 'r' key)
- [ ] Auto-refresh implemented (`auto_refresh_after_action()`)
- [ ] Multi-instance detection implemented (lock files, PID checking)
- [ ] Refresh indicators implemented (timestamp, spinner, warnings)
- [ ] Cache invalidation working correctly
- [ ] ~42 tests written and passing (>90% coverage)
- [ ] Manual testing confirms refresh works after actions
- [ ] Multi-instance warning displays correctly
- [ ] Lock file cleanup verified
- [ ] Code documented with docstrings and comments
- [ ] EXECUTION_TASK_23_01 complete
- [ ] Achievement feedback received (APPROVED_23.md or FIX_23.md)
- [ ] Ready for archive

**Specific Success Indicators**:

1. User sees state update automatically after executing action
2. User can press 'r' to manually refresh
3. Dashboard shows warning if another instance running
4. Lock file cleaned up on dashboard exit
5. All 42 tests pass
6. No linter errors in new code

---

## ✅ Completion Workflow (Filesystem-First)

**After All Work Complete**:

1. **Request Review**: Ask reviewer to assess achievement completion
2. **Reviewer Creates Feedback File**:
   - **If Approved**: Create `execution/feedbacks/APPROVED_23.md`
   - **If Fixes Needed**: Create `execution/feedbacks/FIX_23.md` with detailed issues
3. **Filesystem = Source of Truth**: Achievement completion tracked by APPROVED file existence

**Do NOT**:
- ❌ Manually update PLAN markdown with "✅ Achievement complete"
- ❌ Add checkmarks to Achievement Index
- ❌ Update "Current Status & Handoff"

**DO**:
- ✅ Request reviewer feedback after work complete
- ✅ Wait for `APPROVED_23.md` or `FIX_23.md` file creation
- ✅ If FIX required: Address issues, request re-review

---

## 📝 Notes

**Common Pitfalls**:

- **Threading Issues**: Ensure thread-safe access to shared state
- **Lock File Cleanup**: Handle crashes gracefully (check PID validity)
- **Cache Verification**: Verify caching is actually implemented before clearing
- **Polling Performance**: Monitor CPU usage, adjust interval if needed
- **Rich Live Complexity**: Defer live mode if too complex, focus on refresh

**Resources**:

- Python threading documentation
- Rich Live documentation: https://rich.readthedocs.io/en/stable/live.html
- Unix process management
- Existing dashboard code for patterns

**Design Notes**:

- **Polling vs Watchdog**: Chose polling for simplicity (no dependencies)
- **Live Mode**: Defer to future if complex, focus on refresh mechanisms
- **Refresh Triggers**: Auto after actions, manual via 'r' key
- **Multi-Instance**: Detect via lock file, allow override with confirmation

---

## 🔄 Active EXECUTION_TASKs

**Real-Time Tracking**:

| EXECUTION                                       | Status   | Progress | Notes |
| ----------------------------------------------- | -------- | -------- | ----- |
| EXECUTION_TASK_LLM-DASHBOARD-CLI_23_01 | Planning | 0%       | -     |

---

## 📊 Execution Results Synthesis

**To be completed after execution finishes**

---

## 📖 What to Read (Focus Rules)

**When working on this SUBPLAN**, follow these focus rules:

**✅ READ ONLY**:

- This SUBPLAN file (complete file)
- Parent PLAN Achievement 2.3 section (~159 lines)
- Active EXECUTION_TASK (EXECUTION_TASK_LLM-DASHBOARD-CLI_23_01.md)
- `LLM/dashboard/plan_dashboard.py` (integration point)
- `LLM/dashboard/state_detector.py` (cache verification)

**❌ DO NOT READ**:

- Parent PLAN full content (3000+ lines)
- Other achievements in PLAN
- Other SUBPLANs
- Completed EXECUTION_TASKs

**Context Budget**: ~600 lines total

**Why**: SUBPLAN defines HOW to achieve Achievement 2.3. Reading other achievements adds unnecessary scope.

---

**Ready to Execute**:

- **Designer**: SUBPLAN design complete ✅
- **Next Step**: Create EXECUTION_TASK_LLM-DASHBOARD-CLI_23_01.md
- **Executor**: Will read SUBPLAN objective + approach, then execute
- **Reference**: `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` for workflow

