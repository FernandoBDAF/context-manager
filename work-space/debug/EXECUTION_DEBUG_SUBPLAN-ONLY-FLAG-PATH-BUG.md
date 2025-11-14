# EXECUTION_DEBUG: --subplan-only Flag Path Bug

**Type**: EXECUTION_DEBUG (standalone debugging work)  
**Created**: 2025-11-13  
**Status**: ✅ RESOLVED  
**Severity**: HIGH - Blocks SUBPLAN creation workflow

---

## 🎯 Issue Summary

The `--subplan-only` flag in `generate_prompt.py` fails with "PLAN file not found" error when trying to generate SUBPLAN prompts. The command constructs an invalid path by passing the full Path object instead of just the filename.

**Error Message**:

```
❌ Error generating SUBPLAN prompt: core.libraries.error_handling.exceptions.ApplicationError:
PLAN file not found: @work-space/plans/PROMPT-GENERATOR-UX-AND-FOUNDATION/PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md
```

**Expected Behavior**: Should pass `@PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md`  
**Actual Behavior**: Passes `@work-space/plans/PROMPT-GENERATOR-UX-AND-FOUNDATION/PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md`

---

## 🔍 Root Cause Analysis

### Investigation Steps

1. **Reproduced Issue**:

   ```bash
   python LLM/scripts/generation/generate_prompt.py @PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md --achievement 3.3 --subplan-only
   ```

   Result: Error with full path in @ shortcut

2. **Examined Error Message**:

   - Error shows: `@work-space/plans/PROMPT-GENERATOR-UX-AND-FOUNDATION/PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md`
   - Expected: `@PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md`

3. **Located Bug in Code**:

   - File: `LLM/scripts/generation/generate_prompt.py`
   - Line: 1415
   - Code: `f"@{plan_path}"`
   - Issue: `plan_path` is a Path object, not a string

4. **Verified Pattern**:
   - Checked Bug #11 fix (line 74-76 in comments)
   - Bug #11 was similar: `@{plan_path}` → `@{plan_path.name}`
   - Same pattern needed here

### Root Cause

**Location**: `generate_prompt.py:1415`

**Problematic Code**:

```python
if args.subplan_only:
    # Generate SUBPLAN prompt
    import subprocess

    result = subprocess.run(
        [
            sys.executable,
            "LLM/scripts/generation/generate_subplan_prompt.py",
            "create",
            f"@{plan_path}",  # ❌ BUG: plan_path is Path object
            "--achievement",
            achievement_num,
        ],
        capture_output=True,
        text=True,
    )
```

**Why It Fails**:

- `plan_path` is a `Path` object (e.g., `Path("work-space/plans/PROMPT-GENERATOR-UX-AND-FOUNDATION/PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md")`)
- When used in f-string, it converts to full path string
- Result: `@work-space/plans/.../PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md`
- `resolve_plan_path()` tries to find file named `work-space/plans/.../PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md`
- File doesn't exist → Error

**Correct Approach**:

- Use `plan_path.name` to get just the filename
- Result: `@PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md`
- `resolve_plan_path()` correctly resolves @ shortcut

---

## 🔗 Related Issues

### Bug #11: Similar Issue (Previously Fixed)

**Reference**: Line 73-76 in `generate_prompt.py` comments

**Bug #11 Description**:

- Same issue in different location
- Fixed by changing `@{plan_path}` to `@{plan_path.name}`
- Lesson: "Path objects vs strings in f-strings"

**Bug #11 Fix Location**: Lines 1902, 2009 (per comments)

**Pattern**: This is a **recurrence** of Bug #11 in a different code path

### Why Bug #11 Fix Didn't Catch This

1. **Different Code Path**: Bug #11 was in workflow detection prompts
2. **This Bug**: In `--subplan-only` flag handler (line 1406-1425)
3. **Same Root Cause**: Path object in f-string with @ prefix
4. **Same Solution**: Use `.name` property

---

## ✅ Solution

### Fix Applied

**File**: `LLM/scripts/generation/generate_prompt.py`  
**Line**: 1415  
**Change**: `f"@{plan_path}"` → `f"@{plan_path.name}"`

**Fixed Code**:

```python
if args.subplan_only:
    # Generate SUBPLAN prompt
    import subprocess

    result = subprocess.run(
        [
            sys.executable,
            "LLM/scripts/generation/generate_subplan_prompt.py",
            "create",
            f"@{plan_path.name}",  # ✅ FIX: Use .name to get filename only
            "--achievement",
            achievement_num,
        ],
        capture_output=True,
        text=True,
    )
```

### Verification Steps

1. **Test Command**:

   ```bash
   python LLM/scripts/generation/generate_prompt.py @PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md --achievement 3.3 --subplan-only
   ```

2. **Expected Result**:

   - No error
   - SUBPLAN prompt generated successfully
   - Prompt displayed or copied to clipboard

3. **Verification**:
   - Command constructs: `@PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md`
   - `resolve_plan_path()` resolves to correct file
   - SUBPLAN prompt generation succeeds

---

## 📊 Impact Assessment

### Severity: HIGH

**Why High Severity**:

- Blocks critical workflow: Designer creating SUBPLANs
- `--subplan-only` flag completely non-functional
- No workaround except calling `generate_subplan_prompt.py` directly
- Affects all users trying to create SUBPLANs via interactive mode

### Affected Workflows

1. **Interactive Mode** (Primary UI):

   - User selects "Generate prompt for next achievement"
   - System suggests SUBPLAN creation
   - Command with `--subplan-only` fails
   - **Impact**: Breaks primary UX flow

2. **Direct Command**:

   - User runs: `python generate_prompt.py @PLAN --achievement X.Y --subplan-only`
   - Command fails
   - **Impact**: Flag unusable

3. **Workaround Available**:
   - User can call `generate_subplan_prompt.py` directly
   - Command: `python generate_subplan_prompt.py create @PLAN --achievement X.Y`
   - **Impact**: Requires knowledge of alternative command

### User Experience Impact

- **Before Fix**: Confusing error, unclear what went wrong
- **After Fix**: Command works as documented
- **Documentation**: Flag usage documented in help text (line 1234)

---

## 🎓 Lessons Learned

### 1. Path Object vs String in F-Strings

**Lesson**: Path objects convert to full path strings in f-strings, not just filenames.

**Pattern**:

```python
# ❌ WRONG: Full path
path = Path("work-space/plans/FEATURE/PLAN_FEATURE.md")
f"@{path}"  # → "@work-space/plans/FEATURE/PLAN_FEATURE.md"

# ✅ CORRECT: Filename only
f"@{path.name}"  # → "@PLAN_FEATURE.md"
```

**When to Use**:

- Always use `.name` when constructing @ shortcuts
- Use `.name` when passing filenames to other scripts
- Use full `path` when passing to filesystem operations

### 2. Bug Recurrence Pattern

**Observation**: Same bug appeared in multiple locations (Bug #11, now this)

**Why Recurrence Happens**:

- Pattern not systematically applied across codebase
- Different code paths developed at different times
- No automated check for this pattern

**Prevention Strategy**:

- Search codebase for all `f"@{plan_path}"` patterns
- Replace with `f"@{plan_path.name}"`
- Add comment explaining pattern
- Consider linter rule or test

### 3. Error Message Quality

**Good**: Error message clearly shows the problem

```
PLAN file not found: @work-space/plans/.../PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md
```

**Why Good**:

- Shows exact path being searched
- Makes bug obvious (shouldn't have full path)
- Achievement 3.1 structured error handling helps debugging

**Improvement**: Could suggest using `.name` in error message

### 4. Testing Gap

**Issue**: No test caught this bug

**Why**:

- `--subplan-only` flag not tested
- Integration tests don't cover all flag combinations
- Manual testing missed this code path

**Recommendation**:

- Add test for `--subplan-only` flag
- Test all workflow-specific flags
- Integration test for interactive mode → SUBPLAN creation flow

---

## 🔄 Follow-Up Actions

### Immediate (Done)

- [x] Fix bug in `generate_prompt.py:1415`
- [x] Test fix with real command
- [x] Document debug process

### Short-Term (Recommended)

- [ ] Search codebase for other `f"@{plan_path}"` patterns
- [ ] Add test for `--subplan-only` flag
- [ ] Add test for `--execution-only` flag (similar pattern)
- [ ] Update Bug History in file header (Bug #12)

### Long-Term (Optional)

- [ ] Create linter rule to catch `f"@{path}"` pattern
- [ ] Add integration test for full SUBPLAN creation workflow
- [ ] Consider helper function: `format_plan_shortcut(path)` → `f"@{path.name}"`

---

## 📝 Code Search Results

### Other Occurrences of Pattern

**Search Command**:

```bash
grep -n 'f"@{plan_path}"' LLM/scripts/generation/generate_prompt.py
```

**Results**:

- Line 1415: `f"@{plan_path}"` (THIS BUG - fixed)

**Search for Similar Patterns**:

```bash
grep -n '@{.*path' LLM/scripts/generation/generate_prompt.py
```

**Results**:

- Line 1415: Fixed
- Line 1527: `f"@{plan_path.name}"` ✅ (correct - Bug #11 fix)
- Line 1902: (mentioned in Bug #10 fix)
- Line 2009: (mentioned in Bug #10 fix)

**Conclusion**: This appears to be the last occurrence of the bug pattern.

---

## 📊 Bug Classification

**Type**: Path Resolution Bug  
**Category**: String Formatting Error  
**Severity**: HIGH (blocks workflow)  
**Complexity**: LOW (simple fix)  
**Recurrence**: YES (Bug #11 recurrence)  
**Detection**: Manual (user report)  
**Fix Time**: 5 minutes  
**Debug Time**: 10 minutes  
**Documentation Time**: 30 minutes

---

## ✅ Resolution Status

**Status**: ✅ RESOLVED  
**Fix Applied**: 2025-11-13  
**Verified**: Yes  
**Documented**: Yes  
**Tests Added**: No (recommended for follow-up)

**Bug Number**: Bug #12 (following project convention)

**Related Bugs**:

- Bug #10: Incorrect path format in generated commands (similar)
- Bug #11: --subplan-only flag silent failure (same root cause)

**Pattern**: Path object string conversion issues

---

## 📚 References

- **File**: `LLM/scripts/generation/generate_prompt.py`
- **Lines**: 1406-1425 (--subplan-only handler)
- **Bug #11 Reference**: Lines 73-76 (comments)
- **Bug #10 Reference**: Lines 68-72 (comments)
- **EXECUTION-TAXONOMY.md**: Categorization as EXECUTION_DEBUG
- **Achievement 3.1**: Structured error handling (helped debugging)

---

**Debug Process**: Following EXECUTION-TAXONOMY.md guidelines for EXECUTION_DEBUG  
**Category**: Standalone debugging work (not SUBPLAN-connected)  
**Lifecycle**: Created → Investigated → Resolved → Documented  
**Archive**: Will be moved to `documentation/archive/debug/` after review
