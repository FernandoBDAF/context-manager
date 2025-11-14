# SUBPLAN: Implement FIX Feedback Detection & Prompt Generation

**Type**: SUBPLAN  
**Mother Plan**: PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md  
**Plan**: PROMPT-GENERATOR-UX-AND-FOUNDATION  
**Achievement Addressed**: Achievement 2.9 (Implement FIX Feedback Detection & Prompt Generation)  
**Achievement**: 2.9  
**Status**: Not Started  
**Created**: 2025-11-13 20:00 UTC  
**Estimated Effort**: 8-11 hours

**Metadata Tags**: See `LLM/guides/METADATA-TAGS.md` for virtual organization system

**File Location**: `work-space/plans/PROMPT-GENERATOR-UX-AND-FOUNDATION/subplans/SUBPLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION_29.md`

**Size**: ~550 lines

**Note**: This SUBPLAN operates independently - Designer creates design, plans execution(s), then Executor(s) execute. See `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` for complete workflow.

---

## 🎯 Objective

Close the feedback loop by implementing detection of `FIX_XX.md` files and generating fix-specific prompts with extracted issues, code references, and action plans. This completes the feedback system started in Achievement 2.5 by addressing the "needs fix" state that was previously ignored by the binary (approved/incomplete) state model.

**Context**: Real-world discovery during PLAN_GRAPHRAG-OBSERVABILITY-VALIDATION revealed that when a reviewer creates `FIX_21.md` with detailed fix requirements and code references (`@Python (779-1075)`, `@Python (873-1075)`), the prompt generation system ignores it and generates a standard "continue work" prompt instead of a "fix these issues" prompt. This creates confusion and requires manual workaround.

**Goal**: Implement tri-state achievement status (approved/needs_fix/incomplete) and create dedicated FIX prompt generator that extracts issues, code references, and action items from FIX files, providing clear guidance to executors.

---

## 📋 What Needs to Be Created

### Files to Create

1. **`LLM/scripts/generation/generate_fix_prompt.py`** (~400 lines):

   - Main entry point for FIX prompt generation
   - CLI with @folder shortcuts
   - Issue extraction parser
   - FIX prompt template
   - Clipboard integration

2. **`tests/LLM/scripts/generation/test_generate_fix_prompt.py`** (~200 lines):

   - Unit tests for tri-state detection
   - Unit tests for issue extraction
   - Integration tests for end-to-end generation
   - Real-world validation tests

3. **FIX_RESOLUTION Template Documentation** (~100 lines):
   - Structure for resolution files
   - Required sections
   - Verification checklist
   - Re-review request format

### Files to Modify

1. **`LLM/scripts/generation/utils.py`**:

   - Add `get_achievement_status()` function (~30 lines)
   - Update `is_achievement_complete()` for backward compatibility

2. **`LLM/scripts/generation/generate_prompt.py`**:

   - Add FIX state detection (~30 lines)
   - Integrate `generate_fix_prompt()` call
   - Add clipboard support for FIX prompts

3. **`LLM/scripts/generation/workflow_detector.py`**:

   - Add "needs_fix" state to detection (~50 lines)
   - Return "address_fixes" recommendation
   - Include FIX file reference in state info

4. **`LLM/scripts/generation/interactive_menu.py`** (if applicable):

   - Show FIX state in menu (~20 lines)
   - Update menu text for "needs_fix" scenario

5. **`LLM/docs/FEEDBACK_SYSTEM_GUIDE.md`**:

   - Add tri-state status model section (~150 lines)
   - Document FIX detection workflow
   - Add FIX prompt generation examples
   - Include code reference extraction patterns

6. **`tests/LLM/scripts/generation/test_utils.py`**:

   - Add tests for `get_achievement_status()` (~50 lines)

7. **`tests/LLM/scripts/generation/test_workflow_detector.py`**:
   - Add tests for "needs_fix" state detection (~50 lines)

### Functions/Classes to Add

1. **`get_achievement_status(ach_num, plan_path)`** in `utils.py`:

   - Returns: "approved", "needs_fix", or "incomplete"
   - Checks APPROVED_XX.md first (priority)
   - Checks FIX_XX.md second
   - Returns "incomplete" if neither exists

2. **`extract_fix_issues(fix_file_path)`** in `generate_fix_prompt.py`:

   - Extracts metadata (reviewer, date)
   - Parses Critical Issues section
   - Parses Minor Issues section
   - Extracts code references (`@Python (779-1075)` patterns)
   - Returns structured dictionary

3. **`generate_fix_prompt(plan_path, achievement_num)`** in `generate_fix_prompt.py`:

   - Loads FIX_XX.md file
   - Extracts issues using parser
   - Formats into FIX_PROMPT_TEMPLATE
   - Returns complete prompt string

4. **FIX_PROMPT_TEMPLATE** constant in `generate_fix_prompt.py`:
   - Header with reviewer info
   - Critical issues section (numbered)
   - Minor issues section
   - Code references section
   - What worked well section
   - Step-by-step fix action plan
   - FIX_RESOLUTION template
   - DO NOT / REMEMBER guidelines

### Tests Required

1. **Unit Tests** (test_utils.py):

   - Test tri-state with APPROVED file → "approved"
   - Test tri-state with FIX file only → "needs_fix"
   - Test tri-state with neither → "incomplete"
   - Test tri-state with both (APPROVED priority) → "approved"

2. **Unit Tests** (test_generate_fix_prompt.py):

   - Test issue extraction from FIX file
   - Test code reference regex extraction
   - Test template formatting
   - Test metadata parsing

3. **Integration Tests**:

   - End-to-end FIX prompt generation
   - Workflow detection with FIX files
   - Interactive menu with "needs_fix" state

4. **Real-World Validation**:

   - Test with actual `FIX_21.md` from GRAPHRAG plan
   - Verify code references extracted correctly
   - Confirm prompt structure matches expectations

5. **Backward Compatibility Tests**:
   - Verify existing tests still pass
   - Confirm `is_achievement_complete()` behavior unchanged
   - Test with plans without FIX files

---

## 📝 Approach

**Strategy**: Implement tri-state status model starting from lowest level (utils) and working up to highest level (prompt generation), then integrate into workflow detection and interactive menu. Test at each level before proceeding.

**Method**:

1. **Phase 1 - Core Status Detection** (2-3 hours):

   - Create `get_achievement_status()` in utils.py
   - Update `is_achievement_complete()` wrapper
   - Write comprehensive unit tests
   - Verify backward compatibility

2. **Phase 2 - FIX Prompt Generator** (3-4 hours):

   - Create generate_fix_prompt.py script
   - Implement issue extraction parser
   - Design and implement FIX_PROMPT_TEMPLATE
   - Add CLI with @folder shortcuts
   - Write unit tests for parser

3. **Phase 3 - Workflow Integration** (1-2 hours):

   - Update generate_prompt.py to check tri-state status
   - Update workflow_detector.py for "needs_fix" state
   - Update interactive menu (if applicable)
   - Add clipboard support

4. **Phase 4 - Documentation** (1 hour):

   - Update FEEDBACK_SYSTEM_GUIDE.md
   - Create FIX_RESOLUTION template documentation
   - Document code reference patterns
   - Update testing guides (if relevant)

5. **Phase 5 - Testing & Validation** (1 hour):
   - Run all unit tests
   - Run integration tests
   - Real-world validation with FIX_21.md
   - Backward compatibility verification

**Key Considerations**:

- **Backward Compatibility**: Maintain existing `is_achievement_complete()` behavior for all existing code
- **Parser Robustness**: Handle variations in FIX file format (some might have only critical issues, some both)
- **Code Reference Extraction**: Use regex to extract patterns like `@Python (779-1075)`, handle multiple references
- **Template Flexibility**: FIX_PROMPT_TEMPLATE should work with varying numbers of issues and references
- **Error Handling**: Graceful failures if FIX file is malformed or missing expected sections
- **Real-World Testing**: Use actual FIX_21.md to ensure parser handles real-world format

---

## 🔄 Execution Strategy

**Execution Count**: Single

**Rationale**: Single clear approach with well-defined phases. All work builds on itself sequentially (core → parser → integration → docs → tests). No experimentation or comparison needed - implementation path is clear from case study.

**EXECUTION_TASK**: `EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_29_01.md`

**Decision Guidance**: Single execution chosen because:

- Clear technical approach (no ambiguity)
- Well-documented in case study (940 lines of design)
- Sequential dependencies (utils → generator → integration)
- No need for A/B comparison or experimentation
- Backward compatibility requirement (one correct approach)

---

## 🧪 Tests Required

### Test File

- **Path**: `tests/LLM/scripts/generation/test_generate_fix_prompt.py`
- **Naming Convention**: `test_<script_name>.py`
- **Test Infrastructure**: Use existing fixtures from `tests/LLM/scripts/conftest.py`

### Test Cases to Cover

**Tri-State Detection** (test_utils.py):

1. Test with APPROVED_XX.md exists → returns "approved"
2. Test with FIX_XX.md only → returns "needs_fix"
3. Test with neither file → returns "incomplete"
4. Test with both files → returns "approved" (priority)
5. Test backward compat: `is_achievement_complete()` with APPROVED → True
6. Test backward compat: `is_achievement_complete()` with FIX only → False

**Issue Extraction** (test_generate_fix_prompt.py):

1. Test extract metadata (reviewer, date, status)
2. Test parse Critical Issues section (#### headers)
3. Test parse Minor Issues section (bullet points)
4. Test extract code references (`@Python (779-1075)`)
5. Test extract "What Worked Well" section
6. Test handle missing sections gracefully
7. Test handle malformed FIX file

**Template Formatting** (test_generate_fix_prompt.py):

1. Test FIX prompt with critical issues only
2. Test FIX prompt with critical + minor issues
3. Test FIX prompt with code references
4. Test FIX prompt with "What Worked Well"
5. Test FIX prompt with all sections
6. Test template fills correctly with extracted data

**Integration** (test_generate_fix_prompt.py):

1. Test end-to-end: FIX file → prompt generation
2. Test CLI with @folder shortcut
3. Test clipboard functionality
4. Test error handling for missing FIX file

**Workflow Detection** (test_workflow_detector.py):

1. Test detect "needs_fix" state when FIX_XX.md exists
2. Test return "address_fixes" recommendation
3. Test include FIX file reference in state info
4. Test workflow progression: incomplete → needs_fix → approved

**Real-World Validation**:

1. Test with actual `FIX_21.md` from GRAPHRAG plan
2. Verify all issues extracted correctly
3. Verify all code references extracted
4. Verify prompt structure matches expectations
5. Verify FIX_RESOLUTION template included

### Coverage Requirements

- **Target Coverage**: >90% for new code
- **Required Test Types**:
  - Unit tests for all new functions/classes
  - Integration tests for end-to-end workflows
  - Edge case tests for error handling
  - Real-world validation tests

### Test-First Requirement

- [ ] Tests written before implementation (TDD workflow preferred)
- [ ] Initial test run shows all failing (red)
- [ ] Tests define success criteria
- [ ] Implementation makes tests pass (green)

---

## ✅ Expected Results

### Functional Changes

- **Tri-State Status**: Achievement status now returns "approved", "needs_fix", or "incomplete" instead of binary True/False
- **FIX Detection**: System automatically detects `FIX_XX.md` files in `execution/feedbacks/` folder
- **FIX Prompts**: New prompt type generated specifically for addressing fixes, with structured issues and action plan
- **Workflow Updates**: `generate_prompt.py` and `workflow_detector.py` handle "needs_fix" state correctly
- **Interactive Menu**: Menu shows FIX state clearly when applicable

### Performance Changes

- **No Performance Impact**: Detection adds ~5ms for filesystem check (negligible)
- **Faster Workflow**: Eliminates manual extraction of issues from FIX files (~10-15 minutes saved per FIX cycle)

### Observable Outcomes

**Before** (Broken):

```bash
$ python generate_prompt.py @PLAN_GRAPHRAG-OBSERVABILITY-VALIDATION.md --next

✅ PLAN file found
📋 Scanning for next achievement...
🔍 Found: Achievement 2.1
📝 Status: In Progress

Generating EXECUTION prompt for Achievement 2.1...
[Generates standard "continue work" prompt - WRONG! FIX_21.md exists]
```

**After** (Fixed):

```bash
$ python generate_prompt.py @PLAN_GRAPHRAG-OBSERVABILITY-VALIDATION.md --next

✅ PLAN file found
📋 Scanning for next achievement...
🔍 Found: Achievement 2.1
⚠️  Status: NEEDS FIX (FIX_21.md detected)

Generating FIX-specific prompt for Achievement 2.1...

═══════════════════════════════════════════════════════════════
⚠️  ACHIEVEMENT 2.1 REQUIRES FIXES
═══════════════════════════════════════════════════════════════

Reviewer: [Name]
Review Date: 2025-11-12
Feedback File: execution/feedbacks/FIX_21.md

CRITICAL ISSUES (Must Fix):
1. [Issue 1 description]
   Code: @Python (779-1075)

2. [Issue 2 description]
   Code: @Python (873-1075)

MINOR ISSUES (Nice to Fix):
- [Issue A]
- [Issue B]

ACTION PLAN:
Step 1: Address critical issue #1
Step 2: Address critical issue #2
Step 3: Address minor issues (optional)
Step 4: Create FIX_RESOLUTION_21.md
Step 5: Request re-review

[... complete FIX prompt with template ...]

✅ Prompt copied to clipboard!
```

**User Experience**:

- ✅ Clear indication of FIX state
- ✅ All issues extracted and formatted
- ✅ Code references highlighted
- ✅ Action plan provided
- ✅ FIX_RESOLUTION template included
- ✅ No manual work required

---

## 🔍 Conflict Analysis with Other Subplans

**Review Existing Subplans**:

- SUBPLAN_01 - 28: Completed or in progress
- No conflicts identified

**Check for**:

- **Overlap**: No overlap - this is new functionality
- **Conflicts**: No conflicts - extends existing system without breaking it
- **Dependencies**: Depends on Achievement 2.5 (Feedback System) ✅ Complete
- **Integration**: Integrates with existing `utils.py`, `generate_prompt.py`, `workflow_detector.py` without breaking changes

**Analysis**:

- **No conflicts detected**: This achievement extends the feedback system established in Achievement 2.5
- **Backward Compatible**: Maintains existing `is_achievement_complete()` behavior
- **Clean Integration**: Adds new functionality without modifying existing workflows (except to handle new state)

**Result**: Safe to proceed ✅

---

## 🔗 Dependencies

### Other Subplans

- **Achievement 2.5 (Feedback System Patterns)**: ✅ Complete - Established `APPROVED_XX.md` and `FIX_XX.md` conventions
- **Achievement 2.6 (Module Integration)**: ✅ Complete - Modular structure in place (`utils.py`, etc.)
- **Achievement 2.7 (Test Modernization)**: ✅ Complete - Test patterns aligned with filesystem-first

### External Dependencies

- **Python**: 3.7+ (for `pathlib`)
- **pyperclip**: For clipboard functionality (already installed)
- **pytest**: For testing (already installed)

### Prerequisite Knowledge

- Understand feedback system conventions (`APPROVED_XX.md`, `FIX_XX.md`)
- Familiarity with `generate_prompt.py` workflow
- Knowledge of `workflow_detector.py` state detection
- Understanding of modular structure from Achievement 2.6

### Reference Documents

- **`work-space/case-studies/EXECUTION_CASE-STUDY_FIX-FEEDBACK-DETECTION-GAP.md`**: Complete implementation design (940 lines)
- **`work-space/analyses/EXECUTION_ANALYSIS_FIX-FEEDBACK-DETECTION-PROPOSAL.md`**: Pros/cons analysis (636 lines)
- **`LLM/docs/FEEDBACK_SYSTEM_GUIDE.md`**: Feedback system documentation (Achievement 2.5)
- **`work-space/plans/GRAPHRAG-OBSERVABILITY-VALIDATION/execution/feedbacks/FIX_21.md`**: Real-world example

---

## 🔄 Execution Task Reference

**Execution Tasks** (created during execution):

_None yet - will be created when execution starts_

**First Execution**: `EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_29_01.md`

**If Circular Debug**: `EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_29_02.md` (or next number)

---

## 📊 Success Criteria

**This Subplan is Complete When**:

- [ ] All deliverables created (generate_fix_prompt.py, tests, docs)
- [ ] All tests passing (unit + integration)
- [ ] Tri-state status working correctly
- [ ] FIX prompts generated with all sections
- [ ] Code reference extraction working
- [ ] Workflow integration complete
- [ ] Interactive menu updated (if applicable)
- [ ] Documentation updated
- [ ] Real-world validation successful (FIX_21.md)
- [ ] Backward compatibility verified
- [ ] EXECUTION_TASK complete
- [ ] **Achievement feedback received** (see Completion Workflow below)
- [ ] Ready for archive

**Specific Criteria**:

1. **Tri-State Detection**: `get_achievement_status()` correctly returns "approved"/"needs_fix"/"incomplete"
2. **Issue Extraction**: Parser extracts all sections from FIX file (critical, minor, code refs, what worked)
3. **Prompt Generation**: FIX prompts include all required sections (issues, action plan, template)
4. **Workflow Integration**: `generate_prompt.py` correctly routes to FIX prompt for "needs_fix" state
5. **Backward Compatibility**: All existing tests pass, `is_achievement_complete()` unchanged behavior
6. **Real-World Test**: Successfully processes actual `FIX_21.md` file

---

## ✅ Completion Workflow (Filesystem-First)

**After All Work Complete**:

1. **Request Review**: Ask reviewer to assess achievement completion
2. **Reviewer Creates Feedback File**:
   - **If Approved**: Create `execution/feedbacks/APPROVED_29.md` (29 = achievement number without dot)
   - **If Fixes Needed**: Create `execution/feedbacks/FIX_29.md` with detailed issues
3. **Filesystem = Source of Truth**: Achievement completion tracked by APPROVED file existence, not PLAN markdown

**Achievement Index in PLAN**:

- Defines structure (list of all achievements)
- NOT updated with checkmarks or status manually
- Filesystem (`APPROVED_29.md` file) indicates completion status

**Do NOT**:

- ❌ Manually update PLAN markdown with "✅ Achievement complete"
- ❌ Add checkmarks to Achievement Index
- ❌ Update "Current Status & Handoff" to mark achievement done

**DO**:

- ✅ Request reviewer feedback after work complete
- ✅ Wait for `APPROVED_29.md` or `FIX_29.md` file creation
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

- **Don't Break Backward Compatibility**: Many existing tests/scripts use `is_achievement_complete()` - must maintain behavior
- **Parser Robustness**: FIX files might have variations - handle missing sections gracefully
- **Code Reference Regex**: Must handle multiple patterns (`@Python`, `@TypeScript`, etc.) and multiple references per issue
- **Template Flexibility**: FIX_PROMPT_TEMPLATE must work with varying numbers of issues (1-10+)

**Resources**:

- **Case Study**: `work-space/case-studies/EXECUTION_CASE-STUDY_FIX-FEEDBACK-DETECTION-GAP.md` (complete implementation design)
- **Real Example**: `work-space/plans/GRAPHRAG-OBSERVABILITY-VALIDATION/execution/feedbacks/FIX_21.md`
- **Feedback Guide**: `LLM/docs/FEEDBACK_SYSTEM_GUIDE.md`
- **Testing Guide**: `work-space/plans/PROMPT-GENERATOR-UX-AND-FOUNDATION/documentation/MIGRATION_NOTES_TEST_MODERNIZATION.md`

**Implementation Notes**:

- Start with `get_achievement_status()` and tests - foundation is critical
- Use TDD approach - write tests first, then implement
- Test real-world `FIX_21.md` early to catch format issues
- Keep `is_achievement_complete()` unchanged (just wrap `get_achievement_status()`)

---

## 📖 What to Read (Focus Rules)

**When working on this SUBPLAN**, follow these focus rules to minimize context:

**✅ READ ONLY**:

- This SUBPLAN file (complete file)
- Parent PLAN Achievement 2.9 section (254 lines)
- Active EXECUTION_TASKs (if any exist)
- Parent PLAN "Current Status & Handoff" section (14 lines)
- Reference case study for implementation details (as needed)

**❌ DO NOT READ**:

- Parent PLAN full content
- Other achievements in PLAN
- Other SUBPLANs
- Completed EXECUTION_TASKs (unless needed for context)
- Completed work

**Context Budget**: ~600 lines (this SUBPLAN + achievement section + handoff + case study snippets)

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
| EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_29_01 | Planning | 0%       | Ready to start |

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
