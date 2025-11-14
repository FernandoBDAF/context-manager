# Generate_Prompt.py Refactoring Analysis
**Date**: 2025-11-12
**Current**: 1660 lines
**Target**: ~800 lines  
**Reduction Needed**: 860 lines (52%)

## Current Structure

### Functions by Size:
1. main(): 658 lines (40%) - PRIMARY TARGET
2. generate_prompt(): 115 lines (7%)
3. inject_project_context(): 109 lines (7%)
4. check_subplan_status(): 98 lines (6%)
5. detect_workflow_state(): 87 lines (5%)
6. find_subplan_for_achievement(): 68 lines (4%)
7. is_plan_complete(): 62 lines (4%)
8. is_achievement_complete(): 58 lines (3%)
9. detect_validation_scripts(): 47 lines (3%)
10. get_plan_status(): 46 lines (3%)
11. Achievement class: 19 lines (1%)

## Refactoring Strategy

### KEEP in generate_prompt.py (Orchestration):
- **Achievement class** (19 lines) - Data structure
- **main()** - REFACTOR to ~200 lines (currently 658)
  - Keep: CLI argument parsing
  - Keep: Module initialization
  - Keep: Workflow routing
  - REMOVE: Implementation details (delegate to modules)
- **generate_prompt()** - REFACTOR to ~50-70 lines
  - Keep: High-level orchestration
  - REMOVE: Detailed logic (delegate to PromptBuilder, WorkflowDetector)

### MOVE to Existing Modules:

**To WorkflowDetector:**
- detect_workflow_state() (87 lines) - similar to detect_workflow_state_filesystem
- is_plan_complete() (62 lines) - workflow state logic
- is_achievement_complete() (58 lines) - completion checking
- find_subplan_for_achievement() (68 lines) - workflow detection

**To PlanParser:**
- get_plan_status() (46 lines) - plan parsing
- check_subplan_status() (98 lines) - plan file analysis

**To Utils:**
- detect_validation_scripts() (47 lines) - utility function
- inject_project_context() (109 lines) - could be simplified

### Estimated Line Reduction:
- main() refactoring: 658 → 200 = -458 lines
- Functions moved to modules: ~575 lines
- generate_prompt() refactoring: 115 → 60 = -55 lines
- Total reduction: ~1088 lines
- New size: 1660 - 1088 = 572 lines (BELOW target of 800!)

### Adjustment:
- Keep some utility functions inline for now
- Keep inject_project_context() (can refactor later)
- Focus on main() and delegation

### Realistic Target After Phase 2:
- ~750-850 lines (within target range)

## Refactoring Order (Phase 2):

1. **Move functions to modules first** (2 hours):
   a. Move to WorkflowDetector (30 min):
      - detect_workflow_state()
      - is_plan_complete()
      - is_achievement_complete()
      - find_subplan_for_achievement()
   
   b. Move to PlanParser (30 min):
      - get_plan_status()
      - check_subplan_status()
   
   c. Move to Utils (15 min):
      - detect_validation_scripts()
   
   d. Update imports in generate_prompt.py (15 min)

2. **Refactor main()** (30 min):
   - Extract argument parsing to separate function
   - Create module initialization function
   - Simplify workflow routing
   - Remove duplicated code

3. **Refactor generate_prompt()** (30 min):
   - Delegate to PromptBuilder
   - Delegate to WorkflowDetector
   - Keep only orchestration logic

## Module Integration Points:

### Current modules:
- InteractiveMenu (in interactive_menu.py)
- WorkflowDetector (in workflow_detector.py)
- PromptBuilder (in prompt_builder.py)
- PlanParser (in plan_parser.py)  
- Utils (in utils.py)

### How main() should look after:
```python
def main():
    # 1. Parse arguments (~50 lines)
    args = parse_arguments()
    
    # 2. Initialize modules (~20 lines)
    modules = initialize_modules()
    
    # 3. Handle interactive mode (~30 lines)
    if args.interactive:
        menu.show_pre_execution_menu()
        return
    
    # 4. Route to workflow (~50 lines)
    if args.next:
        result = generate_next_achievement(args, modules)
    elif args.achievement:
        result = generate_specific_achievement(args, modules)
    else:
        # Default behavior
        ...
    
    # 5. Handle result (~50 lines)
    handle_result(result, args)
```

Total: ~200 lines for main()

## Success Metrics:
- ✅ generate_prompt.py: 750-850 lines
- ✅ All functions either orchestrate or delegate
- ✅ Clear module boundaries
- ✅ No code duplication
- ✅ All tests pass
