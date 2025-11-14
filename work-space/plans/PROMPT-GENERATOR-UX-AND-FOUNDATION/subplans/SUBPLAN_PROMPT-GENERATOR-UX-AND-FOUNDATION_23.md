# SUBPLAN: Extract Prompt Generation Module

**Achievement**: 2.3  
**Parent PLAN**: PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md  
**Type**: Module Extraction  
**Status**: 🎯 Ready to Execute  
**Estimated Effort**: 3-4 hours

---

## 🎯 Objective

Extract prompt generation logic (~400 lines) from `generate_prompt.py` into a dedicated `prompt_builder.py` module, creating a clean separation between prompt construction and workflow orchestration for improved maintainability and testability.

**Why This Matters**:

- Prompt building is a distinct concern from workflow detection
- ~400 lines of prompt templates can be isolated
- Easier to test prompt generation independently
- Cleaner architecture following extraction pattern from 2.1 and 2.2

---

## 📦 Deliverables

### 1. New Module Created

**File**: `LLM/scripts/generation/prompt_builder.py` (~400 lines)

**Class**: `PromptBuilder`

**Methods to Implement** (5 total):

1. `build_create_subplan_prompt(plan_path, achievement, feature_name, archive_location) -> str`

   - Builds prompt for creating new SUBPLAN
   - Includes context boundaries, steps, validation
   - ~80 lines

2. `build_create_execution_prompt(subplan_path, achievement, feature_name) -> str`

   - Builds prompt for creating new EXECUTION_TASK
   - Includes SUBPLAN context, execution strategy
   - ~80 lines

3. `build_continue_execution_prompt(execution_path) -> str`

   - Builds prompt for continuing active EXECUTION_TASK
   - Includes last iteration context
   - ~60 lines

4. `build_synthesize_prompt(subplan_path, executions, achievement) -> str`

   - Builds prompt for synthesizing completed work
   - Includes all EXECUTION_TASK contexts
   - ~80 lines

5. `build_conflict_message(conflict_data, plan_path, feature_name, achievement_num) -> str`
   - Formats conflict detection messages
   - Includes resolution steps
   - ~100 lines

### 2. Updated Files

**`LLM/scripts/generation/generate_prompt.py`**:

- Import PromptBuilder class
- Initialize builder in relevant functions
- Replace inline prompt building with builder methods
- Delete extracted prompt generation code
- Expected reduction: ~400 lines

### 3. New Test File

**File**: `tests/LLM/scripts/generation/test_prompt_builder.py` (~350 lines)

**Test Coverage** (12+ tests):

- Test each of 5 prompt building methods
- Test context boundary formatting
- Test statistics extraction
- Test template structure
- Test edge cases (missing files, invalid paths)

### 4. Documentation

**File**: `documentation/MIGRATION_NOTES_PROMPT_BUILDER_EXTRACTION.md`

- Extraction process details
- Circular import resolution (if needed)
- Usage examples
- Testing approach

---

## 🔍 Current State Analysis

### Prompt Generation in generate_prompt.py

**Location**: Multiple sections throughout `generate_prompt.py`

**Functions/Logic to Extract**:

1. **Main prompt generation function** (~200 lines):

   - `generate_prompt()` - Core prompt building logic
   - Context boundary formatting
   - Achievement section extraction
   - Template composition

2. **Conflict message formatting** (~100 lines):

   - Conflict detection output
   - Resolution steps formatting
   - Filesystem vs PLAN diff display

3. **Helper utilities** (~100 lines):
   - Statistics extraction
   - Context sizing
   - Section line extraction
   - Validation script detection

**Dependencies**:

- `Path` from pathlib
- `parse_plan_file()` - for PLAN parsing
- `find_subplan_for_achievement()` - for SUBPLAN location
- `extract_handoff_section()` - for handoff parsing
- `detect_validation_scripts()` - for script detection

---

## 📐 Approach

### Phase 1: Module Structure (30 min)

**Actions**:

1. Create `LLM/scripts/generation/prompt_builder.py`
2. Add module docstring explaining prompt generation philosophy
3. Define `PromptBuilder` class skeleton
4. Add necessary imports
5. Test basic import

**Validation**:

- File created with proper structure
- Import statement works in generate_prompt.py
- Class can be instantiated

### Phase 2: Extract Core Prompt Builders (90 min)

**Actions**:

1. **Extract `build_create_subplan_prompt()`**:

   - Copy SUBPLAN prompt template logic
   - Update method signature (add self)
   - Import required dependencies locally
   - Preserve context boundaries format
   - Maintain all template sections

2. **Extract `build_create_execution_prompt()`**:

   - Copy EXECUTION_TASK prompt template logic
   - Update method signature (add self)
   - Preserve SUBPLAN context section
   - Maintain execution strategy formatting

3. **Extract `build_continue_execution_prompt()`**:
   - Copy continuation prompt logic
   - Extract last iteration context
   - Preserve iteration log format

**Validation**:

- All 3 methods compile without errors
- Methods return properly formatted strings
- All template sections present

### Phase 3: Extract Helper Methods (60 min)

**Actions**:

1. **Extract `build_synthesize_prompt()`**:

   - Copy synthesis prompt logic
   - Handle multiple EXECUTION_TASK contexts
   - Aggregate results formatting

2. **Extract `build_conflict_message()`**:

   - Copy conflict message formatting
   - Extract filesystem vs PLAN diff logic
   - Preserve resolution steps

3. **Extract helper utilities** (if needed):
   - Context boundary formatting
   - Statistics extraction
   - Section line helpers

**Validation**:

- All helper methods functional
- Dependencies resolved correctly
- Output format matches original

### Phase 4: Update generate_prompt.py (45 min)

**Actions**:

1. **Add import statement**:

   ```python
   from LLM.scripts.generation.prompt_builder import PromptBuilder
   ```

2. **Initialize builder**:

   - Create `builder = PromptBuilder()` where needed
   - Update `generate_prompt()` function

3. **Replace prompt building calls**:

   - Replace inline SUBPLAN prompt → `builder.build_create_subplan_prompt()`
   - Replace inline EXECUTION prompt → `builder.build_create_execution_prompt()`
   - Replace inline continue prompt → `builder.build_continue_execution_prompt()`
   - Replace inline synthesize prompt → `builder.build_synthesize_prompt()`
   - Replace conflict formatting → `builder.build_conflict_message()`

4. **Delete extracted code**:
   - Remove inline prompt templates
   - Remove helper functions
   - Clean up unused variables

**Validation**:

- Script runs without import errors
- All prompts generated correctly
- Output format unchanged
- Line count reduced by ~400

### Phase 5: Create Module Tests (75 min)

**Actions**:

1. **Create test file**:

   - `tests/LLM/scripts/generation/test_prompt_builder.py`
   - Import PromptBuilder class
   - Set up test fixtures (temp directories, mock files)

2. **Test core builders** (10 tests):

   - `test_build_create_subplan_prompt()`
   - `test_build_create_execution_prompt()`
   - `test_build_continue_execution_prompt()`
   - `test_build_synthesize_prompt()`
   - `test_build_conflict_message()`
   - Test with valid inputs
   - Test with edge cases (missing files, etc.)
   - Verify prompt structure and sections

3. **Test helper methods** (4+ tests):
   - Test context boundary formatting
   - Test statistics extraction
   - Test template completeness
   - Test error handling

**Validation**:

- All 12+ tests pass
- Coverage >90% for prompt_builder.py
- Edge cases handled

### Phase 6: Full Validation (30 min)

**Actions**:

1. **Run existing tests**:

   ```bash
   pytest tests/LLM/scripts/generation/ -v
   ```

   - Verify all tests still pass
   - Check for regressions

2. **Run integration test**:

   ```bash
   python LLM/scripts/generation/generate_prompt.py @PROMPT-GENERATOR-UX-AND-FOUNDATION --interactive
   ```

   - Test all prompt types in interactive mode
   - Verify prompt format unchanged

3. **Verify metrics**:

   - Check line count reduction
   - Verify test coverage
   - Confirm no breaking changes

4. **Create migration notes**:
   - Document extraction process
   - Note any circular import resolutions
   - Provide usage examples

**Validation**:

- All tests passing (0 failures)
- Interactive mode functional
- Prompts generate correctly
- Migration notes complete

---

## 🎯 Execution Strategy

### Single EXECUTION Approach

**Rationale**:

- All 5 prompt builders work together to form complete prompt system
- Must be extracted together to maintain prompt consistency
- Similar to Achievement 2.2 (workflow detector extraction)

**Execution Plan**:

- **EXECUTION_TASK_23_01**: Complete extraction (all 6 phases)
- Duration: 3-4 hours
- Approach: Sequential phases, validate after each

**Risk Mitigation**:

- Follow proven pattern from Achievement 2.2
- Test after each phase
- Use local imports to avoid circular dependencies
- Commit after each successful phase

---

## 🧪 Testing Strategy

### 1. Unit Tests (12+ tests)

**Test each PromptBuilder method independently**:

- Create mock file structures
- Test with valid inputs
- Test edge cases (missing files, invalid paths)
- Verify prompt structure and completeness

### 2. Integration Tests (existing)

**Existing tests should continue to pass**:

- Prompt generation works end-to-end
- All workflow states produce correct prompts
- No regressions in prompt format

### 3. Manual Tests

**Interactive mode validation**:

- Test all prompt types through interactive menu
- Verify clipboard copying works
- Confirm prompt format unchanged

### Test Fixtures

**Mock file structures needed**:

- Plans with different states
- SUBPLANs with various completion levels
- EXECUTION_TASKs with iteration logs
- Conflict scenarios

**Data needed**:

- Sample Achievement objects
- Mock PLAN content
- Sample SUBPLAN templates
- Sample EXECUTION_TASK content

---

## 📊 Expected Results

### Quantitative Metrics

| Metric                   | Before | After  | Change |
| ------------------------ | ------ | ------ | ------ |
| generate_prompt.py lines | 2,258  | ~1,858 | -400   |
| Number of modules        | 3      | 4      | +1     |
| Test files               | 3      | 4      | +1     |
| Test count               | 43     | 55+    | +12    |
| Test coverage (builder)  | N/A    | >90%   | New    |

### Qualitative Benefits

**Maintainability**:

- ✅ Clear separation between prompt building and workflow
- ✅ Prompt logic isolated and easier to modify
- ✅ Template changes don't affect workflow logic
- ✅ Reduced cognitive load (smaller files)

**Testability**:

- ✅ Independent unit tests for each prompt type
- ✅ Easier to test prompt variations
- ✅ Better test organization

**Extensibility**:

- ✅ Easy to add new prompt types
- ✅ Easy to modify existing templates
- ✅ Clear pattern for future prompt additions

---

## ⚠️ Risks & Mitigation

### Risk 1: Prompt Format Changes

**Risk**: Extraction might inadvertently change prompt structure

**Likelihood**: Medium  
**Impact**: High (breaks existing workflows)

**Mitigation**:

- Copy prompts exactly as-is
- Add tests to verify prompt structure
- Compare before/after outputs
- Manual validation of each prompt type

### Risk 2: Circular Imports

**Risk**: PromptBuilder might need functions from generate_prompt.py

**Likelihood**: Medium  
**Impact**: Medium (import errors)

**Mitigation**:

- Use `from __future__ import annotations` for type hints
- Import dependencies locally within methods
- Use TYPE_CHECKING for type-only imports
- Follow pattern from Achievement 2.2

### Risk 3: Context Dependency

**Risk**: Prompts might depend on generate_prompt.py context

**Likelihood**: Low  
**Impact**: Medium (missing context in prompts)

**Mitigation**:

- Pass all required context as parameters
- Ensure builder methods are self-contained
- Test with various input scenarios
- Verify no implicit dependencies

### Risk 4: Test Fixture Complexity

**Risk**: Prompt tests might require complex file structures

**Likelihood**: Medium  
**Impact**: Low (test maintenance burden)

**Mitigation**:

- Create reusable test fixtures
- Use helper functions for setup
- Document fixture requirements
- Keep test data minimal

---

## 🔗 Dependencies

### Input Dependencies

**Required Before Starting**:

- ✅ Achievement 2.1 complete (InteractiveMenu extracted)
- ✅ Achievement 2.2 complete (WorkflowDetector extracted)
- ✅ generate_prompt.py at 2,258 lines
- ✅ Circular import pattern established

### Output Dependencies

**Enables Future Work**:

- Achievement 2.4: Extract Parsing & Utilities Module
- Achievement 2.6: Integrate Modules & Final Refactor
- Template modifications without touching workflow logic

---

## ✅ Completion Criteria

This SUBPLAN is complete when:

1. ✅ PromptBuilder module created (~400 lines)
2. ✅ All 5 prompt building methods implemented
3. ✅ generate_prompt.py reduced to ~1,858 lines
4. ✅ All 55+ tests passing (43 existing + 12 new)
5. ✅ Prompt formats unchanged (validated manually)
6. ✅ >90% coverage on prompt_builder.py
7. ✅ Migration notes created
8. ✅ Interactive mode functional
9. ✅ No regressions in existing functionality

**Next Steps After Completion**:

- Mark SUBPLAN as complete
- Update PLAN with actual metrics
- Request review for APPROVED_23.md
- Move to Achievement 2.4 (Extract Parsing & Utilities)

---

## 📚 References

- **Parent PLAN**: `PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md` (Achievement 2.3)
- **Previous Extractions**:
  - Achievement 2.1: Interactive Menu extraction
  - Achievement 2.2: Workflow Detector extraction (similar pattern)
- **Templates**:
  - `LLM/templates/SUBPLAN-TEMPLATE.md`
  - `LLM/templates/EXECUTION_TASK-TEMPLATE.md`
- **Guides**:
  - `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md`
  - `documentation/STATE_TRACKING_PHILOSOPHY.md`
- **Migration Notes**:
  - `MIGRATION_NOTES_INTERACTIVE_MENU_EXTRACTION.md`
  - `MIGRATION_NOTES_WORKFLOW_DETECTOR_EXTRACTION.md`

---

**SUBPLAN Status**: 🎯 Ready to Execute  
**Waiting on**: Executor to begin work  
**Estimated Duration**: 3-4 hours
