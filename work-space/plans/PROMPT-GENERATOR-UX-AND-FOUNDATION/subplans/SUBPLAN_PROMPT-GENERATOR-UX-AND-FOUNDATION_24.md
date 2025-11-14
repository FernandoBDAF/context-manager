# SUBPLAN: Extract Parsing & Utilities Module

**Achievement**: 2.4  
**Feature**: PROMPT-GENERATOR-UX-AND-FOUNDATION  
**Created**: 2025-11-12  
**Status**: 🎯 Ready for Execution

---

## 📋 Objective

Extract PLAN parsing logic and utility functions from `generate_prompt.py` into dedicated `plan_parser.py` and `utils.py` modules, reducing main file complexity by ~300-350 lines and establishing clean separation between parsing, utilities, and orchestration.

**Strategic Value**: Final major extraction in Priority 2, completing the modular architecture foundation established in Achievements 2.1-2.3.

---

## 🎯 Deliverables

### Primary Deliverables

1. **`LLM/scripts/generation/plan_parser.py`** (~250 lines)

   - `PlanParser` class with parsing methods
   - PLAN file parsing logic
   - Handoff section extraction
   - Statistics calculation
   - Helper parsing functions

2. **`LLM/scripts/generation/utils.py`** (~100 lines)

   - Standalone utility functions
   - Clipboard operations
   - Folder shortcut resolution
   - General-purpose helpers

3. **Updated `generate_prompt.py`** (reduced by ~300-350 lines)

   - Imports PlanParser and utils
   - Calls refactored to use new modules
   - All functionality preserved

4. **Test Suites**

   - `tests/LLM/scripts/generation/test_plan_parser.py` (~300 lines, 15+ tests)
   - `tests/LLM/scripts/generation/test_utils.py` (~150 lines, 8+ tests)
   - All existing tests updated and passing

5. **Documentation**
   - `MIGRATION_NOTES_PLAN_PARSER_EXTRACTION.md`
   - Updated EXECUTION_TASK with results

---

## 📖 Context & Background

### Current State (After Achievement 2.3)

- `generate_prompt.py`: 2,091 lines
- Already extracted:
  - Interactive menu → `interactive_menu.py` (Achievement 2.1)
  - Workflow detection → `workflow_detector.py` (Achievement 2.2)
  - Prompt templates → `prompt_builder.py` (Achievement 2.3)
- Remaining: Parsing logic, helper utilities, orchestration

### What Needs Extraction

**Parsing Functions** (for PlanParser):

1. `parse_plan_file()` - Parse PLAN markdown structure
2. `extract_handoff_section()` - Extract handoff content
3. `extract_plan_statistics()` - Calculate PLAN metrics
4. `estimate_section_size()` - Estimate achievement section lines
5. `find_archive_location()` - Find archive path in PLAN
6. `calculate_handoff_size()` - Calculate handoff section lines

**Utility Functions** (for utils.py):

1. `copy_to_clipboard_safe()` - Safe clipboard operations
2. `resolve_folder_shortcut()` - Resolve @folder shortcuts

**Note**: `find_next_achievement_from_plan()` was already moved to `workflow_detector.py` in Achievement 2.2.

### Why This Matters

- **Maintainability**: Parsing logic separated from orchestration
- **Testability**: Parser can be tested independently
- **Reusability**: PlanParser can be used by other tools
- **Clarity**: Clean separation of concerns (parse vs orchestrate vs format)

---

## 🔍 Approach

### 6-Phase Sequential Extraction

Following the proven pattern from Achievements 2.1-2.3:

**Phase 1: Create Module Structures** (20 min)

- Create `plan_parser.py` with PlanParser class skeleton
- Create `utils.py` with module docstring
- Add `from __future__ import annotations` (prevent circular imports)
- Define method signatures
- Test imports

**Phase 2: Extract PlanParser Core Methods** (60 min)

- Extract `parse_plan_file()` → `PlanParser.parse_plan_file()`
- Extract `extract_handoff_section()` → `PlanParser.extract_handoff_section()`
- Extract `extract_plan_statistics()` → `PlanParser.extract_plan_statistics()`
- Add comprehensive docstrings
- Test each method compiles

**Phase 3: Extract PlanParser Helper Methods** (40 min)

- Extract `estimate_section_size()` → `PlanParser.estimate_section_size()`
- Extract `find_archive_location()` → `PlanParser.find_archive_location()`
- Extract `calculate_handoff_size()` → `PlanParser.calculate_handoff_size()`
- Update internal method calls
- Test compilation

**Phase 4: Extract Utility Functions** (30 min)

- Extract `copy_to_clipboard_safe()` → `utils.copy_to_clipboard_safe()`
- Extract `resolve_folder_shortcut()` → `utils.resolve_folder_shortcut()`
- Keep as standalone functions (not class methods)
- Add comprehensive docstrings
- Test compilation

**Phase 5: Update generate_prompt.py** (45 min)

- Add imports: `from LLM.scripts.generation.plan_parser import PlanParser`
- Add imports: `from LLM.scripts.generation import utils`
- Initialize `parser = PlanParser()` where needed
- Update all call sites:
  - `parse_plan_file()` → `parser.parse_plan_file()`
  - `extract_handoff_section()` → `parser.extract_handoff_section()`
  - `extract_plan_statistics()` → `parser.extract_plan_statistics()`
  - `estimate_section_size()` → `parser.estimate_section_size()`
  - `find_archive_location()` → `parser.find_archive_location()`
  - `calculate_handoff_size()` → `parser.calculate_handoff_size()`
  - `copy_to_clipboard_safe()` → `utils.copy_to_clipboard_safe()`
  - `resolve_folder_shortcut()` → `utils.resolve_folder_shortcut()`
- Remove extracted function definitions
- Test import and basic functionality

**Phase 6: Create Module Tests** (90 min)

- Create `test_plan_parser.py`:
  - Test `parse_plan_file()` with various PLAN structures
  - Test `extract_handoff_section()` with/without section
  - Test `extract_plan_statistics()` accuracy
  - Test helper methods (estimate_section_size, find_archive_location, calculate_handoff_size)
  - Edge cases (malformed PLANs, missing sections, etc.)
  - **Target**: 15+ tests
- Create `test_utils.py`:
  - Test `copy_to_clipboard_safe()` with/without clipboard
  - Test `resolve_folder_shortcut()` with valid/invalid folders
  - Edge cases (empty input, invalid paths, etc.)
  - **Target**: 8+ tests
- Update existing tests to import from new modules
- Run full test suite (all 69+ existing tests + 23+ new tests)

**Phase 7: Full Validation** (15 min)

- Run all test suites (92+ tests)
- Verify line count reduction
- Test generate_prompt.py end-to-end
- Verify interactive mode works
- Create migration notes

---

## 🎯 Execution Strategy

### Single Atomic Execution

**Rationale**: All extractions are tightly coupled - parsing functions reference each other and utilities are used throughout. Single execution maintains consistency.

**Execution Pattern**:

1. Design phase (SUBPLAN) - ✅ This document
2. Single EXECUTION_TASK - All 7 phases in one run
3. Test after each phase
4. Full validation at end

**Time Allocation**:

- Phase 1: 20 min (Module structures)
- Phase 2: 60 min (Core parsing methods)
- Phase 3: 40 min (Helper methods)
- Phase 4: 30 min (Utility functions)
- Phase 5: 45 min (Update main file)
- Phase 6: 90 min (Create tests)
- Phase 7: 15 min (Validation)
- **Total**: 5.0 hours (within 3-4 hour estimate with buffer)

---

## 📐 Technical Design

### PlanParser Class Structure

```python
from __future__ import annotations
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass

@dataclass
class Achievement:
    """Achievement data structure (shared with generate_prompt.py)"""
    number: str
    title: str
    goal: str
    effort: str
    priority: str
    section_lines: int

class PlanParser:
    """
    Parse PLAN files and extract structured information.

    Responsibilities:
    - Parse PLAN markdown structure
    - Extract achievements and metadata
    - Calculate section sizes and statistics
    - Extract handoff sections
    - Find archive locations

    Philosophy: Filesystem-first state tracking (checks APPROVED_XX.md files)
    """

    def __init__(self):
        """Initialize parser (stateless)."""
        pass

    def parse_plan_file(self, plan_path: Path) -> Dict[str, any]:
        """
        Parse PLAN file and extract all structured information.

        Returns dict with:
        - feature_name: PLAN feature name
        - achievements: List[Achievement]
        - handoff_lines: Handoff section line count
        - total_plan_lines: Total PLAN lines
        - archive_location: Archive path from PLAN
        """
        pass

    def extract_handoff_section(self, plan_content: str) -> Optional[str]:
        """Extract 'Current Status & Handoff' section from PLAN."""
        pass

    def extract_plan_statistics(self, plan_path: Path, feature_name: str) -> Dict[str, any]:
        """Calculate PLAN statistics (completed achievements, hours, etc.)."""
        pass

    def estimate_section_size(self, lines: List[str], start_idx: int) -> int:
        """Estimate achievement section size from markdown structure."""
        pass

    def find_archive_location(self, lines: List[str]) -> str:
        """Find archive location from PLAN header."""
        pass

    def calculate_handoff_size(self, lines: List[str]) -> int:
        """Calculate handoff section line count."""
        pass
```

### Utils Module Structure

```python
"""
Utility functions for generate_prompt.py and related modules.

Standalone helper functions that don't fit into specific domain modules.
"""
from pathlib import Path
from typing import Optional

def copy_to_clipboard_safe(text: str, enabled: bool = True) -> bool:
    """
    Safely copy text to clipboard with error handling.

    Returns True if successful, False otherwise.
    Falls back gracefully if clipboard unavailable.
    """
    pass

def resolve_folder_shortcut(folder_name: str) -> Path:
    """
    Resolve @folder shortcut to actual PLAN path.

    Example:
        @GRAPHRAG-OBSERVABILITY → work-space/plans/GRAPHRAG-OBSERVABILITY/PLAN_*.md
    """
    pass
```

---

## ✅ Success Criteria

### Functional Requirements

- ✅ **PlanParser module created**: ~250 lines with 6 methods
- ✅ **Utils module created**: ~100 lines with 2 functions
- ✅ **Main file reduced**: 2,091 → ~1,750 lines (-341 lines, -16.3%)
- ✅ **All tests passing**: 92+ tests (69 existing + 23 new)
- ✅ **No regressions**: Existing functionality preserved
- ✅ **Import successful**: All modules import cleanly
- ✅ **Interactive mode works**: End-to-end testing passes

### Quality Targets

- ✅ **Test coverage**: 23+ new tests (15 for parser, 8 for utils)
- ✅ **Documentation**: Comprehensive docstrings for all methods
- ✅ **Migration notes**: Complete extraction documentation
- ✅ **No circular imports**: Clean import structure
- ✅ **Backward compatibility**: All existing code works

### Performance Targets

- ✅ **Execution time**: ≤5 hours (within 3-4 hour estimate + buffer)
- ✅ **Test run time**: <1 second for new tests
- ✅ **No performance regression**: Same speed as before

---

## 🧪 Testing Strategy

### Test Coverage Plan

**1. PlanParser Tests** (15+ tests):

- **parse_plan_file()**:
  - Valid PLAN with all sections
  - PLAN with missing sections
  - PLAN with malformed achievement index
  - Empty PLAN file
  - Achievements with various formats
- **extract_handoff_section()**:
  - PLAN with handoff section
  - PLAN without handoff section
  - Multiple handoff-like headers
  - Handoff section at different positions
- **extract_plan_statistics()**:
  - PLAN with no completions
  - PLAN with some completions
  - PLAN with all completions
  - Statistics accuracy (hours, achievements)
- **Helper Methods**:
  - `estimate_section_size()` with various structures
  - `find_archive_location()` with/without location
  - `calculate_handoff_size()` with various content

**2. Utils Tests** (8+ tests):

- **copy_to_clipboard_safe()**:
  - Successful clipboard copy
  - Clipboard disabled (enabled=False)
  - Clipboard unavailable (pyperclip error)
  - Empty text
  - Very long text
- **resolve_folder_shortcut()**:
  - Valid @folder shortcut
  - Invalid folder name
  - Folder with spaces
  - Non-existent folder

**3. Integration Tests** (Update existing):

- Update `test_generate_prompt_comprehensive.py` to import from new modules
- Verify end-to-end workflow still works
- Test interactive mode with new structure

---

## ⚠️ Risk Mitigation

### Known Risks & Mitigations

**Risk 1: Circular Import Dependencies**

- **Likelihood**: Medium (parser might need Achievement dataclass)
- **Impact**: High (breaks imports)
- **Mitigation**:
  - Use `from __future__ import annotations` in all new modules
  - Keep Achievement dataclass in generate_prompt.py and import it
  - Use local imports if needed
  - Test imports immediately after creation

**Risk 2: Shared State or Global Variables**

- **Likelihood**: Low (functions appear stateless)
- **Impact**: Medium (unexpected behavior)
- **Mitigation**:
  - Review functions for global state
  - Make PlanParser stateless (no instance variables)
  - Pass all dependencies explicitly
  - Test with multiple instances

**Risk 3: Test Update Complexity**

- **Likelihood**: Medium (existing tests import functions directly)
- **Impact**: Medium (test failures)
- **Mitigation**:
  - Update imports first, verify tests still pass
  - Use search-replace for systematic updates
  - Run tests after each import update
  - Keep comprehensive test log

**Risk 4: Hidden Dependencies Between Functions**

- **Likelihood**: Medium (parser methods call each other)
- **Impact**: Medium (missing functionality)
- **Mitigation**:
  - Analyze call graph before extraction
  - Extract all related functions together
  - Test each method individually
  - Verify internal method calls work

---

## 📊 Expected Results

### Line Count Changes

**Before (After Achievement 2.3)**:

- `generate_prompt.py`: 2,091 lines

**After (Achievement 2.4)**:

- `generate_prompt.py`: ~1,750 lines (-341 lines, -16.3%)
- `plan_parser.py`: ~250 lines (new)
- `utils.py`: ~100 lines (new)
- **Net change**: +9 lines (extraction overhead)

### Test Metrics

**Before**:

- Total tests: 69 (26 prompt_builder + 25 comprehensive + 18 workflow_detector)

**After**:

- Total tests: 92+ (69 existing + 15 plan_parser + 8 utils)
- **New coverage**: PLAN parsing logic, utilities
- **Pass rate**: 100% (92/92)

### Module Structure (Final State)

```
LLM/scripts/generation/
├── generate_prompt.py          (~1,750 lines - orchestration)
├── interactive_menu.py         (~600 lines - Achievement 2.1)
├── workflow_detector.py        (~538 lines - Achievement 2.2)
├── prompt_builder.py           (~314 lines - Achievement 2.3)
├── plan_parser.py              (~250 lines - Achievement 2.4) ← NEW
└── utils.py                    (~100 lines - Achievement 2.4) ← NEW

Total: ~3,552 lines (down from 3,625 before Priority 2)
```

---

## 🔄 Comparison with Previous Achievements

| Metric                | Ach 2.1          | Ach 2.2     | Ach 2.3        | Ach 2.4 (This)         |
| --------------------- | ---------------- | ----------- | -------------- | ---------------------- |
| **Lines Extracted**   | 600              | 613         | 155            | ~341                   |
| **New Module Size**   | 600              | 538         | 314            | ~350 (2 files)         |
| **Methods Extracted** | 1 main + helpers | 6           | 3              | 8 (6 parser + 2 utils) |
| **New Tests Created** | 0 (existing)     | 18          | 26             | 23                     |
| **Execution Time**    | 2.5h             | 4h          | 2.5h           | ~5h (estimated)        |
| **Circular Imports**  | No               | Yes (fixed) | No (prevented) | No (prevent)           |

**Pattern Recognition**:

- Each extraction gets faster (learning curve)
- More comprehensive testing each time
- Proactive circular import prevention now standard
- Design validation before implementation (Achievement 2.3 lesson)

---

## 📝 Learnings to Apply

### From Achievement 2.3

1. **Validate assumptions early**: Check what actually exists vs PLAN description
2. **Adapt design to reality**: Extract what's there, not what's imagined
3. **Prevent circular imports proactively**: Use `from __future__ import annotations`
4. **Comprehensive testing pays off**: 25-30% of time on tests prevents regressions

### From Achievement 2.2

1. **Local imports for shared dependencies**: Avoid circular imports
2. **Systematic approach**: Phase-by-phase with testing after each
3. **Detailed documentation**: Migration notes capture decisions

### From Achievement 2.1

1. **Big extractions first**: Largest modules have most impact
2. **Test after each phase**: Catch issues early
3. **Document thoroughly**: Future maintainers will thank you

---

## 🎯 Definition of Done

This SUBPLAN is complete when:

1. ✅ SUBPLAN reviewed and approved (this document)
2. ✅ EXECUTION_TASK created (single task for all phases)
3. ✅ Execution strategy confirmed (single atomic execution)

This **Achievement** is complete when:

1. ✅ All 7 phases executed successfully
2. ✅ `plan_parser.py` created (~250 lines)
3. ✅ `utils.py` created (~100 lines)
4. ✅ `generate_prompt.py` reduced to ~1,750 lines
5. ✅ 23+ new tests created and passing
6. ✅ All 92+ tests passing (100% success rate)
7. ✅ Migration notes documented
8. ✅ EXECUTION_TASK updated with results
9. ✅ APPROVED_24.md created in execution/feedbacks/

---

## 📚 References

**Templates & Guides**:

- `LLM/templates/SUBPLAN-TEMPLATE.md`
- `LLM/templates/EXECUTION_TASK-TEMPLATE.md`
- `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md`

**Related Achievements**:

- Achievement 2.1 (Interactive Menu Extraction) - Pattern reference
- Achievement 2.2 (Workflow Detector Extraction) - Circular import lessons
- Achievement 2.3 (Prompt Builder Extraction) - Recent success, design validation

**Migration Notes**:

- `MIGRATION_NOTES_INTERACTIVE_MENU_EXTRACTION.md`
- `MIGRATION_NOTES_WORKFLOW_DETECTOR_EXTRACTION.md`
- `MIGRATION_NOTES_PROMPT_BUILDER_EXTRACTION.md`

**Code Files**:

- `LLM/scripts/generation/generate_prompt.py` - Source for extraction
- `tests/LLM/scripts/generation/test_generate_prompt_comprehensive.py` - Existing tests

---

**SUBPLAN Status**: ✅ Ready for Execution  
**Next Step**: Create EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_24_01.md  
**Estimated Duration**: 5.0 hours (7 phases)
