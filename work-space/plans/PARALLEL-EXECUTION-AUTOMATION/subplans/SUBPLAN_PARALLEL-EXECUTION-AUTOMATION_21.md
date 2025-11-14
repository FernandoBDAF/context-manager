# SUBPLAN: Achievement 2.1 - generate_prompt.py Enhanced with Parallel Support

**PLAN**: PARALLEL-EXECUTION-AUTOMATION  
**Achievement**: 2.1  
**Estimated Time**: 5-7 hours  
**Created**: 2025-11-13  
**Status**: 📋 Design Phase

---

## 🎯 Objective

Enhance the main automation script (`generate_prompt.py`) with parallel workflow support, enabling users to discover parallelization opportunities, validate `parallel.json` files, and access batch creation features through an intuitive menu interface. This achievement integrates all foundation work (Achievements 1.1-1.3) into the primary workflow automation tool.

**Core Purpose**: Transform `generate_prompt.py` from a sequential-only tool into a parallel-aware orchestrator that can detect, validate, and guide users through parallel execution workflows while maintaining full backward compatibility.

**Success Definition**: Users can run `generate_prompt.py @PLAN --parallel-upgrade` to generate parallel discovery prompts, and the script automatically detects existing `parallel.json` files, validates them, and presents a menu with batch creation options—all with robust error handling and clear user guidance.

---

## 📦 Deliverables

### 1. Enhanced generate_prompt.py

**File**: `LLM/scripts/generation/generate_prompt.py` (modified, ~150 new lines)

**New Features**:

**A. `--parallel-upgrade` Flag**:
```python
parser.add_argument(
    '--parallel-upgrade',
    action='store_true',
    help='Generate parallel discovery prompt for this PLAN'
)
```
- Generates prompt using `parallel_prompt_builder.py`
- Uses `ParallelPromptBuilder.build_discovery_prompt()`
- Outputs prompt to stdout or file
- Includes independence checklist and schema template

**B. `parallel.json` Detection**:
```python
def detect_parallel_json(plan_path: Path) -> Optional[Path]:
    """Detect parallel.json in plan directory."""
    parallel_json = plan_path / "parallel.json"
    if parallel_json.exists():
        return parallel_json
    return None
```

**C. Validation Integration**:
```python
def validate_and_load_parallel_json(parallel_json_path: Path) -> Optional[Dict]:
    """Validate and load parallel.json."""
    from LLM.scripts.validation.validate_parallel_json import validate_parallel_json
    
    result = validate_parallel_json(parallel_json_path)
    if not result.valid:
        print(f"❌ Invalid parallel.json: {parallel_json_path}")
        for error in result.errors:
            print(f"  - {error}")
        print("\n💡 Fix: Regenerate with --parallel-upgrade or fix errors manually")
        return None
    
    with open(parallel_json_path) as f:
        return json.load(f)
```

**D. Parallel Menu**:
```python
def show_parallel_menu(parallel_data: Dict, plan_name: str):
    """Show parallel execution menu."""
    print("\n🔀 Parallel Execution Options:")
    print("1. Batch Create SUBPLANs (for same level)")
    print("2. Batch Create EXECUTIONs (for same level)")
    print("3. Run Parallel Executions (multi-executor)")
    print("4. View Dependency Graph")
    print("5. Back to Main Menu")
    
    choice = input("\nSelect option (1-5): ")
    # Handle menu selection
```

**E. Error Handling**:
- Invalid JSON: Show error with line number, suggest regeneration
- Circular dependencies: Block execution, show cycle path
- Missing dependencies: Warn user, suggest fixes
- Malformed data: Clear error messages with actionable fixes

### 2. Parallel Workflow Module

**File**: `LLM/scripts/generation/parallel_workflow.py` (~200 lines, NEW)

**Purpose**: Separate module for parallel workflow logic (keeps generate_prompt.py clean)

**Functions**:
```python
def generate_parallel_upgrade_prompt(plan_path: Path) -> str:
    """Generate parallel discovery prompt."""
    from LLM.scripts.generation.parallel_prompt_builder import ParallelPromptBuilder
    
    builder = ParallelPromptBuilder(plan_path)
    return builder.build_discovery_prompt(
        parallelization_level="level_1",  # Default, user can change
        include_independence_checklist=True,
        include_schema_template=True
    )

def detect_and_validate_parallel_json(plan_path: Path) -> Tuple[Optional[Path], Optional[Dict]]:
    """Detect and validate parallel.json."""
    parallel_json = detect_parallel_json(plan_path)
    if not parallel_json:
        return None, None
    
    parallel_data = validate_and_load_parallel_json(parallel_json)
    return parallel_json, parallel_data

def show_parallel_menu(parallel_data: Dict, plan_name: str):
    """Show and handle parallel execution menu."""
    # Menu implementation

def handle_batch_subplan_creation(parallel_data: Dict, plan_name: str):
    """Handle batch SUBPLAN creation option."""
    # Future: Achievement 2.2

def handle_batch_execution_creation(parallel_data: Dict, plan_name: str):
    """Handle batch EXECUTION creation option."""
    # Future: Achievement 2.3

def show_dependency_graph(parallel_data: Dict):
    """Show ASCII dependency graph."""
    # Simple text-based graph visualization
```

### 3. Integration with Main Workflow

**Modifications to `generate_prompt.py` main()**:

```python
def main():
    args = parse_args()
    
    # NEW: Handle --parallel-upgrade
    if args.parallel_upgrade:
        prompt = generate_parallel_upgrade_prompt(args.plan_path)
        print(prompt)
        return 0
    
    # Existing workflow...
    plan_name = get_plan_name(args.plan_path)
    
    # NEW: Detect parallel.json
    parallel_json, parallel_data = detect_and_validate_parallel_json(args.plan_path)
    
    # Show main menu
    if parallel_data:
        print(f"\n🔀 Parallel workflow detected for {plan_name}")
        print("  - Use --parallel-menu to access parallel options")
    
    # Existing menu...
    
    # NEW: Add parallel menu option
    if parallel_data and args.interactive:
        print("P. Parallel Execution Menu")
    
    # Handle menu selection...
```

### 4. Test Suite

**File**: `tests/LLM/scripts/generation/test_parallel_workflow.py` (~300 lines, NEW)

**Test Coverage**:

**A. `--parallel-upgrade` Tests** (~80 lines):
- `test_parallel_upgrade_flag_generates_prompt()` - Generates valid prompt
- `test_parallel_upgrade_with_plan_path()` - Uses correct plan path
- `test_parallel_upgrade_output_format()` - Prompt has all sections
- `test_parallel_upgrade_missing_plan()` - Handles missing plan gracefully

**B. Detection Tests** (~60 lines):
- `test_detect_parallel_json_exists()` - Finds parallel.json
- `test_detect_parallel_json_missing()` - Returns None when missing
- `test_detect_parallel_json_in_subdirectory()` - Checks correct location

**C. Validation Tests** (~80 lines):
- `test_validate_valid_parallel_json()` - Loads valid file
- `test_validate_invalid_json_syntax()` - Shows parse error with line number
- `test_validate_circular_dependencies()` - Shows cycle path
- `test_validate_missing_dependencies()` - Shows missing deps
- `test_validate_schema_errors()` - Shows schema violations

**D. Menu Tests** (~50 lines):
- `test_show_parallel_menu_displays_options()` - Shows all 5 options
- `test_parallel_menu_batch_subplan_option()` - Option 1 works
- `test_parallel_menu_batch_execution_option()` - Option 2 works
- `test_parallel_menu_back_option()` - Option 5 returns

**E. Integration Tests** (~30 lines):
- `test_full_workflow_with_parallel_json()` - End-to-end test
- `test_backward_compatibility()` - Works without parallel.json
- `test_parallel_upgrade_then_detect()` - Generate then use workflow

### 5. Documentation Updates

**File**: `LLM/scripts/generation/README.md` (modified, ~50 new lines)

**New Sections**:
```markdown
## Parallel Workflow Support

### Generate Parallel Discovery Prompt

```bash
python LLM/scripts/generation/generate_prompt.py @PLAN_NAME --parallel-upgrade
```

This generates a prompt that helps you identify parallelization opportunities.

### Using parallel.json

If a `parallel.json` file exists in your plan directory, `generate_prompt.py`
will automatically detect it and offer parallel execution options:

1. **Batch Create SUBPLANs**: Create multiple SUBPLANs at once
2. **Batch Create EXECUTIONs**: Create multiple EXECUTION_TASKs at once
3. **Run Parallel Executions**: Coordinate multi-executor workflows

### Error Handling

- **Invalid JSON**: Script validates on load and shows clear errors
- **Circular Dependencies**: Script detects cycles and blocks execution
- **Missing Dependencies**: Script warns about missing achievements

### Backward Compatibility

All existing functionality works unchanged. Parallel features are opt-in.
```

---

## 🔧 Approach

### Phase 1: Add `--parallel-upgrade` Flag (90 min)

**Goal**: Enable parallel discovery prompt generation

**Steps**:

1. **Add CLI Argument** (10 min):
   - Add `--parallel-upgrade` to argparse
   - Add help text
   - Test flag parsing

2. **Create `parallel_workflow.py` Module** (30 min):
   - Create new file
   - Implement `generate_parallel_upgrade_prompt()`
   - Import `ParallelPromptBuilder`
   - Handle missing plan gracefully

3. **Integrate with main()** (20 min):
   - Check for `--parallel-upgrade` flag
   - Call `generate_parallel_upgrade_prompt()`
   - Output prompt to stdout
   - Exit after generation

4. **Test `--parallel-upgrade`** (30 min):
   - Write unit tests
   - Test with real plan
   - Verify prompt format
   - Test error cases

**Output**: Working `--parallel-upgrade` flag that generates prompts

---

### Phase 2: Add parallel.json Detection & Validation (120 min)

**Goal**: Detect and validate parallel.json files

**Steps**:

1. **Implement Detection** (20 min):
   - Add `detect_parallel_json()` function
   - Check plan directory for `parallel.json`
   - Return Path or None

2. **Integrate Validation** (40 min):
   - Import `validate_parallel_json` from Achievement 1.3
   - Add `validate_and_load_parallel_json()` function
   - Show validation errors clearly
   - Suggest fixes for common errors

3. **Add Error Handling** (30 min):
   - Handle invalid JSON syntax (show line number)
   - Handle circular dependencies (show cycle)
   - Handle missing dependencies (show missing IDs)
   - Handle schema violations (show field errors)

4. **Test Detection & Validation** (30 min):
   - Test with valid parallel.json
   - Test with invalid JSON syntax
   - Test with circular dependencies
   - Test with missing dependencies
   - Test with missing file

**Output**: Robust detection and validation with clear error messages

---

### Phase 3: Implement Parallel Menu (90 min)

**Goal**: Add interactive menu for parallel workflows

**Steps**:

1. **Design Menu Structure** (15 min):
   - 5 options: Batch SUBPLANs, Batch EXECUTIONs, Run Parallel, View Graph, Back
   - Clear numbering and descriptions
   - Consistent with existing menu style

2. **Implement Menu Display** (25 min):
   - Add `show_parallel_menu()` function
   - Display options
   - Get user input
   - Validate input (1-5)

3. **Add Menu Handlers** (30 min):
   - Implement option handlers (stubs for 2.2, 2.3)
   - Add "Coming soon" messages for future features
   - Implement "View Dependency Graph" (simple ASCII)
   - Implement "Back" option

4. **Integrate with Main Menu** (20 min):
   - Add "P. Parallel Menu" option to main menu
   - Show parallel indicator when parallel.json detected
   - Handle menu navigation

**Output**: Working parallel menu with navigation

---

### Phase 4: Testing & Documentation (120 min)

**Goal**: Comprehensive tests and documentation

**Steps**:

1. **Write Unit Tests** (60 min):
   - Test `--parallel-upgrade` flag (20 min)
   - Test detection logic (15 min)
   - Test validation integration (15 min)
   - Test menu display and navigation (10 min)

2. **Write Integration Tests** (30 min):
   - Test full workflow with parallel.json
   - Test backward compatibility (no parallel.json)
   - Test error scenarios end-to-end

3. **Update Documentation** (20 min):
   - Update README with parallel workflow section
   - Add usage examples
   - Document error messages

4. **Manual Testing** (10 min):
   - Test with real plan
   - Verify all menu options work
   - Check error messages are clear

**Output**: >90% test coverage, complete documentation

---

## 🔄 Execution Strategy

### Type: Single Execution (Recommended)

**Rationale**:

1. **Cohesive Feature**: All components work together (flag → detection → validation → menu)
2. **Manageable Scope**: 5-7 hours, can be done in one focused session
3. **Sequential Dependencies**: Each phase builds on previous (flag → detection → menu)
4. **Atomic Integration**: All pieces needed together for feature to work

**Alternative Considered**: Split into 2 executions (flag/detection + menu), but integration overhead would exceed benefits.

**Execution**: Create single `EXECUTION_TASK_PARALLEL-EXECUTION-AUTOMATION_21_01.md`

---

## 🧪 Testing Strategy

### Unit Testing

**Scope**: Test each function in isolation

**Test Files**:
1. `test_parallel_workflow.py` - All parallel workflow functions
2. Extend `test_generate_prompt.py` - Integration with main script

**Coverage Target**: >90% for new code

**Key Tests**:
- `--parallel-upgrade` flag parsing and execution
- `detect_parallel_json()` with various scenarios
- `validate_and_load_parallel_json()` with valid/invalid files
- Menu display and navigation
- Error handling for all error types

### Integration Testing

**Scope**: Test full workflows end-to-end

**Test Cases**:
1. **Parallel Upgrade Workflow**:
   - Run `--parallel-upgrade` → generates prompt
   - Create parallel.json from prompt
   - Run script again → detects and validates
   - Access parallel menu → shows options

2. **Backward Compatibility**:
   - Run script without parallel.json → works normally
   - No breaking changes to existing functionality

3. **Error Scenarios**:
   - Invalid JSON → shows clear error
   - Circular dependencies → blocks and shows cycle
   - Missing dependencies → warns user

### Manual Testing

**Verification**:
- Test with real plan (PARALLEL-EXECUTION-AUTOMATION)
- Generate parallel.json using `--parallel-upgrade`
- Verify menu navigation works
- Check error messages are helpful

---

## 📊 Expected Results

### Success Criteria

**Functional**:
- ✅ `--parallel-upgrade` generates valid discovery prompt
- ✅ Detects `parallel.json` in plan directory
- ✅ Validates parallel.json before use (shows errors if invalid)
- ✅ Shows parallel menu with 5 options
- ✅ Handles all error scenarios gracefully
- ✅ Backward compatible (no breaking changes)

**Quality**:
- ✅ Test coverage >90% for new code
- ✅ All tests passing
- ✅ No linter errors
- ✅ Clear, actionable error messages

**Integration**:
- ✅ Works with Achievement 1.1 (ParallelPromptBuilder)
- ✅ Works with Achievement 1.3 (validate_parallel_json)
- ✅ Ready for Achievement 2.2 (batch SUBPLANs)
- ✅ Ready for Achievement 2.3 (batch EXECUTIONs)

### Deliverable Metrics

**Files Created/Modified**: 3 files (~650 lines total)
- Modified: 1 file (~150 lines)
- New: 2 files (~500 lines)

**Test Metrics**:
- Total Tests: ~25 new tests
- Coverage: >90% for new code
- All tests passing

---

## 🚨 Risks & Mitigations

### Risk 1: Breaking Existing Functionality

**Risk**: Changes to generate_prompt.py could break existing workflows

**Impact**: HIGH - Users rely on this script daily

**Mitigation**:
- Add new code, don't modify existing logic
- All parallel features are opt-in (require flag or parallel.json)
- Comprehensive backward compatibility tests
- Test with real plans before release

### Risk 2: Complex Error Messages

**Risk**: Validation errors might be unclear or overwhelming

**Impact**: MEDIUM - Users may not know how to fix issues

**Mitigation**:
- Use clear, actionable error messages
- Include "Fix:" suggestions for each error
- Show one error at a time (most critical first)
- Link to documentation for complex issues

### Risk 3: Menu Navigation Confusion

**Risk**: Users might get lost in nested menus

**Impact**: LOW - Can always exit, but frustrating

**Mitigation**:
- Keep menu structure flat (max 2 levels)
- Always show "Back" option
- Show current context in menu header
- Add breadcrumbs if needed

---

## 💡 Design Decisions

### Decision 1: Separate Module vs Inline Code

**Chosen**: Separate `parallel_workflow.py` module

**Rationale**:
- Keeps generate_prompt.py clean and focused
- Easier to test parallel logic in isolation
- Better code organization
- Easier to extend in future

**Trade-off**: One more file, but worth the organization

### Decision 2: Validation on Load vs On Demand

**Chosen**: Validation on load (when parallel.json detected)

**Rationale**:
- Fail fast - catch errors immediately
- Clear error messages before user tries to use
- Prevents confusing errors later in workflow
- Users can fix issues before proceeding

**Trade-off**: Slight startup delay, but <100ms is acceptable

### Decision 3: Menu Stubs vs Full Implementation

**Chosen**: Menu stubs for batch features (2.2, 2.3)

**Rationale**:
- This achievement focuses on infrastructure
- Batch features are separate achievements
- Stubs show future functionality
- Users understand what's coming

**Trade-off**: Menu has "Coming soon" items, but sets expectations

### Decision 4: ASCII Graph vs No Graph

**Chosen**: Simple ASCII dependency graph

**Rationale**:
- Helps users visualize dependencies
- Simple text-based (no external libs)
- Quick to implement
- Better than nothing

**Alternative Considered**: No graph (defer to future), but simple ASCII is valuable now

---

## 📝 Implementation Notes

### Error Message Format

All error messages follow this pattern:
```
❌ [Error Type]: [Brief description]
  - [Specific error 1]
  - [Specific error 2]

💡 Fix: [Actionable suggestion]
```

Example:
```
❌ Invalid parallel.json: circular dependencies detected
  - Circular dependency: 1.1 → 1.2 → 1.1

💡 Fix: Remove one dependency to break the cycle
```

### Menu Navigation Pattern

```
🔀 Parallel Execution Menu
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Plan: PARALLEL-EXECUTION-AUTOMATION
Parallelization Level: level_1
Achievements: 3 (1 complete, 2 available)

Options:
  1. Batch Create SUBPLANs (for same level)
  2. Batch Create EXECUTIONs (for same level)
  3. Run Parallel Executions (multi-executor)
  4. View Dependency Graph
  5. Back to Main Menu

Select option (1-5): _
```

### Backward Compatibility Checklist

- ✅ All existing flags work unchanged
- ✅ Script works without parallel.json
- ✅ No changes to existing menu options
- ✅ No changes to output format (unless --parallel-upgrade)
- ✅ No new required arguments

---

## 🔗 Dependencies

### Requires (from previous achievements):
- Achievement 1.1: `parallel_prompt_builder.py` ✅
- Achievement 1.3: `validate_parallel_json.py` ✅

### Enables (for future achievements):
- Achievement 2.2: Batch SUBPLAN Creation (menu option 1)
- Achievement 2.3: Batch EXECUTION Creation (menu option 2)

### External Dependencies:
- Python 3.8+ (existing)
- No new external libraries needed

---

## ✅ Definition of Done

**Code Complete**:
- [ ] `generate_prompt.py` enhanced with `--parallel-upgrade` flag
- [ ] `parallel_workflow.py` created with all functions
- [ ] Detection and validation integrated
- [ ] Parallel menu implemented
- [ ] Error handling comprehensive

**Tests Complete**:
- [ ] 25+ tests written and passing
- [ ] >90% coverage for new code
- [ ] Integration tests pass
- [ ] Backward compatibility verified

**Quality Complete**:
- [ ] No linter errors
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] Error messages clear and actionable

**Integration Complete**:
- [ ] Works with ParallelPromptBuilder (1.1)
- [ ] Works with validate_parallel_json (1.3)
- [ ] Backward compatible (no breaking changes)
- [ ] Ready for batch features (2.2, 2.3)

**Documentation Complete**:
- [ ] README updated with parallel workflow section
- [ ] Usage examples added
- [ ] Error messages documented

---

**Status**: 📋 Ready for Execution  
**Next Step**: Create `EXECUTION_TASK_PARALLEL-EXECUTION-AUTOMATION_21_01.md` and execute work  
**Executor**: Begin with Phase 1 (Add `--parallel-upgrade` Flag)



