# EXECUTION_CASE-STUDY: FIX Feedback Detection Gap in Automated Workflow

**Type**: EXECUTION_CASE-STUDY  
**Created**: 2025-11-13  
**Status**: 🔍 Active Analysis  
**Context**: Achievement 2.7 complete (Test Modernization), discovered gap while working on @GRAPHRAG-OBSERVABILITY-VALIDATION  
**Impact**: HIGH - Affects feedback loop for all achievements requiring fixes

---

## 🎯 Executive Summary

**Issue Discovered**: The automated prompt generation system detects `APPROVED_XX.md` files (achievement complete) but does **NOT** detect `FIX_XX.md` files (achievement needs fixes). This creates a blind spot where the system generates incorrect prompts when reviewer feedback requires fixes.

**Real-World Impact**: During work on Achievement 2.1 of `PLAN_GRAPHRAG-OBSERVABILITY-VALIDATION.md`, a `FIX_21.md` file was created with detailed fix requirements including specific code references (`@Python (779-1075)`, `@Python (873-1075)`). The prompt generation system ignored this file and generated a standard "continue execution" prompt instead of a "address fixes" prompt.

**Root Cause**: The feedback system was designed with a **binary state model** (complete/incomplete) instead of a **tri-state model** (approved/needs_fix/incomplete). The `is_achievement_complete()` function only checks for `APPROVED_XX.md` files.

**Proposed Solution**: Implement tri-state achievement status detection and create a dedicated FIX-specific prompt generator that extracts issues, code references, and action items from `FIX_XX.md` files.

---

## 📋 Background & Context

### Feedback System Overview

The feedback system (Achievement 2.5 in `PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION`) established:

1. **Achievement Index** in PLAN defines structure
2. **Filesystem tracking** via `execution/feedbacks/` files:
   - `APPROVED_XX.md` → Achievement approved ✅
   - `FIX_XX.md` → Achievement needs fixes ⚠️
3. **Single source of truth**: Filesystem, not markdown

### Current Implementation

**File**: `LLM/scripts/generation/utils.py`

```python
def is_achievement_complete(ach_num: str, plan_content: str, plan_path: Path = None) -> bool:
    """
    Check if achievement is complete (FILESYSTEM-ONLY approach).
    
    Detection Logic:
    1. Check if execution/feedbacks/ folder exists
    2. Check if APPROVED_XX.md file exists
    3. Return True if file exists, False otherwise
    """
    if not plan_path:
        return False
    
    plan_folder = plan_path.parent
    feedbacks_folder = plan_folder / "execution" / "feedbacks"
    
    if not feedbacks_folder.exists():
        return False
    
    # Format: "0.1" → "01", "1.2" → "12"
    ach_num_clean = ach_num.replace(".", "")
    approved_file = feedbacks_folder / f"APPROVED_{ach_num_clean}.md"
    
    return approved_file.exists()  # ⚠️ ONLY checks APPROVED, ignores FIX
```

**Problem**: Function returns `False` when `FIX_XX.md` exists (should return a different state).

---

## 🔍 The Problem: Real-World Discovery

### Scenario

**Plan**: `PLAN_GRAPHRAG-OBSERVABILITY-VALIDATION.md`  
**Achievement**: 2.1 - Baseline Pipeline Run Executed  
**Situation**: Achievement 2.1 executed, but reviewer found critical issues

### Filesystem State

```
work-space/plans/GRAPHRAG-OBSERVABILITY-VALIDATION/execution/feedbacks/
├── APPROVED_01.md   ✅
├── APPROVED_02.md   ✅
├── APPROVED_03.md   ✅
├── APPROVED_11.md   ✅
├── APPROVED_12.md   ✅
├── APPROVED_13.md   ✅
├── APPROVED_21.md   ✅ (later created)
├── FIX_21.md        ⚠️ (exists, but IGNORED by system)
└── FIX_21_RESOLUTION.md  📝
```

### FIX_21.md Contents (Excerpt)

```markdown
# FIX REQUIRED: Achievement 2.1

**Status**: ⚠️ **NEEDS FIXES**

## Issues Found

### Critical Issues (must fix)

#### 1. **PRIMARY OBJECTIVE NOT ACHIEVED** ⚠️ BLOCKER

**Code References**:
- @Python (779-1075) - graph_construction.py - Entity resolution logic
- @Python (873-1075) - graph_construction.py - Community detection section

**Fix Required**:
1. Execute pipeline end-to-end with all 3 bug fixes applied
2. Verify all 4 stages complete successfully
3. Complete Phase 3 (Post-execution Analysis)
4. Complete Phase 4 (Documentation - create 3 required documents)

[... detailed fix requirements ...]
```

### What Happened (WRONG)

User ran:
```bash
python LLM/scripts/generation/generate_prompt.py @GRAPHRAG-OBSERVABILITY-VALIDATION --interactive
```

**Expected Behavior**:
- Detect `FIX_21.md` exists
- Generate FIX-specific prompt with:
  - Issues from FIX_21.md
  - Code references (@Python patterns)
  - Step-by-step fix guidance
  - Re-review instructions

**Actual Behavior**:
- System ignored `FIX_21.md`
- Generated standard "continue Achievement 2.1" prompt
- No mention of reviewer feedback
- No code references extracted
- No fix guidance provided

### User Feedback

> "@GRAPHRAG-OBSERVABILITY-VALIDATION I realize that in the case we have a fix the generated prompt is not correct - it did not detected @Python (779-1075) @Python (873-1075)
> 
> This is a case of a not approved execution in which the automated scripts did not recommended the fix. We need to have a prompt and an automation for that."

---

## 📊 System Analysis

### Current State Detection Logic

**File**: `LLM/scripts/generation/workflow_detector.py`

```python
class WorkflowDetector:
    def detect_workflow_state_filesystem(self, plan_path, feature_name, achievement_num):
        """
        Detect workflow state using filesystem structure.
        
        States Returned:
        - no_subplan: SUBPLAN doesn't exist
        - subplan_complete: SUBPLAN marked complete
        - subplan_no_execution: SUBPLAN exists, no EXECUTION files
        - active_execution: Some EXECUTIONs incomplete
        - subplan_all_executed: All EXECUTIONs complete
        
        ⚠️ MISSING: needs_fix state
        """
        # ... detection logic ...
        # ⚠️ Uses is_achievement_complete() which only checks APPROVED
```

### Feedback File Patterns

| File Pattern | Meaning | Current Detection | Should Detect |
|--------------|---------|-------------------|---------------|
| `APPROVED_XX.md` | Achievement approved ✅ | ✅ Yes | ✅ Yes |
| `FIX_XX.md` | Needs fixes ⚠️ | ❌ No | ✅ Yes |
| `FIX_XX_RESOLUTION.md` | Fixes documented 📝 | ❌ No | ⏸️ Optional |
| (neither) | Incomplete | ✅ Yes (default) | ✅ Yes |

### State Model Gap

**Current (Binary)**:
```
Achievement State:
├── Complete (APPROVED_XX.md exists) → Mark done, move to next
└── Incomplete (no APPROVED_XX.md) → Continue work
```

**Needed (Tri-State)**:
```
Achievement State:
├── Approved (APPROVED_XX.md exists) → Mark done, move to next
├── Needs Fix (FIX_XX.md exists, no APPROVED) → Generate FIX prompt
└── Incomplete (neither exists) → Continue work
```

---

## 🎯 Proposed Solution

### Phase 1: Enhance Status Detection

**Replace**: `is_achievement_complete(ach_num, plan_content, plan_path) -> bool`

**With**: `get_achievement_status(ach_num, plan_path) -> str`

**Implementation**:

```python
def get_achievement_status(ach_num: str, plan_path: Path) -> str:
    """
    Get achievement status from filesystem (tri-state).
    
    Args:
        ach_num: Achievement number (e.g., "2.1")
        plan_path: Path to PLAN file
    
    Returns:
        "approved"    - APPROVED_XX.md exists
        "needs_fix"   - FIX_XX.md exists (no APPROVED)
        "incomplete"  - Neither exists
    
    Example:
        >>> get_achievement_status("2.1", plan_path)
        "needs_fix"  # FIX_21.md exists, APPROVED_21.md doesn't
    """
    if not plan_path:
        return "incomplete"
    
    plan_folder = plan_path.parent
    feedbacks_folder = plan_folder / "execution" / "feedbacks"
    
    if not feedbacks_folder.exists():
        return "incomplete"
    
    ach_num_clean = ach_num.replace(".", "")
    approved_file = feedbacks_folder / f"APPROVED_{ach_num_clean}.md"
    fix_file = feedbacks_folder / f"FIX_{ach_num_clean}.md"
    
    # Priority: APPROVED overrides FIX
    if approved_file.exists():
        return "approved"
    elif fix_file.exists():
        return "needs_fix"
    else:
        return "incomplete"
```

**Backward Compatibility**:

```python
def is_achievement_complete(ach_num: str, plan_content: str, plan_path: Path = None) -> bool:
    """Legacy function - calls get_achievement_status() for backward compatibility."""
    status = get_achievement_status(ach_num, plan_path)
    return status == "approved"
```

### Phase 2: Create FIX Prompt Generator

**New Script**: `LLM/scripts/generation/generate_fix_prompt.py`

**Structure**:

```python
#!/usr/bin/env python3
"""Generate prompt to address fixes in FIX_XX.md feedback file."""

from pathlib import Path
from typing import Dict, List, Optional
import re

def extract_fix_issues(fix_file_path: Path) -> Dict[str, any]:
    """
    Extract issues and code references from FIX_XX.md file.
    
    Returns:
        {
            "critical_issues": List[Dict],  # title, impact, fix_required
            "minor_issues": List[Dict],     # title, suggestion
            "code_references": List[str],   # @Python (779-1075), etc.
            "what_worked_well": List[str],  # Positive feedback
            "reviewer": str,
            "review_date": str,
            "status": str
        }
    """
    with open(fix_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {
        "critical_issues": [],
        "minor_issues": [],
        "code_references": [],
        "what_worked_well": [],
        "reviewer": "Unknown",
        "review_date": "Unknown",
        "status": "NEEDS FIXES"
    }
    
    # Extract metadata
    reviewer_match = re.search(r'\*\*Reviewer\*\*:\s*(.+)', content)
    if reviewer_match:
        result["reviewer"] = reviewer_match.group(1).strip()
    
    date_match = re.search(r'\*\*Review Date\*\*:\s*(.+)', content)
    if date_match:
        result["review_date"] = date_match.group(1).strip()
    
    # Extract Critical Issues section
    critical_section = re.search(
        r'### Critical Issues.*?\n(.*?)(?=###|\n---|\Z)', 
        content, 
        re.DOTALL | re.IGNORECASE
    )
    if critical_section:
        critical_text = critical_section.group(1)
        # Parse individual issues (starts with ####)
        issues = re.findall(
            r'####\s+\d+\.\s+\*\*(.+?)\*\*.*?\n\n(.*?)(?=####|\n---|\Z)',
            critical_text,
            re.DOTALL
        )
        for title, body in issues:
            result["critical_issues"].append({
                "title": title.strip(),
                "body": body.strip()
            })
    
    # Extract Minor Issues section
    minor_section = re.search(
        r'### Minor Issues.*?\n(.*?)(?=###|\n---|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    if minor_section:
        minor_text = minor_section.group(1)
        # Parse bullet points
        issues = re.findall(r'^-\s+(.+)$', minor_text, re.MULTILINE)
        result["minor_issues"] = [{"text": issue.strip()} for issue in issues]
    
    # Extract code references (@Python, @file patterns)
    code_refs = re.findall(
        r'@(\w+)\s*\((\d+-\d+)\)',
        content
    )
    for file_type, line_range in code_refs:
        result["code_references"].append(f"@{file_type} ({line_range})")
    
    # Extract "What Worked Well" section
    worked_well_section = re.search(
        r'## What Worked Well.*?\n(.*?)(?=##|\n---|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    if worked_well_section:
        worked_well_text = worked_well_section.group(1)
        items = re.findall(r'^-\s+(.+)$', worked_well_text, re.MULTILINE)
        result["what_worked_well"] = [item.strip() for item in items]
    
    return result


FIX_PROMPT_TEMPLATE = """Address fixes for Achievement {achievement} in @{plan_path}

═══════════════════════════════════════════════════════════════════════

⚠️  REVIEWER FEEDBACK: NEEDS FIXES

Reviewer: {reviewer}
Review Date: {review_date}
Status: {status}
Feedback File: @FIX_{achievement_clean}.md

═══════════════════════════════════════════════════════════════════════

CRITICAL ISSUES TO FIX:

{critical_issues}

═══════════════════════════════════════════════════════════════════════

{minor_issues_section}

═══════════════════════════════════════════════════════════════════════

CODE REFERENCES FROM FEEDBACK:

{code_references}

═══════════════════════════════════════════════════════════════════════

WHAT WORKED WELL (Acknowledged):

{what_worked_well}

═══════════════════════════════════════════════════════════════════════

FIX ACTION PLAN:

Step 1: Review Feedback File
- Read complete feedback: @FIX_{achievement_clean}.md
- Understand all critical and minor issues
- Note code references for investigation

Step 2: Address Critical Issues (REQUIRED)
{critical_action_items}

Step 3: Address Minor Issues (RECOMMENDED)
{minor_action_items}

Step 4: Update EXECUTION_TASK
- Document fixes applied
- Update status to reflect resolution
- Add learning summary about issues

Step 5: Request Re-Review
Create: execution/feedbacks/FIX_{achievement_clean}_RESOLUTION.md

Structure:
```markdown
# FIX RESOLUTION: Achievement {achievement}

**Executor**: [Your name/role]
**Resolution Date**: [Date]
**Status**: ✅ FIXES APPLIED

## Summary

[2-3 sentences on fixes applied]

## Critical Issues Resolved

1. [Issue 1]
   - Fix Applied: [Description]
   - Verification: [How verified]

2. [Issue 2]
   - Fix Applied: [Description]
   - Verification: [How verified]

## Minor Issues Addressed

- [Issue and fix]
- [Issue and fix]

## Verification

- [ ] All critical issues resolved
- [ ] All minor issues addressed or explained
- [ ] Tests passing
- [ ] Deliverables complete
- [ ] Ready for re-review

## Request

Ready for re-review. Please create APPROVED_{achievement_clean}.md if satisfied.
```

═══════════════════════════════════════════════════════════════════════

DO NOT:
❌ Ignore reviewer feedback
❌ Skip critical issues
❌ Assume issues are minor without addressing
❌ Request approval without creating FIX_RESOLUTION

REMEMBER:
✓ Address ALL critical issues (required)
✓ Address or explain ALL minor issues
✓ Update EXECUTION_TASK with learnings
✓ Create FIX_RESOLUTION before requesting re-review
✓ Verify all fixes work as expected

═══════════════════════════════════════════════════════════════════════

Now addressing feedback for Achievement {achievement}...

"""


def generate_fix_prompt(plan_path: Path, achievement_num: str) -> str:
    """
    Generate prompt to address fixes in FIX_XX.md feedback file.
    
    Args:
        plan_path: Path to PLAN file
        achievement_num: Achievement number (e.g., "2.1")
    
    Returns:
        Formatted fix prompt string
    """
    plan_folder = plan_path.parent
    ach_num_clean = achievement_num.replace(".", "")
    fix_file = plan_folder / "execution" / "feedbacks" / f"FIX_{ach_num_clean}.md"
    
    if not fix_file.exists():
        return f"❌ Error: FIX file not found: {fix_file}"
    
    # Extract issues from FIX file
    issues_data = extract_fix_issues(fix_file)
    
    # Format critical issues
    critical_issues_text = ""
    critical_action_items = ""
    for i, issue in enumerate(issues_data["critical_issues"], 1):
        critical_issues_text += f"{i}. **{issue['title']}**\n\n"
        critical_issues_text += f"{issue['body']}\n\n"
        critical_issues_text += "---\n\n"
        
        critical_action_items += f"{i}. Fix: {issue['title']}\n"
    
    if not critical_issues_text:
        critical_issues_text = "(No critical issues specified)\n"
    if not critical_action_items:
        critical_action_items = "(See feedback file for details)\n"
    
    # Format minor issues
    minor_issues_section = ""
    minor_action_items = ""
    if issues_data["minor_issues"]:
        minor_issues_section = "MINOR ISSUES (Should Address):\n\n"
        for i, issue in enumerate(issues_data["minor_issues"], 1):
            minor_issues_section += f"{i}. {issue['text']}\n"
            minor_action_items += f"{i}. {issue['text']}\n"
        minor_issues_section += "\n"
    
    if not minor_action_items:
        minor_action_items = "(None specified)\n"
    
    # Format code references
    code_references_text = ""
    if issues_data["code_references"]:
        for ref in issues_data["code_references"]:
            code_references_text += f"- {ref}\n"
        code_references_text += "\nThese code sections were mentioned in feedback.\n"
        code_references_text += "Review them carefully during fixes.\n"
    else:
        code_references_text = "(No specific code references in feedback)\n"
    
    # Format what worked well
    worked_well_text = ""
    if issues_data["what_worked_well"]:
        for item in issues_data["what_worked_well"]:
            worked_well_text += f"- {item}\n"
    else:
        worked_well_text = "(See feedback file for positive acknowledgments)\n"
    
    # Generate prompt
    prompt = FIX_PROMPT_TEMPLATE.format(
        achievement=achievement_num,
        plan_path=plan_path.name,
        achievement_clean=ach_num_clean,
        reviewer=issues_data["reviewer"],
        review_date=issues_data["review_date"],
        status=issues_data["status"],
        critical_issues=critical_issues_text.strip(),
        minor_issues_section=minor_issues_section.strip(),
        code_references=code_references_text.strip(),
        what_worked_well=worked_well_text.strip(),
        critical_action_items=critical_action_items.strip(),
        minor_action_items=minor_action_items.strip()
    )
    
    return prompt


def main():
    """Main entry point for CLI usage."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description="Generate prompt to address fixes in FIX_XX.md feedback file"
    )
    parser.add_argument("plan_file", help="PLAN file (e.g., @PLAN_FEATURE.md)")
    parser.add_argument("achievement", help="Achievement number (e.g., 2.1)")
    parser.add_argument("--clipboard", action="store_true", help="Copy to clipboard")
    
    args = parser.parse_args()
    
    # Resolve plan path
    from LLM.scripts.generation.utils import resolve_folder_shortcut
    plan_path = resolve_folder_shortcut(args.plan_file)
    
    # Generate prompt
    prompt = generate_fix_prompt(plan_path, args.achievement)
    
    # Output
    print(prompt)
    
    # Clipboard support
    if args.clipboard:
        try:
            import pyperclip
            pyperclip.copy(prompt)
            print("\n✅ Prompt copied to clipboard!")
        except Exception as e:
            print(f"\n⚠️  Clipboard copy failed: {e}")


if __name__ == "__main__":
    main()
```

### Phase 3: Integrate with Main Workflow

**Update**: `LLM/scripts/generation/generate_prompt.py`

```python
def main():
    # ... existing argument parsing ...
    
    # Check achievement status (tri-state)
    from LLM.scripts.generation.utils import get_achievement_status
    status = get_achievement_status(achievement_num, plan_path)
    
    if status == "needs_fix":
        # Generate FIX-specific prompt
        from LLM.scripts.generation.generate_fix_prompt import generate_fix_prompt
        prompt = generate_fix_prompt(plan_path, achievement_num)
        print(prompt)
        
        # Copy to clipboard if requested
        if args.clipboard:
            utils.copy_to_clipboard_safe(prompt)
        
        return  # Exit after FIX prompt
    
    elif status == "approved":
        # Achievement complete, find next
        # ... existing logic ...
    
    else:  # status == "incomplete"
        # Normal execution prompt
        # ... existing logic ...
```

### Phase 4: Update Workflow Detector

**Update**: `LLM/scripts/generation/workflow_detector.py`

```python
class WorkflowDetector:
    def detect_workflow_state_filesystem(self, plan_path, feature_name, achievement_num):
        """Enhanced detection including FIX state."""
        from LLM.scripts.generation.utils import get_achievement_status
        
        # Check achievement status (tri-state)
        status = get_achievement_status(achievement_num, plan_path)
        
        if status == "needs_fix":
            return {
                "state": "needs_fix",
                "recommendation": "address_fixes",
                "fix_file": f"FIX_{achievement_num.replace('.', '')}.md",
                "message": "Reviewer feedback requires fixes before proceeding"
            }
        
        # ... rest of existing logic ...
```

---

## 📈 Expected Impact

### Before (Current System)

| Scenario | Current Behavior | User Experience |
|----------|------------------|-----------------|
| `APPROVED_21.md` exists | ✅ Correct: Move to next achievement | ✅ Good |
| `FIX_21.md` exists (no APPROVED) | ❌ Wrong: Generate continue prompt | ❌ Poor - No guidance |
| Neither exists | ✅ Correct: Continue work | ✅ Good |

### After (Proposed System)

| Scenario | New Behavior | User Experience |
|----------|--------------|-----------------|
| `APPROVED_21.md` exists | ✅ Move to next achievement | ✅ Excellent |
| `FIX_21.md` exists (no APPROVED) | ✅ Generate FIX prompt with issues + code refs | ✅ Excellent - Clear guidance |
| Neither exists | ✅ Continue work | ✅ Excellent |

### Benefits

1. **Automated FIX Detection**: System automatically detects when fixes are needed
2. **Contextual Prompts**: Prompt includes specific issues, code references, action plan
3. **Complete Feedback Loop**: Closes the gap between review and re-execution
4. **Code Reference Extraction**: Automatically extracts `@Python (779-1075)` patterns
5. **Structured Resolution**: Guides executor through fix process with FIX_RESOLUTION template

---

## 🎓 Lessons Learned

### 1. Binary State Models Are Fragile

**Lesson**: Designing systems with binary states (complete/incomplete) is simpler initially but creates gaps when edge cases emerge.

**Pattern**: Real-world workflows have intermediate states:
- Complete (approved) ✅
- Needs revision (fix required) ⚠️
- In progress (incomplete) ⏳

**Recommendation**: Design state models with tri-state or multi-state from the start, even if not all states are initially implemented.

### 2. Feedback Systems Need Closed Loops

**Lesson**: Creating `FIX_XX.md` files is only half the solution. The system must **detect and act** on them to close the feedback loop.

**Pattern**: 
```
Review → Feedback File → Detection → Action Prompt → Resolution → Re-Review
   ↑                                                                      ↓
   └──────────────────────────────────────────────────────────────────────┘
```

**Recommendation**: When designing feedback systems, always implement both **write path** (creating feedback) and **read path** (acting on feedback).

### 3. Discovery Through Real-World Usage

**Lesson**: This gap was discovered during actual workflow usage on a real plan (`@GRAPHRAG-OBSERVABILITY-VALIDATION`), not during initial design or testing.

**Pattern**: Comprehensive testing covers known scenarios, but real-world usage reveals edge cases and workflow gaps.

**Recommendation**: 
- Deploy to real workflows as early as possible
- Expect to discover gaps and iterate
- Document discovered patterns as case studies for future reference

### 4. Code Reference Extraction Is Valuable

**Lesson**: The user specifically mentioned `@Python (779-1075)` and `@Python (873-1075)` as critical references that should be detected and included in prompts.

**Pattern**: Reviewer feedback often includes:
- File references
- Line number ranges
- Function/class names
- Code patterns to fix

**Recommendation**: 
- Standardize code reference patterns (e.g., `@<FileType> (start-end)`)
- Parse and extract these automatically
- Include in generated prompts for easy navigation

### 5. Backward Compatibility During Enhancement

**Lesson**: Changing `is_achievement_complete()` from boolean to tri-state could break existing code that depends on boolean return.

**Solution**: 
- Create new function: `get_achievement_status() -> str` (tri-state)
- Keep old function: `is_achievement_complete() -> bool` (backward compatible wrapper)
- Gradually migrate callers to new function

**Recommendation**: When enhancing core functions, maintain backward compatibility to avoid cascading breaks.

---

## 📋 Implementation Checklist

### Phase 1: Core Status Detection (2-3 hours)

- [ ] Create `get_achievement_status()` function in `utils.py`
- [ ] Test with real feedback directories (APPROVED, FIX, neither)
- [ ] Update `is_achievement_complete()` to use new function (backward compat)
- [ ] Write unit tests for tri-state detection
- [ ] Document function in `FEEDBACK_SYSTEM_GUIDE.md`

### Phase 2: FIX Prompt Generator (3-4 hours)

- [ ] Create `generate_fix_prompt.py` script
- [ ] Implement `extract_fix_issues()` parser
- [ ] Implement code reference extraction (`@Python (X-Y)` patterns)
- [ ] Design FIX_PROMPT_TEMPLATE with action plan
- [ ] Add CLI support (`python generate_fix_prompt.py @PLAN 2.1`)
- [ ] Test with real `FIX_21.md` from GRAPHRAG plan
- [ ] Write unit tests for extraction logic

### Phase 3: Workflow Integration (1-2 hours)

- [ ] Update `generate_prompt.py` main() to check tri-state status
- [ ] Add FIX prompt generation branch
- [ ] Update `workflow_detector.py` to detect "needs_fix" state
- [ ] Update interactive menu to show FIX state
- [ ] Test end-to-end with real FIX file

### Phase 4: Documentation (1 hour)

- [ ] Update `FEEDBACK_SYSTEM_GUIDE.md` with FIX workflow
- [ ] Add FIX_RESOLUTION template to documentation
- [ ] Update `MIGRATION_NOTES_TEST_MODERNIZATION.md` (if relevant)
- [ ] Create example FIX file for testing
- [ ] Document code reference patterns

### Phase 5: Testing & Validation (1 hour)

- [ ] Test with `@GRAPHRAG-OBSERVABILITY-VALIDATION` (real case)
- [ ] Verify code references extracted correctly
- [ ] Test backward compatibility (existing tests still pass)
- [ ] Test interactive mode with FIX state
- [ ] Create integration tests

**Total Estimated Effort**: 8-11 hours (could be single achievement or split into 2)

---

## 🚀 Recommendations

### Immediate Action (Recommended)

**Create Achievement 2.8** in `PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md`:

**Achievement 2.8**: Implement FIX Feedback Detection & Prompt Generation
- **Goal**: Close feedback loop by detecting FIX files and generating fix-specific prompts
- **Priority**: HIGH (blocking current workflow issue)
- **Effort**: 8-11 hours (or split into 2 achievements)
- **Deliverables**:
  1. `get_achievement_status()` tri-state function
  2. `generate_fix_prompt.py` script
  3. Integration with main workflow
  4. Documentation updates
  5. Tests

### Alternative: Hotfix Approach

If immediate fix needed for `@GRAPHRAG-OBSERVABILITY-VALIDATION`:

1. Create simple FIX prompt manually
2. Document as known limitation
3. Address systematically in Achievement 2.8 later

### Long-Term Enhancements

1. **FIX_RESOLUTION Tracking**: Track resolution files and auto-detect when ready for re-review
2. **Multi-Round Fixes**: Handle FIX → RESOLUTION → FIX_V2 → RESOLUTION_V2 workflows
3. **Code Reference Linking**: Generate direct links to code sections
4. **Auto-Generated Checklists**: Extract fix requirements as checklist items
5. **Metrics**: Track fix cycles, common issues, resolution time

---

## 🔗 Related Documentation

- **Feedback System Guide**: `LLM/docs/FEEDBACK_SYSTEM_GUIDE.md`
- **Feedback System Integration**: `work-space/plans/PROMPT-GENERATOR-UX-AND-FOUNDATION/documentation/FEEDBACK_SYSTEM_INTEGRATION.md`
- **Achievement 2.5**: Codify Feedback System Patterns (established conventions)
- **Achievement 2.7**: Test Modernization (where this gap was discovered)
- **Real FIX File**: `work-space/plans/GRAPHRAG-OBSERVABILITY-VALIDATION/execution/feedbacks/FIX_21.md`

---

## 📝 Appendix: Real-World Example

### FIX_21.md Structure (Actual File)

```markdown
# FIX REQUIRED: Achievement 2.1

**Reviewer**: AI Mentor/Code Analyst  
**Review Date**: 2025-11-12  
**Status**: ⚠️ **NEEDS FIXES**

## Summary
Achievement 2.1 has made significant progress but is INCOMPLETE.

## Issues Found

### Critical Issues (must fix)

#### 1. **PRIMARY OBJECTIVE NOT ACHIEVED** ⚠️ BLOCKER
**Code References**:
- @Python (779-1075) - graph_construction.py
- @Python (873-1075) - graph_construction.py

**Fix Required**:
1. Execute pipeline end-to-end
2. Verify all stages complete
3. Complete documentation

#### 2. **REQUIRED DELIVERABLES MISSING** ⚠️ BLOCKER
- Baseline-Performance-Report.md - NOT FOUND
- Baseline-Run-Summary.md - NOT FOUND

### Minor Issues
- EXECUTION_TASK status inaccurate
- Some sections incomplete

## What Worked Well
- Excellent debugging work (3 bugs fixed)
- Clear documentation of issues
```

### Generated FIX Prompt (Expected Output)

```
Address fixes for Achievement 2.1 in @PLAN_GRAPHRAG-OBSERVABILITY-VALIDATION.md

═══════════════════════════════════════════════════════════════════════

⚠️  REVIEWER FEEDBACK: NEEDS FIXES

Reviewer: AI Mentor/Code Analyst
Review Date: 2025-11-12
Status: NEEDS FIXES
Feedback File: @FIX_21.md

═══════════════════════════════════════════════════════════════════════

CRITICAL ISSUES TO FIX:

1. **PRIMARY OBJECTIVE NOT ACHIEVED**

Code References:
- @Python (779-1075) - graph_construction.py
- @Python (873-1075) - graph_construction.py

Fix Required:
1. Execute pipeline end-to-end
2. Verify all stages complete
3. Complete documentation

---

2. **REQUIRED DELIVERABLES MISSING**

- Baseline-Performance-Report.md - NOT FOUND
- Baseline-Run-Summary.md - NOT FOUND

[... rest of formatted prompt with action plan ...]
```

---

**Status**: ✅ Complete  
**Next Steps**: Awaiting decision on implementation approach (Achievement 2.8 vs hotfix)  
**Author**: AI Assistant (Claude Sonnet 4.5)  
**Date**: 2025-11-13


