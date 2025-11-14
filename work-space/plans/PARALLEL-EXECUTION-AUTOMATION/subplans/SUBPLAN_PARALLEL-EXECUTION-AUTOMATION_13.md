# SUBPLAN: Achievement 1.3 - Validation Script Created

**PLAN**: PARALLEL-EXECUTION-AUTOMATION  
**Achievement**: 1.3  
**Estimated Time**: 3-4 hours  
**Created**: 2025-11-13  
**Status**: 📋 Design Phase

---

## 🎯 Objective

Create validation and status detection scripts for `parallel.json` files that ensure structural integrity, detect circular dependencies, and derive achievement status from the filesystem. This establishes the validation foundation required for all parallel workflow automation (Achievements 2.1-2.3).

**Core Purpose**: Provide robust validation and read-only status detection that prevents invalid parallel.json files from breaking automation workflows while maintaining filesystem-first philosophy.

**Success Definition**: Two focused scripts that validate parallel.json structure/dependencies and derive status from filesystem, with >90% test coverage and clear error messages.

---

## 📦 Deliverables

### 1. Validation Script

**File**: `LLM/scripts/validation/validate_parallel_json.py` (~200 lines)

**Purpose**: Validate parallel.json structure and dependencies (validation only, no status)

**Functions**:
- `validate_parallel_json(file_path: Path) -> ValidationResult`
- `check_circular_dependencies(achievements: List[Dict]) -> List[List[str]]`
- `validate_schema(data: Dict) -> List[str]`
- `format_validation_errors(errors: List[str]) -> str`

**Validations**:
1. **Schema Validation**:
   - Required fields present (`plan_name`, `parallelization_level`, `achievements`)
   - Field types match schema (string, array, object)
   - Enum values valid (`parallelization_level`: level_1, level_2, level_3)
   - Achievement IDs match pattern (`^\d+\.\d+$`)

2. **Dependency Validation**:
   - All dependency IDs exist in achievements array
   - No circular dependencies (A→B→C→A)
   - Dependencies reference valid achievements

3. **Error Messages**:
   - Clear, actionable error descriptions
   - Line numbers (where possible)
   - Suggested fixes

**Does NOT**:
- Read or write status fields
- Modify parallel.json
- Check filesystem for APPROVED files

### 2. Status Detection Script

**File**: `LLM/scripts/validation/get_parallel_status.py` (~150 lines)

**Purpose**: Derive achievement status from filesystem (read-only, runtime)

**Functions**:
- `get_parallel_status(parallel_json_path: Path) -> Dict[str, str]`
- `get_achievement_status_from_filesystem(achievement_id: str, plan_name: str) -> str`
- `enrich_parallel_json_with_status(parallel_data: Dict) -> Dict`

**Status Detection Logic** (follows existing `get_achievement_status()` pattern):
```python
def get_achievement_status_from_filesystem(achievement_id: str, plan_name: str) -> str:
    """
    Derive status from filesystem (read-only).
    
    Status hierarchy (check in order):
    1. APPROVED file exists → "complete"
    2. FIX file exists → "failed"
    3. EXECUTION_TASK file exists → "execution_created"
    4. SUBPLAN file exists → "subplan_created"
    5. None of above → "not_started"
    """
    # Check for APPROVED file
    approved_path = f"execution/feedbacks/APPROVED_{achievement_id.replace('.', '')}.md"
    if approved_path.exists():
        return "complete"
    
    # Check for FIX file
    fix_path = f"execution/feedbacks/FIX_{achievement_id.replace('.', '')}.md"
    if fix_path.exists():
        return "failed"
    
    # Check for EXECUTION_TASK file
    execution_path = f"execution/EXECUTION_TASK_{plan_name}_{achievement_id.replace('.', '')}_01.md"
    if execution_path.exists():
        return "execution_created"
    
    # Check for SUBPLAN file
    subplan_path = f"subplans/SUBPLAN_{plan_name}_{achievement_id.replace('.', '')}.md"
    if subplan_path.exists():
        return "subplan_created"
    
    # Default
    return "not_started"
```

**Key Principle**: Status is **derived at runtime**, never persisted to parallel.json

### 3. Test Suite

**File**: `tests/LLM/scripts/validation/test_validate_parallel_json.py` (~250 lines)

**Test Coverage** (>90% target):

**Schema Validation Tests** (~80 lines):
- Valid parallel.json (all 3 levels)
- Missing required fields
- Invalid field types
- Invalid enum values
- Invalid achievement ID patterns
- Malformed JSON

**Circular Dependency Tests** (~70 lines):
- No dependencies (valid)
- Linear dependencies (A→B→C, valid)
- Simple cycle (A→B→A)
- Complex cycle (A→B→C→A)
- Multiple cycles
- Self-dependency (A→A)

**Error Message Tests** (~50 lines):
- Error formatting
- Actionable suggestions
- Clear descriptions

**Status Detection Tests** (~50 lines):
- Status detection from filesystem
- All status types (not_started, subplan_created, execution_created, complete, failed)
- Status enrichment (adds status to parallel.json data)
- Missing files (returns not_started)

### 4. Error Messages Documentation

**File**: `documentation/parallel-validation-errors.md` (~100 lines)

**Contents**:
- Common validation errors
- Error codes and meanings
- Suggested fixes for each error
- Examples of valid vs invalid parallel.json

---

## 🔧 Approach

### Phase 1: Validation Script Implementation (90 minutes)

**Goal**: Implement schema and dependency validation

**Steps**:

1. **Create Directory Structure** (5 min):
```bash
mkdir -p LLM/scripts/validation
touch LLM/scripts/validation/__init__.py
touch LLM/scripts/validation/validate_parallel_json.py
```

2. **Implement Schema Validation** (30 min):
```python
def validate_schema(data: Dict) -> List[str]:
    """Validate parallel.json against schema."""
    errors = []
    
    # Check required fields
    required_fields = ['plan_name', 'parallelization_level', 'achievements']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate parallelization_level enum
    if 'parallelization_level' in data:
        valid_levels = ['level_1', 'level_2', 'level_3']
        if data['parallelization_level'] not in valid_levels:
            errors.append(
                f"Invalid parallelization_level: {data['parallelization_level']}. "
                f"Must be one of: {', '.join(valid_levels)}"
            )
    
    # Validate achievements array
    if 'achievements' in data:
        if not isinstance(data['achievements'], list):
            errors.append("Field 'achievements' must be an array")
        else:
            for i, ach in enumerate(data['achievements']):
                # Validate achievement_id pattern
                if 'achievement_id' in ach:
                    if not re.match(r'^\d+\.\d+$', ach['achievement_id']):
                        errors.append(
                            f"Achievement {i}: Invalid achievement_id format: {ach['achievement_id']}. "
                            f"Must match pattern X.Y (e.g., 1.1, 2.3)"
                        )
                else:
                    errors.append(f"Achievement {i}: Missing required field 'achievement_id'")
                
                # Validate dependencies array
                if 'dependencies' not in ach:
                    errors.append(f"Achievement {i}: Missing required field 'dependencies'")
                elif not isinstance(ach['dependencies'], list):
                    errors.append(f"Achievement {i}: Field 'dependencies' must be an array")
    
    return errors
```

3. **Implement Circular Dependency Detection** (40 min):
```python
def check_circular_dependencies(achievements: List[Dict]) -> List[List[str]]:
    """
    Detect circular dependencies using DFS.
    
    Returns:
        List of cycles found (each cycle is a list of achievement IDs)
    """
    # Build adjacency list
    graph = {}
    for ach in achievements:
        ach_id = ach['achievement_id']
        deps = ach.get('dependencies', [])
        graph[ach_id] = deps
    
    # DFS to detect cycles
    cycles = []
    visited = set()
    rec_stack = set()
    
    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path.copy())
            elif neighbor in rec_stack:
                # Found cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)
        
        rec_stack.remove(node)
    
    for node in graph:
        if node not in visited:
            dfs(node, [])
    
    return cycles
```

4. **Implement Main Validation Function** (15 min):
```python
@dataclass
class ValidationResult:
    valid: bool
    errors: List[str]
    warnings: List[str]
    cycles: List[List[str]]

def validate_parallel_json(file_path: Path) -> ValidationResult:
    """
    Validate parallel.json file.
    
    Returns:
        ValidationResult with errors, warnings, and detected cycles
    """
    errors = []
    warnings = []
    cycles = []
    
    # Load JSON
    try:
        with open(file_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return ValidationResult(
            valid=False,
            errors=[f"Invalid JSON: {e.msg} at line {e.lineno}, column {e.colno}"],
            warnings=[],
            cycles=[]
        )
    except FileNotFoundError:
        return ValidationResult(
            valid=False,
            errors=[f"File not found: {file_path}"],
            warnings=[],
            cycles=[]
        )
    
    # Schema validation
    schema_errors = validate_schema(data)
    errors.extend(schema_errors)
    
    # Circular dependency detection
    if 'achievements' in data and isinstance(data['achievements'], list):
        cycles = check_circular_dependencies(data['achievements'])
        if cycles:
            for cycle in cycles:
                cycle_str = ' → '.join(cycle)
                errors.append(f"Circular dependency detected: {cycle_str}")
    
    # Dependency existence validation
    if 'achievements' in data:
        achievement_ids = {ach['achievement_id'] for ach in data['achievements'] if 'achievement_id' in ach}
        for ach in data['achievements']:
            if 'dependencies' in ach:
                for dep in ach['dependencies']:
                    if dep not in achievement_ids:
                        errors.append(
                            f"Achievement {ach.get('achievement_id', '?')}: "
                            f"Dependency '{dep}' not found in achievements list"
                        )
    
    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        cycles=cycles
    )
```

---

### Phase 2: Status Detection Script Implementation (60 minutes)

**Goal**: Implement read-only status detection from filesystem

**Steps**:

1. **Create Status Detection Script** (5 min):
```bash
touch LLM/scripts/validation/get_parallel_status.py
```

2. **Implement Status Detection Function** (40 min):
```python
def get_achievement_status_from_filesystem(
    achievement_id: str,
    plan_name: str,
    workspace_root: Path
) -> str:
    """
    Derive achievement status from filesystem (read-only).
    
    Follows filesystem-first philosophy: status is derived, not persisted.
    
    Args:
        achievement_id: Achievement ID (e.g., "1.1")
        plan_name: PLAN name (e.g., "PARALLEL-EXECUTION-AUTOMATION")
        workspace_root: Path to workspace root
    
    Returns:
        Status string: "not_started", "subplan_created", "execution_created",
                       "complete", "failed", "skipped"
    """
    ach_num = achievement_id.replace('.', '')
    plan_dir = workspace_root / "work-space" / "plans" / plan_name
    
    # Check for APPROVED file (terminal state)
    approved_path = plan_dir / "execution" / "feedbacks" / f"APPROVED_{ach_num}.md"
    if approved_path.exists():
        return "complete"
    
    # Check for FIX file
    fix_path = plan_dir / "execution" / "feedbacks" / f"FIX_{ach_num}.md"
    if fix_path.exists():
        return "failed"
    
    # Check for EXECUTION_TASK file
    execution_pattern = f"EXECUTION_TASK_{plan_name}_{ach_num}_*.md"
    execution_files = list((plan_dir / "execution").glob(execution_pattern))
    if execution_files:
        return "execution_created"
    
    # Check for SUBPLAN file
    subplan_path = plan_dir / "subplans" / f"SUBPLAN_{plan_name}_{ach_num}.md"
    if subplan_path.exists():
        return "subplan_created"
    
    # Check for SKIPPED file
    skipped_path = plan_dir / "execution" / f"SKIPPED_{ach_num}.md"
    if skipped_path.exists():
        return "skipped"
    
    # Default: not started
    return "not_started"

def get_parallel_status(parallel_json_path: Path) -> Dict[str, str]:
    """
    Get status for all achievements in parallel.json.
    
    Returns:
        Dict mapping achievement_id to status
    """
    with open(parallel_json_path) as f:
        data = json.load(f)
    
    plan_name = data['plan_name']
    workspace_root = parallel_json_path.parent.parent.parent  # Assumes standard structure
    
    status_map = {}
    for ach in data.get('achievements', []):
        ach_id = ach['achievement_id']
        status = get_achievement_status_from_filesystem(ach_id, plan_name, workspace_root)
        status_map[ach_id] = status
    
    return status_map

def enrich_parallel_json_with_status(parallel_data: Dict, workspace_root: Path) -> Dict:
    """
    Enrich parallel.json data with runtime status (read-only, not persisted).
    
    Args:
        parallel_data: Loaded parallel.json data
        workspace_root: Path to workspace root
    
    Returns:
        Enriched data with status fields (for display only, not for writing back)
    """
    plan_name = parallel_data['plan_name']
    
    # Create copy to avoid modifying original
    enriched = json.loads(json.dumps(parallel_data))
    
    for ach in enriched.get('achievements', []):
        ach_id = ach['achievement_id']
        status = get_achievement_status_from_filesystem(ach_id, plan_name, workspace_root)
        ach['status'] = status  # Add status for display
    
    return enriched
```

3. **Add CLI Interface** (15 min):
```python
def main():
    """CLI interface for status detection."""
    parser = argparse.ArgumentParser(description='Get parallel.json status from filesystem')
    parser.add_argument('parallel_json', type=Path, help='Path to parallel.json')
    parser.add_argument('--format', choices=['json', 'table'], default='table',
                       help='Output format')
    
    args = parser.parse_args()
    
    # Get status
    status_map = get_parallel_status(args.parallel_json)
    
    # Output
    if args.format == 'json':
        print(json.dumps(status_map, indent=2))
    else:
        # Table format
        print("Achievement Status (from filesystem):")
        print("-" * 40)
        for ach_id, status in status_map.items():
            print(f"{ach_id}: {status}")

if __name__ == '__main__':
    main()
```

---

### Phase 3: Testing (70 minutes)

**Goal**: Achieve >90% test coverage

**Steps**:

1. **Create Test Directory** (5 min):
```bash
mkdir -p tests/LLM/scripts/validation
touch tests/LLM/scripts/validation/__init__.py
touch tests/LLM/scripts/validation/test_validate_parallel_json.py
```

2. **Write Schema Validation Tests** (25 min):
```python
class TestSchemaValidation:
    def test_valid_level1_json(self):
        """Test valid level 1 parallel.json."""
        data = {
            "plan_name": "TEST-PLAN",
            "parallelization_level": "level_1",
            "achievements": [
                {
                    "achievement_id": "1.1",
                    "dependencies": [],
                    "status": "not_started"
                }
            ]
        }
        errors = validate_schema(data)
        assert len(errors) == 0
    
    def test_missing_required_field(self):
        """Test missing required field."""
        data = {
            "plan_name": "TEST-PLAN"
            # Missing parallelization_level and achievements
        }
        errors = validate_schema(data)
        assert len(errors) >= 2
        assert any("parallelization_level" in e for e in errors)
        assert any("achievements" in e for e in errors)
    
    def test_invalid_parallelization_level(self):
        """Test invalid parallelization_level."""
        data = {
            "plan_name": "TEST-PLAN",
            "parallelization_level": "invalid",
            "achievements": []
        }
        errors = validate_schema(data)
        assert any("parallelization_level" in e for e in errors)
    
    def test_invalid_achievement_id_format(self):
        """Test invalid achievement ID format."""
        data = {
            "plan_name": "TEST-PLAN",
            "parallelization_level": "level_1",
            "achievements": [
                {
                    "achievement_id": "invalid",  # Should be X.Y
                    "dependencies": []
                }
            ]
        }
        errors = validate_schema(data)
        assert any("achievement_id" in e and "format" in e for e in errors)
```

3. **Write Circular Dependency Tests** (25 min):
```python
class TestCircularDependencies:
    def test_no_dependencies(self):
        """Test achievements with no dependencies."""
        achievements = [
            {"achievement_id": "1.1", "dependencies": []},
            {"achievement_id": "1.2", "dependencies": []}
        ]
        cycles = check_circular_dependencies(achievements)
        assert len(cycles) == 0
    
    def test_linear_dependencies(self):
        """Test linear dependency chain (no cycle)."""
        achievements = [
            {"achievement_id": "1.1", "dependencies": []},
            {"achievement_id": "1.2", "dependencies": ["1.1"]},
            {"achievement_id": "1.3", "dependencies": ["1.2"]}
        ]
        cycles = check_circular_dependencies(achievements)
        assert len(cycles) == 0
    
    def test_simple_cycle(self):
        """Test simple cycle: A→B→A."""
        achievements = [
            {"achievement_id": "1.1", "dependencies": ["1.2"]},
            {"achievement_id": "1.2", "dependencies": ["1.1"]}
        ]
        cycles = check_circular_dependencies(achievements)
        assert len(cycles) > 0
        # Check cycle contains both 1.1 and 1.2
        assert any("1.1" in cycle and "1.2" in cycle for cycle in cycles)
    
    def test_complex_cycle(self):
        """Test complex cycle: A→B→C→A."""
        achievements = [
            {"achievement_id": "1.1", "dependencies": ["1.2"]},
            {"achievement_id": "1.2", "dependencies": ["1.3"]},
            {"achievement_id": "1.3", "dependencies": ["1.1"]}
        ]
        cycles = check_circular_dependencies(achievements)
        assert len(cycles) > 0
    
    def test_self_dependency(self):
        """Test self-dependency: A→A."""
        achievements = [
            {"achievement_id": "1.1", "dependencies": ["1.1"]}
        ]
        cycles = check_circular_dependencies(achievements)
        assert len(cycles) > 0
```

4. **Write Status Detection Tests** (15 min):
```python
class TestStatusDetection:
    def test_not_started_status(self, tmp_path):
        """Test not_started status (no files exist)."""
        status = get_achievement_status_from_filesystem("1.1", "TEST-PLAN", tmp_path)
        assert status == "not_started"
    
    def test_subplan_created_status(self, tmp_path):
        """Test subplan_created status."""
        # Create SUBPLAN file
        plan_dir = tmp_path / "work-space" / "plans" / "TEST-PLAN" / "subplans"
        plan_dir.mkdir(parents=True)
        (plan_dir / "SUBPLAN_TEST-PLAN_11.md").touch()
        
        status = get_achievement_status_from_filesystem("1.1", "TEST-PLAN", tmp_path)
        assert status == "subplan_created"
    
    def test_complete_status(self, tmp_path):
        """Test complete status (APPROVED file exists)."""
        # Create APPROVED file
        feedback_dir = tmp_path / "work-space" / "plans" / "TEST-PLAN" / "execution" / "feedbacks"
        feedback_dir.mkdir(parents=True)
        (feedback_dir / "APPROVED_11.md").touch()
        
        status = get_achievement_status_from_filesystem("1.1", "TEST-PLAN", tmp_path)
        assert status == "complete"
```

---

### Phase 4: Documentation and Integration (20 minutes)

**Goal**: Document errors and create CLI

**Steps**:

1. **Create Error Documentation** (15 min):

Create `documentation/parallel-validation-errors.md` with:
- Common validation errors
- Error codes and meanings
- Suggested fixes
- Examples

2. **Add CLI to validate_parallel_json.py** (5 min):
```python
def main():
    """CLI interface for validation."""
    parser = argparse.ArgumentParser(description='Validate parallel.json file')
    parser.add_argument('parallel_json', type=Path, help='Path to parallel.json')
    parser.add_argument('--verbose', action='store_true', help='Show detailed errors')
    
    args = parser.parse_args()
    
    # Validate
    result = validate_parallel_json(args.parallel_json)
    
    if result.valid:
        print("✅ Validation passed!")
        return 0
    else:
        print("❌ Validation failed!")
        print(f"\nErrors ({len(result.errors)}):")
        for error in result.errors:
            print(f"  - {error}")
        
        if result.cycles:
            print(f"\nCircular Dependencies ({len(result.cycles)}):")
            for cycle in result.cycles:
                print(f"  - {' → '.join(cycle)}")
        
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

---

## 🔄 Execution Strategy

**Type**: Single EXECUTION

**Rationale**:
- Validation and status detection are tightly coupled (both work with parallel.json)
- Small scope (3-4 hours total)
- Foundation work best done atomically
- Single test pass validates both scripts

**Execution Order**:
1. Phase 1: Validation Script (90 min)
2. Phase 2: Status Detection Script (60 min)
3. Phase 3: Testing (70 min)
4. Phase 4: Documentation (20 min)

**Not Parallel**: Scripts have clear dependencies (validation → status detection → tests)

---

## 🧪 Testing Strategy

### Unit Tests (Priority)

**Location**: `tests/LLM/scripts/validation/`

**Test File**: `test_validate_parallel_json.py` (~250 lines)

**Test Coverage** (>90% target):

1. **Schema Validation Tests** (~80 lines):
   - Valid parallel.json (all 3 levels)
   - Missing required fields
   - Invalid field types
   - Invalid enum values
   - Invalid achievement ID patterns
   - Malformed JSON

2. **Circular Dependency Tests** (~70 lines):
   - No dependencies
   - Linear dependencies
   - Simple cycle (A→B→A)
   - Complex cycle (A→B→C→A)
   - Multiple cycles
   - Self-dependency

3. **Status Detection Tests** (~50 lines):
   - All status types
   - Status enrichment
   - Missing files

4. **Error Message Tests** (~50 lines):
   - Error formatting
   - Actionable suggestions

### Integration Tests

**Manual Verification**:
- Validate example files from Achievement 1.2
- Test with real PLAN directory structure
- Verify status detection matches filesystem

---

## 📊 Expected Results

### Files Created (4 new files)

**Source Files**:
1. `LLM/scripts/validation/__init__.py` (~10 lines)
2. `LLM/scripts/validation/validate_parallel_json.py` (~200 lines)
3. `LLM/scripts/validation/get_parallel_status.py` (~150 lines)

**Documentation**:
4. `documentation/parallel-validation-errors.md` (~100 lines)

**Test Files**:
5. `tests/LLM/scripts/validation/__init__.py` (~5 lines)
6. `tests/LLM/scripts/validation/test_validate_parallel_json.py` (~250 lines)

**Total Lines**: ~715 lines (source + tests + docs)

### Test Results

**Expected**:
- All tests pass (pytest exit code 0)
- Coverage >90%
- No linter errors
- All imports resolve

---

## ✅ Success Criteria

1. **Functionality**:
   - ✅ Validates JSON structure against schema
   - ✅ Detects circular dependencies
   - ✅ Provides actionable error messages
   - ✅ Read-only status detection from filesystem
   - ✅ Status derived at runtime, not persisted

2. **Quality**:
   - ✅ Test coverage >90%
   - ✅ All tests pass
   - ✅ No linter errors
   - ✅ Type hints present

3. **Documentation**:
   - ✅ Error messages documented
   - ✅ CLI help text clear
   - ✅ Usage examples provided

4. **Integration**:
   - ✅ Can validate example files from Achievement 1.2
   - ✅ Ready for Achievement 2.1 integration
   - ✅ Follows filesystem-first philosophy

---

## 🔗 Dependencies

**External**:
- Python 3.8+ (for type hints)
- pytest (for testing)
- jsonschema (optional, for schema validation)

**Internal**:
- Achievement 1.2 (needs parallel-schema.json and examples)

**Blocks**:
- Achievement 2.1 (generate_prompt.py needs validation)
- Achievement 2.2 (batch SUBPLAN needs validation)
- Achievement 2.3 (batch EXECUTION needs validation)

---

## 📚 References

**Project Patterns**:
- `LLM/scripts/generation/plan_parser.py` - Existing status detection patterns
- `LLM/scripts/generation/workflow_detector.py` - Filesystem-first philosophy
- `tests/LLM/scripts/generation/` - Existing test patterns

**Schema**:
- `parallel-schema.json` - JSON Schema for validation
- `documentation/parallel-schema-documentation.md` - Schema documentation

**Methodology**:
- `LLM/templates/SUBPLAN-TEMPLATE.md` - SUBPLAN structure
- `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` - Workflow guidance

---

## 🎯 Implementation Notes

**Key Design Principles**:
1. **Filesystem-First**: Status derived from filesystem, not persisted
2. **Read-Only**: Scripts never modify parallel.json
3. **Validation-Only**: Separate validation from status detection
4. **Clear Errors**: Actionable error messages with suggestions

**Common Pitfalls to Avoid**:
- ❌ Writing status to parallel.json (read-only!)
- ❌ Caching status (always derive from filesystem)
- ❌ Vague error messages (be specific and actionable)
- ❌ Over-validating (validate structure, not business logic)

**Success Indicators During Implementation**:
- Can detect circular dependencies in <1 second
- Error messages are immediately actionable
- Status detection matches manual filesystem check
- Tests run in <2 seconds

---

**Status**: 📋 Ready for Execution  
**Next**: Execute EXECUTION_TASK_PARALLEL-EXECUTION-AUTOMATION_13_01.md

