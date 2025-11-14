# EXECUTION_ANALYSIS: Batch SUBPLAN Fill Prompt Feature

**Type**: EXECUTION_ANALYSIS (Planning-Strategy)  
**Date**: 2025-11-14  
**Status**: 🎯 DESIGN PHASE  
**Context**: Post batch-creation workflow enhancement

---

## 🎯 Problem Statement

### Current Situation

After batch SUBPLAN creation, users get placeholder files like:

```markdown
# SUBPLAN: Achievement 5.1

**Status**: 📋 Design Phase (Batch Created - Needs Content)

## 🎯 Objective
[TO BE FILLED: Objective from PLAN Achievement 5.1]

## 📦 Deliverables
[TO BE FILLED: List of deliverables]
...
```

**User Challenge**: How to fill these placeholders efficiently?

**Current Options**:
1. Fill manually (slow, tedious for 6+ SUBPLANs)
2. Use `generate_prompt.py` for each achievement individually (repetitive)
3. No guidance on what to do next

**Gap**: No streamlined way to generate content for multiple placeholder SUBPLANs at once.

---

## 🎯 Proposed Solution

### Feature: Batch SUBPLAN Fill Prompt Generator

**Purpose**: Generate a single LLM prompt that creates content for ALL placeholder SUBPLANs in one go.

**Key Characteristics**:
- **Batch-aware**: Handles multiple SUBPLANs in one prompt
- **Context-rich**: Includes PLAN context, achievement details
- **Streamlined**: Less guidance than single SUBPLAN (essential only)
- **Efficient**: One LLM call fills all placeholders

---

## 💡 User Experience Design

### Flow Option A: Immediate (Right After Batch Creation)

**Scenario**: User just created 6 placeholder SUBPLANs

```
🔨 Creating SUBPLANs...
  ✅ Created: SUBPLAN_..._51.md
  ✅ Created: SUBPLAN_..._52.md
  ...

✅ Created 6 SUBPLANs

💡 NEXT STEP: Fill placeholder content

Would you like to generate a prompt to fill these SUBPLANs? (y/N): y

📝 Generating batch fill prompt...

════════════════════════════════════════════════════════════════════════════════
BATCH SUBPLAN FILL PROMPT
════════════════════════════════════════════════════════════════════════════════

You are tasked with filling 6 placeholder SUBPLAN files for the 
GRAPHRAG-OBSERVABILITY-VALIDATION plan.

CONTEXT:
- Plan: GRAPHRAG-OBSERVABILITY-VALIDATION
- Achievements: 5.1, 5.2, 6.1, 6.2, 6.3, 7.1
- Files: All created as placeholders with [TO BE FILLED] markers

TASK:
For each achievement, extract the relevant information from the PLAN and 
create a complete SUBPLAN following the template structure.

[... detailed instructions ...]

════════════════════════════════════════════════════════════════════════════════

✅ Prompt generated!

Options:
  1. Copy to clipboard
  2. Save to file
  3. Display full prompt
  4. Back to menu

Select option (1-4):
```

### Flow Option B: Deferred (Access Later)

**Scenario**: User created SUBPLANs yesterday, wants to fill them now

```
🔀 Parallel Execution Menu
...
🎯 NEXT AVAILABLE:
   5.1: Performance Impact Measured (not_started)
   5.2: Storage Growth Analyzed (not_started)
   ...
   
   Status: SUBPLANs are placeholders - need content

💡 RECOMMENDED ACTION:
   Generate prompt to fill 6 placeholder SUBPLANs (option 7)

Options:
  1. Batch Create SUBPLANs (level 4: 5.1, 5.2, +4 more)
  2. Batch Create EXECUTIONs (for same level)
  3. Run Parallel Executions (multi-executor)
  4. View Dependency Graph
  5. Generate prompt for next available (5.1)
  6. Generate prompt to FILL placeholder SUBPLANs  ← NEW!
  7. Back to Main Menu
```

### Recommended: **Hybrid Approach**

**Immediate**: Offer right after batch creation (Option A)
**Deferred**: Also available in menu if placeholders detected (Option B)

**Rationale**: 
- Best UX: Offer when most relevant (right after creation)
- Flexibility: User can defer if needed
- Discoverability: Menu shows option when placeholders exist

---

## 📋 Prompt Design

### Key Differences from Single SUBPLAN Prompt

**Single SUBPLAN Prompt** (verbose, ~500 lines):
- Detailed SUBPLAN-WORKFLOW-GUIDE.md sections
- Step-by-step instructions
- Multiple examples
- Extensive templates

**Batch SUBPLAN Fill Prompt** (streamlined, ~200 lines):
- Essential structure only
- Concise instructions
- Focus on extraction from PLAN
- Batch processing guidance

### Prompt Structure

```
════════════════════════════════════════════════════════════════════════════════
BATCH SUBPLAN FILL PROMPT
════════════════════════════════════════════════════════════════════════════════

## CONTEXT

Plan: {PLAN_NAME}
Achievements: {ACHIEVEMENT_IDS}
Total SUBPLANs to fill: {COUNT}

Files to update:
  - {SUBPLAN_FILE_1}
  - {SUBPLAN_FILE_2}
  ...

## TASK

Fill the placeholder SUBPLANs with content extracted from the PLAN.

Each SUBPLAN should have:
1. Objective (from PLAN achievement description)
2. Deliverables (specific, measurable)
3. Approach (phases/steps)
4. Execution Strategy (single or multiple executions)
5. Testing Strategy (how to verify)
6. Expected Results (success criteria)

## PLAN CONTENT

[Relevant sections from PLAN for each achievement]

Achievement 5.1: Performance Impact Measured
---
{PLAN_CONTENT_5.1}

Achievement 5.2: Storage Growth Analyzed
---
{PLAN_CONTENT_5.2}

...

## INSTRUCTIONS

For each achievement:

1. Read the PLAN content for that achievement
2. Extract objective, deliverables, approach
3. Fill the SUBPLAN template sections
4. Ensure consistency with PLAN
5. Keep it concise but complete

## TEMPLATE STRUCTURE

Use this structure for each SUBPLAN:

```markdown
# SUBPLAN: Achievement {ID}

**PLAN**: {PLAN_NAME}
**Achievement**: {ID}
**Status**: 📋 Design Phase

## 🎯 Objective

[Clear, specific objective from PLAN]

## 📦 Deliverables

1. [Deliverable 1]
2. [Deliverable 2]
...

## 🔧 Approach

### Phase 1: [Phase Name]
- [Step 1]
- [Step 2]

### Phase 2: [Phase Name]
- [Step 1]
- [Step 2]

## 🔄 Execution Strategy

[Single execution or multiple? Parallel or sequential?]

## 🧪 Testing Strategy

[How to verify deliverables]

## 📊 Expected Results

[Success criteria]
```

## OUTPUT FORMAT

For each SUBPLAN, provide:

```
=== SUBPLAN_{PLAN_NAME}_{ACHIEVEMENT_ID}.md ===

[Complete SUBPLAN content]

=== END ===
```

## REFERENCE

- PLAN file: @{PLAN_FILE_PATH}
- SUBPLAN template: @LLM/templates/SUBPLAN-TEMPLATE.md
- Workflow guide: @LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md

════════════════════════════════════════════════════════════════════════════════
```

---

## 🛠️ Implementation Plan

### Phase 1: Create Prompt Generator Function (30 min)

**File**: `LLM/scripts/generation/batch_subplan_fill.py` (new)

**Functions**:
1. `generate_batch_fill_prompt(plan_path, achievement_ids)` - Main function
2. `extract_plan_content_for_achievement(plan_data, ach_id)` - Extract relevant PLAN sections
3. `format_batch_fill_prompt(plan_name, achievements, plan_content)` - Format prompt
4. `detect_placeholder_subplans(plan_path)` - Find SUBPLANs with [TO BE FILLED]

**Key Logic**:
```python
def generate_batch_fill_prompt(plan_path: Path, achievement_ids: List[str]) -> str:
    """Generate prompt to fill multiple placeholder SUBPLANs."""
    # Load PLAN
    plan_data = parse_plan_file(plan_path)
    
    # Extract content for each achievement
    plan_content = {}
    for ach_id in achievement_ids:
        plan_content[ach_id] = extract_plan_content_for_achievement(plan_data, ach_id)
    
    # Format prompt
    prompt = format_batch_fill_prompt(plan_name, achievement_ids, plan_content)
    
    return prompt
```

### Phase 2: Integrate into Batch Creation Flow (15 min)

**File**: `LLM/scripts/generation/parallel_workflow.py`

**Location**: After batch SUBPLAN creation success (line ~646)

**Changes**:
```python
# Create SUBPLANs (pass achievements, skip confirmation - already done above)
result = batch_create_subplans(
    plan_path, dry_run=False, achievements=next_avail, skip_confirmation=True
)
print("\n" + "=" * 80)
print(result)
print("=" * 80)

# NEW: Offer to generate fill prompt
if result.created:
    print("\n💡 NEXT STEP: Fill placeholder content")
    print()
    response = input("Would you like to generate a prompt to fill these SUBPLANs? (y/N): ").strip().lower()
    
    if response in ['y', 'yes']:
        from LLM.scripts.generation.batch_subplan_fill import generate_batch_fill_prompt
        
        achievement_ids = [a.get("achievement_id") for a in next_avail]
        prompt = generate_batch_fill_prompt(plan_path, achievement_ids)
        
        # Show options
        print("\n✅ Prompt generated!")
        print("\nOptions:")
        print("  1. Display full prompt")
        print("  2. Copy to clipboard")
        print("  3. Save to file")
        print("  4. Continue without prompt")
        print()
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == "1":
            print("\n" + "=" * 80)
            print(prompt)
            print("=" * 80)
        elif choice == "2":
            # Copy to clipboard (if pyperclip available)
            try:
                import pyperclip
                pyperclip.copy(prompt)
                print("✅ Copied to clipboard!")
            except ImportError:
                print("⚠️  pyperclip not installed. Displaying prompt instead:")
                print("\n" + "=" * 80)
                print(prompt)
                print("=" * 80)
        elif choice == "3":
            # Save to file
            output_file = plan_path / f"BATCH_FILL_PROMPT_{plan_name}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(prompt)
            print(f"✅ Saved to: {output_file}")
```

### Phase 3: Add Menu Option for Deferred Access (20 min)

**File**: `LLM/scripts/generation/parallel_workflow.py`

**Function**: `show_parallel_menu()`

**Changes**:
1. Detect placeholder SUBPLANs in state
2. Add option 6: "Generate prompt to FILL placeholder SUBPLANs"
3. Show only if placeholders detected

**Detection Logic**:
```python
# In get_parallel_menu_state()
placeholder_subplans = []
for ach in next_available:
    ach_id = ach.get("achievement_id")
    subplan_num = ach_id.replace(".", "")
    subplan_files = list(plan_path.glob(f"subplans/SUBPLAN_*_{subplan_num}.md"))
    
    if subplan_files:
        # Check if it's a placeholder
        with open(subplan_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
            if "[TO BE FILLED]" in content:
                placeholder_subplans.append(ach)

# Add to state
return {
    ...
    "placeholder_subplans": placeholder_subplans
}
```

**Menu Update**:
```python
# In show_parallel_menu()
if state and state.get("placeholder_subplans"):
    print(f"  6. Generate prompt to FILL {len(state['placeholder_subplans'])} placeholder SUBPLANs")
    print("  7. Back to Main Menu")
    max_option = "7"
else:
    print("  6. Back to Main Menu")
    max_option = "6"
```

### Phase 4: Testing (15 min)

**Test Cases**:
1. Create batch SUBPLANs → accept fill prompt → verify prompt quality
2. Create batch SUBPLANs → decline fill prompt → access later from menu
3. Menu shows option only when placeholders exist
4. Prompt includes all achievements
5. Prompt has correct PLAN content

---

## 📊 Prompt Content Specification

### Essential Elements (Must Include)

1. **Context Section**
   - Plan name
   - Achievement IDs
   - File names
   - Total count

2. **Task Description**
   - What to do
   - Expected output format
   - Quality criteria

3. **PLAN Content**
   - Relevant sections for each achievement
   - Extracted from PLAN file
   - Organized by achievement ID

4. **Template Structure**
   - SUBPLAN sections
   - Markdown format
   - Example structure

5. **Output Format**
   - How to separate SUBPLANs
   - File naming
   - Delimiters

6. **References**
   - PLAN file path
   - Template path
   - Workflow guide path

### Optional Elements (Nice to Have)

1. **Examples**
   - One filled SUBPLAN example
   - Show expected quality

2. **Tips**
   - Common pitfalls
   - Best practices

3. **Verification**
   - How to check completeness
   - Quality checklist

### Excluded Elements (Too Verbose for Batch)

1. ~~Detailed SUBPLAN-WORKFLOW-GUIDE.md sections~~
2. ~~Step-by-step phase instructions~~
3. ~~Multiple examples~~
4. ~~Extensive methodology explanations~~

**Rationale**: Keep prompt focused and concise for batch processing.

---

## 🎯 Success Criteria

### User Experience

- ✅ Offered immediately after batch creation
- ✅ Available in menu if placeholders exist
- ✅ Clear instructions
- ✅ Multiple output options (display, copy, save)
- ✅ Non-intrusive (can decline)

### Prompt Quality

- ✅ Includes all necessary context
- ✅ Extracts correct PLAN content
- ✅ Provides clear structure
- ✅ References templates
- ✅ Concise but complete (~200 lines)

### Technical

- ✅ Detects placeholder SUBPLANs correctly
- ✅ Handles multiple achievements
- ✅ Integrates seamlessly with batch creation
- ✅ No breaking changes to existing flow

---

## 📝 Example Prompt Output

```
════════════════════════════════════════════════════════════════════════════════
BATCH SUBPLAN FILL PROMPT
════════════════════════════════════════════════════════════════════════════════

## CONTEXT

Plan: GRAPHRAG-OBSERVABILITY-VALIDATION
Achievements: 5.1, 5.2, 6.1, 6.2, 6.3, 7.1
Total SUBPLANs to fill: 6

Files to update:
  - work-space/plans/GRAPHRAG-OBSERVABILITY-VALIDATION/subplans/SUBPLAN_GRAPHRAG-OBSERVABILITY-VALIDATION_51.md
  - work-space/plans/GRAPHRAG-OBSERVABILITY-VALIDATION/subplans/SUBPLAN_GRAPHRAG-OBSERVABILITY-VALIDATION_52.md
  - work-space/plans/GRAPHRAG-OBSERVABILITY-VALIDATION/subplans/SUBPLAN_GRAPHRAG-OBSERVABILITY-VALIDATION_61.md
  - work-space/plans/GRAPHRAG-OBSERVABILITY-VALIDATION/subplans/SUBPLAN_GRAPHRAG-OBSERVABILITY-VALIDATION_62.md
  - work-space/plans/GRAPHRAG-OBSERVABILITY-VALIDATION/subplans/SUBPLAN_GRAPHRAG-OBSERVABILITY-VALIDATION_63.md
  - work-space/plans/GRAPHRAG-OBSERVABILITY-VALIDATION/subplans/SUBPLAN_GRAPHRAG-OBSERVABILITY-VALIDATION_71.md

## TASK

Fill the placeholder SUBPLANs with content extracted from the PLAN.

Each SUBPLAN must include:
1. 🎯 Objective - Clear, specific goal from PLAN
2. 📦 Deliverables - Concrete, measurable outputs
3. 🔧 Approach - Phases and steps to achieve objective
4. 🔄 Execution Strategy - Single or multiple executions
5. 🧪 Testing Strategy - Verification approach
6. 📊 Expected Results - Success criteria

## PLAN CONTENT

### Achievement 5.1: Performance Impact Measured

**From PLAN**:
Measure and document the performance impact of GraphRAG observability features
on pipeline execution time, memory usage, and resource consumption.

**Details**:
- Baseline performance metrics
- Observability overhead measurement
- Resource consumption analysis
- Performance recommendations

### Achievement 5.2: Storage Growth Analyzed

**From PLAN**:
Analyze storage growth patterns for observability data (logs, metrics, traces)
and provide recommendations for retention policies and optimization.

**Details**:
- Storage growth rate measurement
- Data retention analysis
- Optimization strategies
- Cost-benefit analysis

[... continues for all achievements ...]

## TEMPLATE STRUCTURE

For each SUBPLAN, use this structure:

```markdown
# SUBPLAN: Achievement {ID}

**PLAN**: GRAPHRAG-OBSERVABILITY-VALIDATION
**Achievement**: {ID}
**Status**: 📋 Design Phase

## 🎯 Objective

[1-2 sentences: What will be achieved?]

## 📦 Deliverables

1. [Specific deliverable 1]
2. [Specific deliverable 2]
3. [Specific deliverable 3]

## 🔧 Approach

### Phase 1: [Phase Name]
- [Action 1]
- [Action 2]

### Phase 2: [Phase Name]
- [Action 1]
- [Action 2]

[Add more phases as needed]

## 🔄 Execution Strategy

**Execution Count**: [Single or Multiple]
**Reasoning**: [Why this approach?]

## 🧪 Testing Strategy

[How to verify deliverables are complete and correct]

## 📊 Expected Results

- ✅ [Success criterion 1]
- ✅ [Success criterion 2]
- ✅ [Success criterion 3]
```

## OUTPUT FORMAT

Provide each filled SUBPLAN in this format:

```
=== SUBPLAN_GRAPHRAG-OBSERVABILITY-VALIDATION_51.md ===

[Complete SUBPLAN content for 5.1]

=== END ===

=== SUBPLAN_GRAPHRAG-OBSERVABILITY-VALIDATION_52.md ===

[Complete SUBPLAN content for 5.2]

=== END ===

[... continue for all achievements ...]
```

## QUALITY CHECKLIST

For each SUBPLAN, ensure:
- [ ] Objective is clear and specific
- [ ] Deliverables are measurable
- [ ] Approach has concrete phases
- [ ] Execution strategy is justified
- [ ] Testing strategy is practical
- [ ] Expected results are verifiable

## REFERENCES

- PLAN: work-space/plans/GRAPHRAG-OBSERVABILITY-VALIDATION/PLAN_GRAPHRAG-OBSERVABILITY-VALIDATION.md
- Template: LLM/templates/SUBPLAN-TEMPLATE.md
- Guide: LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md

════════════════════════════════════════════════════════════════════════════════
```

---

## 🔗 Related Documentation

- `LLM/templates/SUBPLAN-TEMPLATE.md` - SUBPLAN structure
- `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` - SUBPLAN creation workflow
- `work-space/debug/EXECUTION_DEBUG_BATCH-SUBPLAN-DOUBLE-CONFIRMATION.md` - Batch creation fixes
- `LLM/guides/EXECUTION-TAXONOMY.md` - Documentation guidelines

---

## ✅ Status

**Status**: 🎯 DESIGN COMPLETE

**Next Steps**:
1. Implement Phase 1: Create `batch_subplan_fill.py`
2. Implement Phase 2: Integrate into batch creation flow
3. Implement Phase 3: Add menu option
4. Test end-to-end
5. Document in README

**Estimated Effort**: ~1.5 hours (4 phases)

---

**Design Complete**: 2025-11-14  
**Ready for Implementation**: YES ✅

