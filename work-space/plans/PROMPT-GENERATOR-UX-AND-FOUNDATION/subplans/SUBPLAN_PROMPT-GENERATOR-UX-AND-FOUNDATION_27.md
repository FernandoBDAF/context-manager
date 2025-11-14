# SUBPLAN: Modernize Test Suite for Filesystem-First Architecture

**Achievement**: 2.7 - Modernize Test Suite for Filesystem-First Architecture  
**Feature**: PROMPT-GENERATOR-UX-AND-FOUNDATION  
**Created**: 2025-11-12  
**Effort Estimate**: 3-4 hours

---

## 🎯 Objective

Update 47 legacy tests (from Achievement 2.6) to align with filesystem-first state tracking architecture. These tests currently fail because they expect old PLAN markdown parsing behavior instead of the new APPROVED_XX.md file-based approach.

**Why This Matters**:

- 287 tests passing, 47 failing (86% pass rate) - need 100%
- Failing tests block safe refactoring
- Test patterns misaligned with current architecture
- No clear migration guide for future test writers

**Success Criteria**:

- ✅ All 47 failing tests updated and passing
- ✅ Test patterns align with filesystem-first philosophy
- ✅ Fixtures properly create APPROVED_XX.md files
- ✅ All function calls pass required parameters (plan_path)
- ✅ Migration documentation created
- ✅ Zero regressions in 287 currently passing tests

---

## 📦 Deliverables

### Code Changes (5-7 test files, ~350 lines modified)

1. **test_achievement_finding.py** (~50 lines modified)

   - Update is_achievement_complete() calls
   - Add plan_path parameters
   - Create APPROVED_XX.md files in fixtures
   - Status: 4 tests failing

2. **test_edge_cases.py** (~30 lines modified)

   - Update completion detection patterns
   - Add feedbacks directory creation
   - Status: 2 tests failing

3. **test_generate_prompt.py** (~20 lines modified)

   - Update function calls with plan_path
   - Status: 1 test failing

4. **test_dual_structure_discovery.py** (~15 lines modified)

   - Update test fixtures
   - Status: 1 test failing

5. **test_conflict_detection.py** (~80 lines modified)

   - Update conflict detection tests
   - Add filesystem state setup
   - Status: 8 tests failing

6. **test_generate_pause_prompt.py** (~60 lines modified)

   - Update pause prompt tests
   - Status: 6 tests failing

7. **test_generate_resume_prompt.py** (~100 lines modified)

   - Update resume prompt tests
   - Status: 10 tests failing

8. **test_generate_verify_prompt.py** (~30 lines modified)

   - Update verification tests
   - Status: 2 tests failing

9. **test_integration_workflows.py** (~50 lines modified)

   - Update workflow integration tests
   - Status: 2 tests failing

10. **test_interactive_output_menu.py** (~15 lines modified)
    - Update menu tests
    - Status: 11 tests failing (some may be assertion fixes)

### Documentation (1 file, ~200 lines)

11. **MIGRATION_NOTES_TEST_MODERNIZATION.md**
    - OLD vs NEW test patterns
    - Migration guide for test writers
    - Common patterns and anti-patterns
    - Examples for each scenario

---

## 🗺️ Approach

### Phase 1: Audit & Analysis (30 min)

**Objective**: Understand failure patterns and categorize fixes needed

**Tasks**:

1. Run full test suite, capture all failures
2. Categorize failures by type:
   - Missing plan_path parameter
   - Incorrect fixture setup (no APPROVED files)
   - Outdated assertions (expecting markdown)
   - Function signature mismatches
3. Create failure matrix (file × failure type)
4. Identify common patterns for batch fixes

**Output**:

- Test failure analysis document (inline in EXECUTION_TASK)
- Priority order for fixes
- Estimated lines per file

### Phase 2: Update Test Patterns (2-2.5 hours)

**Objective**: Systematically update each test file

**Strategy**: Work file-by-file, test after each file

**Pattern Updates**:

**OLD PATTERN (Markdown-based)**:

```python
# Test setup
plan_content = """
## Current Status & Handoff
- ✅ Achievement 1.1 Complete
"""

# Assertion
assert is_achievement_complete("1.1", plan_content)
```

**NEW PATTERN (Filesystem-first)**:

```python
# Test setup
feedbacks_dir = plan_path.parent / "execution" / "feedbacks"
feedbacks_dir.mkdir(parents=True)
(feedbacks_dir / "APPROVED_11.md").write_text("""# Achievement 1.1 Approval

**Status**: ✅ Approved
**Reviewer**: Test Suite
**Date**: 2025-11-12
""")

# Assertion
assert is_achievement_complete("1.1", "", plan_path)
```

**Fixture Updates**:

```python
@pytest.fixture
def temp_plan_structure():
    """Create complete plan structure with feedbacks."""
    temp_dir = tempfile.mkdtemp()
    plan_dir = Path(temp_dir) / "TEST-FEATURE"
    plan_dir.mkdir(parents=True)

    # Create plan file
    plan_file = plan_dir / "PLAN_TEST-FEATURE.md"
    plan_file.write_text("# PLAN: Test Feature\n...")

    # Create execution structure
    feedbacks_dir = plan_dir / "execution" / "feedbacks"
    feedbacks_dir.mkdir(parents=True)

    yield plan_dir, plan_file

    # Cleanup
    shutil.rmtree(temp_dir)
```

**Function Call Updates**:

```python
# OLD
is_achievement_complete("1.1", plan_content)

# NEW
is_achievement_complete("1.1", "", plan_path)

# OLD
find_next_achievement_from_root(achievements, plan_content)

# NEW
find_next_achievement_from_root(achievements, plan_content, plan_path)
```

**Per-File Strategy**:

1. Read file, identify all failures
2. Update fixtures to create feedbacks directory
3. Update all is_achievement_complete() calls
4. Create APPROVED_XX.md files as needed
5. Update function signatures
6. Run tests for that file only
7. Fix any remaining issues
8. Move to next file

**Priority Order**:

1. test_achievement_finding.py (4 failures, core functionality)
2. test_conflict_detection.py (8 failures, important)
3. test_generate_resume_prompt.py (10 failures, high count)
4. test_generate_pause_prompt.py (6 failures, medium)
5. test_integration_workflows.py (2 failures, integration)
6. test_edge_cases.py (2 failures, edge cases)
7. test_generate_verify_prompt.py (2 failures, verification)
8. test_generate_prompt.py (1 failure, single issue)
9. test_dual_structure_discovery.py (1 failure, single issue)
10. test_interactive_output_menu.py (11 failures, may be assertion-only)

### Phase 3: Create Migration Documentation (45 min)

**Objective**: Document patterns for future test writers

**Content**:

1. **Overview**: Why we migrated, what changed
2. **OLD vs NEW Patterns**: Side-by-side comparisons
3. **Common Scenarios**:
   - Testing achievement completion
   - Testing next achievement finding
   - Testing conflict detection
   - Creating test fixtures
4. **Anti-Patterns**: What NOT to do
5. **Quick Reference**: Cheat sheet for test writers

**Structure**:

```markdown
# Test Modernization Migration Notes

## Overview

- Why filesystem-first?
- What changed in tests?
- Impact on test writing

## Pattern Updates

### Pattern 1: Achievement Completion

OLD: [example]
NEW: [example]
WHY: [explanation]

### Pattern 2: Test Fixtures

...

## Common Scenarios

- Scenario 1: Testing completed achievement
- Scenario 2: Testing in-progress achievement
- Scenario 3: Testing achievement not started
  ...

## Anti-Patterns

- ❌ Parsing markdown for state
- ❌ Not creating feedbacks directory
- ❌ Missing plan_path parameter
  ...

## Quick Reference

[Cheat sheet table]
```

### Phase 4: Validation & Regression Check (30 min)

**Objective**: Ensure 100% test pass rate, zero regressions

**Tasks**:

1. Run full test suite (all 334 tests)
2. Verify all 47 previously failing tests now pass
3. Verify 287 previously passing tests still pass
4. Check for any new failures
5. Document final test counts
6. Run linter on modified files
7. Verify code quality

**Acceptance Criteria**:

- ✅ 334 tests passing (100% pass rate)
- ✅ Zero new failures introduced
- ✅ No linter errors
- ✅ All modified files formatted correctly

---

## 🎯 Execution Strategy

**Type**: Single Execution  
**Reason**: All work is cohesive (test file updates), sequential (file-by-file), and interdependent (patterns must be consistent)

**Execution Plan**:

- EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_27_01.md
  - Complete all 4 phases in sequence
  - Update 10 test files
  - Create 1 migration doc
  - Achieve 100% test pass rate

**Why Single Execution**:

- Work is highly related (same pattern updates across files)
- Can't parallelize (need to test incrementally)
- Benefits from context retention (pattern consistency)
- Relatively short duration (3-4 hours)
- Clear completion criteria (all tests passing)

**Workflow**:

1. Executor reads SUBPLAN + EXECUTION_TASK
2. Follows Phase 1-4 systematically
3. Documents progress in iteration log
4. Updates completion checklist
5. Requests APPROVED_27.md from reviewer

---

## 🧪 Testing Strategy

### Unit Test Validation

**Per-File Testing**:

```bash
# After each file modification
pytest tests/LLM/scripts/generation/test_achievement_finding.py -v

# Expected: All tests in file passing
```

**Incremental Validation**:

- Test after each file update
- Catch regressions immediately
- Build confidence incrementally

### Integration Testing

**Full Suite Run**:

```bash
# After all files updated
pytest tests/LLM/scripts/generation/ -v --tb=short

# Expected: 334 tests passing, 0 failures
```

**Coverage Check**:

```bash
# Ensure no coverage loss
pytest tests/LLM/scripts/generation/ --cov=LLM.scripts.generation --cov-report=term
```

### Regression Prevention

**Before/After Comparison**:

- Capture test output before changes
- Capture test output after changes
- Compare pass/fail counts
- Document any differences

**Validation Checklist**:

- [ ] All 47 previously failing tests now pass
- [ ] All 287 previously passing tests still pass
- [ ] No new failures introduced
- [ ] Total: 334 tests passing (100%)

---

## 📊 Expected Results

### Quantitative Metrics

**Test Suite**:

- Before: 287 passing, 47 failing (86% pass rate)
- After: 334 passing, 0 failing (100% pass rate)
- Improvement: +47 tests, +14 percentage points

**Code Changes**:

- Files modified: 10 test files
- Lines changed: ~350 lines
- Patterns updated: ~47 test cases
- Documentation added: ~200 lines

### Qualitative Improvements

**Test Quality**:

- ✅ Tests aligned with production code
- ✅ Filesystem-first patterns throughout
- ✅ Consistent fixture patterns
- ✅ Clear migration documentation

**Developer Experience**:

- ✅ 100% test pass rate (confidence boost)
- ✅ Clear patterns for new tests
- ✅ Safe to refactor (tests reliable)
- ✅ Migration guide available

**System Stability**:

- ✅ No broken tests blocking work
- ✅ Feedback system fully tested
- ✅ State tracking validated
- ✅ Ready for production use

---

## 🎓 Key Design Decisions

### Decision 1: Single vs Multiple Executions

**Chosen**: Single Execution  
**Rationale**:

- All work is related (test pattern updates)
- Sequential work (file-by-file testing)
- Short duration (3-4 hours)
- Pattern consistency required

**Alternative Considered**: Multiple executions per file  
**Rejected Because**:

- Too much overhead (context switching)
- Pattern inconsistencies risk
- Doesn't save time (can't parallelize)

### Decision 2: Update All Tests vs Just Failing

**Chosen**: Update all failing tests (47)  
**Rationale**:

- Need 100% pass rate for confidence
- Failing tests block refactoring
- Clear completion criteria

**Alternative Considered**: Update only critical tests  
**Rejected Because**:

- Leaves system in partial state
- Doesn't achieve full alignment
- Still have broken tests

### Decision 3: Migration Doc Scope

**Chosen**: Comprehensive guide (~200 lines)  
**Rationale**:

- Prevents future misalignment
- Valuable for new developers
- Documents architectural decision

**Content Included**:

- OLD vs NEW patterns
- Common scenarios
- Anti-patterns
- Quick reference

---

## 🔗 Dependencies

### Prerequisites

**From Previous Achievements**:

- ✅ Achievement 2.5 (Feedback System Codified)
  - APPROVED_XX.md convention established
  - Filesystem-first philosophy documented
- ✅ Achievement 2.6 (Module Integration)
  - is_achievement_complete() in utils.py
  - Function signatures updated
  - Core system working

**Required State**:

- Script functional with feedback system
- 287 tests currently passing
- Feedback system validation tool available

### Downstream Impact

**Enables**:

- Achievement 2.8 (Template Modernization) - same patterns apply
- Achievement 3.x (Polish work) - tests validate improvements
- Future refactoring - safe with 100% test coverage

**Blocks**:

- None (no dependencies on this)

---

## ✅ Definition of Done

### Code Criteria

- [ ] All 47 failing tests updated
- [ ] All tests use filesystem-first patterns
- [ ] Fixtures create feedbacks directories
- [ ] APPROVED_XX.md files created properly
- [ ] Function calls include plan_path parameter
- [ ] No hardcoded markdown parsing for state

### Test Criteria

- [ ] 334 tests passing (100% pass rate)
- [ ] Zero test failures
- [ ] Zero new regressions
- [ ] All modified files pass linter

### Documentation Criteria

- [ ] MIGRATION_NOTES_TEST_MODERNIZATION.md created (~200 lines)
- [ ] OLD vs NEW patterns documented
- [ ] Common scenarios covered
- [ ] Anti-patterns documented
- [ ] Quick reference included

### Quality Criteria

- [ ] Code follows existing patterns
- [ ] Fixtures are reusable
- [ ] Tests are maintainable
- [ ] Documentation is clear

### Completion Criteria

- [ ] EXECUTION_TASK marked complete
- [ ] All deliverables verified
- [ ] Reviewer creates APPROVED_27.md
- [ ] PLAN achievement index updated

---

## 📝 Notes for Executor

### Critical Success Factors

1. **Work File-by-File**: Don't try to fix all at once
2. **Test Incrementally**: Run tests after each file
3. **Pattern Consistency**: Use same patterns across all files
4. **Don't Skip Documentation**: Migration guide is critical

### Common Pitfalls

1. **Forgetting plan_path**: Many functions now require it
2. **Not creating feedbacks dir**: Tests fail if directory missing
3. **Incomplete APPROVED files**: Should have basic content
4. **Assertion confusion**: Some tests may need assertion updates too

### Time Management

- Phase 1 (Audit): 30 min - don't rush, understand patterns
- Phase 2 (Updates): 2-2.5 hours - bulk of work, stay focused
- Phase 3 (Docs): 45 min - don't skimp, this is valuable
- Phase 4 (Validation): 30 min - thorough check, zero tolerance for regressions

### If You Get Stuck

1. Check FEEDBACK_SYSTEM_GUIDE.md for patterns
2. Look at test_plan_parser.py (updated in 2.4)
3. Look at test_utils.py (created in 2.4)
4. Check utils.py for is_achievement_complete() signature
5. Ask for clarification if function signatures unclear

---

**SUBPLAN Status**: ✅ Ready for Execution  
**Estimated Duration**: 3-4 hours  
**Complexity**: Medium (systematic updates, clear patterns)  
**Risk**: Low (well-defined work, clear success criteria)
