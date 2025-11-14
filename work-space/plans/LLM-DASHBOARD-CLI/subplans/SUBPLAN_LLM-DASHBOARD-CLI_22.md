# SUBPLAN: Interactive Workflow Execution

**Type**: SUBPLAN  
**Mother Plan**: PLAN_LLM-DASHBOARD-CLI.md  
**Plan**: LLM-DASHBOARD-CLI  
**Achievement Addressed**: Achievement 2.2 (Interactive Workflow Execution)  
**Achievement**: 2.2  
**Status**: Not Started  
**Created**: 2025-11-14 21:00 UTC  
**Estimated Effort**: 3-4 hours

**Metadata Tags**: `#dashboard #workflow-execution #interactive-cli #progress-tracking`

**File Location**: `work-space/plans/LLM-DASHBOARD-CLI/subplans/SUBPLAN_LLM-DASHBOARD-CLI_22.md`

**Size**: 200-600 lines (within target range)

---

## 🎯 Objective

Create an interactive workflow execution system that enables users to execute LLM methodology workflows directly from the dashboard. This implements Achievement 2.2 (Interactive Workflow Execution) and provides real-time progress tracking, result display, and error recovery for the three primary workflows: "Execute Next", "Create SUBPLAN", and "Create EXECUTION". This builds upon the quick action shortcuts from Achievement 1.3 by transforming simple command execution into an intelligent, interactive workflow system with live feedback and guided user prompts.

---

## 📋 What Needs to Be Created

### Files to Create

1. **`LLM/dashboard/workflow_executor.py`** (300-400 lines)
   - Main workflow execution engine
   - `WorkflowExecutor` class with workflow routing
   - Progress tracking for long-running operations
   - Result display with Rich panels
   - Error handling and recovery suggestions

2. **`LLM/dashboard/models.py`** (additions to existing file)
   - `ExecutionResult` dataclass for capturing workflow results
   - `WorkflowState` dataclass for workflow progress tracking
   - Enums for workflow types and states

3. **`tests/LLM/dashboard/test_workflow_executor.py`** (400-500 lines)
   - Unit tests for workflow execution
   - Mock tests for subprocess calls
   - Progress tracking tests
   - Result display tests
   - Error handling tests

### Files to Modify

1. **`LLM/dashboard/plan_dashboard.py`**
   - Import `WorkflowExecutor`
   - Update action methods to use `WorkflowExecutor` instead of `ActionExecutor`
   - Add interactive prompts for workflow confirmation
   - Display workflow results after execution

2. **`LLM/dashboard/action_executor.py`** (potentially deprecate or refactor)
   - Review current implementation
   - Either extend with workflow capabilities or replace with `WorkflowExecutor`
   - Decision: Extend `ActionExecutor` with workflow methods vs. create new `WorkflowExecutor`

### Functions/Classes to Add

**WorkflowExecutor Class**:

```python
class WorkflowExecutor:
    """Execute LLM methodology workflows interactively."""
    
    def __init__(self, plan_path: Path, console: Console):
        """Initialize executor with plan context."""
        
    def execute_workflow(self, workflow_type: str, **kwargs):
        """Route to appropriate workflow handler."""
        
    def _execute_next_workflow(self):
        """Execute the 'next' workflow with state detection."""
        
    def _execute_subplan_workflow(self, achievement_id: str):
        """Execute SUBPLAN creation workflow."""
        
    def _execute_execution_workflow(self, subplan_id: str):
        """Execute EXECUTION_TASK creation workflow."""
        
    def _track_progress(self, process: subprocess.Popen, task_name: str):
        """Track execution progress with Rich Progress."""
        
    def _display_result(self, result: ExecutionResult):
        """Display execution result with Rich panels."""
        
    def _handle_error(self, error: Exception, workflow: str):
        """Handle workflow errors with recovery suggestions."""
```

**Supporting Functions**:

```python
def parse_workflow_output(output: str) -> ExecutionResult:
    """Parse workflow script output into structured result."""
    
def estimate_workflow_duration(workflow_type: str) -> int:
    """Estimate workflow duration in seconds."""
    
def format_workflow_result(result: ExecutionResult) -> Panel:
    """Format workflow result as Rich Panel."""
```

### Tests Required

**Test File**: `tests/LLM/dashboard/test_workflow_executor.py`

**Test Cases**:

1. **Workflow Routing Tests** (5 tests)
   - Test `execute_workflow()` routes to correct handler
   - Test unknown workflow type raises error
   - Test workflow type validation

2. **Next Workflow Tests** (8 tests)
   - Test next workflow with "create_subplan" state
   - Test next workflow with "create_execution" state
   - Test next workflow with "continue_execution" state
   - Test next workflow with "no_next" state
   - Test subprocess execution and capture
   - Test error handling during execution
   - Test result parsing
   - Test interactive prompts (mocked)

3. **SUBPLAN Workflow Tests** (6 tests)
   - Test SUBPLAN creation command building
   - Test SUBPLAN workflow with valid achievement
   - Test SUBPLAN workflow with invalid achievement
   - Test progress tracking during SUBPLAN creation
   - Test result display after SUBPLAN creation
   - Test error recovery suggestions

4. **EXECUTION Workflow Tests** (6 tests)
   - Test EXECUTION creation command building
   - Test EXECUTION workflow with valid SUBPLAN
   - Test EXECUTION workflow without SUBPLAN
   - Test progress tracking during EXECUTION creation
   - Test result display after EXECUTION creation
   - Test prerequisite validation errors

5. **Progress Tracking Tests** (4 tests)
   - Test progress bar creation
   - Test progress updates during execution
   - Test progress completion
   - Test progress error state

6. **Result Display Tests** (5 tests)
   - Test success result display (green panel)
   - Test failure result display (red panel)
   - Test result with deliverables list
   - Test result with test results
   - Test result with duration formatting

7. **Error Handling Tests** (4 tests)
   - Test subprocess error capture
   - Test error message formatting
   - Test recovery suggestion generation
   - Test error logging

8. **Integration Tests** (3 tests)
   - Test complete workflow: next → create_subplan
   - Test complete workflow: next → create_execution
   - Test complete workflow: next → continue_execution

**Total**: ~35-40 comprehensive tests

---

## 📝 Approach

**Strategy**: Build an intelligent workflow executor that wraps existing LLM methodology scripts with interactive prompts, progress tracking, and rich result display. Focus on user experience by providing real-time feedback and actionable error messages.

**Method**:

1. **Create Data Models** (30 min)
   - Define `ExecutionResult` dataclass with fields: success, error, deliverables, tests_passing, tests_total, duration, log_file
   - Define `WorkflowState` enum: PENDING, RUNNING, SUCCESS, FAILED
   - Define `WorkflowType` enum: NEXT, SUBPLAN, EXECUTION

2. **Implement WorkflowExecutor Core** (1 hour)
   - Create `WorkflowExecutor` class with plan context and console
   - Implement `execute_workflow()` router with type validation
   - Add structured logging for all workflow operations
   - Implement subprocess execution with output capture

3. **Implement Workflow Handlers** (1.5 hours)
   - `_execute_next_workflow()`: Detect state, route to appropriate action
   - `_execute_subplan_workflow()`: Build command, execute, parse result
   - `_execute_execution_workflow()`: Build command, validate prerequisites, execute
   - Each handler includes: confirmation prompt, execution, progress tracking, result display

4. **Add Progress Tracking** (45 min)
   - Implement `_track_progress()` with Rich Progress bars
   - Monitor subprocess output for progress indicators
   - Update progress bar based on workflow phase (e.g., "Analyzing...", "Creating...", "Testing...")
   - Show estimated time remaining

5. **Add Result Display** (30 min)
   - Implement `_display_result()` with Rich panels
   - Success panel (green): Show deliverables, test results, duration
   - Failure panel (red): Show error message, log file path, recovery suggestions
   - Format results with appropriate styling

6. **Add Error Handling** (30 min)
   - Implement `_handle_error()` with context-aware suggestions
   - Capture subprocess errors with full output
   - Generate recovery suggestions based on error type
   - Log errors with structured context

7. **Write Comprehensive Tests** (1.5 hours)
   - Write 35-40 tests covering all functionality
   - Mock subprocess calls for deterministic testing
   - Test all error paths and edge cases
   - Verify Rich output formatting

8. **Integration with PlanDashboard** (30 min)
   - Update `plan_dashboard.py` to use `WorkflowExecutor`
   - Replace simple subprocess calls with interactive workflows
   - Add confirmation prompts before executing
   - Display results after workflow completion

**Key Considerations**:

- **User Experience**: Interactive prompts should be clear and concise, not overwhelming
- **Progress Feedback**: Users need to know long-running operations are progressing
- **Error Recovery**: Error messages must provide actionable next steps
- **Existing Scripts**: Workflow executor wraps existing scripts, doesn't replace them
- **Backwards Compatibility**: Ensure existing functionality (Achievement 1.3) continues to work
- **Performance**: Progress tracking should not significantly slow down workflows
- **Testing**: Mock subprocess calls to avoid actually executing workflows during tests

**Trade-offs**:

- **Simplicity vs Features**: Balance between simple execution and advanced features like progress estimation
- **Decision**: Start with simple progress (indeterminate spinner), add estimation in future if needed
- **Wrapper vs Replacement**: Wrap existing scripts vs reimplement workflow logic
- **Decision**: Wrap existing scripts to leverage proven functionality and tests
- **Confirmation Prompts**: Always confirm vs smart confirmation (only for destructive actions)
- **Decision**: Always confirm for now, can add "quick mode" later

**Risks to Watch For**:

- **Subprocess Hanging**: Workflows might hang without timeout, add timeout handling
- **Output Parsing**: Script output format might change, use robust parsing with fallbacks
- **Rich UI Conflicts**: Progress bars might conflict with other Rich displays, test thoroughly
- **Error Message Quality**: Generic error messages won't help users, invest in good error formatting

---

## 🔄 Execution Strategy

**Execution Count**: Single

**Rationale**: Single clear approach, straightforward implementation

- **Clear Requirements**: Achievement 2.2 has well-defined deliverables and approach
- **Proven Pattern**: Similar to `ActionExecutor` (Achievement 1.3), extending with workflow intelligence
- **No Alternatives**: No competing approaches to compare, single optimal design
- **Sequential Implementation**: Each component builds naturally on the previous

**EXECUTION_TASK**: `EXECUTION_TASK_LLM-DASHBOARD-CLI_22_01.md`

**Implementation Flow**:

1. Create data models → 2. Implement core executor → 3. Add workflow handlers → 4. Add progress tracking → 5. Add result display → 6. Write tests → 7. Integrate with dashboard

---

## 🧪 Tests Required

### Test File

- **Path**: `tests/LLM/dashboard/test_workflow_executor.py`
- **Naming Convention**: `test_<script_name>.py` in `tests/LLM/dashboard/`
- **Test Infrastructure**: Use existing fixtures from `tests/LLM/dashboard/conftest.py` (console fixture, plan fixtures)

### Test Cases to Cover

**1. Workflow Routing** (5 tests):
- `test_execute_workflow_routes_to_next`
- `test_execute_workflow_routes_to_subplan`
- `test_execute_workflow_routes_to_execution`
- `test_execute_workflow_invalid_type`
- `test_execute_workflow_validates_kwargs`

**2. Next Workflow** (8 tests):
- `test_next_workflow_creates_subplan`
- `test_next_workflow_creates_execution`
- `test_next_workflow_continues_execution`
- `test_next_workflow_no_next_available`
- `test_next_workflow_subprocess_success`
- `test_next_workflow_subprocess_failure`
- `test_next_workflow_parses_output`
- `test_next_workflow_interactive_prompt` (mocked input)

**3. SUBPLAN Workflow** (6 tests):
- `test_subplan_workflow_builds_command`
- `test_subplan_workflow_executes_successfully`
- `test_subplan_workflow_invalid_achievement`
- `test_subplan_workflow_tracks_progress`
- `test_subplan_workflow_displays_result`
- `test_subplan_workflow_error_recovery`

**4. EXECUTION Workflow** (6 tests):
- `test_execution_workflow_builds_command`
- `test_execution_workflow_executes_successfully`
- `test_execution_workflow_missing_subplan`
- `test_execution_workflow_tracks_progress`
- `test_execution_workflow_displays_result`
- `test_execution_workflow_prerequisite_validation`

**5. Progress Tracking** (4 tests):
- `test_track_progress_creates_bar`
- `test_track_progress_updates`
- `test_track_progress_completes`
- `test_track_progress_error_state`

**6. Result Display** (5 tests):
- `test_display_result_success_panel`
- `test_display_result_failure_panel`
- `test_display_result_with_deliverables`
- `test_display_result_with_tests`
- `test_display_result_formats_duration`

**7. Error Handling** (4 tests):
- `test_handle_error_captures_subprocess_error`
- `test_handle_error_formats_message`
- `test_handle_error_generates_suggestions`
- `test_handle_error_logs_context`

**8. Integration** (3 tests):
- `test_integration_next_to_subplan`
- `test_integration_next_to_execution`
- `test_integration_next_to_continue`

### Coverage Requirements

- **Target Coverage**: >90% for new code
- **Required Test Types**:
  - Unit tests for all workflow handlers
  - Integration tests for complete workflows
  - Edge case tests for error scenarios
  - Mock tests for subprocess execution

### Test-First Requirement

- [ ] Tests written before implementation (TDD workflow)
- [ ] Initial test run shows all failing (red)
- [ ] Tests define success criteria
- [ ] Implementation makes tests pass (green)

**Approach**: Write tests for data models first, then workflow routing, then individual handlers, then integration tests.

---

## ✅ Expected Results

### Functional Changes

**After this SUBPLAN is complete, users will be able to**:

1. **Execute Workflows Interactively**:
   - Select "Execute Next" action from plan dashboard
   - See confirmation prompt with workflow details
   - Confirm execution with 'y' or cancel with 'n'
   - Watch real-time progress with spinner or progress bar
   - See detailed result panel upon completion

2. **Create SUBPLANs Interactively**:
   - Select "Create SUBPLAN" action
   - Enter achievement ID when prompted
   - Watch SUBPLAN creation progress
   - See success panel with SUBPLAN path and details
   - Return to dashboard to continue work

3. **Create EXECUTION_TASKs Interactively**:
   - Select "Create EXECUTION" action
   - Enter SUBPLAN ID when prompted
   - Watch prerequisite validation and EXECUTION creation
   - See success panel with EXECUTION_TASK path
   - Get guided to next step (execute the task)

4. **See Rich Feedback**:
   - Green success panels with checkmarks and details
   - Red error panels with clear error messages and recovery suggestions
   - Progress indicators for long-running operations
   - Formatted duration display (e.g., "2m 34s")

5. **Recover from Errors**:
   - See actionable error messages
   - Get suggestions for fixing common problems
   - View log file paths for detailed debugging
   - Return to dashboard to try again

### Performance Changes

- **Perceived Performance**: Progress tracking makes workflows feel faster by providing feedback
- **Actual Performance**: Minimal overhead (<50ms) from progress tracking
- **User Experience**: Significant improvement - users know what's happening

### Observable Outcomes

**Success Indicators**:

1. **User runs workflow from dashboard**:
   ```
   [Dashboard displays]
   User presses '1' (Execute Next)
   
   → Confirmation prompt appears:
     "Execute workflow: create_subplan for Achievement 1.1
      This will create SUBPLAN_LLM-DASHBOARD-CLI_11.md
      Continue? [y/n]"
   
   User presses 'y'
   
   → Progress indicator appears:
     "⠋ Creating SUBPLAN..."
   
   → Success panel appears:
     "✅ SUBPLAN created successfully!
      
      File: SUBPLAN_LLM-DASHBOARD-CLI_11.md
      Lines: 342
      Duration: 1m 23s
      
      Next step: Create EXECUTION_TASK"
   
   → Dashboard refreshes with updated state
   ```

2. **Workflow fails gracefully**:
   ```
   User presses '3' (Create EXECUTION)
   
   → Error panel appears:
     "❌ EXECUTION creation failed
      
      Error: SUBPLAN_LLM-DASHBOARD-CLI_11.md not found
      
      Suggestions:
      • Create SUBPLAN first (action 2)
      • Verify achievement 1.1 is ready
      
      See: logs/workflow_execution_20251114_210534.log"
   
   → Dashboard remains accessible
   ```

3. **Tests verify all functionality**:
   ```bash
   $ python -m pytest tests/LLM/dashboard/test_workflow_executor.py -v
   
   test_execute_workflow_routes_to_next ✓
   test_next_workflow_creates_subplan ✓
   test_subplan_workflow_executes_successfully ✓
   ... (35-40 tests)
   
   ========== 40 passed in 2.43s ==========
   ```

---

## 🔍 Conflict Analysis with Other Subplans

**Review Existing Subplans**:

From PLAN tracking:
- ✅ SUBPLAN_11 (Achievement 1.1 - Plan-Specific Dashboard) - Complete
- ✅ SUBPLAN_12 (Achievement 1.2 - Achievement State Visualization) - Complete
- ✅ SUBPLAN_13 (Achievement 1.3 - Quick Action Shortcuts) - Complete
- ✅ SUBPLAN_21 (Achievement 2.1 - Parallel Execution Detection) - Complete
- 🆕 SUBPLAN_22 (Achievement 2.2 - Interactive Workflow Execution) - This SUBPLAN

**Check for Conflicts**:

- **Overlap**: None - This is new functionality (interactive workflow execution)
- **Conflicts**: None - Builds on Achievement 1.3 (ActionExecutor), extends rather than replaces
- **Dependencies**: 
  - ✅ Achievement 1.3 complete (ActionExecutor exists, can be extended or coexist)
  - ✅ Achievement 1.1 complete (PlanDashboard exists for integration)
- **Integration**:
  - Integrates with Achievement 1.3 (ActionExecutor) - extends or coexists
  - Integrates with Achievement 1.1 (PlanDashboard) - adds workflow execution to actions

**Analysis**:

- **No conflicts detected**: This achievement extends the dashboard with new workflow execution capabilities
- **Depends on Achievement 1.3**: Uses action system as foundation, adds interactivity
- **Complements Achievement 2.1**: Parallel execution detection (2.1) identifies what to execute, interactive workflows (2.2) execute it
- **Clean extension point**: ActionExecutor (1.3) provides simple execution, WorkflowExecutor (2.2) adds interactivity and progress tracking

**Decision Architecture**:

Two possible approaches:

**Option A: Extend ActionExecutor**
- Add workflow methods to existing `ActionExecutor` class
- Pro: Single execution class, simpler imports
- Con: Larger class, mixed responsibilities

**Option B: New WorkflowExecutor (Recommended)**
- Create separate `WorkflowExecutor` class
- Pro: Separation of concerns, focused responsibilities
- Con: Two similar classes, need to coordinate

**Chosen**: Option B (New WorkflowExecutor)
- **Rationale**: 
  - ActionExecutor handles simple command execution
  - WorkflowExecutor handles interactive workflows with progress tracking
  - Clear separation: commands vs workflows
  - Both can coexist, PlanDashboard can use appropriate tool for each action

**Result**: Safe to proceed - No conflicts, dependencies met, clean integration path

---

## 🔗 Dependencies

### Other Subplans

- **Depends on SUBPLAN_13** (Achievement 1.3 - Quick Action Shortcuts): ✅ Complete
  - Provides `ActionExecutor` as reference for command execution patterns
  - Provides action system in `PlanDashboard` for integration point

- **Depends on SUBPLAN_11** (Achievement 1.1 - Plan-Specific Dashboard): ✅ Complete
  - Provides `PlanDashboard` class for integration
  - Provides action handling infrastructure

- **Complements SUBPLAN_21** (Achievement 2.1 - Parallel Execution Detection): ✅ Complete
  - Parallel detection identifies opportunities
  - Workflow execution enables acting on those opportunities
  - No blocking dependency, complementary features

### External Dependencies

**Python Libraries** (already in project):
- `rich`: For Progress bars, Panels, and console output
- `subprocess`: For executing workflow scripts
- `pathlib`: For file path handling
- `dataclasses`: For ExecutionResult and WorkflowState models
- `enum`: For WorkflowType enum
- `typing`: For type hints

**LLM Methodology Scripts** (already exist):
- `LLM/scripts/generation/generate_prompt.py`: Used by workflows
- `LLM/scripts/generation/interactive_menu.py`: Reference for workflow states
- `LLM/scripts/generation/batch_subplan.py`: For SUBPLAN creation
- `LLM/scripts/generation/batch_execution.py`: For EXECUTION creation

**Dashboard Infrastructure** (already exists):
- `LLM/dashboard/base_dashboard.py`: Base class with console
- `LLM/dashboard/models.py`: Existing models to extend
- `LLM/dashboard/plan_dashboard.py`: Integration point
- `LLM/dashboard/action_executor.py`: Reference for execution patterns

**No new external dependencies required**.

### Prerequisite Knowledge

- **Rich Library**: Understanding of Progress, Panel, Console for UI components
- **Subprocess Module**: Capturing output, handling errors, timeouts
- **LLM Methodology**: Understanding of SUBPLAN → EXECUTION → Feedback workflow
- **Dashboard Architecture**: How PlanDashboard, ActionExecutor, and actions interact

**Documentation to Review**:
- Rich documentation for Progress and Live displays
- Existing ActionExecutor implementation for patterns
- LLM methodology scripts for workflow details

---

## 🔄 Execution Task Reference

**Execution Tasks**:

- `EXECUTION_TASK_LLM-DASHBOARD-CLI_22_01.md` - Create interactive workflow executor (3-4 hours)

**Status**: Planning

---

## 📊 Success Criteria

**This Subplan is Complete When**:

- [ ] `WorkflowExecutor` class created with all workflow handlers
- [ ] Progress tracking implemented with Rich Progress
- [ ] Result display implemented with Rich Panels
- [ ] Error handling with recovery suggestions implemented
- [ ] Data models (`ExecutionResult`, `WorkflowState`) created
- [ ] Integration with `PlanDashboard` complete
- [ ] 35-40 tests written and passing (>90% coverage)
- [ ] Manual testing confirms workflows execute correctly
- [ ] User can execute all three workflows from dashboard
- [ ] Error messages are clear and actionable
- [ ] Code documented with docstrings and comments
- [ ] EXECUTION_TASK_22_01 complete
- [ ] Achievement feedback received (APPROVED_22.md or FIX_22.md)
- [ ] Ready for archive

**Specific Success Indicators**:

1. User can press '1' in plan dashboard and execute next workflow interactively
2. User sees progress indicator during workflow execution
3. User sees rich success/failure panel after workflow completes
4. All 35-40 tests pass
5. No linter errors in new code
6. Dashboard remains stable after adding workflow execution

---

## ✅ Completion Workflow (Filesystem-First)

**After All Work Complete**:

1. **Request Review**: Ask reviewer to assess achievement completion
2. **Reviewer Creates Feedback File**:
   - **If Approved**: Create `execution/feedbacks/APPROVED_22.md`
   - **If Fixes Needed**: Create `execution/feedbacks/FIX_22.md` with detailed issues
3. **Filesystem = Source of Truth**: Achievement completion tracked by APPROVED file existence, not PLAN markdown

**Achievement Index in PLAN**:
- Defines structure (list of all achievements)
- NOT updated with checkmarks or status manually
- Filesystem (`APPROVED_22.md` file) indicates completion status

**Do NOT**:
- ❌ Manually update PLAN markdown with "✅ Achievement complete"
- ❌ Add checkmarks to Achievement Index
- ❌ Update "Current Status & Handoff" to mark achievement done

**DO**:
- ✅ Request reviewer feedback after work complete
- ✅ Wait for `APPROVED_22.md` or `FIX_22.md` file creation
- ✅ If FIX required: Address issues, request re-review

**Why Filesystem-First**:
- Single source of truth (files, not markdown parsing)
- Automated detection by scripts (`generate_prompt.py`)
- Clear audit trail (feedback files are timestamped, contain rationale)
- Prevents markdown parsing issues

---

## 📝 Notes

**Common Pitfalls**:

- **Progress Tracking Overhead**: Don't make progress tracking so complex it slows workflows down
- **Output Parsing Brittleness**: Script output formats might change, use robust parsing
- **Subprocess Timeouts**: Long-running workflows need appropriate timeouts
- **Rich UI Conflicts**: Test that Progress bars don't conflict with dashboard rendering
- **Error Message Quality**: Invest time in clear, actionable error messages

**Resources**:

- Rich Progress documentation: https://rich.readthedocs.io/en/stable/progress.html
- Python subprocess documentation: https://docs.python.org/3/library/subprocess.html
- Existing `ActionExecutor` implementation: `LLM/dashboard/action_executor.py`
- LLM methodology scripts: `LLM/scripts/generation/`

**Design Notes**:

- **WorkflowExecutor vs ActionExecutor**: Keep both, different responsibilities
  - ActionExecutor: Simple command execution
  - WorkflowExecutor: Interactive workflows with progress and rich feedback
  
- **Progress Estimation**: Start with indeterminate spinner, can add time estimation later if needed
  
- **Confirmation Prompts**: Always confirm for now, can add "quick mode" later
  
- **Error Recovery**: Focus on actionable suggestions, not just error messages

---

## 🔄 Active EXECUTION_TASKs

**Real-Time Tracking**:

| EXECUTION                                       | Status   | Progress | Notes |
| ----------------------------------------------- | -------- | -------- | ----- |
| EXECUTION_TASK_LLM-DASHBOARD-CLI_22_01 | Planning | 0%       | -     |

**Status Options**:
- **Planning**: EXECUTION_TASK created, not yet executing
- **Executing**: Work in progress
- **Complete**: Execution finished, deliverables verified
- **Failed**: Execution encountered issues (document in notes)

---

## 📊 Execution Results Synthesis

**To be completed after execution finishes**

---

## 📖 What to Read (Focus Rules)

**When working on this SUBPLAN**, follow these focus rules to minimize context:

**✅ READ ONLY**:

- This SUBPLAN file (complete file)
- Parent PLAN Achievement 2.2 section (~90 lines)
- Active EXECUTION_TASK (EXECUTION_TASK_LLM-DASHBOARD-CLI_22_01.md)
- Parent PLAN "Current Status & Handoff" section (~30-50 lines)
- `LLM/dashboard/action_executor.py` (reference for patterns)
- `LLM/dashboard/plan_dashboard.py` (integration point)

**❌ DO NOT READ**:

- Parent PLAN full content (3000+ lines)
- Other achievements in PLAN
- Other SUBPLANs
- Completed EXECUTION_TASKs
- Completed work from other achievements

**Context Budget**: ~600 lines total

**Why**: SUBPLAN defines HOW to achieve Achievement 2.2. Reading other achievements or full PLAN adds scope and confusion. Focus on this achievement only.

**📖 See**: `LLM/guides/FOCUS-RULES.md` for complete focus rules and examples.

---

**Ready to Execute**:

- **Designer**: SUBPLAN design complete ✅
- **Next Step**: Create EXECUTION_TASK_LLM-DASHBOARD-CLI_22_01.md
- **Executor**: Will read SUBPLAN objective + approach, then execute according to plan
- **Reference**: `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` for complete workflow

