# State Tracking Philosophy

**Date**: 2025-11-11  
**Context**: Achievement 2.1 - Extract Interactive Menu Module  
**Related Changes**: Filesystem-first state tracking implementation

---

## 🎯 Core Philosophy

**Single Responsibility Principle for State Tracking**:

1. **PLAN's ONLY Responsibility**: Define the Achievement Index

   - List all achievements in the plan
   - Provide sequence and structure
   - NO completion status tracking

2. **Filesystem's Responsibility**: Track all state
   - Completion: `APPROVED_XX.md` files in `execution/feedbacks/`
   - Work in progress: SUBPLANs, EXECUTION_TASKs
   - NO markdown parsing for state

---

## 📋 Achievement Index

**Location**: `## 📋 Achievement Index` section in PLAN

**Purpose**:

- Single source of truth for what achievements exist
- Enables scripts to detect all achievements without parsing full PLAN
- Shows progress at a glance (✅ = completed via APPROVED feedback)

**Example**:

```markdown
## 📋 Achievement Index

**All Achievements in This Plan** (for sequence reference):

**Priority 0: IMMEDIATE IMPACT (COMPLETE ✅)**

- ✅ Achievement 0.1: @folder Shortcut Support
- ✅ Achievement 0.2: Clipboard Default (--clipboard flag)
- ✅ Achievement 0.3: Interactive Mode as Primary UI

**Priority 1: FOUNDATION (MOSTLY COMPLETE)**

- ✅ Achievement 1.1: Critical Path Tests (Core Parsing)
- ✅ Achievement 1.2: Comprehensive Documentation
- ✅ Achievement 1.3: Complete Test Coverage (90%)

**Priority 2: ARCHITECTURE (HIGH - Structured Foundation)**

- Achievement 2.1: Extract Interactive Menu Module
- Achievement 2.2: Extract Workflow Detection Module
```

**Note**: The ✅ markers in the Index are VISUAL ONLY for human readers. Scripts ignore them and check the filesystem.

---

## 📁 Filesystem State Tracking

### Completion Tracking

**Location**: `[plan-folder]/execution/feedbacks/`

**Files**:

- `APPROVED_XX.md` - Achievement approved and complete
- `FIX_XX.md` - Achievement needs fixes (not used for completion detection)

**Naming Convention**:

- Achievement 1.1 → `APPROVED_11.md`
- Achievement 2.1 → `APPROVED_21.md`
- Achievement 10.3 → `APPROVED_103.md`

**Detection Logic**:

```python
def is_achievement_complete(ach_num: str, plan_path: Path) -> bool:
    """Check if APPROVED_XX.md exists (FILESYSTEM-ONLY)."""
    feedbacks_folder = plan_path.parent / "execution" / "feedbacks"
    ach_filename = ach_num.replace(".", "")  # "2.1" -> "21"
    approved_file = feedbacks_folder / f"APPROVED_{ach_filename}.md"
    return approved_file.exists()
```

**No Fallback**: If `APPROVED_XX.md` doesn't exist, achievement is NOT complete. Period.

### Work in Progress Tracking

**Locations**:

- `[plan-folder]/subplans/` - SUBPLANs for achievements
- `[plan-folder]/execution/` - EXECUTION_TASKs for achievements

**Detection Logic**:

- SUBPLAN exists → Design phase complete
- EXECUTION_TASK exists → Implementation in progress
- All EXECUTION_TASKs marked complete → Awaiting review
- APPROVED file exists → Achievement complete

---

## ⚠️ Conflict Detection

**Philosophy**: Conflicts ONLY occur when Achievement Index and filesystem disagree.

### Conflict Type 1: Achievement Not in Index

**Scenario**: Filesystem has `APPROVED_21.md` but Achievement 2.1 is not in the Index.

**Likely Cause**:

- Achievement was completed but not added to Index
- Index was updated but old APPROVED file remains

**Resolution**:

- Add Achievement 2.1 to the Achievement Index section, OR
- Remove `APPROVED_21.md` if it's obsolete

### Conflict Type 2: Orphaned Work

**Scenario**: Filesystem has `SUBPLAN_FEATURE_21.md` but Achievement 2.1 is not in the Index.

**Likely Cause**:

- SUBPLAN was created but achievement was removed from Index
- Index was updated but old SUBPLAN remains

**Resolution**:

- Add Achievement 2.1 to the Achievement Index, OR
- Archive `SUBPLAN_FEATURE_21.md` if obsolete

### What's NOT a Conflict Anymore

**Removed Conflict Types** (no longer detected):

1. ~~PLAN handoff section staleness~~ - Not filesystem's concern
2. ~~Completion status mismatches~~ - Filesystem is source of truth
3. ~~Work state conflicts~~ - Filesystem determines state

**Rationale**: The PLAN's handoff section is for HUMAN communication. Scripts should ONLY rely on:

1. Achievement Index (what achievements exist)
2. Filesystem (what's complete, what's in progress)

---

## 🔄 Workflow States

**Detected from Filesystem** (not PLAN markdown):

1. **no_subplan**: SUBPLAN doesn't exist → Create SUBPLAN
2. **subplan_no_execution**: SUBPLAN exists, no EXECUTION files → Create EXECUTION
3. **active_execution**: Some EXECUTIONs incomplete → Continue or create next
4. **subplan_all_executed**: All EXECUTIONs complete, no APPROVED → **Awaiting review** (normal state)
5. **achievement_complete**: APPROVED file exists → Next achievement

**Key Insight**: `subplan_all_executed` without `APPROVED_XX.md` is a **normal workflow state**, not a conflict. It means work is done and awaiting review.

---

## 🎓 Benefits

1. **Simplicity**: One source of truth for each concern

   - Index = what exists
   - Filesystem = what's done

2. **Reliability**: No markdown parsing fragility

   - File exists = True
   - File doesn't exist = False

3. **Clarity**: Clear separation of responsibilities

   - PLAN = human communication + achievement list
   - Filesystem = machine state

4. **Flexibility**: PLAN can be updated without breaking state
   - Handoff section can change freely
   - Only Achievement Index matters for scripts

---

## 📝 Migration Notes

**For Existing Plans**:

1. Add Achievement Index section if missing
2. Create `execution/feedbacks/` folder
3. Create `APPROVED_XX.md` files for completed achievements
4. Update scripts to use filesystem-first detection

**For New Plans**:

1. Include Achievement Index from the start
2. Create folder structure: `subplans/`, `execution/`, `execution/feedbacks/`, `documentation/`
3. Follow naming conventions for all files

---

## 🔗 Related Documents

- **PLAN**: `PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md`
- **SUBPLAN**: `SUBPLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION_21.md`
- **EXECUTION_TASK**: `EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_21_01.md`
- **Migration Notes**: `MIGRATION_NOTES_INTERACTIVE_MENU_EXTRACTION.md`

---

**Status**: ✅ Implemented in Achievement 2.1  
**Last Updated**: 2025-11-11
