# Module Migration Guide (Achievement 2.6)

**Date**: 2025-11-12  
**Achievement**: 2.6 - Integrate Modules & Final Refactor  
**Audience**: Developers using extracted modules in other scripts

---

## 📖 Purpose

This guide shows how to use the extracted modules from `generate_prompt.py` in your own scripts. After Achievements 2.1-2.6, functionality has been organized into 5 specialized modules.

---

## 🎯 Quick Start

### Basic Import Pattern

```python
# Standard imports
from pathlib import Path
from LLM.scripts.generation.utils import Achievement, is_achievement_complete
from LLM.scripts.generation.plan_parser import PlanParser
from LLM.scripts.generation.workflow_detector import WorkflowDetector
from LLM.scripts.generation.prompt_builder import PromptBuilder

# Initialize modules
parser = PlanParser()
detector = WorkflowDetector()
builder = PromptBuilder()
```

---

## 📦 Module Usage Examples

### 1. Parse a PLAN File

```python
from pathlib import Path
from LLM.scripts.generation.plan_parser import PlanParser

plan_path = Path("work-space/plans/FEATURE/PLAN_FEATURE.md")
parser = PlanParser()

# Parse PLAN
plan_data = parser.parse_plan_file(plan_path)

# Access data
feature_name = plan_data["feature_name"]
achievements = plan_data["achievements"]  # List[Achievement]
archive_location = plan_data["archive_location"]

# Work with achievements
for ach in achievements:
    print(f"Achievement {ach.number}: {ach.title}")
    print(f"  Effort: {ach.effort}")
```

### 2. Check Achievement Completion

```python
from pathlib import Path
from LLM.scripts.generation.utils import is_achievement_complete

plan_path = Path("work-space/plans/FEATURE/PLAN_FEATURE.md")

# Check if achievement is complete (checks for APPROVED_XX.md file)
if is_achievement_complete("1.1", "", plan_path):
    print("✅ Achievement 1.1 is complete")
else:
    print("⏳ Achievement 1.1 is in progress")
```

### 3. Find Next Achievement

```python
from pathlib import Path
from LLM.scripts.generation.workflow_detector import WorkflowDetector
from LLM.scripts.generation.plan_parser import PlanParser

plan_path = Path("work-space/plans/FEATURE/PLAN_FEATURE.md")
parser = PlanParser()
detector = WorkflowDetector()

# Parse PLAN
plan_data = parser.parse_plan_file(plan_path)

# Find next incomplete achievement
next_ach = detector.find_next_achievement_hybrid(
    plan_path=plan_path,
    feature_name=plan_data["feature_name"],
    achievements=plan_data["achievements"],
    archive_location=plan_data["archive_location"]
)

if next_ach:
    print(f"Next: Achievement {next_ach.number} - {next_ach.title}")
else:
    print("✅ All achievements complete!")
```

### 4. Build a Prompt

```python
from pathlib import Path
from LLM.scripts.generation.prompt_builder import PromptBuilder
from LLM.scripts.generation.plan_parser import PlanParser

plan_path = Path("work-space/plans/FEATURE/PLAN_FEATURE.md")
parser = PlanParser()
builder = PromptBuilder()

# Get achievement data
plan_data = parser.parse_plan_file(plan_path)
achievement = plan_data["achievements"][0]  # First achievement

# Build prompt
prompt = builder.build_achievement_prompt(
    achievement_number=achievement.number,
    achievement_section="... achievement text ...",
    handoff_section="... handoff text ...",
    project_context="... context ...",
    validation_scripts=[]
)

print(prompt)
```

### 5. Extract PLAN Statistics

```python
from pathlib import Path
from LLM.scripts.generation.plan_parser import PlanParser

plan_path = Path("work-space/plans/FEATURE/PLAN_FEATURE.md")
parser = PlanParser()

# Extract statistics
stats = parser.extract_plan_statistics(plan_path, "FEATURE-NAME")

print(f"Total achievements: {stats['total_achievements']}")
print(f"SUBPLANs created: {stats['subplan_count']}")
print(f"EXECUTIONs completed: {stats['execution_count']}")
print(f"Total time: {stats['total_time']}")
```

---

## 🚨 Common Pitfalls

### Pitfall 1: Importing from Wrong Module

**❌ Wrong**:

```python
from LLM.scripts.generation.generate_prompt import Achievement
from LLM.scripts.generation.generate_prompt import is_achievement_complete
```

**✅ Correct**:

```python
from LLM.scripts.generation.utils import Achievement, is_achievement_complete
```

**Why**: These were moved to utils in Achievement 2.6 to break circular dependencies.

### Pitfall 2: Creating Circular Dependencies

**❌ Wrong**:

```python
# In my_new_module.py
from LLM.scripts.generation.generate_prompt import some_function

# In generate_prompt.py
from my_new_module import my_function
```

**✅ Correct**:

```python
# Use shared utils or create independent modules
from LLM.scripts.generation.utils import shared_function
```

### Pitfall 3: Parsing Markdown for State

**❌ Wrong**:

```python
# Checking for ✅ in PLAN markdown
if "✅ Achievement 1.1" in plan_content:
    achievement_complete = True
```

**✅ Correct**:

```python
# Use feedback system
from LLM.scripts.generation.utils import is_achievement_complete
achievement_complete = is_achievement_complete("1.1", "", plan_path)
```

### Pitfall 4: Duplicating Achievement Class

**❌ Wrong**:

```python
# Creating your own Achievement class
@dataclass
class Achievement:
    number: str
    title: str
```

**✅ Correct**:

```python
# Use the shared class
from LLM.scripts.generation.utils import Achievement
```

---

## 🔧 Migration Patterns

### Pattern 1: Update Old Imports

**If your script has**:

```python
from LLM.scripts.generation.generate_prompt import parse_plan_file
```

**Update to**:

```python
from LLM.scripts.generation.plan_parser import PlanParser
parser = PlanParser()
plan_data = parser.parse_plan_file(plan_path)
```

### Pattern 2: Use Module Instances

**Old style** (function calls):

```python
next_ach = find_next_achievement_hybrid(plan_path, ...)
```

**New style** (method calls):

```python
detector = WorkflowDetector()
next_ach = detector.find_next_achievement_hybrid(plan_path, ...)
```

### Pattern 3: Import Shared Utilities

**Always import from utils**:

```python
from LLM.scripts.generation.utils import (
    Achievement,           # Shared dataclass
    is_achievement_complete,  # Core feedback system function
    copy_to_clipboard_safe,   # Clipboard utility
    resolve_folder_shortcut,  # Path utility
)
```

---

## ✅ Validation

### Test Your Integration

**1. Check Imports**:

```python
# Run this to verify imports work
python3 -c "
from LLM.scripts.generation.utils import Achievement, is_achievement_complete
from LLM.scripts.generation.plan_parser import PlanParser
from LLM.scripts.generation.workflow_detector import WorkflowDetector
print('✅ All imports successful')
"
```

**2. Test Basic Functionality**:

```python
from pathlib import Path
from LLM.scripts.generation.plan_parser import PlanParser

plan_path = Path("work-space/plans/PROMPT-GENERATOR-UX-AND-FOUNDATION/PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md")
parser = PlanParser()
plan_data = parser.parse_plan_file(plan_path)
print(f"✅ Parsed {len(plan_data['achievements'])} achievements")
```

**3. Run Your Script's Tests**:

```bash
pytest tests/your_script/ -v
```

---

## 📚 Reference Quick Links

### Module Documentation

- **utils.py**: `LLM/scripts/generation/utils.py` - Shared utilities and dataclasses
- **plan_parser.py**: `LLM/scripts/generation/plan_parser.py` - PLAN file parsing
- **workflow_detector.py**: `LLM/scripts/generation/workflow_detector.py` - State detection
- **prompt_builder.py**: `LLM.scripts.generation.prompt_builder.py` - Prompt templates
- **interactive_menu.py**: `LLM/scripts/generation/interactive_menu.py` - UI menus

### System Documentation

- **Architecture**: `ARCHITECTURE_POST_REFACTOR.md`
- **Feedback System**: `LLM/docs/FEEDBACK_SYSTEM_GUIDE.md`
- **State Philosophy**: `LLM/docs/STATE_TRACKING_PHILOSOPHY.md`

---

**Last Updated**: 2025-11-12  
**Maintained by**: Achievement 2.6 - Integrate Modules & Final Refactor
