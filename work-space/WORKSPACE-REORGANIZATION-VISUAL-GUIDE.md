# Work-Space Reorganization: Visual Guide

**Date**: November 15, 2025  
**Purpose**: Visual representation of current issues and proposed fixes  
**Companion to**: WORKSPACE-STRUCTURE-REVIEW-2025-11-15.md

---

## 🎯 The Big Picture

### Current State ❌

```
work-space/
├── subplans/                           ❌ FLAT - 32 orphaned SUBPLANs
│   ├── SUBPLAN_METHODOLOGY-V2_31.md
│   ├── SUBPLAN_RESTORE-EXECUTION_15.md
│   └── ... (30 more)
│
├── execution/                          ❌ FLAT - 6 orphaned EXECUTION_TASKs
│   ├── EXECUTION_TASK_OBSERVABILITY_62_01.md
│   └── ... (5 more)
│
├── analyses/                           ⚠️ OVER-SUBDIVIDED - 12 subdirs
│   ├── archiving-system/
│   ├── coordination/
│   ├── implementation_automation/
│   └── ... (9 more subdirs + 28 root files)
│
├── plans/
│   ├── a_paused/                       ⚠️ Prefix naming
│   ├── a_real-use-cases/               ⚠️ Prefix naming
│   ├── LLM-DASHBOARD-CLI/              ✅ Good structure
│   └── PARALLEL-EXECUTION-AUTOMATION/  ✅ Good structure
│
├── work-space/                         ❌ DUPLICATE nested directory
│   └── plans/
│
└── archive/                            ⚠️ Wrong location (should be in documentation/)
```

### Target State ✅

```
work-space/
├── north-stars/                        ✅ Strategic vision docs
│   └── NORTH_STAR_*.md
│
├── grammaplans/                        ✅ Strategic coordination
│   └── GRAMMAPLAN_*.md
│
├── plans/                              ✅ Nested PLAN structure
│   ├── PLAN-NAME-1/
│   │   ├── PLAN_FEATURE.md
│   │   ├── subplans/                   ✅ SUBPLANs nested here
│   │   │   ├── SUBPLAN_FEATURE_01.md
│   │   │   └── SUBPLAN_FEATURE_02.md
│   │   ├── execution/                  ✅ EXECUTIONs nested here
│   │   │   ├── EXECUTION_TASK_FEATURE_01_01.md
│   │   │   └── feedbacks/
│   │   │       └── APPROVED_01.md
│   │   └── documentation/
│   │       └── *.md
│   │
│   └── PLAN-NAME-2/
│       └── [same structure]
│
├── analyses/                           ✅ Flat structure
│   ├── EXECUTION_ANALYSIS_TOPIC-1.md
│   ├── EXECUTION_ANALYSIS_TOPIC-2.md
│   └── ... (all 125 files at root)
│
├── case-studies/                       ✅ Flat structure
│   └── EXECUTION_CASE-STUDY_*.md
│
├── observations/                       ✅ Flat structure
│   └── EXECUTION_OBSERVATION_*.md
│
├── debug-logs/                         ✅ Flat structure (debug/ removed)
│   └── EXECUTION_DEBUG_*.md
│
├── reviews/                            ✅ Flat structure
│   └── EXECUTION_REVIEW_*.md
│
├── knowledge/                          ❓ To be reclassified and removed
│
├── backlog-plans/                      ✅ Future work
│   └── GRAMMAPLAN_*.md
│
└── README.md                           ✅ Workspace guide
```

---

## 🔍 Issue #1: Orphaned SUBPLANs (32 files)

### Current Problem

**7 PLANs have SUBPLANs scattered in flat `/subplans/` folder:**

```
work-space/
├── subplans/                                    ❌ Flat directory
│   ├── SUBPLAN_METHODOLOGY-V2-ENHANCEMENTS_31.md
│   ├── SUBPLAN_METHODOLOGY-V2-ENHANCEMENTS_21.md
│   ├── SUBPLAN_METHODOLOGY-V2-ENHANCEMENTS_11.md
│   ├── SUBPLAN_RESTORE-EXECUTION-..._15.md
│   ├── SUBPLAN_RESTORE-EXECUTION-..._14.md
│   └── ... (27 more)
│
└── plans/
    ├── a_paused/
    │   ├── METHODOLOGY-HIERARCHY-EVOLUTION/     ❌ SUBPLANs not here!
    │   │   └── PLAN_METHODOLOGY-...md
    │   └── EXECUTION-ANALYSIS-INTEGRATION-RESTRUCTURING/
    │       └── PLAN_EXECUTION-...md
    └── ... (other plans)
```

### Why This is a Problem

1. **Discoverability**: Can't see which SUBPLANs belong to which PLAN
2. **Navigation**: Have to search across folders to find related files
3. **Context**: SUBPLANs separated from their parent PLAN context
4. **Automation**: Scripts can't find SUBPLANs by PLAN relationship
5. **Methodology**: Violates nested structure principle

### The Fix

**Move SUBPLANs to parent PLAN directories:**

```
work-space/plans/
├── METHODOLOGY-V2-ENHANCEMENTS/          (create if doesn't exist)
│   ├── PLAN_METHODOLOGY-V2-ENHANCEMENTS.md
│   └── subplans/                         ✅ Create subplans/ directory
│       ├── SUBPLAN_METHODOLOGY-V2-ENHANCEMENTS_01.md  ← MOVE HERE
│       ├── SUBPLAN_METHODOLOGY-V2-ENHANCEMENTS_11.md  ← MOVE HERE
│       ├── SUBPLAN_METHODOLOGY-V2-ENHANCEMENTS_21.md  ← MOVE HERE
│       ├── SUBPLAN_METHODOLOGY-V2-ENHANCEMENTS_31.md  ← MOVE HERE
│       ├── SUBPLAN_METHODOLOGY-V2-ENHANCEMENTS_41.md  ← MOVE HERE
│       └── SUBPLAN_METHODOLOGY-V2-ENHANCEMENTS_51.md  ← MOVE HERE
│
└── RESTORE-EXECUTION-WORKFLOW-AUTOMATION/
    ├── PLAN_RESTORE-EXECUTION-WORKFLOW-AUTOMATION.md
    └── subplans/
        ├── SUBPLAN_RESTORE-EXECUTION-..._14.md  ← MOVE HERE
        └── SUBPLAN_RESTORE-EXECUTION-..._15.md  ← MOVE HERE
```

**Result**: `/work-space/subplans/` becomes empty and can be removed

---

## 🔍 Issue #2: Orphaned EXECUTION_TASKs (6 files)

### Current Problem

**EXECUTION_TASKs in flat `/execution/` folder instead of nested with PLAN:**

```
work-space/
├── execution/                                   ❌ Flat directory
│   ├── EXECUTION_TASK_OBSERVABILITY-VALIDATION_62_01.md
│   ├── EXECUTION_TASK_GRAPHRAG-OBSERVABILITY-VALIDATION_61_01.md
│   ├── EXECUTION_TASK_GRAPHRAG-OBSERVABILITY-VALIDATION_63_01.md
│   ├── EXECUTION_TASK_GRAPHRAG-OBSERVABILITY-VALIDATION_71_01.md
│   └── ... (2 more)
│
└── plans/
    └── a_real-use-cases/
        └── GRAPHRAG-OBSERVABILITY-VALIDATION/   ❌ EXECUTIONs not here!
            ├── PLAN_GRAPHRAG-OBSERVABILITY-VALIDATION.md
            └── execution/                       ✅ Should be here but has feedbacks only
                └── feedbacks/
                    └── APPROVED_*.md
```

### Why This is a Problem

1. **Feedback System**: Can't find EXECUTION_TASKs for feedback approval
2. **Achievement Tracking**: Disconnect between achievement and execution
3. **Context Loss**: EXECUTION_TASKs separated from SUBPLAN context
4. **Archiving**: Can't archive PLAN with all related executions
5. **Methodology**: Violates nested structure for EXECUTION_TASKs

### The Fix

**Move EXECUTION_TASKs to parent PLAN execution/ directories:**

```
work-space/plans/a_real-use-cases/
└── GRAPHRAG-OBSERVABILITY-VALIDATION/
    ├── PLAN_GRAPHRAG-OBSERVABILITY-VALIDATION.md
    ├── subplans/
    │   ├── SUBPLAN_..._61.md
    │   ├── SUBPLAN_..._62.md
    │   └── SUBPLAN_..._63.md
    └── execution/                              ✅ Move EXECUTION_TASKs here
        ├── EXECUTION_TASK_GRAPHRAG-OBSERVABILITY-VALIDATION_61_01.md  ← MOVE HERE
        ├── EXECUTION_TASK_GRAPHRAG-OBSERVABILITY-VALIDATION_62_01.md  ← MOVE HERE
        ├── EXECUTION_TASK_GRAPHRAG-OBSERVABILITY-VALIDATION_63_01.md  ← MOVE HERE
        ├── EXECUTION_TASK_GRAPHRAG-OBSERVABILITY-VALIDATION_71_01.md  ← MOVE HERE
        └── feedbacks/
            ├── APPROVED_61.md
            ├── APPROVED_62.md
            └── APPROVED_63.md
```

**Result**: `/work-space/execution/` becomes empty (or contains only EXECUTION_WORK docs) and can be removed

---

## 🔍 Issue #3: Analyses Over-Subdivision (125 files, 12 subdirs)

### Current Problem

**Analyses folder has 12 subdirectories + 28 root files:**

```
work-space/analyses/
├── archiving-system/                   [6 files]
│   ├── EXECUTION_ANALYSIS_ARCHIVE-AUTOMATION.md
│   ├── EXECUTION_ANALYSIS_ARCHIVE-STRUCTURE.md
│   └── ...
│
├── coordination/                       [10 files]
│   ├── EXECUTION_ANALYSIS_MULTI-PLAN-COORDINATION.md
│   └── ...
│
├── implementation_automation/          [26 files]  ← Largest subdir
│   ├── EXECUTION_ANALYSIS_PROMPT-AUTOMATION.md
│   ├── EXECUTION_ANALYSIS_VALIDATION-SCRIPTS.md
│   └── ...
│
├── methodology-evolution/              [11 files]
│   └── ...
│
├── graphrag-domain/                    [6 files]
│   └── ...
│
├── quality-validation/                 [8 files]
│   └── ...
│
└── ... (6 more subdirs)
│
└── [28 files at root]
```

### Why This is a Problem

1. **Discovery**: Have to check 12 folders to find analyses
2. **Inconsistency**: Some analyses at root, some in subdirs
3. **Categorization**: Overlap between categories (e.g., automation vs. methodology)
4. **Search**: Can't easily list all analyses
5. **Methodology**: Violates flat structure for EXECUTION_ANALYSIS

### The Fix

**Flatten to single directory:**

```
work-space/analyses/
├── EXECUTION_ANALYSIS_ARCHIVE-AUTOMATION.md              ← From archiving-system/
├── EXECUTION_ANALYSIS_ARCHIVE-STRUCTURE.md               ← From archiving-system/
├── EXECUTION_ANALYSIS_MULTI-PLAN-COORDINATION.md         ← From coordination/
├── EXECUTION_ANALYSIS_PROMPT-AUTOMATION.md               ← From implementation_automation/
├── EXECUTION_ANALYSIS_VALIDATION-SCRIPTS.md              ← From implementation_automation/
├── EXECUTION_ANALYSIS_METHODOLOGY-HIERARCHY.md           ← From methodology-evolution/
├── EXECUTION_ANALYSIS_GRAPHRAG-VALIDATION.md             ← From graphrag-domain/
├── EXECUTION_ANALYSIS_TEST-COVERAGE.md                   ← From quality-validation/
└── ... (all 125 files at root level)
```

**Optional**: Create INDEX.md with categorization metadata:

```markdown
# Analyses Index

## By Category

### Archiving & Organization (18 files)
- EXECUTION_ANALYSIS_ARCHIVE-AUTOMATION.md
- EXECUTION_ANALYSIS_ARCHIVE-STRUCTURE.md
- ...

### Automation & Tooling (26 files)
- EXECUTION_ANALYSIS_PROMPT-AUTOMATION.md
- EXECUTION_ANALYSIS_VALIDATION-SCRIPTS.md
- ...

### Methodology Evolution (11 files)
- ...
```

**Result**: Single flat directory with optional index for categorization

---

## 🔍 Issue #4: Duplicate Debug Folders

### Current Problem

**Both `debug/` and `debug-logs/` exist:**

```
work-space/
├── debug/          [14 files]  ❌ Non-standard name
└── debug-logs/     [14 files]  ✅ Methodology-compliant name
```

### Why This is a Problem

1. **Confusion**: Which folder to use for new debug documents?
2. **Duplication**: Possible duplicate content or split information
3. **Methodology**: Only `debug-logs/` is documented in methodology
4. **Discovery**: Have to check two folders

### The Fix

**Consolidate to single folder:**

```
work-space/
└── debug-logs/     [28 files]  ✅ All debug docs here
    ├── EXECUTION_DEBUG_ISSUE-1.md    ← From debug/
    ├── EXECUTION_DEBUG_ISSUE-2.md    ← From debug/
    ├── EXECUTION_DEBUG_ISSUE-3.md    ← From debug-logs/
    └── ... (all 28 files)
```

**Result**: Remove `debug/` folder, all debug documents in `debug-logs/`

---

## 🔍 Issue #5: Nested work-space/work-space/

### Current Problem

**Duplicate nested directory:**

```
work-space/
└── work-space/         ❌ Duplicate!
    └── plans/
        └── ... (files?)
```

### Why This is a Problem

1. **Confusion**: Unclear which work-space is "real"
2. **Errors**: Easy to navigate to wrong directory
3. **Clutter**: Takes up space in listings
4. **Bugs**: Possible result of path construction error

### The Fix

**Remove nested directory:**

```bash
# 1. Check for important files
find work-space/work-space -type f

# 2. If files exist, move to correct location
# (Based on content/type)

# 3. Remove nested directory
rm -rf work-space/work-space
```

**Result**: Only one `work-space/` directory exists

---

## 🔍 Issue #6: PLAN Naming Inconsistency

### Current Problem

**Mixed naming conventions for PLAN organization:**

```
work-space/plans/
├── a_paused/                           ⚠️ Prefix for status
│   ├── EXECUTION-ANALYSIS-INTEGRATION-RESTRUCTURING/
│   ├── METHODOLOGY-HIERARCHY-EVOLUTION/
│   └── ... (10+ PLANs)
│
├── a_real-use-cases/                   ⚠️ Prefix for category
│   ├── GRAPHRAG-OBSERVABILITY-VALIDATION/
│   ├── ENTITY-RESOLUTION-REFACTOR/
│   └── ... (11 PLANs)
│
├── LLM-DASHBOARD-CLI/                  ✅ Direct name
├── PARALLEL-EXECUTION-AUTOMATION/      ✅ Direct name
└── PROMPT-GENERATOR-UX-AND-FOUNDATION/ ✅ Direct name
```

### Why This is a Problem

1. **Inconsistency**: Three different organizational approaches
2. **Sorting**: Prefixes (`a_`) force artificial ordering
3. **Automation**: Hard to distinguish status from name
4. **Metadata**: Status should be in metadata, not directory name
5. **Scale**: What happens with more statuses? (`a_paused`, `b_blocked`, `c_complete`?)

### The Fix (Recommended: Flatten + Metadata)

**Remove prefixes, use consistent structure:**

```
work-space/plans/
├── EXECUTION-ANALYSIS-INTEGRATION-RESTRUCTURING/
│   ├── PLAN_EXECUTION-ANALYSIS-INTEGRATION-RESTRUCTURING.md
│   │   [metadata: status: paused, category: methodology]
│   └── ...
│
├── METHODOLOGY-HIERARCHY-EVOLUTION/
│   ├── PLAN_METHODOLOGY-HIERARCHY-EVOLUTION.md
│   │   [metadata: status: paused, category: methodology]
│   └── ...
│
├── GRAPHRAG-OBSERVABILITY-VALIDATION/
│   ├── PLAN_GRAPHRAG-OBSERVABILITY-VALIDATION.md
│   │   [metadata: status: active, category: real-use-case]
│   └── ...
│
├── LLM-DASHBOARD-CLI/
│   └── [metadata: status: active, category: tooling]
│
└── PARALLEL-EXECUTION-AUTOMATION/
    └── [metadata: status: active, category: methodology]
```

**Metadata in PLAN front matter:**

```markdown
---
type: PLAN
status: paused
category: methodology
priority: 2
---
# PLAN: Methodology Hierarchy Evolution
```

**Alternative: Subdirectories by Status**

```
work-space/plans/
├── active/
│   ├── LLM-DASHBOARD-CLI/
│   └── PARALLEL-EXECUTION-AUTOMATION/
│
├── paused/
│   ├── EXECUTION-ANALYSIS-INTEGRATION-RESTRUCTURING/
│   └── METHODOLOGY-HIERARCHY-EVOLUTION/
│
└── completed/
    └── (archived PLANs before moving to documentation/archive/)
```

**Recommendation**: Use metadata (Option 1) for consistency with methodology's metadata tag approach

---

## 📋 Migration Checklist

### Phase 1: Critical Structure (Week 1)

**Day 1-2: SUBPLANs Migration**
- [ ] List all 32 SUBPLANs in `/work-space/subplans/`
- [ ] For each SUBPLAN:
  - [ ] Extract PLAN name from filename
  - [ ] Find or create `plans/<PLAN>/subplans/` directory
  - [ ] Move SUBPLAN file
  - [ ] Update any references in PLAN document
- [ ] Verify all SUBPLANs moved (count should be 0 in flat folder)
- [ ] Remove `/work-space/subplans/` directory

**Day 3: EXECUTION_TASKs Migration**
- [ ] List all 6 EXECUTION_TASKs in `/work-space/execution/`
- [ ] For each EXECUTION_TASK:
  - [ ] Extract PLAN name from filename
  - [ ] Find or create `plans/<PLAN>/execution/` directory
  - [ ] Move EXECUTION_TASK file
  - [ ] Update feedback references if needed
- [ ] Verify all EXECUTION_TASKs moved
- [ ] Check if `/work-space/execution/` has other file types
- [ ] Remove or reclassify remaining files

**Day 4: Nested Directory Cleanup**
- [ ] Check contents of `/work-space/work-space/`
- [ ] Move any important files to correct locations
- [ ] Document any unexpected findings
- [ ] Remove nested `/work-space/work-space/` directory

**Day 5: Verification**
- [ ] Run structure validation script
- [ ] Verify all PLAN directories have correct nested structure
- [ ] Test a few PLAN workflows end-to-end
- [ ] Document any issues found

### Phase 2: Structural Improvements (Week 2)

**Day 1-2: Analyses Flattening**
- [ ] Create backup of `/work-space/analyses/`
- [ ] List all files in subdirectories
- [ ] Move all files to `/work-space/analyses/` root
- [ ] Remove empty subdirectories
- [ ] Create INDEX.md with categorization (optional)
- [ ] Verify count: 125 files at root level

**Day 3: Debug Consolidation**
- [ ] Compare files in `debug/` vs `debug-logs/`
- [ ] Identify any duplicates
- [ ] Move all files to `debug-logs/`
- [ ] Remove `debug/` directory
- [ ] Verify naming: `EXECUTION_DEBUG_*.md`

**Day 4: Archive Migration**
- [ ] List files in `/work-space/archive/`
- [ ] For each file, identify parent PLAN/feature
- [ ] Create structure: `documentation/archive/<FEATURE>/`
- [ ] Move files maintaining type structure (subplans/, execution/)
- [ ] Remove `/work-space/archive/` directory

**Day 5: Knowledge Reclassification**
- [ ] Review 8 files in `/knowledge/`
- [ ] Classify each by EXECUTION-TAXONOMY type
- [ ] Move to appropriate folders
- [ ] Remove `/knowledge/` directory

### Phase 3: Policy & Standards (Week 3)

- [ ] **PLAN Organization**: Decide on status handling (metadata vs. subdirs)
- [ ] **Session Summaries**: Create policy and location
- [ ] **Discovery Aids**: Create indexes where needed
- [ ] **Documentation**: Update workspace README
- [ ] **Guidelines**: Document file placement rules

### Phase 4: Automation (Week 4)

- [ ] **Validation Script**: Add structure checks
- [ ] **File Placement**: Auto-create correct directories
- [ ] **Pre-commit Hooks**: Prevent violations
- [ ] **Dashboard**: Create health monitoring (optional)

---

## 📊 Before/After Summary

| Aspect | Before | After |
|--------|--------|-------|
| **SUBPLANs** | 32 in flat `/subplans/` | 0 in flat, all nested in plans/ |
| **EXECUTION_TASKs** | 6 in flat `/execution/` | 0 in flat, all nested in plans/ |
| **Analyses Structure** | 12 subdirectories + 28 root files | 125 files at root level (flat) |
| **Debug Folders** | 2 folders (debug/ + debug-logs/) | 1 folder (debug-logs/ only) |
| **Nested work-space/** | 1 duplicate directory | 0 (removed) |
| **Archive Location** | work-space/archive/ | documentation/archive/ |
| **PLAN Naming** | Mixed (prefixes + direct) | Consistent (metadata-based) |
| **Methodology Compliance** | ~60% | ~95% |
| **Discoverability** | Poor (scattered) | Good (predictable) |
| **Automation Support** | Difficult | Easy |

---

## 🎯 Expected Benefits

### For Humans
1. ✅ **Faster Navigation**: Know exactly where files are
2. ✅ **Better Context**: Related files grouped together
3. ✅ **Clear Status**: Metadata shows PLAN status at a glance
4. ✅ **Easy Search**: Flat structures easier to search

### For LLMs
1. ✅ **Predictable Structure**: Can navigate without guessing
2. ✅ **Complete Context**: Find all related files (PLAN → SUBPLAN → EXECUTION)
3. ✅ **Better Prompts**: Correct file locations in generated prompts
4. ✅ **Automation Works**: Scripts find files reliably

### For Methodology
1. ✅ **Compliance**: Structure matches documented methodology
2. ✅ **Consistency**: All PLANs follow same pattern
3. ✅ **Scalability**: Structure supports growth
4. ✅ **Maintainability**: Clear rules for file placement

---

## 🚀 Quick Start Guide

### If You Want to Start Now

**Quick Win #1: Fix One PLAN (30 minutes)**

```bash
# Pick one PLAN with misplaced SUBPLANs
# Example: METHODOLOGY-V2-ENHANCEMENTS

# 1. Create structure
mkdir -p work-space/plans/METHODOLOGY-V2-ENHANCEMENTS/subplans

# 2. Move SUBPLANs
mv work-space/subplans/SUBPLAN_METHODOLOGY-V2-ENHANCEMENTS_*.md \
   work-space/plans/METHODOLOGY-V2-ENHANCEMENTS/subplans/

# 3. Verify
ls work-space/plans/METHODOLOGY-V2-ENHANCEMENTS/subplans/

# Result: One PLAN now fully compliant!
```

**Quick Win #2: Flatten One Subdirectory (15 minutes)**

```bash
# Example: Move archiving-system analyses to root

# 1. Move files
mv work-space/analyses/archiving-system/*.md \
   work-space/analyses/

# 2. Remove empty directory
rmdir work-space/analyses/archiving-system

# Result: 6 files now easier to find!
```

**Quick Win #3: Remove Duplicate Folder (5 minutes)**

```bash
# Remove nested work-space/ directory

# 1. Check contents first
find work-space/work-space -type f

# 2. If empty or unimportant, remove
rm -rf work-space/work-space

# Result: Cleaner structure!
```

---

## 📚 Related Documents

- **WORKSPACE-STRUCTURE-REVIEW-2025-11-15.md**: Detailed analysis and recommendations
- **LLM-METHODOLOGY.md**: Full methodology specification
- **work-space/README.md**: Workspace documentation (needs update post-reorganization)
- **LLM/guides/EXECUTION-TAXONOMY.md**: EXECUTION_WORK categorization

---

**Status**: ✅ Complete Visual Guide  
**Next Step**: Review with user, then create reorganization PLAN  
**Estimated Impact**: 10-20 minutes saved per navigation, 95%+ methodology compliance

