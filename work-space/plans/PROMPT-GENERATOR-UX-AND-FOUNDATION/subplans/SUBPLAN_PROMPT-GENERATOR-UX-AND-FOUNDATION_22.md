# SUBPLAN: Extract Workflow Detection Module

**Achievement**: 2.2  
**Feature**: PROMPT-GENERATOR-UX-AND-FOUNDATION  
**Created**: 2025-11-12  
**Status**: 🎯 Ready for Execution

---

## 📋 Objective

Extract workflow detection logic (~500 lines) from `generate_prompt.py` into a dedicated `workflow_detector.py` module, creating a clean separation of concerns for filesystem-first state detection, conflict checking, and achievement finding functionality.

**Success Criteria**:

- ✅ WorkflowDetector module created (~500 lines)
- ✅ Main file reduced by ~500 lines (2,866 → ~2,366)
- ✅ All 25 workflow detection tests passing
- ✅ Filesystem-first approach preserved
- ✅ Conflict detection working correctly
- ✅ No regressions in existing functionality

---

## 🎯 Deliverables

### Primary Deliverables

1. **`LLM/scripts/generation/workflow_detector.py`** (~500 lines)

   - WorkflowDetector class with complete implementation
   - Filesystem-first state detection
   - Conflict detection logic
   - Achievement finding algorithms
   - Helper functions

2. **Updated `LLM/scripts/generation/generate_prompt.py`** (reduced by ~500 lines)

   - Import WorkflowDetector class
   - Replace function calls with class methods
   - Remove extracted functions
   - Maintain all CLI functionality

3. **Module Tests** (~300 lines)

   - `tests/LLM/scripts/generation/test_workflow_detector.py`
   - 15+ test cases covering all detector methods
   - Edge cases and error handling
   - Filesystem-first behavior validation

4. **Migration Notes** (~100 lines)
   - Document extraction process
   - API changes and migration path
   - Breaking changes (if any)
   - Integration patterns

### Quality Targets

- **Test Coverage**: >90% for new module
- **Line Reduction**: ~500 lines from main file
- **Test Pass Rate**: 100% (all 25+ tests)
- **No Regressions**: All existing functionality preserved

---

## 🔍 Current State Analysis

### File Size Analysis

**generate_prompt.py**: 2,866 lines total

**Workflow Detection Section** (~500 lines):

- `detect_workflow_state_filesystem()` (~150 lines)
- `detect_plan_filesystem_conflict()` (~120 lines)
- `find_next_achievement_hybrid()` (~100 lines)
- `find_next_achievement_from_plan()` (~50 lines)
- `find_next_achievement_from_archive()` (~40 lines)
- `find_next_achievement_from_root()` (~40 lines)

### Key Functions to Extract

**Primary Functions** (3):

1. `detect_workflow_state_filesystem()` - State detection (filesystem-first)
2. `detect_plan_filesystem_conflict()` - Conflict detection (Achievement Index vs filesystem)
3. `find_next_achievement_hybrid()` - Achievement finding (multiple strategies)

**Helper Functions** (3): 4. `find_next_achievement_from_plan()` - Parse handoff section 5. `find_next_achievement_from_archive()` - Check archived SUBPLANs 6. `find_next_achievement_from_root()` - Check root directory

### Dependencies Analysis

**External Dependencies**:

- `Path` from pathlib
- `Optional`, `Dict` from typing
- `re` for pattern matching
- `Achievement` dataclass from generate_prompt

**Internal Dependencies**:

- `is_achievement_complete()` - stays in generate_prompt.py (used by multiple modules)
- `extract_handoff_section()` - stays in generate_prompt.py (parsing utility)

**Dependent Functions** (callers that need updating):

- `main()` in generate_prompt.py
- Tests in test_generate_prompt_comprehensive.py

---

## 📐 Approach

### Phase 1: Create Module Structure (30 min)

**Objective**: Set up workflow_detector.py with proper structure

**Actions**:

1. Create `LLM/scripts/generation/workflow_detector.py`
2. Add module docstring explaining filesystem-first philosophy
3. Define `WorkflowDetector` class with methods
4. Add imports and type hints
5. Document class responsibilities

**Validation**:

- File created with proper structure
- Import statement works in generate_prompt.py
- No syntax errors

### Phase 2: Extract Core Detection Functions (90 min)

**Objective**: Move 3 core detection functions to module

**Actions**:

1. **Extract `detect_workflow_state_filesystem()`**:

   - Copy function to WorkflowDetector class as method
   - Update method signature (add self)
   - Update all internal function calls
   - Add comprehensive docstring
   - Test import in generate_prompt.py

2. **Extract `detect_plan_filesystem_conflict()`**:

   - Copy function to WorkflowDetector class as method
   - Update method signature (add self)
   - Preserve filesystem-first conflict detection logic
   - Add comprehensive docstring
   - Document Achievement Index philosophy

3. **Extract `find_next_achievement_hybrid()`**:
   - Copy function to WorkflowDetector class as method
   - Update method signature (add self)
   - Maintain multiple detection strategies
   - Add comprehensive docstring
   - Preserve warnings for stale handoffs

**Validation**:

- All 3 methods present in WorkflowDetector
- Methods compile without errors
- Docstrings complete and accurate

### Phase 3: Extract Helper Functions (60 min)

**Objective**: Move 3 helper functions to module

**Actions**:

1. **Extract `find_next_achievement_from_plan()`**:

   - Copy to WorkflowDetector as method
   - Update to use extract_handoff_section from generate_prompt
   - Handle handoff parsing edge cases

2. **Extract `find_next_achievement_from_archive()`**:

   - Copy to WorkflowDetector as method
   - Update to call is_achievement_complete correctly
   - Maintain completion skipping logic

3. **Extract `find_next_achievement_from_root()`**:
   - Copy to WorkflowDetector as method
   - Update to call is_achievement_complete correctly
   - Maintain completion skipping logic

**Validation**:

- All helper methods functional
- Dependencies resolved
- Internal method calls work

### Phase 4: Update generate_prompt.py (60 min)

**Objective**: Integrate WorkflowDetector and remove old functions

**Actions**:

1. **Add import statement**:

   ```python
   from LLM.scripts.generation.workflow_detector import WorkflowDetector
   ```

2. **Update main() function**:

   - Initialize `detector = WorkflowDetector()`
   - Replace `detect_workflow_state_filesystem()` → `detector.detect_workflow_state_filesystem()`
   - Replace `detect_plan_filesystem_conflict()` → `detector.detect_plan_filesystem_conflict()`
   - Replace `find_next_achievement_hybrid()` → `detector.find_next_achievement_hybrid()`

3. **Delete extracted functions** (6 functions):

   - Remove function definitions
   - Verify no orphaned references
   - Update any remaining callers

4. **Verify file reduction**:
   - Check line count (should be ~2,366 lines)
   - Verify ~500 line reduction

**Validation**:

- Script runs without import errors
- All CLI functionality works
- Interactive mode functional
- Line count reduced as expected

### Phase 5: Create Module Tests (90 min)

**Objective**: Test WorkflowDetector independently

**Actions**:

1. **Create test file**:

   - `tests/LLM/scripts/generation/test_workflow_detector.py`
   - Import WorkflowDetector class
   - Set up test fixtures (temp directories, feedbacks)

2. **Test core detection methods** (9 tests):

   - `test_detect_workflow_no_subplan()`
   - `test_detect_workflow_subplan_no_execution()`
   - `test_detect_workflow_active_execution()`
   - `test_detect_conflict_orphaned_approved_file()`
   - `test_detect_conflict_orphaned_subplan()`
   - `test_detect_conflict_none_when_aligned()`
   - `test_find_next_achievement_from_handoff()`
   - `test_find_next_achievement_skips_completed()`
   - `test_find_next_achievement_returns_none_when_complete()`

3. **Test helper methods** (6 tests):
   - `test_find_from_plan_parses_handoff()`
   - `test_find_from_archive_skips_completed()`
   - `test_find_from_root_skips_completed()`
   - `test_find_from_plan_handles_missing_achievement()`
   - `test_find_from_plan_warns_on_stale_handoff()`
   - `test_find_hybrid_fallback_chain()`

**Validation**:

- All 15+ tests pass
- Coverage >90% for workflow_detector.py
- No test failures

### Phase 6: Run Full Test Suite & Validation (30 min)

**Objective**: Ensure no regressions

**Actions**:

1. **Run existing tests**:

   ```bash
   pytest tests/LLM/scripts/generation/test_generate_prompt_comprehensive.py -v
   pytest tests/LLM/scripts/generation/test_workflow_detector.py -v
   ```

2. **Run integration test**:

   ```bash
   python LLM/scripts/generation/generate_prompt.py @PROMPT-GENERATOR-UX-AND-FOUNDATION --interactive
   ```

3. **Verify functionality**:

   - Workflow detection works
   - Conflict detection works
   - Achievement finding works
   - Interactive mode works
   - No regressions

4. **Create migration notes**:
   - Document extraction process
   - Note API changes
   - Provide usage examples

**Validation**:

- All 25+ tests pass (0 failures)
- Interactive mode functional
- No error messages
- Migration notes complete

---

## 🔧 Execution Strategy

### Single EXECUTION Approach

**Rationale**:

- All 6 functions are tightly coupled (call each other)
- Must be extracted together to maintain functionality
- Single atomic change easier to test and validate
- ~4-5 hour estimate fits single execution session

**Execution Plan**:

- **EXECUTION_TASK_22_01**: Complete extraction (all 6 phases)
- Duration: 4-5 hours
- Approach: Sequential phases, validate after each

**Risk Mitigation**:

- Test after each phase
- Commit after each successful phase
- Keep generate_prompt.py functional throughout
- Roll back if issues arise

---

## 🧪 Testing Strategy

### Test Categories

**1. Unit Tests** (15+ tests):

- Test each WorkflowDetector method independently
- Use temp directories and mock filesystems
- Cover edge cases and error handling

**2. Integration Tests** (existing):

- test_generate_prompt_comprehensive.py (25 tests)
- Verify no regressions
- All existing tests must pass

**3. Manual Tests**:

- Run interactive mode
- Test workflow detection
- Verify conflict detection
- Test achievement finding

### Coverage Targets

- **workflow_detector.py**: >90%
- **generate_prompt.py**: Maintain current 70-75%
- **Overall project**: Maintain current levels

### Test Data Requirements

**Filesystem Fixtures**:

- Plans with execution/feedbacks/ structure
- APPROVED_XX.md files for completed achievements
- SUBPLANs and EXECUTION_TASKs
- Achievement Index in PLAN files

---

## 📊 Expected Results

### Quantitative Metrics

| Metric                   | Before | After  | Change |
| ------------------------ | ------ | ------ | ------ |
| generate_prompt.py lines | 2,866  | ~2,366 | -500   |
| Number of modules        | 1      | 2      | +1     |
| Test files               | 4      | 5      | +1     |
| Test count               | 67     | 82+    | +15    |
| Test coverage (detector) | N/A    | >90%   | New    |

### Qualitative Benefits

**Maintainability**:

- ✅ Clear separation of concerns
- ✅ Workflow detection logic isolated
- ✅ Easier to understand and modify
- ✅ Reduced cognitive load

**Testability**:

- ✅ Independent unit tests possible
- ✅ Easier to mock and test
- ✅ Better test coverage
- ✅ Isolated failure domains

**Extensibility**:

- ✅ Easy to add new detection strategies
- ✅ Easy to enhance conflict detection
- ✅ Ready for future refactoring
- ✅ Clean API for other scripts

### Success Indicators

**Must Have**:

- ✅ All 25+ existing tests pass
- ✅ 15+ new tests added and passing
- ✅ ~500 line reduction in main file
- ✅ WorkflowDetector module functional

**Should Have**:

- ✅ >90% test coverage for new module
- ✅ Migration notes complete
- ✅ No breaking changes to CLI
- ✅ Clean, documented API

**Nice to Have**:

- ✅ Performance maintained or improved
- ✅ Code quality metrics maintained
- ✅ Documentation examples added

---

## 🚨 Risks & Mitigation

### Risk 1: Breaking Existing Functionality

**Probability**: Medium  
**Impact**: High

**Mitigation**:

- Run tests after each phase
- Keep main file functional throughout
- Use git for easy rollback
- Test interactive mode manually

### Risk 2: Complex Dependencies

**Probability**: Medium  
**Impact**: Medium

**Mitigation**:

- Map all dependencies before extraction
- Extract in order (helpers before core)
- Keep shared utilities in main file
- Document all cross-module calls

### Risk 3: Test Failures

**Probability**: Low  
**Impact**: Medium

**Mitigation**:

- Update test imports immediately
- Run tests frequently during extraction
- Fix test failures before proceeding
- Maintain test fixtures

### Risk 4: Import Errors

**Probability**: Low  
**Impact**: Low

**Mitigation**:

- Test imports after module creation
- Use absolute imports
- Add **init**.py if needed
- Verify Python path configuration

---

## 📝 Notes

### Key Decisions

1. **Single Execution**: All phases in one execution for atomic change
2. **Filesystem-First Preserved**: No changes to state tracking philosophy
3. **Test Coverage**: Aim for >90% on new module
4. **API Stability**: Maintain all existing CLI functionality

### Follow-up Work

This extraction enables:

- **Achievement 2.3**: Extract Prompt Generation Module
- **Achievement 2.4**: Extract Parsing & Utilities Module
- **Achievement 2.6**: Integrate all modules

### References

- `LLM/templates/SUBPLAN-TEMPLATE.md` - Template structure
- `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` - Workflow guidance
- `PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md` - Parent PLAN
- Achievement 2.1 (Interactive Menu) - Previous extraction pattern
- `STATE_TRACKING_PHILOSOPHY.md` - Filesystem-first principles

---

## ✅ Completion Checklist

### Design Phase (Complete)

- [x] SUBPLAN created
- [x] Approach defined
- [x] Execution strategy documented
- [x] Testing strategy defined
- [x] Deliverables listed

### Execution Phase (Pending)

- [ ] Phase 1: Module structure created
- [ ] Phase 2: Core functions extracted
- [ ] Phase 3: Helper functions extracted
- [ ] Phase 4: Main file updated
- [ ] Phase 5: Tests created
- [ ] Phase 6: Full validation complete

### Review Phase (Pending)

- [ ] All tests passing
- [ ] Line count verified
- [ ] Migration notes complete
- [ ] APPROVED_22.md created

---

**SUBPLAN Status**: 🎯 Ready for Execution  
**Next Step**: Create EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_22_01.md  
**Estimated Duration**: 4-5 hours
