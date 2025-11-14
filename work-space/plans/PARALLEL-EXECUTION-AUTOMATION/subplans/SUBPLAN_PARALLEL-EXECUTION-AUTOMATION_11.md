# SUBPLAN: Achievement 1.1 - Parallel Discovery Prompt Created

**PLAN**: PARALLEL-EXECUTION-AUTOMATION  
**Achievement**: 1.1  
**Estimated Time**: 4-6 hours  
**Created**: 2025-11-13  
**Status**: 📋 Design Phase

---

## 🎯 Objective

Create a Python module (`parallel_prompt_builder.py`) that generates discovery prompts for analyzing PLANs to identify parallel execution opportunities. This module will follow the existing `prompt_builder.py` pattern, embedding prompt templates in code rather than markdown files, and will support the `--parallel-upgrade` flag workflow.

**Core Purpose**: Enable automated discovery of parallelizable achievements within a PLAN by generating structured prompts that guide LLMs through independence analysis and dependency tree creation.

**Success Definition**: A working Python module that generates discovery prompts, validates independence criteria, and produces valid `parallel.json` structures for 3 levels of parallelization.

---

## 📦 Deliverables

### 1. Core Module

**File**: `LLM/scripts/generation/parallel_prompt_builder.py`

**Contents**:

- `ParallelPromptBuilder` class (follows `PromptBuilder` pattern)
- Discovery prompt generation methods
- Independence validation criteria (embedded)
- Prompt templates as Python strings (not markdown files)
- Integration points with `generate_prompt.py`

**Size**: ~300-400 lines

**Key Methods**:

- `build_discovery_prompt(plan_path, level)` - Generate discovery prompt for specific parallelization level
- `build_independence_checklist()` - Return independence validation criteria
- `build_parallel_json_template()` - Return `parallel.json` schema structure
- `validate_independence(achievement_data)` - Validate independence criteria

### 2. Prompt Templates (Embedded in Code)

**Templates** (as Python strings in module):

- Level 1: Same Achievement Multi-Execution Discovery
- Level 2: Same Priority Achievement Discovery (Intra-Plan)
- Level 3: Different Priority Discovery (Cross-Priority)

**Each Template Includes**:

- PLAN context injection points
- Independence validation checklist
- Dependency tree structure guidance
- `parallel.json` output format

### 3. Independence Validation Criteria

**Criteria** (embedded in code):

- **Technical Independence**: No shared state, no file conflicts, no race conditions
- **Testing Independence**: Tests can run in parallel without interference
- **Mergeability**: Changes can be merged without conflicts
- **Dependency Clarity**: Clear dependency chain, no circular dependencies

**Format**: Python dict/dataclass with validation functions

### 4. Example Analysis

**Files**:

- `examples/parallel_analysis_graphrag_observability.md` (example 1)
- `examples/parallel_analysis_prompt_generator.md` (example 2)

**Contents**:

- PLAN analysis using generated prompts
- Identified parallel opportunities
- Generated `parallel.json` structures
- Independence validation results

**Purpose**: Demonstrate prompt effectiveness and validate approach

### 5. Schema Specification

**File**: `parallel-schema.json` (JSON Schema format)

**Contents**:

- JSON Schema for `parallel.json` structure
- Field definitions and constraints
- Status enum values
- Dependency relationship structure

**Integration**: Used by validation script (Achievement 1.3)

---

## 🔧 Approach

### Phase 1: Module Structure Setup (1 hour)

**Goal**: Create module skeleton following `prompt_builder.py` pattern

**Tasks**:

1. Create `parallel_prompt_builder.py` file
2. Define `ParallelPromptBuilder` class
3. Set up module docstring and imports
4. Create placeholder methods for all deliverables
5. Add type hints and basic error handling

**Reference**: Study `LLM/scripts/generation/prompt_builder.py` for pattern

**Output**: Module skeleton with all methods defined

### Phase 2: Prompt Template Development (2-3 hours)

**Goal**: Develop and embed prompt templates for 3 parallelization levels

**Tasks**:

1. **Level 1 Template** (Same Achievement Multi-Execution):

   - Identify execution-level parallelization within single achievement
   - Check for independent execution paths
   - Generate multi-execution structure

2. **Level 2 Template** (Same Priority Intra-Plan):

   - Identify achievements within same priority that can run in parallel
   - Validate independence criteria
   - Build dependency tree for priority level

3. **Level 3 Template** (Cross-Priority):
   - Identify achievements across priorities that can run in parallel
   - Handle complex dependency chains
   - Generate full PLAN parallel structure

**Template Structure** (for each level):

```python
def build_level_X_discovery_prompt(self, plan_path: Path, plan_data: Dict) -> str:
    """Generate Level X discovery prompt."""
    template = f"""
    Analyze PLAN for Level {X} parallelization opportunities.

    CONTEXT:
    - PLAN: {plan_path.name}
    - Achievements: {len(plan_data['achievements'])}
    - Current Status: {plan_data['status']}

    INDEPENDENCE CRITERIA:
    {self.build_independence_checklist()}

    ANALYSIS INSTRUCTIONS:
    [Level-specific analysis guidance]

    OUTPUT FORMAT:
    {self.build_parallel_json_template()}
    """
    return template
```

**Output**: 3 complete prompt templates embedded in code

### Phase 3: Independence Validation Logic (1 hour)

**Goal**: Implement independence validation criteria and helper functions

**Tasks**:

1. Define independence criteria as Python data structures
2. Create validation helper functions
3. Implement checklist generation
4. Add validation result formatting

**Independence Criteria Structure**:

```python
@dataclass
class IndependenceCriteria:
    technical: List[str]  # No shared state, no file conflicts, no race conditions
    testing: List[str]    # Tests can run in parallel
    mergeability: List[str]  # Changes can be merged without conflicts
    dependency: List[str]  # Clear dependency chain

    def validate(self, achievement_data: Dict) -> ValidationResult:
        """Validate achievement against criteria."""
        # Validation logic
```

**Output**: Working validation logic with clear criteria

### Phase 4: Schema Definition (30 minutes)

**Goal**: Define `parallel.json` schema structure

**Tasks**:

1. Create JSON Schema file
2. Define all required fields
3. Add field descriptions and constraints
4. Document status transitions
5. Add examples

**Schema Structure**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "plan_name": { "type": "string" },
    "parallelization_level": {
      "type": "string",
      "enum": ["level_1", "level_2", "level_3"]
    },
    "achievements": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "achievement_id": { "type": "string", "pattern": "^\\d+\\.\\d+$" },
          "dependencies": { "type": "array", "items": { "type": "string" } },
          "status": {
            "type": "string",
            "enum": [
              "not_started",
              "subplan_created",
              "execution_created",
              "in_progress",
              "complete",
              "failed",
              "skipped"
            ]
          }
        }
      }
    }
  }
}
```

**Output**: Complete JSON Schema file

### Phase 5: Example Analysis (1-1.5 hours)

**Goal**: Test prompts on 2 real PLANs and document results

**Tasks**:

1. Run discovery prompts on GRAPHRAG-OBSERVABILITY-VALIDATION plan
2. Run discovery prompts on PROMPT-GENERATOR-UX-AND-FOUNDATION plan
3. Document identified opportunities
4. Generate `parallel.json` structures
5. Validate independence criteria
6. Document lessons learned

**Output**: 2 example analysis documents with working `parallel.json` files

### Phase 6: Integration and Testing (30 minutes)

**Goal**: Ensure module integrates with existing workflow

**Tasks**:

1. Test import in `generate_prompt.py`
2. Verify method signatures match expected interface
3. Test prompt generation for all 3 levels
4. Validate JSON Schema
5. Check for circular imports
6. Run basic smoke tests

**Output**: Verified integration with no breaking changes

---

## 🎯 Execution Strategy

### Single Execution Approach

**Rationale**: This is a cohesive module creation task that benefits from single-pass implementation. All components are tightly coupled (templates reference criteria, criteria inform templates, schema structures both).

**Execution Plan**:

- **Single EXECUTION_TASK**: `EXECUTION_TASK_PARALLEL-EXECUTION-AUTOMATION_11_01.md`
- **Approach**: Sequential phase execution (1→2→3→4→5→6)
- **Duration**: 4-6 hours (as estimated)

**Why Not Multiple Executions**:

- Templates and criteria are interdependent
- Schema must align with template output format
- Examples validate the entire system together
- Context switching overhead would exceed benefits

### Execution Order

**Phase Sequence**:

1. Module Structure (foundation)
2. Prompt Templates (core functionality)
3. Independence Validation (quality gates)
4. Schema Definition (output format)
5. Example Analysis (validation)
6. Integration Testing (verification)

**Dependencies**:

- Phase 2 depends on Phase 1 (need module structure)
- Phase 3 can overlap with Phase 2 (criteria inform templates)
- Phase 4 depends on Phase 2 (schema matches template output)
- Phase 5 depends on Phases 2, 3, 4 (needs working system)
- Phase 6 depends on all previous phases (integration test)

---

## 🧪 Testing Requirements

### Unit Tests

**Not Required for This Achievement**: This is infrastructure/tooling code that will be validated through:

1. Example analysis (Phase 5) - demonstrates prompt effectiveness
2. Integration testing (Phase 6) - verifies module works in workflow
3. Achievement 1.3 will create comprehensive tests for validation logic

**Rationale**:

- Prompt templates are validated by usage, not unit tests
- Schema validation happens in Achievement 1.3
- Focus on working examples over test coverage for this foundational work

### Integration Tests

**Manual Integration Tests** (Phase 6):

1. Import module in `generate_prompt.py` - verify no errors
2. Generate Level 1 prompt - verify output format
3. Generate Level 2 prompt - verify output format
4. Generate Level 3 prompt - verify output format
5. Validate JSON Schema - verify schema is valid JSON Schema
6. Run example analysis - verify prompts produce useful results

**Success Criteria**:

- All imports work without errors
- All prompt generation methods return valid strings
- JSON Schema validates with JSON Schema validator
- Example analysis produces actionable insights

### Validation Tests

**Example Analysis Validation** (Phase 5):

1. Apply prompts to 2 real PLANs
2. Verify independence criteria can be evaluated
3. Verify `parallel.json` structures are valid
4. Verify identified opportunities are realistic
5. Document any edge cases or limitations

**Success Criteria**:

- At least 1 parallel opportunity identified per PLAN
- Generated `parallel.json` structures are valid JSON
- Independence criteria are clear and actionable
- No false positives (invalid parallel opportunities)

---

## 📊 Expected Results

### Deliverable Checklist

**Files Created**:

- ✅ `LLM/scripts/generation/parallel_prompt_builder.py` (~300-400 lines)
- ✅ `parallel-schema.json` (~100-150 lines)
- ✅ `examples/parallel_analysis_graphrag_observability.md` (~200-300 lines)
- ✅ `examples/parallel_analysis_prompt_generator.md` (~200-300 lines)

**Total**: 4 files, ~800-1,150 lines

### Functional Outcomes

**Prompt Generation**:

- ✅ 3 prompt templates embedded in code (Level 1, 2, 3)
- ✅ Dynamic prompt generation from PLAN data
- ✅ Independence validation checklist generation
- ✅ `parallel.json` template generation

**Independence Validation**:

- ✅ 4 independence criteria defined (technical, testing, mergeability, dependency)
- ✅ Validation helper functions implemented
- ✅ Clear, actionable criteria descriptions

**Schema Definition**:

- ✅ Complete JSON Schema for `parallel.json`
- ✅ All required fields defined
- ✅ Status enum documented
- ✅ Dependency structure specified

**Example Analysis**:

- ✅ 2 real PLANs analyzed
- ✅ Parallel opportunities identified
- ✅ `parallel.json` structures generated
- ✅ Independence validation demonstrated

### Integration Outcomes

**Workflow Integration**:

- ✅ Module importable in `generate_prompt.py`
- ✅ No breaking changes to existing workflow
- ✅ Ready for `--parallel-upgrade` flag implementation (Achievement 2.1)
- ✅ Schema ready for validation script (Achievement 1.3)

**Documentation Outcomes**:

- ✅ Module docstrings complete
- ✅ Method signatures documented
- ✅ Example usage demonstrated
- ✅ Independence criteria clearly defined

---

## 🎯 Success Criteria

### Must Have (Blocking)

1. **Module Created**: `parallel_prompt_builder.py` exists and is importable
2. **3 Prompt Templates**: Level 1, 2, 3 templates embedded in code
3. **Independence Criteria**: 4 criteria defined and documented
4. **JSON Schema**: `parallel-schema.json` is valid JSON Schema
5. **2 Examples**: Both example analyses complete with `parallel.json` outputs
6. **Integration Verified**: Module imports without errors in `generate_prompt.py`

### Should Have (Important)

1. **Clear Docstrings**: All methods have comprehensive docstrings
2. **Type Hints**: All methods have type hints
3. **Error Handling**: Basic error handling for invalid inputs
4. **Validation Functions**: Helper functions for independence validation
5. **Example Quality**: Examples demonstrate real parallel opportunities

### Nice to Have (Optional)

1. **Additional Examples**: More than 2 example analyses
2. **Visualization**: Dependency tree visualization helpers
3. **CLI Interface**: Standalone CLI for prompt generation
4. **Extended Criteria**: Additional independence validation criteria

---

## 🚧 Risks and Mitigations

### Risk 1: Prompt Template Effectiveness

**Risk**: Generated prompts may not effectively guide LLMs to identify parallel opportunities

**Likelihood**: Medium  
**Impact**: High (defeats purpose of module)

**Mitigation**:

- Test prompts on 2 real PLANs (Phase 5)
- Iterate on template wording based on results
- Include clear examples in prompts
- Provide structured output format

**Contingency**: Refine templates based on example analysis feedback

### Risk 2: Independence Criteria Too Strict/Loose

**Risk**: Criteria may be too strict (miss opportunities) or too loose (false positives)

**Likelihood**: Medium  
**Impact**: Medium (affects quality of parallel discovery)

**Mitigation**:

- Base criteria on real-world patterns from existing PLANs
- Validate criteria against known parallel/non-parallel cases
- Document edge cases and limitations
- Plan for criteria refinement in future iterations

**Contingency**: Adjust criteria based on example analysis results

### Risk 3: Schema Incompatibility

**Risk**: Schema may not support all parallelization scenarios

**Likelihood**: Low  
**Impact**: Medium (requires schema redesign)

**Mitigation**:

- Design schema to support all 3 levels
- Include extensibility points (optional fields)
- Validate schema against example `parallel.json` files
- Review schema with validation script requirements (Achievement 1.3)

**Contingency**: Extend schema with additional optional fields

### Risk 4: Integration Issues

**Risk**: Module may not integrate cleanly with existing workflow

**Likelihood**: Low  
**Impact**: High (blocks Achievement 2.1)

**Mitigation**:

- Follow existing `prompt_builder.py` pattern closely
- Test imports early (Phase 6)
- Avoid circular dependencies
- Use consistent naming conventions

**Contingency**: Refactor module structure if integration issues arise

---

## 📝 Notes and Considerations

### Design Decisions

**1. Code Over Configuration**

- **Decision**: Embed templates in Python code, not markdown files
- **Rationale**: Follows `prompt_builder.py` pattern, enables dynamic generation
- **Trade-off**: Less readable than markdown, but more flexible

**2. Single Module**

- **Decision**: All functionality in one module (`parallel_prompt_builder.py`)
- **Rationale**: Cohesive functionality, easier to maintain
- **Trade-off**: Larger file, but still manageable (~300-400 lines)

**3. 3 Parallelization Levels**

- **Decision**: Support Level 1 (same achievement), Level 2 (same priority), Level 3 (cross-priority)
- **Rationale**: Covers all identified parallelization scenarios
- **Trade-off**: More complex, but comprehensive

**4. Filesystem-First Status**

- **Decision**: Status derived from filesystem (APPROVED files), not persisted to `parallel.json`
- **Rationale**: Aligns with existing methodology (Achievement 2.8)
- **Trade-off**: Status must be computed at runtime, but ensures single source of truth

### Implementation Patterns

**Prompt Builder Pattern** (from `prompt_builder.py`):

```python
class ParallelPromptBuilder:
    """Build parallel discovery prompts."""

    def build_discovery_prompt(self, plan_path: Path, level: int) -> str:
        """Generate discovery prompt for specified level."""
        if level == 1:
            return self._build_level_1_prompt(plan_path)
        elif level == 2:
            return self._build_level_2_prompt(plan_path)
        elif level == 3:
            return self._build_level_3_prompt(plan_path)
        else:
            raise ValueError(f"Invalid level: {level}")

    def _build_level_1_prompt(self, plan_path: Path) -> str:
        """Build Level 1 (same achievement) prompt."""
        # Template as Python f-string
        return f"""..."""
```

**Independence Validation Pattern**:

```python
@dataclass
class IndependenceCriteria:
    technical: List[str]
    testing: List[str]
    mergeability: List[str]
    dependency: List[str]

    def to_checklist(self) -> str:
        """Format as markdown checklist."""
        # Generate markdown checklist
```

### Future Enhancements

**Not in Scope for 1.1** (defer to future work):

1. Automatic parallel opportunity detection (requires LLM integration)
2. Dependency graph visualization
3. Parallel execution simulation
4. Performance prediction
5. Rollback/recovery mechanisms

**Rationale**: Focus on foundational prompt generation infrastructure first. Advanced features can be added incrementally.

### Dependencies

**Depends On**:

- None (this is the first achievement)

**Blocks**:

- Achievement 1.2 (needs schema definition)
- Achievement 1.3 (needs schema for validation)
- Achievement 2.1 (needs prompt builder for `--parallel-upgrade`)

**Critical Path**: This achievement is on the critical path - must complete before any other Priority 1 work.

---

## 🔄 Execution Workflow

### For Executor

**Step 1: Read This SUBPLAN**

- Understand objective and approach
- Review deliverables checklist
- Note success criteria

**Step 2: Read EXECUTION_TASK**

- File: `EXECUTION_TASK_PARALLEL-EXECUTION-AUTOMATION_11_01.md`
- Follow phase-by-phase instructions
- Track progress in iteration log

**Step 3: Execute Phases Sequentially**

- Phase 1: Module Structure Setup (1h)
- Phase 2: Prompt Template Development (2-3h)
- Phase 3: Independence Validation Logic (1h)
- Phase 4: Schema Definition (30min)
- Phase 5: Example Analysis (1-1.5h)
- Phase 6: Integration and Testing (30min)

**Step 4: Verify Deliverables**

- Check all 4 files created
- Verify integration works
- Validate examples produce useful results

**Step 5: Update EXECUTION_TASK**

- Mark phases complete
- Document any issues or learnings
- Update status to "Complete"

**Step 6: Request Review**

- Notify reviewer that work is complete
- Provide summary of deliverables
- Highlight any deviations from SUBPLAN

---

## ✅ Definition of Done

**Achievement 1.1 is complete when**:

1. ✅ `parallel_prompt_builder.py` module created and importable
2. ✅ 3 prompt templates embedded in code (Level 1, 2, 3)
3. ✅ Independence validation criteria defined and documented
4. ✅ `parallel-schema.json` created and valid
5. ✅ 2 example analyses complete with `parallel.json` outputs
6. ✅ Integration verified (imports work, no errors)
7. ✅ All deliverables listed in "Expected Results" section exist
8. ✅ EXECUTION_TASK marked complete with iteration log
9. ✅ APPROVED_11.md created after review

**Ready for Next Achievement**: Achievement 1.2 (parallel.json Schema Implemented) can start immediately after 1.1 is approved, as it depends on the schema definition from 1.1.

---

**SUBPLAN Status**: 📋 Ready for Execution  
**Next Step**: Create EXECUTION_TASK_PARALLEL-EXECUTION-AUTOMATION_11_01.md  
**Estimated Duration**: 4-6 hours
