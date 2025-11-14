# EXECUTION_TASK: Achievement 3.1 - Interactive Menu Polished

**PLAN**: PARALLEL-EXECUTION-AUTOMATION  
**SUBPLAN**: SUBPLAN_PARALLEL-EXECUTION-AUTOMATION_31.md  
**Achievement**: 3.1  
**Task**: 01 (Single Execution)  
**Estimated Time**: 2-3 hours  
**Created**: 2025-11-14  
**Status**: 📋 Ready for Execution

---

## 📋 SUBPLAN Context

### Objective

Polish the parallel execution menu UX and add enhanced features including progress indicators, colored output, comprehensive help text, and keyboard shortcuts.

### Approach

**4 Sequential Phases**:
1. Progress Indicators (45 min)
2. Colored Output (30 min)
3. Help Text and Option 3 Implementation (60 min)
4. Keyboard Shortcuts and Testing (30 min)

### Success Criteria

- Menu displays progress (X/Y achievements complete)
- Colored output with status emojis
- Help text is comprehensive
- Option 3 allows achievement selection
- Keyboard shortcuts work
- Menu is intuitive (tested with 3 scenarios)

---

## 🎯 Execution Instructions

### Phase 1: Progress Indicators (45 min)

**Goal**: Add progress tracking to menu display

**Steps**:

1. **Add progress calculation function** to `parallel_workflow.py`:

```python
def calculate_progress(parallel_data: Dict, plan_path: Path) -> Dict:
    """Calculate progress metrics for menu display."""
    from LLM.scripts.validation.get_parallel_status import get_parallel_status
    
    achievements = parallel_data.get("achievements", [])
    
    # Get status for each achievement
    parallel_json_path = plan_path / "parallel.json"
    status_map = get_parallel_status(parallel_json_path)
    
    # Count by status
    total = len(achievements)
    complete = sum(1 for s in status_map.values() if s == "complete")
    in_progress = sum(1 for s in status_map.values() if s in ["subplan_created", "execution_created"])
    not_started = sum(1 for s in status_map.values() if s == "not_started")
    
    # Calculate percentage
    percentage = int((complete / total * 100)) if total > 0 else 0
    
    return {
        "total": total,
        "complete": complete,
        "in_progress": in_progress,
        "not_started": not_started,
        "percentage": percentage,
        "status_map": status_map
    }
```

2. **Update `show_parallel_menu()` to display progress**:

```python
def show_parallel_menu(parallel_data: Dict, plan_name: str, plan_path: Path) -> str:
    """Show parallel execution menu with progress indicators."""
    
    # Calculate progress
    progress = calculate_progress(parallel_data, plan_path)
    
    print("\n" + "=" * 80)
    print("🔀 Parallel Execution Menu")
    print("=" * 80)
    print(f"Plan: {plan_name}")
    print(f"Parallelization Level: {parallel_data.get('parallelization_level', 'unknown')}")
    print(f"Total Progress: {progress['complete']}/{progress['total']} achievements ({progress['percentage']}%)")
    
    # Show progress bar
    bar_length = 40
    filled = int(bar_length * progress['percentage'] / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"Progress: [{bar}] {progress['percentage']}%")
    
    print()
    print("Options:")
    print("  1. Batch Create SUBPLANs (for same level)")
    print("  2. Batch Create EXECUTIONs (for same level)")
    print("  3. Run Parallel Executions (multi-executor)")
    print("  4. View Dependency Graph")
    print("  5. Help & Documentation")
    print("  6. Back to Main Menu")
    print()
    
    choice = input("Select option (1-6): ").strip()
    return choice
```

3. **Update calls to `show_parallel_menu()` to pass `plan_path`**

**Verification**: Menu shows progress correctly

---

### Phase 2: Colored Output (30 min)

**Goal**: Add emoji status indicators throughout menu

**Steps**:

1. **Define status emoji mapping**:

```python
STATUS_EMOJI = {
    "not_started": "⚪",
    "subplan_created": "📋",
    "execution_created": "📝",
    "in_progress": "🟡",
    "complete": "✅",
    "failed": "❌",
    "skipped": "⏭️",
    "blocked": "🔴"
}
```

2. **Add emoji to achievement displays**:
- Update batch preview functions
- Add emoji to dependency graph
- Use consistent emoji throughout

3. **Test visual output**:
- Verify emojis display correctly
- Test readability

**Verification**: Status is visually clear with emojis

---

### Phase 3: Help Text and Option 3 (60 min)

**Goal**: Add help and implement parallel execution selection

**Steps**:

1. **Add help option** (20 min):

```python
def show_help():
    """Display comprehensive help for parallel execution menu."""
    print("\n" + "="*80)
    print("📚 Parallel Execution Menu Help")
    print("="*80)
    
    print("\nOPTION 1: Batch Create SUBPLANs")
    print("  Purpose: Create multiple SUBPLAN files at once")
    print("  Usage: Automatically detects next incomplete level")
    print("  Example: Creates SUBPLANs for all achievements at same level")
    
    print("\nOPTION 2: Batch Create EXECUTIONs")
    print("  Purpose: Create multiple EXECUTION_TASK files at once")
    print("  Usage: Validates SUBPLANs exist first")
    print("  Example: Creates EXECUTIONs after SUBPLANs are ready")
    
    # ... more help text
```

2. **Implement Option 3** (30 min):

```python
def handle_run_parallel_executions(parallel_data: Dict, plan_name: str, plan_path: Path):
    """Handle option 3: Run Parallel Executions."""
    from LLM.scripts.generation.batch_subplan import find_next_incomplete_level
    from LLM.scripts.validation.get_parallel_status import get_parallel_status
    
    achievements = parallel_data.get("achievements", [])
    
    # Find current level
    parallel_json_path = plan_path / "parallel.json"
    next_level = find_next_incomplete_level(plan_path, achievements)
    
    if next_level is None:
        print("✅ All achievements complete!")
        return
    
    # Show achievements at current level
    level_achievements = filter_by_dependency_level(achievements, level=next_level)
    
    print(f"\nAvailable Achievements at Level {next_level}:")
    for i, ach in enumerate(level_achievements, 1):
        ach_id = ach.get("achievement_id")
        title = ach.get("title", "")
        hours = ach.get("estimated_hours", "?")
        print(f"  {i}. Achievement {ach_id} - {title} ({hours}h)")
    
    # Allow selection
    selection = input("\nSelect achievements (comma-separated, e.g., 1,2,3 or 'all'): ").strip()
    
    if selection.lower() == 'all':
        selected = level_achievements
    else:
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
        selected = [level_achievements[i] for i in indices if 0 <= i < len(level_achievements)]
    
    print(f"\n✅ Selected {len(selected)} achievements for parallel execution")
    print("Generate execution prompts for each and execute in parallel")
```

3. **Update menu handler** (10 min):
- Add case for option 5 (help)
- Update option 3 to call new function

**Verification**: Help displays, option 3 works

---

### Phase 4: Keyboard Shortcuts and Testing (30 min)

**Goal**: Add shortcuts and test UX

**Steps**:

1. **Add keyboard shortcuts** (15 min):
- Accept single-key input
- Map 'h' to help, 'q' to quit
- Update input prompt

2. **Test with 3 scenarios** (10 min):
- Scenario 1: New user exploring menu
- Scenario 2: User creating batch SUBPLANs
- Scenario 3: User executing parallel achievements

3. **Polish and refine** (5 min):
- Fix any UX issues
- Improve clarity

**Verification**: Menu is intuitive and efficient

---

## 📊 Iteration Log

### Iteration 1: [Date]

**Phase**: [Phase Number]  
**Duration**: [Actual Time]  
**Status**: [In Progress / Complete]

**Work Completed**:

- [List what was done]

**Issues Encountered**:

- [List any issues]

**Solutions Applied**:

- [List solutions]

**Next Steps**:

- [What's next]

---

## ✅ Completion Checklist

**Deliverables**:

- [ ] Progress indicators implemented
- [ ] Colored output with emojis
- [ ] Help text and examples
- [ ] Keyboard shortcuts
- [ ] Option 3 (Run Parallel Executions) implemented
- [ ] Tests created (~200 lines)

**Functionality**:

- [ ] Menu shows progress (X/Y complete)
- [ ] Progress bar displays
- [ ] Emojis show status
- [ ] Help option works
- [ ] Option 3 allows selection
- [ ] Shortcuts work (h, q, r)

**Testing**:

- [ ] All tests pass (15+ tests)
- [ ] Coverage >90%
- [ ] Manual testing complete (3 scenarios)
- [ ] No linter errors

**Quality**:

- [ ] Type hints present
- [ ] Docstrings complete
- [ ] Help text is clear
- [ ] UX is intuitive

---

## 🎯 Success Criteria Met

**Achievement 3.1 is complete when**:

- ✅ Menu displays progress indicators
- ✅ Colored output with emojis
- ✅ Help text is comprehensive
- ✅ Keyboard shortcuts work
- ✅ Option 3 implemented
- ✅ Tested with 3 scenarios
- ✅ All tests passing
- ✅ This EXECUTION_TASK marked complete
- ✅ Ready for review (APPROVED_31.md creation)

---

**EXECUTION_TASK Status**: 📋 Ready for Execution  
**Estimated Duration**: 2-3 hours  
**Next Step**: Begin Phase 1 (Progress Indicators)
