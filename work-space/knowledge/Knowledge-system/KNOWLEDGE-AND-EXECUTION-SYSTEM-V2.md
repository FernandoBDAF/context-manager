# Knowledge and Execution System v2.0

**Version**: 2.0  
**Status**: 🚧 Proposal (Refining Current System)  
**Created**: 2025-11-13  
**Purpose**: Define unified knowledge production and execution tracking system for LLM-assisted development

---

## 🎯 Executive Summary

This document proposes a refined taxonomy for knowledge production and execution tracking, building on lessons from 200+ hours of real usage across 10+ plans.

**Key Changes from v1.0**:

1. **Simplified Naming**: `KW_` (knowledge) and `EXE_` (execution) prefixes
2. **Context-Aware Paths**: Documents stored by scope (global, plan, subplan)
3. **Entry Point System**: User specifies intent, LLM selects appropriate type
4. **Automation-Ready**: Clear triggers for knowledge creation vs execution
5. **Reduced Overhead**: Guidelines to prevent document explosion

**Core Principle**: **Knowledge documents are expensive** - create them strategically, not reflexively.

---

## 📊 Current State Analysis

### What's Working (Keep)

**From 200+ hours of usage**:

1. **Achievement-based progress** - Clear milestones, easy tracking
2. **Feedback system** - Filesystem-first completion detection (APPROVED_XX.md)
3. **Nested structure** - Plans contain subplans contain executions
4. **Test-driven workflow** - Quality first, prevents regressions
5. **Knowledge preservation** - Case studies, analyses capture learnings

### What's Problematic (Fix)

**Pain Points Identified**:

1. **Naming Confusion**: `EXECUTION_ANALYSIS` vs `EXECUTION_TASK` vs `EXECUTION_DEBUG`
   - Users don't know which to create
   - Automation can't reliably detect document type
   - Inconsistent prefixes across 5+ types

2. **Document Explosion**: 87 documents in `analyses/` folder alone
   - Many are one-time investigations
   - Unclear when to create vs when to skip
   - No guidelines for "knowledge worth preserving"

3. **Path Ambiguity**: Where does knowledge live?
   - Global? (`work-space/knowledge/`)
   - Plan-scoped? (`work-space/plans/FEATURE/knowledge/`)
   - Subplan-scoped? (`work-space/plans/FEATURE/subplans/XX/knowledge/`)

4. **Type Selection**: User must choose type upfront
   - "Is this an ANALYSIS or a CASE_STUDY?"
   - "Should I create DEBUG or ANALYSIS?"
   - Cognitive overhead before work even starts

5. **Automation Gap**: Scripts can't determine intent
   - No clear trigger: "When should I create knowledge?"
   - No clear routing: "Which template should I use?"
   - Manual intervention required

---

## 🎯 Proposed Solution: v2.0 System

### Core Concepts

**1. Two Document Categories**:

```
KW_  (Knowledge)  - Strategic, preserved, expensive to create
EXE_ (Execution)  - Tactical, transient, cheap to create
```

**2. Entry Point System**:

```
User Intent → LLM Selection → Template Application

User says: "I need to understand X"
LLM determines: Is this knowledge (KW_) or execution (EXE_)?
LLM selects: Which specific type? (ANALYSIS, DEBUG, TASK, WORK)
```

**3. Context-Aware Paths**:

```
Scope determines path, not name:

Global:  work-space/knowledge/KW_TYPE_SUBJECT.md
Plan:    work-space/plans/FEATURE/knowledge/KW_TYPE_SUBJECT.md
Subplan: work-space/plans/FEATURE/subplans/XX/knowledge/KW_TYPE_SUBJECT.md
```

**4. Strategic Knowledge Creation**:

```
Knowledge is expensive - create only when:
✅ Reusable across multiple contexts
✅ Informs future architectural decisions
✅ Captures non-obvious patterns
✅ Documents complex debugging journey
❌ One-time investigation (use EXE_WORK instead)
❌ Simple bug fix (document in EXECUTION_TASK)
❌ Routine implementation (track in EXECUTION_TASK)
```

---

## 📋 Document Type Taxonomy

### KW_ (Knowledge Documents)

**Purpose**: Strategic knowledge preservation for future reference

**Types** (5 categories):

#### 1. KW_ANALYSIS_*

**When**: Structured investigation requiring evidence and recommendations

**Characteristics**:
- Problem definition with context
- Evidence-based findings
- Root cause analysis
- Actionable recommendations
- 300-1000 lines

**Subcategories**:
- `KW_ANALYSIS_BUG_*` - Root cause of complex bugs
- `KW_ANALYSIS_METHODOLOGY_*` - Process and workflow assessment
- `KW_ANALYSIS_IMPLEMENTATION_*` - Code/feature quality review
- `KW_ANALYSIS_PROCESS_*` - System and workflow analysis
- `KW_ANALYSIS_STRATEGY_*` - Strategic planning and roadmaps

**Example**: `KW_ANALYSIS_BUG_ENTITY-RESOLUTION-RACE-CONDITION.md`

**Trigger Scenarios**:
- ✅ Bug affects multiple components
- ✅ Root cause non-obvious, requires investigation
- ✅ Solution informs future architecture
- ❌ Simple bug (use EXE_TASK iteration instead)

#### 2. KW_CASE-STUDY_*

**When**: Deep dive into feature/pattern with extractable lessons

**Characteristics**:
- Real example from codebase
- Pattern identification and extraction
- Generalizable insights
- Practical guidance for similar situations
- 400-1200 lines

**Example**: `KW_CASE-STUDY_FILESYSTEM-STATE-MANAGEMENT.md`

**Trigger Scenarios**:
- ✅ Implementation demonstrates reusable pattern
- ✅ Approach applicable to other features
- ✅ Lessons learned worth preserving
- ❌ Routine implementation (track in EXE_TASK)

#### 3. KW_OBSERVATION_*

**When**: Real-time discoveries during work worth preserving

**Characteristics**:
- Informal findings
- Immediate insights
- Quick feedback
- May evolve into ANALYSIS later
- 100-400 lines

**Example**: `KW_OBSERVATION_GRAPHRAG-BEHAVIOR_2025-11-13.md`

**Trigger Scenarios**:
- ✅ Unexpected behavior discovered
- ✅ Performance characteristics observed
- ✅ User experience insights
- ❌ Expected behavior (no document needed)

#### 4. KW_REVIEW_*

**When**: Post-completion assessment of implementation quality

**Characteristics**:
- Quality evaluation
- Requirements verification
- Gap identification
- Improvement suggestions
- 300-800 lines

**Example**: `KW_REVIEW_AUTHENTICATION-IMPLEMENTATION.md`

**Trigger Scenarios**:
- ✅ Major feature completed, needs assessment
- ✅ Multiple achievements need holistic review
- ✅ Quality concerns identified
- ❌ Single achievement (use APPROVED_XX.md feedback)

#### 5. KW_DEBUG_*

**When**: Complex debugging journey worth documenting

**Characteristics**:
- Deep investigation steps
- Reproduction process
- Root cause discovery
- Solution documentation
- 300-1000 lines

**Example**: `KW_DEBUG_CIRCULAR-REFERENCE-BUG.md`

**Trigger Scenarios**:
- ✅ Bug took >2 hours to debug
- ✅ Solution non-obvious, required experimentation
- ✅ Similar bugs likely in future
- ❌ Quick fix (<30 min, document in EXE_TASK)

---

### EXE_ (Execution Documents)

**Purpose**: Tactical execution tracking (transient, task-focused)

**Types** (2 categories):

#### 1. EXE_TASK_*

**When**: Implementing a SUBPLAN achievement

**Characteristics**:
- Connected to specific SUBPLAN
- Iteration tracking with TDD workflow
- <200 lines (hard limit)
- Deleted when SUBPLAN archived
- Location: `work-space/plans/FEATURE/execution/`

**Naming**: `EXE_TASK_<FEATURE>_<SUBPLAN>_<EXEC>.md`

**Example**: `EXE_TASK_PROMPT-GENERATOR_22_01.md`

**Trigger Scenarios**:
- ✅ SUBPLAN ready to execute
- ✅ Achievement has clear deliverables
- ✅ Implementation journey needs tracking
- ❌ No SUBPLAN (use EXE_WORK instead)

#### 2. EXE_WORK_*

**When**: Ad-hoc work not connected to SUBPLAN

**Characteristics**:
- Standalone, not SUBPLAN-connected
- Quick investigations, experiments
- 50-200 lines
- Location: `work-space/worker/`

**Naming**: `EXE_WORK_<SUBJECT>.md`

**Example**: `EXE_WORK_QUICK-BUG-FIX-CLIPBOARD.md`

**Trigger Scenarios**:
- ✅ Quick bug fix needed
- ✅ Small experiment or spike
- ✅ One-time investigation
- ❌ Reusable knowledge (use KW_ instead)

---

## 🗂️ File Organization System

### Path Structure by Scope

**Global Knowledge** (cross-project insights):

```
work-space/knowledge/
├── KW_ANALYSIS_BUG_*.md
├── KW_ANALYSIS_METHODOLOGY_*.md
├── KW_CASE-STUDY_*.md
├── KW_OBSERVATION_*.md
├── KW_REVIEW_*.md
└── KW_DEBUG_*.md
```

**Plan-Scoped Knowledge** (specific to one PLAN):

```
work-space/plans/FEATURE/
├── PLAN_FEATURE.md
├── knowledge/
│   ├── KW_ANALYSIS_*.md
│   ├── KW_CASE-STUDY_*.md
│   └── KW_DEBUG_*.md
├── subplans/
│   └── SUBPLAN_FEATURE_XX.md
└── execution/
    ├── EXE_TASK_FEATURE_XX_01.md
    └── feedbacks/
        └── APPROVED_XX.md
```

**Subplan-Scoped Knowledge** (specific to one SUBPLAN):

```
work-space/plans/FEATURE/subplans/XX/
├── SUBPLAN_FEATURE_XX.md
├── knowledge/
│   ├── KW_ANALYSIS_*.md
│   └── KW_DEBUG_*.md
└── (no execution/ - lives in parent plan)
```

**Ad-hoc Execution Work**:

```
work-space/worker/
└── EXE_WORK_*.md
```

---

## 🎯 Entry Point System (User Intent → LLM Selection)

### How It Works

**User doesn't specify document type** - they specify intent:

```
User: "I need to understand why entity resolution is failing"

LLM Analysis:
1. Is this knowledge (preserve) or execution (transient)?
   → Knowledge (complex bug, worth documenting)

2. Which knowledge type?
   → KW_DEBUG (investigation journey)

3. What scope?
   → Plan-scoped (specific to GRAPHRAG-VALIDATION plan)

4. Create: work-space/plans/GRAPHRAG-VALIDATION/knowledge/KW_DEBUG_ENTITY-RESOLUTION-FAILURE.md
```

### Entry Point Categories

**1. Knowledge Entry Points**:

| User Intent | LLM Selects | Scope Determination |
|-------------|-------------|---------------------|
| "Understand why X is failing" | KW_DEBUG or KW_ANALYSIS_BUG | Where is X used? |
| "Document pattern from X" | KW_CASE-STUDY | Where is pattern applicable? |
| "Review X implementation" | KW_REVIEW | What does X belong to? |
| "Analyze X strategy" | KW_ANALYSIS_STRATEGY | What does X affect? |
| "Observe X behavior" | KW_OBSERVATION | What context is X in? |

**2. Execution Entry Points**:

| User Intent | LLM Selects | Path |
|-------------|-------------|------|
| "Implement achievement X.Y" | EXE_TASK | plan/execution/ |
| "Quick fix for X" | EXE_WORK | work-space/worker/ |
| "Experiment with X" | EXE_WORK | work-space/worker/ |

---

## 📐 Decision Framework

### When to Create Knowledge (KW_)

**Strategic Value Test** (must pass 2+ criteria):

1. **Reusability**: Will this inform future work?
2. **Complexity**: Did this take >2 hours to understand?
3. **Non-Obvious**: Is the solution surprising or counterintuitive?
4. **Pattern**: Does this represent a generalizable pattern?
5. **Architecture**: Does this inform system design?

**If YES to 2+**: Create KW_ document  
**If NO**: Track in EXE_TASK or EXE_WORK

### When to Create Execution (EXE_)

**EXE_TASK** (SUBPLAN-connected):
- ✅ SUBPLAN exists and ready to execute
- ✅ Achievement has clear deliverables
- ✅ Implementation journey needs iteration tracking

**EXE_WORK** (Ad-hoc):
- ✅ Quick investigation (<2 hours)
- ✅ One-time fix or experiment
- ✅ No SUBPLAN connection

### Scope Determination

**Global** (`work-space/knowledge/`):
- Affects multiple plans
- Methodology or process insights
- Cross-cutting architectural patterns

**Plan-Scoped** (`plans/FEATURE/knowledge/`):
- Specific to one PLAN
- Feature-specific insights
- Plan-level architecture

**Subplan-Scoped** (`plans/FEATURE/subplans/XX/knowledge/`):
- Specific to one SUBPLAN
- Achievement-specific insights
- Rarely used (most knowledge is plan-scoped)

---

## 🤖 Automation Integration

### Prompt Generation System

**Current**: User runs `generate_prompt.py @PLAN_NAME`

**Proposed**: User specifies intent, automation routes

```bash
# Knowledge creation
python generate_prompt.py @PLAN_NAME --knowledge "understand entity resolution bug"

# Execution task
python generate_prompt.py @PLAN_NAME --execute 2.3

# Ad-hoc work
python generate_prompt.py --work "quick clipboard fix"
```

### LLM Routing Logic

**Step 1: Categorize Intent**

```python
def categorize_intent(user_message: str) -> str:
    """Determine if user wants knowledge or execution."""
    
    knowledge_keywords = ["understand", "analyze", "review", "document", 
                         "investigate", "why", "how does"]
    execution_keywords = ["implement", "fix", "create", "build", "add"]
    
    if any(kw in user_message.lower() for kw in knowledge_keywords):
        return "knowledge"
    elif any(kw in user_message.lower() for kw in execution_keywords):
        return "execution"
    else:
        # Default: ask user
        return "clarify"
```

**Step 2: Select Type**

```python
def select_knowledge_type(user_message: str, context: dict) -> str:
    """Determine specific knowledge type."""
    
    if "bug" in user_message or "failing" in user_message:
        if context.get("complexity") == "high":
            return "KW_DEBUG"
        else:
            return "KW_ANALYSIS_BUG"
    
    elif "pattern" in user_message or "document" in user_message:
        return "KW_CASE-STUDY"
    
    elif "review" in user_message or "assess" in user_message:
        return "KW_REVIEW"
    
    elif "observe" in user_message or "behavior" in user_message:
        return "KW_OBSERVATION"
    
    else:
        return "KW_ANALYSIS_STRATEGY"
```

**Step 3: Determine Scope**

```python
def determine_scope(context: dict) -> str:
    """Determine document scope."""
    
    if context.get("plan"):
        if context.get("subplan"):
            return f"plans/{context['plan']}/subplans/{context['subplan']}/knowledge/"
        else:
            return f"plans/{context['plan']}/knowledge/"
    else:
        return "knowledge/"  # Global
```

### Template Selection

**Automation provides context to LLM**:

```markdown
You are creating a KW_DEBUG document.

Template: LLM/templates/KW_DEBUG-TEMPLATE.md
Scope: Plan-scoped (GRAPHRAG-VALIDATION)
Path: work-space/plans/GRAPHRAG-VALIDATION/knowledge/

User Intent: "Understand why entity resolution is failing"

Create the document following the template structure.
```

---

## 📚 Template System

### Template Naming Convention

**Knowledge Templates**:
- `LLM/templates/KW_ANALYSIS-TEMPLATE.md` (base)
- `LLM/templates/KW_ANALYSIS_BUG-TEMPLATE.md` (specialized)
- `LLM/templates/KW_CASE-STUDY-TEMPLATE.md`
- `LLM/templates/KW_OBSERVATION-TEMPLATE.md`
- `LLM/templates/KW_REVIEW-TEMPLATE.md`
- `LLM/templates/KW_DEBUG-TEMPLATE.md`

**Execution Templates**:
- `LLM/templates/EXE_TASK-TEMPLATE.md`
- `LLM/templates/EXE_WORK-TEMPLATE.md`

### Template Structure

**All templates include**:

1. **Metadata Header**: Type, scope, created date, purpose
2. **Executive Summary**: Quick overview (3-5 sentences)
3. **Type-Specific Sections**: Varies by document type
4. **Recommendations**: Actionable next steps
5. **References**: Related documents and context

---

## 🎓 Migration from v1.0

### Naming Changes

| v1.0 | v2.0 | Rationale |
|------|------|-----------|
| `EXECUTION_ANALYSIS_*` | `KW_ANALYSIS_*` | Clearer category (knowledge) |
| `EXECUTION_CASE-STUDY_*` | `KW_CASE-STUDY_*` | Clearer category (knowledge) |
| `EXECUTION_OBSERVATION_*` | `KW_OBSERVATION_*` | Clearer category (knowledge) |
| `EXECUTION_DEBUG_*` | `KW_DEBUG_*` | Clearer category (knowledge) |
| `EXECUTION_REVIEW_*` | `KW_REVIEW_*` | Clearer category (knowledge) |
| `EXECUTION_TASK_*` | `EXE_TASK_*` | Shorter, clearer |
| N/A | `EXE_WORK_*` | New category for ad-hoc work |

### Path Changes

**v1.0** (Flat structure):
```
work-space/
├── analyses/
├── case-studies/
├── observations/
├── debug-logs/
└── execution/
```

**v2.0** (Context-aware):
```
work-space/
├── knowledge/           # Global
├── worker/              # Ad-hoc execution
└── plans/
    └── FEATURE/
        ├── knowledge/   # Plan-scoped
        └── execution/   # SUBPLAN-connected tasks
```

### Migration Script

```bash
# Migrate existing documents to v2.0 structure
python LLM/scripts/migration/migrate_to_v2.py --dry-run

# Apply migration
python LLM/scripts/migration/migrate_to_v2.py --apply
```

---

## 🎯 Guidelines for Preventing Document Explosion

### The "Knowledge is Expensive" Principle

**Every knowledge document costs**:
- 1-3 hours to create
- 30-60 min to read
- Maintenance overhead
- Discovery overhead (more docs = harder to find)

**Create knowledge only when**:
- Strategic value test passes (2+ criteria)
- Multiple people will benefit
- Pattern is non-obvious
- Complexity justifies documentation

### Quick Decision Tree

```
Need to document something?
│
├─ Will this inform future work? (YES/NO)
│  └─ YES: Continue
│  └─ NO: Skip or use EXE_WORK
│
├─ Did this take >2 hours? (YES/NO)
│  └─ YES: Continue
│  └─ NO: Skip or use EXE_WORK
│
├─ Is solution non-obvious? (YES/NO)
│  └─ YES: Create KW_ document ✅
│  └─ NO: Track in EXE_TASK
```

### Examples: Create vs Skip

**CREATE Knowledge**:
- ✅ Filesystem-based state management (architectural pattern)
- ✅ Entity resolution race condition (complex bug, 4 hours debug)
- ✅ Interactive mode implementation (reusable UX pattern)
- ✅ Module extraction methodology (generalizable approach)

**SKIP Knowledge** (use EXE_TASK or EXE_WORK):
- ❌ Fixed typo in variable name (trivial)
- ❌ Added validation to form field (routine)
- ❌ Updated dependency version (maintenance)
- ❌ Refactored function names (simple refactor)

---

## 📊 Success Metrics

**System Health Indicators**:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Knowledge creation rate | <5 per plan | Count KW_ docs per PLAN |
| Knowledge reuse rate | >50% referenced | Track references in new work |
| Document discovery time | <2 min | Time to find relevant doc |
| Automation routing accuracy | >90% | LLM selects correct type |
| User intent clarity | >80% | User doesn't need to clarify |

**Quality Indicators**:

- Knowledge documents cited in future work
- Execution tasks completed without knowledge creation
- Reduced debugging time (knowledge reuse)
- Faster onboarding (knowledge library)

---

## 🔄 Relationship to Existing System

### What Stays the Same

- **Achievement-based progress** - No change
- **Feedback system** - APPROVED_XX.md files unchanged
- **Nested structure** - Plans → Subplans → Executions
- **Test-driven workflow** - TDD still mandatory
- **Templates** - Updated but same structure

### What Changes

- **Naming convention** - `KW_` and `EXE_` prefixes
- **Path structure** - Context-aware (global, plan, subplan)
- **Entry points** - User intent, not document type
- **Automation** - Routing logic for type selection
- **Guidelines** - Explicit criteria for knowledge creation

### Backward Compatibility

**v1.0 documents still work**:
- Existing `EXECUTION_ANALYSIS_*` files readable
- Migration script available (optional)
- Templates support both naming conventions
- Scripts detect both v1.0 and v2.0 formats

---

## 🚀 Implementation Plan

### Phase 1: Templates (Week 1)

- Create `KW_*` templates (6 templates)
- Create `EXE_*` templates (2 templates)
- Update existing templates with v2.0 guidance

### Phase 2: Automation (Week 2)

- Implement intent categorization
- Implement type selection logic
- Implement scope determination
- Update `generate_prompt.py` with routing

### Phase 3: Migration (Week 3)

- Create migration script
- Test on sample plans
- Document migration process
- Provide rollback mechanism

### Phase 4: Documentation (Week 4)

- Update `LLM-METHODOLOGY.md`
- Update `EXECUTION-TAXONOMY.md`
- Create user guide
- Create automation guide

---

## 📚 Related Documentation

- `LLM-METHODOLOGY.md` - Overall methodology
- `EXECUTION-TAXONOMY.md` - Current taxonomy (v1.0)
- `LLM/templates/PROMPTS.md` - Prompt templates
- `LLM/guides/MULTIPLE-PLANS-PROTOCOL.md` - Multi-plan coordination

---

**Status**: 🚧 Proposal - Awaiting Review  
**Next Step**: Review with user, refine based on feedback  
**Implementation**: Pending approval


