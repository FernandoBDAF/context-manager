# SUBPLAN: Extract Interactive Menu Module

**Achievement**: 2.1  
**Status**: 🚀 Ready to Execute  
**Created**: 2025-11-11  
**Estimated Effort**: 4-5 hours

---

## 📋 Objective

Extract interactive menu functionality (~600 lines) from `generate_prompt.py` into a dedicated `interactive_menu.py` module to improve maintainability and reduce file complexity.

**Why Critical**: Interactive mode is the most complex part of the codebase, spanning three functions (output_interactive_menu, prompt_interactive_menu, generate_feedback_prompt_interactive) with ~600 lines total. Extracting it first provides the biggest maintainability win and establishes the pattern for subsequent module extractions.

**Success Criteria**: InteractiveMenu module created, main file reduced by ~600 lines, all 18 interactive mode tests passing, zero breaking changes to UX.

---

## 📦 Deliverables

1. **`LLM/scripts/generation/interactive_menu.py`** (~600 lines)

   - InteractiveMenu class with three main methods
   - All interactive logic self-contained
   - Clean imports and dependencies

2. **Updated `generate_prompt.py`** (reduced by ~600 lines)

   - Import InteractiveMenu class
   - Replace function calls with class methods
   - Maintain all existing behavior

3. **Module tests** (10+ tests)

   - Test menu display logic
   - Test user input handling
   - Test feedback generation
   - Test all menu variations

4. **Migration verification**
   - All 18 existing interactive mode tests passing
   - No linter errors
   - No breaking changes to UX

---

## 🎯 Approach

### Phase 1: Analyze Current Implementation (30 min)

**Goal**: Understand the current interactive menu implementation and dependencies.

**Actions**:

1. Identify the three functions to extract:

   - `output_interactive_menu()` - Post-generation menu (lines ~2282-2500)
   - `prompt_interactive_menu()` - Pre-execution menu (lines ~2823-3000)
   - `generate_feedback_prompt_interactive()` - Feedback helper (lines ~2239-2279)

2. Map dependencies:

   - Imports needed (Path, subprocess, pyperclip, etc.)
   - Helper functions used (copy_to_clipboard_safe, etc.)
   - Data structures (workflow states, menu choices)

3. Document current behavior:
   - Two-stage interactive design
   - Menu options and variations
   - User input handling
   - Command execution logic

**Validation**: Clear understanding of what needs to be extracted and how it's currently structured.

---

### Phase 2: Create InteractiveMenu Class (1.5 hours)

**Goal**: Create the new module with InteractiveMenu class containing all interactive logic.

**Actions**:

1. **Create file structure**:

   ```python
   # LLM/scripts/generation/interactive_menu.py

   from pathlib import Path
   from typing import Optional
   import subprocess
   import sys

   class InteractiveMenu:
       """
       Handle two-stage interactive mode for prompt generation workflow.

       Two-Stage Design:
       - Stage 1 (Pre): show_pre_execution_menu() - Choose workflow
       - Stage 2 (Post): show_post_generation_menu() - Handle output

       Features:
       - Smart defaults (Enter = copy to clipboard)
       - Context-aware options (execute command when available)
       - Feedback generation integration
       - Seamless navigation through workflow
       """

       def __init__(self):
           """Initialize interactive menu handler."""
           pass

       def show_pre_execution_menu(self, plan_path: Path) -> None:
           """
           Show pre-execution menu (Stage 1: Choose workflow).

           Menu Options:
           1. Generate next achievement (auto-detect)
           2. Generate specific achievement
           3. View all available achievements
           4. Copy prompt to clipboard
           5. Exit

           Modifies sys.argv and returns to main for re-parsing.
           """
           pass

       def show_post_generation_menu(
           self,
           prompt: str,
           workflow_state: str,
           command: str = None,
           plan_path: Path = None,
           achievement_num: str = None
       ) -> None:
           """
           Show post-generation menu (Stage 2: Handle output).

           Menu Options (dynamic based on context):
           1. Copy command to clipboard (if command available)
           2. Copy full message
           3. View full prompt
           4. Save to file
           5. Generate feedback (if plan_path and achievement_num provided)
           6. Execute recommended command
           7. Get help
           8. Exit

           Handles user choice and executes corresponding action.
           """
           pass

       def generate_feedback_interactive(
           self,
           plan_path: Path,
           achievement_num: str
       ) -> None:
           """
           Generate feedback prompt for achievement (interactive helper).

           Calls generate_feedback_prompt.py script and copies output to clipboard.
           Shows next steps for creating APPROVED_XX.md or FIX_XX.md file.
           """
           pass
   ```

2. **Extract and adapt functions**:

   - Copy `output_interactive_menu()` → `show_post_generation_menu()`
   - Copy `prompt_interactive_menu()` → `show_pre_execution_menu()`
   - Copy `generate_feedback_prompt_interactive()` → `generate_feedback_interactive()`
   - Adapt to class methods (self parameter, consistent naming)

3. **Add helper methods**:

   - `_display_menu()` - Common menu display logic
   - `_get_user_choice()` - Input validation and handling
   - `_execute_command()` - Command execution wrapper
   - `_copy_to_clipboard()` - Clipboard operations

4. **Add comprehensive docstrings**:
   - Module-level documentation
   - Class documentation
   - Method documentation with examples
   - Parameter and return type documentation

**Validation**: Module file created with all interactive logic, well-documented, self-contained.

---

### Phase 3: Update generate_prompt.py (1 hour)

**Goal**: Replace function calls with class methods, maintain all existing behavior.

**Actions**:

1. **Add import at top of file**:

   ```python
   from interactive_menu import InteractiveMenu
   ```

2. **Replace function calls**:

   - Find all calls to `output_interactive_menu()`
   - Replace with `InteractiveMenu().show_post_generation_menu()`
   - Find all calls to `prompt_interactive_menu()`
   - Replace with `InteractiveMenu().show_pre_execution_menu()`
   - Find all calls to `generate_feedback_prompt_interactive()`
   - Replace with `InteractiveMenu().generate_feedback_interactive()`

3. **Remove old function definitions**:

   - Delete `output_interactive_menu()` function (~220 lines)
   - Delete `prompt_interactive_menu()` function (~180 lines)
   - Delete `generate_feedback_prompt_interactive()` function (~40 lines)
   - Total reduction: ~440-600 lines

4. **Verify imports**:
   - Ensure no unused imports remain
   - Ensure all needed imports for InteractiveMenu are present

**Validation**: generate_prompt.py updated, reduced by ~600 lines, imports correct.

---

### Phase 4: Run Tests (30 min)

**Goal**: Verify all existing tests pass with no breaking changes.

**Actions**:

1. **Run interactive mode tests**:

   ```bash
   pytest tests/LLM/scripts/generation/test_interactive_output_menu.py -v
   ```

   - Expected: 18 tests passing (or current count)
   - Fix any failures due to import changes

2. **Run all generation tests**:

   ```bash
   pytest tests/LLM/scripts/generation/ -v
   ```

   - Expected: All tests passing
   - Fix any failures

3. **Manual testing**:

   ```bash
   python generate_prompt.py @PROMPT-GENERATOR-UX-AND-FOUNDATION --interactive
   ```

   - Test pre-execution menu (Stage 1)
   - Test post-generation menu (Stage 2)
   - Test feedback generation option
   - Verify all menu options work

4. **Check for linter errors**:
   ```bash
   # No command needed - linter runs automatically
   ```

**Validation**: All tests passing, no linter errors, manual testing confirms UX unchanged.

---

### Phase 5: Create Module Tests (1 hour)

**Goal**: Add dedicated tests for the new InteractiveMenu module.

**Actions**:

1. **Create test file**:

   ```python
   # tests/LLM/scripts/generation/test_interactive_menu.py

   import pytest
   from pathlib import Path
   from unittest.mock import Mock, patch
   from LLM.scripts.generation.interactive_menu import InteractiveMenu

   class TestInteractiveMenu:
       """Test InteractiveMenu class."""

       def test_init(self):
           """Test InteractiveMenu initialization."""
           menu = InteractiveMenu()
           assert menu is not None

       def test_show_pre_execution_menu_modifies_argv(self):
           """Test pre-execution menu modifies sys.argv."""
           # Test that menu adds --next flag when option 1 chosen
           pass

       def test_show_post_generation_menu_with_command(self):
           """Test post-generation menu with command available."""
           # Test menu displays command copy option
           pass

       def test_show_post_generation_menu_without_command(self):
           """Test post-generation menu without command."""
           # Test menu doesn't show command option
           pass

       def test_generate_feedback_interactive(self):
           """Test feedback generation helper."""
           # Test calls generate_feedback_prompt.py correctly
           pass

       # Add 6+ more tests for different menu variations
   ```

2. **Test menu display logic**:

   - Test menu options appear correctly
   - Test dynamic options (command, feedback)
   - Test menu numbering adjusts correctly

3. **Test user input handling**:

   - Test valid choices
   - Test invalid choices
   - Test default choice (Enter key)
   - Test exit option

4. **Test feedback generation**:

   - Test script call with correct arguments
   - Test clipboard copy
   - Test error handling

5. **Test all menu variations**:
   - Single command menu
   - Multiple commands menu
   - No commands menu
   - With/without feedback option

**Validation**: 10+ new tests created, all passing, good coverage of InteractiveMenu class.

---

### Phase 6: Documentation & Verification (30 min)

**Goal**: Document the extraction and verify everything works.

**Actions**:

1. **Update module docstring in generate_prompt.py**:

   - Note that interactive menu logic is now in interactive_menu.py
   - Update architecture overview
   - Update import documentation

2. **Create migration notes**:

   - Document what was extracted
   - Document how to use the new module
   - Document any API changes (none expected)

3. **Final verification**:

   - Run all tests one more time
   - Check file sizes (generate_prompt.py should be ~3,000 lines)
   - Check interactive_menu.py size (~600 lines)
   - Verify no linter errors

4. **Update EXECUTION_TASK**:
   - Mark all phases complete
   - Add learning summary
   - Verify deliverables

**Validation**: Documentation updated, migration notes created, final verification complete.

---

## 🧪 Testing Strategy

### Existing Tests (Must Pass)

- `test_interactive_output_menu.py` - 18 tests for interactive mode
- All tests in `tests/LLM/scripts/generation/`
- Manual testing of interactive mode

### New Tests (To Create)

- `test_interactive_menu.py` - 10+ tests for InteractiveMenu class
- Test menu display logic
- Test user input handling
- Test feedback generation
- Test all menu variations

### Manual Testing

- Run interactive mode with various plans
- Test both pre and post-generation menus
- Test feedback generation option
- Verify UX is unchanged

---

## 📊 Expected Results

### File Size Changes

- **Before**: generate_prompt.py = 3,625 lines
- **After**: generate_prompt.py = ~3,000 lines (-600 lines)
- **New**: interactive_menu.py = ~600 lines

### Test Results

- All 18 existing interactive mode tests passing
- 10+ new module tests passing
- Total test count: 67 → 77+ tests

### Code Quality

- No linter errors
- Clear separation of concerns
- Improved maintainability
- Self-contained module

### UX Impact

- Zero breaking changes
- All menu options work identically
- Same user experience
- Same command-line interface

---

## 🔄 Execution Strategy

**Single EXECUTION**: This work will be completed in one execution task.

**Rationale**:

- Logical unit of work (extract one module)
- Clear dependencies (must be done together)
- Reasonable scope (4-5 hours)
- All phases build on each other

**Execution Flow**:

1. EXECUTION_TASK_21_01: Extract Interactive Menu Module
   - Complete all 6 phases sequentially
   - Verify at each phase
   - Document progress in iteration log

**Dependencies**:

- No external dependencies
- All code is in generate_prompt.py
- Tests already exist

**Risks**:

- Breaking existing tests (mitigated by running tests after each phase)
- Import issues (mitigated by careful import management)
- UX changes (mitigated by maintaining exact behavior)

---

## 📝 Notes

### Why Interactive Menu First?

- Most complex part (~600 lines)
- Biggest maintainability win
- Establishes pattern for other extractions
- Self-contained functionality

### Backward Compatibility

- Function calls → class methods
- Same parameters, same behavior
- No API changes
- Tests should pass without modification

### Future Work

- This extraction enables subsequent module extractions
- Establishes pattern for Achievements 2.2-2.4
- Reduces main file to manageable size
- Improves code organization

---

**Status**: 🚀 Ready for Execution  
**Next**: Create EXECUTION_TASK_21_01.md and begin extraction
