# SUBPLAN: Achievement 2.2 - Batch SUBPLAN Creation Implemented

**PLAN**: PARALLEL-EXECUTION-AUTOMATION  
**Achievement**: 2.2  
**Estimated Time**: 5-7 hours  
**Created**: 2025-11-13  
**Status**: 📋 Design Phase

---

## 🎯 Objective

Enable batch creation of SUBPLANs for multiple achievements at the same dependency level, providing safety features (dry-run, confirmation, rollback) to prevent errors and ensure reliable parallel workflow orchestration. This achievement transforms the SUBPLAN creation process from sequential (one at a time) to parallel (multiple at once), enabling users to efficiently prepare multiple achievements for simultaneous execution.

**Core Purpose**: Implement batch SUBPLAN creation functionality that intelligently filters achievements by dependency level, only creates missing SUBPLANs, provides preview capabilities, and includes comprehensive safety mechanisms to prevent workflow disruption.

**Success Definition**:
- Users can generate prompts for multiple SUBPLANs at once using `--batch` flag
- System only creates SUBPLANs that don't already exist (no overwrites)
- Achievements are grouped by dependency level (0 dependencies can run together)
- `--dry-run` mode shows preview without creating files
- Rollback strategy documented and tested
- Integration with `generate_prompt.py` parallel menu (menu option 1)
- All components tested with >90% coverage

---

## 📦 Deliverables

### 1. Enhanced generate_subplan_prompt.py

**File**: `LLM/scripts/generation/generate_subplan_prompt.py` (modified, ~100 new lines)

**New Features**:

**A. `--batch` Flag**:
```python
parser.add_argument(
    '--batch',
    action='store_true',
    help='Batch create SUBPLANs for multiple achievements (requires parallel.json)'
)
```

**B. `--dry-run` Flag**:
```python
parser.add_argument(
    '--dry-run',
    action='store_true',
    help='Preview batch creation without creating files'
)
```

**C. Batch Logic Integration**:
```python
def main():
    args = parse_args()
    
    # Handle --batch flag
    if args.batch:
        from LLM.scripts.generation.batch_subplan import batch_create_subplans
        
        batch_create_subplans(
            plan_path=args.plan_path,
            dry_run=args.dry_run,
            parallel_json_path=args.parallel_json
        )
        return 0
    
    # Existing single SUBPLAN logic...
```

### 2. Batch SUBPLAN Creation Module

**File**: `LLM/scripts/generation/batch_subplan.py` (~350 lines, NEW)

**Purpose**: Core batch creation logic with safety features

**Key Functions**:

```python
def batch_create_subplans(
    plan_path: Path,
    dry_run: bool = False,
    parallel_json_path: Optional[Path] = None
) -> BatchResult:
    """
    Batch create SUBPLANs for achievements in parallel.json.
    
    Args:
        plan_path: Path to PLAN directory
        dry_run: If True, preview without creating files
        parallel_json_path: Optional path to parallel.json (auto-detect if None)
    
    Returns:
        BatchResult with created SUBPLANs, skipped, and errors
    
    Example:
        >>> result = batch_create_subplans(Path("work-space/plans/MY-PLAN"))
        >>> print(f"Created: {len(result.created)}, Skipped: {len(result.skipped)}")
    """

def filter_by_dependency_level(
    achievements: List[Dict],
    level: int = 0
) -> List[Dict]:
    """
    Filter achievements by dependency level.
    
    Level 0: No dependencies (can run immediately)
    Level 1: Depends only on level 0 achievements
    Level 2: Depends on level 1 achievements
    Etc.
    
    Args:
        achievements: List of achievement dicts from parallel.json
        level: Dependency level to filter (default: 0)
    
    Returns:
        List of achievements at specified level
    
    Example:
        >>> achievements = [
        ...     {"achievement_id": "1.1", "dependencies": []},
        ...     {"achievement_id": "1.2", "dependencies": ["1.1"]},
        ...     {"achievement_id": "1.3", "dependencies": []}
        ... ]
        >>> level_0 = filter_by_dependency_level(achievements, level=0)
        >>> print([a["achievement_id"] for a in level_0])
        ['1.1', '1.3']
    """

def detect_missing_subplans(
    plan_path: Path,
    achievements: List[Dict]
) -> List[Dict]:
    """
    Detect which achievements are missing SUBPLANs.
    
    Args:
        plan_path: Path to PLAN directory
        achievements: List of achievement dicts
    
    Returns:
        List of achievements without SUBPLANs
    
    Example:
        >>> missing = detect_missing_subplans(plan_path, achievements)
        >>> print(f"Missing SUBPLANs: {len(missing)}")
    """

def show_batch_preview(
    achievements: List[Dict],
    plan_name: str
) -> None:
    """
    Show preview of what would be created in batch.
    
    Args:
        achievements: List of achievements to create SUBPLANs for
        plan_name: Name of the plan
    
    Example:
        >>> show_batch_preview(achievements, "MY-PLAN")
        📋 Batch SUBPLAN Creation Preview
        ================================================================================
        Plan: MY-PLAN
        Achievements to create: 3
        
        SUBPLANs that will be created:
          1. Achievement 1.1 - SUBPLAN_MY-PLAN_11.md
          2. Achievement 1.2 - SUBPLAN_MY-PLAN_12.md
          3. Achievement 1.3 - SUBPLAN_MY-PLAN_13.md
        ================================================================================
    """

def confirm_batch_creation(
    achievements: List[Dict]
) -> bool:
    """
    Ask user to confirm batch creation.
    
    Args:
        achievements: List of achievements to create
    
    Returns:
        True if user confirms, False otherwise
    
    Example:
        >>> if confirm_batch_creation(achievements):
        ...     # Proceed with creation
    """

def create_subplan_file(
    plan_path: Path,
    achievement_id: str,
    plan_data: Dict
) -> Path:
    """
    Create a single SUBPLAN file.
    
    Args:
        plan_path: Path to PLAN directory
        achievement_id: Achievement ID (e.g., "1.1")
        plan_data: Parsed PLAN data
    
    Returns:
        Path to created SUBPLAN file
    
    Raises:
        SubplanCreationError: If creation fails
    """

@dataclass
class BatchResult:
    """Result of batch SUBPLAN creation."""
    created: List[Path] = field(default_factory=list)
    skipped: List[str] = field(default_factory=list)
    errors: List[Tuple[str, str]] = field(default_factory=list)  # (achievement_id, error_msg)
    
    def __str__(self) -> str:
        """Format batch result as string."""
        lines = []
        
        if self.created:
            lines.append(f"✅ Created {len(self.created)} SUBPLANs:")
            for path in self.created:
                lines.append(f"  - {path.name}")
        
        if self.skipped:
            lines.append(f"\n⏭️  Skipped {len(self.skipped)} (already exist):")
            for ach_id in self.skipped:
                lines.append(f"  - Achievement {ach_id}")
        
        if self.errors:
            lines.append(f"\n❌ Errors ({len(self.errors)}):")
            for ach_id, error in self.errors:
                lines.append(f"  - Achievement {ach_id}: {error}")
        
        return "\n".join(lines)
```

### 3. Rollback Strategy Module

**File**: `LLM/scripts/generation/batch_rollback.py` (~150 lines, NEW)

**Purpose**: Git-based rollback for batch operations

**Key Functions**:

```python
def create_rollback_point(
    plan_path: Path
) -> str:
    """
    Create git commit before batch operation.
    
    Args:
        plan_path: Path to PLAN directory
    
    Returns:
        Commit SHA for rollback
    
    Example:
        >>> commit_sha = create_rollback_point(plan_path)
        >>> print(f"Rollback point: {commit_sha}")
    """

def rollback_to_point(
    commit_sha: str,
    plan_path: Path
) -> bool:
    """
    Rollback to previous commit.
    
    Args:
        commit_sha: Commit SHA to rollback to
        plan_path: Path to PLAN directory
    
    Returns:
        True if rollback successful, False otherwise
    """

def cleanup_partial_batch(
    created_files: List[Path]
) -> None:
    """
    Clean up partially created SUBPLANs on error.
    
    Args:
        created_files: List of files created before error
    """
```

### 4. Integration with generate_prompt.py Menu

**File**: `LLM/scripts/generation/parallel_workflow.py` (modified, ~50 new lines)

**Changes**:

```python
def handle_parallel_menu_selection(choice: str, parallel_data: Dict, plan_name: str):
    """Handle parallel menu selection."""
    if choice == "1":
        # Batch SUBPLAN creation (Achievement 2.2)
        from LLM.scripts.generation.batch_subplan import batch_create_subplans
        
        print("\n🔀 Batch SUBPLAN Creation")
        print("="*80)
        
        # Filter level 0 achievements (no dependencies)
        level_0 = filter_by_dependency_level(parallel_data["achievements"], level=0)
        
        if not level_0:
            print("❌ No achievements at level 0 (no dependencies)")
            return
        
        # Detect missing SUBPLANs
        missing = detect_missing_subplans(plan_path, level_0)
        
        if not missing:
            print("✅ All SUBPLANs already exist for level 0 achievements")
            return
        
        # Show preview
        show_batch_preview(missing, plan_name)
        
        # Confirm
        if not confirm_batch_creation(missing):
            print("❌ Batch creation cancelled")
            return
        
        # Create SUBPLANs
        result = batch_create_subplans(plan_path, dry_run=False)
        print(result)
        
    elif choice == "2":
        print("\n⏳ Batch EXECUTION creation (Coming in Achievement 2.3)")
    # ... rest of menu options
```

### 5. Test Suite

**File**: `tests/LLM/scripts/generation/test_batch_subplan.py` (~400 lines, NEW)

**Test Coverage**:

**A. Batch Creation Tests** (~100 lines):
- `test_batch_create_subplans_success()` - Creates multiple SUBPLANs
- `test_batch_create_subplans_dry_run()` - Preview without creating
- `test_batch_create_subplans_empty_list()` - Handles empty achievement list
- `test_batch_create_subplans_all_exist()` - Skips when all exist
- `test_batch_create_subplans_partial_exist()` - Creates only missing

**B. Filtering Tests** (~80 lines):
- `test_filter_by_dependency_level_0()` - Level 0 (no dependencies)
- `test_filter_by_dependency_level_1()` - Level 1 (depends on level 0)
- `test_filter_by_dependency_level_2()` - Level 2 (depends on level 1)
- `test_filter_by_dependency_level_empty()` - No achievements at level
- `test_filter_by_dependency_level_circular()` - Handles circular deps

**C. Detection Tests** (~60 lines):
- `test_detect_missing_subplans_none_exist()` - All missing
- `test_detect_missing_subplans_all_exist()` - None missing
- `test_detect_missing_subplans_some_exist()` - Partial missing

**D. Preview Tests** (~40 lines):
- `test_show_batch_preview()` - Preview displays correctly
- `test_confirm_batch_creation_yes()` - User confirms
- `test_confirm_batch_creation_no()` - User cancels

**E. Rollback Tests** (~60 lines):
- `test_create_rollback_point()` - Creates git commit
- `test_rollback_to_point()` - Restores previous state
- `test_cleanup_partial_batch()` - Cleans up on error

**F. Integration Tests** (~60 lines):
- `test_batch_integration_with_parallel_json()` - End-to-end test
- `test_batch_integration_with_menu()` - Menu integration
- `test_batch_error_handling()` - Error scenarios

### 6. Documentation Updates

**File**: `documentation/batch-subplan-creation.md` (~200 lines, NEW)

**Contents**:
- Overview of batch SUBPLAN creation
- Usage examples (`--batch`, `--dry-run`)
- Safety features explanation
- Rollback strategy documentation
- Troubleshooting guide
- Best practices

---

## 🔧 Approach

### Phase 1: Core Batch Logic (120 min)

**Goal**: Implement batch creation logic with filtering

**Steps**:

1. **Create `batch_subplan.py` module** (30 min):
   - Define `BatchResult` dataclass
   - Implement `batch_create_subplans()` main function
   - Add error handling and logging

2. **Implement filtering functions** (40 min):
   - `filter_by_dependency_level()` - Group by dependency level
   - `detect_missing_subplans()` - Find which SUBPLANs don't exist
   - Test with sample parallel.json

3. **Implement preview and confirmation** (30 min):
   - `show_batch_preview()` - Display what will be created
   - `confirm_batch_creation()` - User confirmation prompt
   - Test user interaction flow

4. **Implement SUBPLAN file creation** (20 min):
   - `create_subplan_file()` - Generate SUBPLAN from template
   - Use existing SUBPLAN generation logic
   - Handle file I/O errors

**Verification**:
- Can filter achievements by level
- Can detect missing SUBPLANs
- Preview shows correct information
- Confirmation works

---

### Phase 2: Safety Features (90 min)

**Goal**: Implement dry-run and rollback mechanisms

**Steps**:

1. **Implement `--dry-run` mode** (30 min):
   - Add flag to argparse
   - Modify `batch_create_subplans()` to skip file creation in dry-run
   - Show preview only
   - Test dry-run vs actual creation

2. **Create `batch_rollback.py` module** (40 min):
   - Implement `create_rollback_point()` using git
   - Implement `rollback_to_point()` for restoration
   - Implement `cleanup_partial_batch()` for partial failures
   - Test rollback scenarios

3. **Integrate safety features** (20 min):
   - Add rollback point creation before batch
   - Add partial success handling
   - Add error recovery logic
   - Test error scenarios

**Verification**:
- Dry-run shows preview without creating files
- Rollback restores previous state
- Partial failures handled gracefully

---

### Phase 3: CLI Integration (60 min)

**Goal**: Integrate with generate_subplan_prompt.py and parallel menu

**Steps**:

1. **Enhance `generate_subplan_prompt.py`** (30 min):
   - Add `--batch` flag
   - Add `--dry-run` flag
   - Add batch logic routing
   - Test CLI interface

2. **Update `parallel_workflow.py`** (30 min):
   - Implement menu option 1 (Batch Create SUBPLANs)
   - Add level filtering for menu
   - Add preview and confirmation
   - Test menu integration

**Verification**:
- `generate_subplan_prompt.py --batch` works
- `generate_subplan_prompt.py --batch --dry-run` works
- Parallel menu option 1 works
- All flags work together

---

### Phase 4: Testing & Documentation (150 min)

**Goal**: Achieve >90% test coverage and complete documentation

**Steps**:

1. **Create `test_batch_subplan.py`** (90 min):
   - Write batch creation tests (20 min)
   - Write filtering tests (15 min)
   - Write detection tests (15 min)
   - Write preview tests (10 min)
   - Write rollback tests (15 min)
   - Write integration tests (15 min)

2. **Run tests and fix issues** (30 min):
   ```bash
   pytest tests/LLM/scripts/generation/test_batch_subplan.py -v
   ```
   - Fix any test failures
   - Achieve >90% coverage
   - No linter errors

3. **Create documentation** (30 min):
   - Create `documentation/batch-subplan-creation.md`
   - Document usage examples
   - Document safety features
   - Document rollback strategy
   - Add troubleshooting guide

**Verification**:
- All tests pass (30+ tests)
- Coverage >90%
- No linter errors
- Documentation complete

---

## 🔄 Execution Strategy

### Type: Single EXECUTION (Recommended)

**Rationale**:

1. **Cohesive Feature**: All components work together (batch logic → safety → CLI integration)
2. **Manageable Scope**: 5-7 hours, can be done in one focused session
3. **Sequential Dependencies**: Each phase builds on previous (core → safety → integration)
4. **Atomic Integration**: All pieces needed together for feature to work

**Execution**: Create single `EXECUTION_TASK_PARALLEL-EXECUTION-AUTOMATION_22_01.md`

---

## 🧪 Testing Strategy

### Unit Testing

**Scope**: Test each function in isolation

**Test Files**:
1. `test_batch_subplan.py` - All batch creation functions
2. `test_batch_rollback.py` - Rollback mechanisms

**Coverage Target**: >90% for new code

**Key Tests**:
- Batch creation with various scenarios
- Dependency level filtering (0, 1, 2)
- Missing SUBPLAN detection
- Dry-run mode
- Rollback mechanisms
- Error handling

### Integration Testing

**Scope**: Test full workflows end-to-end

**Test Cases**:
1. **Batch Creation Workflow**:
   - Load parallel.json → filter level 0 → detect missing → create SUBPLANs
   - Verify all SUBPLANs created correctly

2. **Dry-Run Workflow**:
   - Run with `--dry-run` → verify preview shown → verify no files created

3. **Rollback Workflow**:
   - Create rollback point → batch create → simulate error → rollback → verify restored

4. **Menu Integration**:
   - Access parallel menu → select option 1 → batch create SUBPLANs

### Manual Testing

**Verification**:
- Test with real plan (PARALLEL-EXECUTION-AUTOMATION)
- Create parallel.json with 3+ achievements
- Run batch creation
- Verify SUBPLANs created correctly
- Test dry-run mode
- Test rollback scenario

---

## 📊 Expected Results

### Success Criteria

**Functional**:
- ✅ Can generate prompts for multiple SUBPLANs at once
- ✅ Only creates SUBPLANs that don't exist (no overwrites)
- ✅ Groups achievements by dependency level
- ✅ Dry-run shows preview without creating files
- ✅ Rollback strategy works correctly
- ✅ Tested with 3+ achievements
- ✅ Integration with parallel menu works

**Quality**:
- ✅ Test coverage >90% for new code
- ✅ All tests passing (30+ tests)
- ✅ No linter errors
- ✅ Clear, actionable error messages

**Safety**:
- ✅ Dry-run mode prevents accidental creation
- ✅ Confirmation prompt prevents mistakes
- ✅ Rollback strategy documented and tested
- ✅ Partial success handling works

### Deliverable Metrics

**Files Created/Modified**: 6 files (~1,250 lines total)
- New: 4 files (~1,100 lines)
- Modified: 2 files (~150 lines)

**Test Metrics**:
- Total Tests: ~30 new tests
- Coverage: >90% for new code
- All tests passing

---

## 🚨 Risks & Mitigations

### Risk 1: File Overwrites

**Risk**: Batch creation might overwrite existing SUBPLANs

**Impact**: HIGH - Could lose work

**Mitigation**:
- Always check if SUBPLAN exists before creating
- Skip existing SUBPLANs (don't overwrite)
- Show skipped SUBPLANs in result
- Test overwrite prevention thoroughly

### Risk 2: Partial Batch Failures

**Risk**: Some SUBPLANs might fail to create, leaving incomplete batch

**Impact**: MEDIUM - Confusing state

**Mitigation**:
- Track which SUBPLANs were created successfully
- Keep successful SUBPLANs, report failed ones
- Provide option to retry failed SUBPLANs
- Document partial success handling

### Risk 3: Rollback Complexity

**Risk**: Git-based rollback might not work in all environments

**Impact**: MEDIUM - Can't undo mistakes

**Mitigation**:
- Check if git is available before rollback
- Provide manual cleanup instructions if git unavailable
- Test rollback in various scenarios
- Document rollback limitations

### Risk 4: Dependency Level Calculation

**Risk**: Circular dependencies or complex dependency chains might break level calculation

**Impact**: MEDIUM - Wrong achievements grouped together

**Mitigation**:
- Use validation from Achievement 1.3 (circular dependency detection)
- Handle circular dependencies gracefully (skip or error)
- Test with complex dependency graphs
- Document dependency level algorithm

---

## 💡 Design Decisions

### Decision 1: Level-Based Filtering

**Chosen**: Filter by dependency level (0, 1, 2, etc.)

**Rationale**:
- Level 0 (no dependencies) can always run in parallel
- Level 1 (depends on level 0) can run after level 0 completes
- Clear, predictable grouping
- Matches user mental model

**Alternative Considered**: Filter by priority, but dependency level is more precise

### Decision 2: Git-Based Rollback

**Chosen**: Use git commits for rollback

**Rationale**:
- Git is already required for the project
- Atomic rollback (all or nothing)
- Can rollback to any previous state
- Standard practice for version control

**Alternative Considered**: Manual file deletion, but git is more reliable

### Decision 3: Dry-Run as Separate Flag

**Chosen**: `--dry-run` as separate flag (not `--batch --preview`)

**Rationale**:
- Standard Unix convention (many tools use `--dry-run`)
- Clear intent (preview without action)
- Can be used with other flags
- Familiar to users

**Alternative Considered**: `--preview` flag, but `--dry-run` is more standard

### Decision 4: Skip Existing SUBPLANs

**Chosen**: Skip existing SUBPLANs, don't overwrite

**Rationale**:
- Prevents accidental data loss
- Idempotent operation (can run multiple times safely)
- Clear feedback (shows skipped SUBPLANs)
- Matches user expectations

**Alternative Considered**: `--force` flag to overwrite, but skip is safer default

### Decision 5: Single EXECUTION

**Chosen**: Single EXECUTION_TASK for all phases

**Rationale**:
- All components tightly coupled
- 5-7 hours is manageable in one session
- Sequential dependencies (core → safety → integration)
- Atomic feature delivery

**Alternative Considered**: Split into 2 EXECUTIONs (core + safety, integration), but overhead not worth it

---

## 📝 Implementation Notes

### Dependency Level Algorithm

```python
def calculate_dependency_level(achievement_id: str, achievements: List[Dict]) -> int:
    """
    Calculate dependency level for an achievement.
    
    Level 0: No dependencies
    Level 1: Depends only on level 0 achievements
    Level 2: Depends on level 1 achievements
    Etc.
    
    Algorithm:
    1. If no dependencies → level 0
    2. Otherwise → max(dependency levels) + 1
    """
    ach = next(a for a in achievements if a["achievement_id"] == achievement_id)
    
    if not ach["dependencies"]:
        return 0
    
    # Recursive: level = max(dep levels) + 1
    dep_levels = [
        calculate_dependency_level(dep_id, achievements)
        for dep_id in ach["dependencies"]
    ]
    
    return max(dep_levels) + 1
```

### SUBPLAN File Naming Convention

```
SUBPLAN_{PLAN_NAME}_{ACHIEVEMENT_ID}.md

Examples:
- SUBPLAN_PARALLEL-EXECUTION-AUTOMATION_11.md
- SUBPLAN_PARALLEL-EXECUTION-AUTOMATION_12.md
- SUBPLAN_MY-PLAN_21.md
```

### Batch Result Format

```
✅ Created 3 SUBPLANs:
  - SUBPLAN_PARALLEL-EXECUTION-AUTOMATION_11.md
  - SUBPLAN_PARALLEL-EXECUTION-AUTOMATION_12.md
  - SUBPLAN_PARALLEL-EXECUTION-AUTOMATION_13.md

⏭️  Skipped 1 (already exist):
  - Achievement 1.4

❌ Errors (1):
  - Achievement 2.1: Invalid achievement format
```

---

## 🔗 Dependencies

### Requires (from previous achievements):
- Achievement 2.1: `parallel_workflow.py`, `generate_prompt.py` enhanced ✅
- Achievement 1.3: `validate_parallel_json.py` (for validation) ✅
- Achievement 1.1: `parallel_prompt_builder.py` (for prompt generation) ✅

### Enables (for future achievements):
- Achievement 2.3: Batch EXECUTION Creation (similar pattern)

### External Dependencies:
- Python 3.8+ (existing)
- Git (for rollback strategy)
- No new external libraries needed

---

## ✅ Definition of Done

**Code Complete**:
- [ ] `batch_subplan.py` created (~350 lines)
- [ ] `batch_rollback.py` created (~150 lines)
- [ ] `generate_subplan_prompt.py` enhanced (~100 new lines)
- [ ] `parallel_workflow.py` enhanced (~50 new lines)
- [ ] `test_batch_subplan.py` created (~400 lines)
- [ ] `documentation/batch-subplan-creation.md` created (~200 lines)

**Tests Complete**:
- [ ] 30+ tests written and passing
- [ ] >90% coverage for new code
- [ ] Integration tests pass
- [ ] Rollback scenarios tested

**Quality Complete**:
- [ ] No linter errors
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] Error messages clear and actionable

**Integration Complete**:
- [ ] Works with `generate_subplan_prompt.py --batch`
- [ ] Works with `generate_subplan_prompt.py --batch --dry-run`
- [ ] Works with parallel menu option 1
- [ ] Backward compatible (no breaking changes)

**Documentation Complete**:
- [ ] Usage examples documented
- [ ] Safety features explained
- [ ] Rollback strategy documented
- [ ] Troubleshooting guide complete

---

**Status**: 📋 Ready for Execution  
**Next Step**: Create `EXECUTION_TASK_PARALLEL-EXECUTION-AUTOMATION_22_01.md` and execute work  
**Executor**: Begin with Phase 1 (Core Batch Logic)


