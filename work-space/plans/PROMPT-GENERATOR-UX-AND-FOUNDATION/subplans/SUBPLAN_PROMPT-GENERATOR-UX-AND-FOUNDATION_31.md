# SUBPLAN: Comprehensive Error Messages + Library Integration

**Type**: SUBPLAN  
**Mother Plan**: PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md  
**Plan**: PROMPT-GENERATOR-UX-AND-FOUNDATION  
**Achievement Addressed**: Achievement 3.1 (Comprehensive Error Messages + Library Integration)  
**Achievement**: 3.1  
**Status**: Not Started  
**Created**: 2025-11-13 21:00 UTC  
**Estimated Effort**: 2 hours

**Metadata Tags**: See `LLM/guides/METADATA-TAGS.md` for virtual organization system

**File Location**: `work-space/plans/PROMPT-GENERATOR-UX-AND-FOUNDATION/subplans/SUBPLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION_31.md`

**Size**: ~530 lines

**Note**: This SUBPLAN operates independently - Designer creates design, plans execution(s), then Executor(s) execute. See `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` for complete workflow.

---

## 🎯 Objective

Transform error handling from basic try/except blocks to production-grade structured error handling with actionable suggestions, while integrating production-ready libraries (`error_handling`, `logging`, `validation`) from `core/libraries/`. This establishes reusable patterns for future CLI platform development.

**Context**: Current LLM/scripts/generation/ codebase has 18 basic try/except blocks with minimal context (just print and sys.exit). Users get cryptic errors without guidance on how to fix them. This achievement upgrades to structured exceptions, actionable suggestions, comprehensive logging, and input validation.

**Goal**: Replace all basic error handling with library-based structured handling, providing +300% improvement in error message quality and enabling JSON-structured debugging logs.

---

## 📋 What Needs to Be Created

### Files to Create

1. **`LLM/scripts/generation/exceptions.py`** (~100 lines):

   - Custom exception classes for domain errors
   - `PlanNotFoundError`
   - `AchievementNotFoundError`
   - `SubplanNotFoundError`
   - `InvalidAchievementFormatError`
   - Each with structured error data

2. **`LLM/docs/ERROR_HANDLING_PATTERNS.md`** (~100 lines):
   - Error handling patterns guide
   - Custom exception reference
   - Example usage patterns
   - Troubleshooting guide

### Files to Modify

1. **`LLM/scripts/generation/generate_prompt.py`**:

   - Replace 6-8 try/except blocks with structured error handling
   - Add logging integration
   - Add input validation for user inputs
   - Add color-coded output

2. **`LLM/scripts/generation/generate_fix_prompt.py`**:

   - Replace 2-3 try/except blocks
   - Add structured error handling
   - Add logging

3. **`LLM/scripts/generation/workflow_detector.py`**:

   - Replace 3-4 try/except blocks
   - Add structured error handling
   - Add logging

4. **`LLM/scripts/generation/plan_parser.py`**:

   - Replace 2-3 try/except blocks
   - Add structured error handling
   - Add logging

5. **`LLM/scripts/generation/utils.py`**:

   - Replace 2-3 try/except blocks
   - Add structured error handling
   - Add validation helpers

6. **Other generation scripts** (as needed):
   - `generate_subplan_prompt.py`
   - `generate_execution_prompt.py`
   - `interactive_menu.py`

### Tests to Create/Modify

1. **`tests/LLM/scripts/generation/test_exceptions.py`** (~50 lines):

   - Test custom exception classes
   - Test error message formatting
   - Test suggestion generation

2. **Update existing tests** (~100 lines):
   - Test error scenarios with new structured errors
   - Test validation failures
   - Test logging output

---

## 📝 Approach

**Strategy**: Systematic upgrade of error handling across all generation scripts, starting with core modules (utils, plan_parser) and progressing to higher-level scripts (generate_prompt). Integrate libraries incrementally - error handling first, then logging, then validation.

**Method**:

1. **Phase 1 - Error Handling Library Integration** (30 min):

   - Create custom exception classes in `exceptions.py`
   - Identify all 18 try/except blocks across scripts
   - Replace with `@handle_errors` decorator and `ApplicationError`
   - Add context and suggestions to all errors
   - Test each replacement

2. **Phase 2 - Logging Library Integration** (30 min):

   - Replace print statements with structured logging
   - Add `get_logger(__name__)` to each module
   - Set log context at entry points (main functions)
   - Enable JSON log output for debugging
   - Test logging output

3. **Phase 3 - Validation Library Integration** (30 min):

   - Identify all user input points
   - Add validation for folder shortcuts, achievement numbers, file paths
   - Add validation for flag combinations
   - Test validation failures

4. **Phase 4 - Enhanced Error Messages** (30 min):
   - Add color coding (red/yellow/green/blue)
   - Ensure all errors have actionable suggestions
   - Add auto-copy to clipboard for errors
   - Test error message quality
   - Update documentation

**Key Considerations**:

- **Backward Compatibility**: Maintain existing function signatures
- **Incremental Testing**: Test after each phase, don't break existing functionality
- **Pattern Consistency**: Establish consistent patterns for future development
- **Library Usage**: Rely on `core/libraries/` for production-grade implementations
- **Error Message Quality**: Every error must have clear description, context, and suggestions

---

## 🔄 Execution Strategy

**Execution Count**: Single

**Rationale**: This is a systematic upgrade task with clear sequential phases. All work builds on the same codebase and requires a single coordinated pass to ensure consistency. No experimentation or comparison needed - implementation path is clear from the supporting analysis document.

**EXECUTION_TASK**: `EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_31_01.md`

**Decision Guidance**: Single execution chosen because:

- Clear technical approach (no ambiguity)
- Well-documented in supporting analysis (EXECUTION_ANALYSIS_LIBRARY-INTEGRATION-OPPORTUNITIES-PRIORITY-3.md)
- Sequential dependencies (error handling → logging → validation)
- Systematic replacement task (not exploratory)
- Consistent patterns needed across all files

---

## 🧪 Tests Required

### Test File

- **Path**: `tests/LLM/scripts/generation/test_exceptions.py`
- **Naming Convention**: `test_<module_name>.py`
- **Test Infrastructure**: Use existing pytest fixtures

### Test Cases to Cover

**Custom Exceptions** (test_exceptions.py):

1. Test PlanNotFoundError with context and suggestions
2. Test AchievementNotFoundError with context
3. Test SubplanNotFoundError with file path
4. Test InvalidAchievementFormatError with format details
5. Test exception serialization for logging

**Error Handling Integration**:

1. Test @handle_errors decorator wraps errors correctly
2. Test ApplicationError includes all required fields
3. Test error messages have actionable suggestions
4. Test errors copied to clipboard
5. Test color coding in terminal output

**Logging Integration**:

1. Test structured logging replaces print statements
2. Test log context propagation
3. Test JSON log output format
4. Test log levels (info, warning, error)

**Validation Integration**:

1. Test folder shortcut validation (valid/invalid formats)
2. Test achievement number validation (X.Y format)
3. Test file path validation (existence, permissions)
4. Test flag combination validation (conflicting flags)
5. Test validation error messages

**Integration Tests**:

1. Test end-to-end error flow (error → structured → logged → clipboard)
2. Test validation → error → suggestion flow
3. Test logging context in multi-function calls
4. Test backward compatibility (existing scripts still work)

### Coverage Requirements

- **Target Coverage**: >90% for new exception classes
- **Required Test Types**:
  - Unit tests for all custom exceptions
  - Integration tests for error handling flow
  - Validation tests for all input types
  - Logging tests for structured output

---

## ✅ Expected Results

### Functional Changes

- **Error Handling**: All try/except blocks use structured `ApplicationError` with context and suggestions
- **Logging**: All print statements replaced with structured logging (JSON format available)
- **Validation**: All user inputs validated before processing
- **Error Messages**: Every error includes what/why/how-to-fix with color coding
- **Clipboard**: Errors automatically copied to clipboard for easy sharing

### Performance Changes

- **Minimal Performance Impact**: Library overhead ~1-2ms per operation (negligible)
- **Debugging Speed**: +1000% faster with structured JSON logs vs print statements
- **Error Resolution Time**: -80% with actionable suggestions vs cryptic errors

### Observable Outcomes

**Before** (Basic):

```bash
$ python generate_prompt.py @NONEXISTENT.md --next

❌ Error: [Errno 2] No such file or directory: 'work-space/plans/NONEXISTENT.md'
```

**After** (Structured):

```bash
$ python generate_prompt.py @NONEXISTENT.md --next

❌ ERROR: PLAN file not found

File: work-space/plans/NONEXISTENT/PLAN_NONEXISTENT.md
Reason: No folder matching '@NONEXISTENT' found in work-space/plans/

HOW TO FIX:
1. Check spelling: ls work-space/plans/
2. Use correct format: @FOLDER-NAME (e.g., @PROMPT-GENERATOR)
3. Or use full path: work-space/plans/FEATURE/PLAN_FEATURE.md

Available plans:
  - @PROMPT-GENERATOR-UX-AND-FOUNDATION
  - @GRAPHRAG-OBSERVABILITY-VALIDATION
  - @STAGE-DOMAIN-REFACTOR

✅ Error details copied to clipboard!
```

**User Experience**:

- ✅ Clear error description
- ✅ Reason explained
- ✅ Specific commands to fix
- ✅ Available options shown
- ✅ Error auto-copied for help requests

---

## 🔍 Conflict Analysis with Other Subplans

**Review Existing Subplans**:

- SUBPLAN_01 - 29: Completed or approved
- No conflicts identified

**Check for**:

- **Overlap**: No overlap - this is new error handling infrastructure
- **Conflicts**: No conflicts - backward compatible additions
- **Dependencies**: No dependencies on other in-progress work
- **Integration**: Integrates with existing scripts without breaking changes

**Analysis**:

- **No conflicts detected**: This achievement adds error handling infrastructure without modifying core logic
- **Backward Compatible**: Existing function signatures maintained
- **Clean Integration**: New error handling wraps existing code without breaking it

**Result**: Safe to proceed ✅

---

## 🔗 Dependencies

### Other Subplans

- **None**: This achievement is independent and can proceed immediately

### External Dependencies

- **Python**: 3.7+ (for typing support)
- **Libraries**: `core/libraries/error_handling`, `core/libraries/logging`, `core/libraries/validation` (already exist in codebase)
- **pytest**: For testing (already installed)
- **colorama** or similar: For terminal color output (check if available, add if needed)

### Prerequisite Knowledge

- Understand existing error handling in generation scripts
- Familiarity with decorator patterns (@handle_errors)
- Knowledge of structured logging (JSON format)
- Understanding of input validation patterns

### Reference Documents

- **`work-space/analyses/EXECUTION_ANALYSIS_LIBRARY-INTEGRATION-OPPORTUNITIES-PRIORITY-3.md`**: Complete implementation design (lines 119-334)
- **`core/libraries/error_handling/`**: Error handling library documentation
- **`core/libraries/logging/`**: Logging library documentation
- **`core/libraries/validation/`**: Validation library documentation

---

## 🔄 Execution Task Reference

**Execution Tasks** (created during execution):

_None yet - will be created when execution starts_

**First Execution**: `EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_31_01.md`

---

## 📊 Success Criteria

**This Subplan is Complete When**:

- [ ] All 18 try/except blocks replaced with structured error handling
- [ ] Custom exception classes created (4 types)
- [ ] All print statements replaced with structured logging
- [ ] All user inputs validated (folder shortcuts, achievement numbers, paths, flags)
- [ ] All errors have context + suggestions + auto-copy
- [ ] Color-coded terminal output implemented
- [ ] All tests passing (>90% coverage for new code)
- [ ] Documentation created (ERROR_HANDLING_PATTERNS.md)
- [ ] Backward compatibility verified (existing scripts work)
- [ ] Real-world validation successful (test with common errors)
- [ ] EXECUTION_TASK complete
- [ ] **Achievement feedback received** (see Completion Workflow below)
- [ ] Ready for archive

**Specific Criteria**:

1. **Error Quality**: Every error includes what/why/how with specific commands
2. **Logging**: Structured JSON logs available for debugging
3. **Validation**: All inputs validated before processing
4. **Color Coding**: Errors (red), warnings (yellow), success (green), info (blue)
5. **Clipboard**: Errors auto-copied with full context

---

## ✅ Completion Workflow (Filesystem-First)

**After All Work Complete**:

1. **Request Review**: Ask reviewer to assess achievement completion
2. **Reviewer Creates Feedback File**:
   - **If Approved**: Create `execution/feedbacks/APPROVED_31.md` (31 = achievement number without dot)
   - **If Fixes Needed**: Create `execution/feedbacks/FIX_31.md` with detailed issues
3. **Filesystem = Source of Truth**: Achievement completion tracked by APPROVED file existence, not PLAN markdown

**Achievement Index in PLAN**:

- Defines structure (list of all achievements)
- NOT updated with checkmarks or status manually
- Filesystem (`APPROVED_31.md` file) indicates completion status

**Do NOT**:

- ❌ Manually update PLAN markdown with "✅ Achievement complete"
- ❌ Add checkmarks to Achievement Index
- ❌ Update "Current Status & Handoff" to mark achievement done

**DO**:

- ✅ Request reviewer feedback after work complete
- ✅ Wait for `APPROVED_31.md` or `FIX_31.md` file creation
- ✅ If FIX required: Address issues, request re-review

**Why Filesystem-First**:

- Single source of truth (files, not markdown parsing)
- Automated detection by scripts (`generate_prompt.py`)
- Clear audit trail (feedback files are timestamped, contain rationale)
- Prevents markdown parsing issues

**Reference**: See `LLM/docs/FEEDBACK_SYSTEM_GUIDE.md` for complete guidance

---

## 📝 Notes

**Common Pitfalls**:

- **Don't Break Existing Functionality**: Test after each change, maintain backward compatibility
- **Library Availability**: Verify `core/libraries/` modules exist before importing
- **Error Message Consistency**: Use consistent format for all errors (what/why/how)
- **Performance**: Don't add expensive operations in error paths (keep fast)
- **Testing**: Test error scenarios explicitly, not just happy paths

**Resources**:

- **Analysis Document**: `work-space/analyses/EXECUTION_ANALYSIS_LIBRARY-INTEGRATION-OPPORTUNITIES-PRIORITY-3.md` (lines 119-334 - complete implementation examples)
- **Library Docs**: `core/libraries/*/README.md` for each library
- **Pattern Examples**: See before/after examples in analysis document

**Implementation Notes**:

- Start with lower-level modules (utils, plan_parser) before higher-level (generate_prompt)
- Test each module independently before moving to next
- Use consistent error message format across all scripts
- Add logging at entry points (main functions) for context propagation

---

## 📖 What to Read (Focus Rules)

**When working on this SUBPLAN**, follow these focus rules to minimize context:

**✅ READ ONLY**:

- This SUBPLAN file (complete file)
- Parent PLAN Achievement 3.1 section (162 lines)
- Active EXECUTION_TASKs (if any exist)
- Parent PLAN "Current Status & Handoff" section (14 lines)
- Supporting analysis document (as needed for implementation details)

**❌ DO NOT READ**:

- Parent PLAN full content
- Other achievements in PLAN
- Other SUBPLANs
- Completed EXECUTION_TASKs (unless needed for context)
- Completed work

**Context Budget**: ~700 lines (this SUBPLAN + achievement section + handoff + analysis snippets)

**Independent Operation**: This SUBPLAN operates independently:

- **Designer Phase**: Create SUBPLAN, design approach, plan execution(s) ✅
- **Executor Phase**: Execute EXECUTION_TASK(s) according to plan
- **Synthesis Phase**: Review results, synthesize learnings, complete SUBPLAN

**Executor Context**: Executor reads SUBPLAN objective (~2 sentences) and approach section only, not full SUBPLAN.

**Why**: SUBPLAN defines HOW to achieve one achievement. Reading other achievements or full PLAN adds scope and confusion.

**📖 See**: `LLM/guides/FOCUS-RULES.md` for complete focus rules and `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` for workflow.

---

## 🔄 Active EXECUTION_TASKs

**Real-Time Tracking** (update as EXECUTIONs progress):

| EXECUTION                                               | Status   | Progress | Notes          |
| ------------------------------------------------------- | -------- | -------- | -------------- |
| EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_31_01 | Planning | 0%       | Ready to start |

**Status Options**:

- **Planning**: EXECUTION_TASK created, not yet executing
- **Executing**: Work in progress
- **Complete**: Execution finished, deliverables verified
- **Failed**: Execution encountered issues (document in notes)

**Update Frequency**: Update this table as EXECUTIONs progress

**For Single Execution**: Single row in table

---

## 📊 Execution Results Synthesis

**Review All Results** (complete after all EXECUTIONs finish):

**EXECUTION Summary**:

- **EXECUTION_01 Results**: [Summary of what was achieved, learnings, outcomes]

**Learnings**:

- [What worked?]
- [What didn't work?]
- [What patterns emerged?]
- [What should be adopted?]

**For Single Execution**: Document learnings from that execution

**When to Complete**: After EXECUTION finishes, before marking SUBPLAN complete

---

**Ready to Execute**:

- **Designer**: Complete SUBPLAN design ✅, plan execution ✅, now create EXECUTION_TASK ✅
- **Executor**: Read SUBPLAN objective, execute according to plan
- **Reference**: `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` for complete workflow, `LLM/protocols/IMPLEMENTATION_START_POINT.md` for execution workflows
