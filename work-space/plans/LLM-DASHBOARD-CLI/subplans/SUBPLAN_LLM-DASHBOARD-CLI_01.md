# SUBPLAN: Rich Dashboard Framework Setup (Achievement 0.1)

**Achievement**: 0.1 - Rich Dashboard Framework Setup  
**Plan**: LLM-DASHBOARD-CLI  
**Type**: SUBPLAN  
**Status**: 📋 Ready for Execution  
**Created**: 2025-11-13  
**Estimated Effort**: 2-3 hours  
**Execution Strategy**: Single EXECUTION (all components interdependent)

---

## 🎯 Objective

Set up the foundational dashboard framework using the Rich library, establishing the core architecture for all future dashboard implementations. This includes installing dependencies, creating the directory structure, implementing base classes, and providing reusable UI components that will be used by all dashboard types (main, plan-specific, etc.).

**Success Criteria**:
- Rich library installed and importable
- Dashboard directory structure created
- Base dashboard class with core methods
- Reusable UI components library
- Entry point (`LLM/main.py`) exists
- All components tested (>80% coverage)
- Zero linter errors
- Documentation complete

---

## 📋 Deliverables

### 1. Dependency Management
**File**: `requirements.txt` (modified)
- Add `rich>=13.0.0` dependency
- Ensure compatibility with existing dependencies
- Document why Rich library (terminal UI framework)

### 2. Entry Point
**File**: `LLM/main.py` (new, ~50 lines)
- Main entry point for dashboard CLI
- Imports Console from Rich
- Placeholder for dashboard routing
- Basic error handling structure
- Help message for --help flag

### 3. Dashboard Directory Structure
**Directory**: `LLM/dashboard/` (new)
```
LLM/dashboard/
├── __init__.py              # Package initialization
├── base_dashboard.py        # Base dashboard class (~100 lines)
├── ui_components.py         # Reusable UI components (~150 lines)
└── utils.py                 # Helper functions (~50 lines)
```

### 4. Base Dashboard Class
**File**: `LLM/dashboard/base_dashboard.py` (~100 lines)
- `BaseDashboard` abstract class
- Core methods: `show()`, `clear()`, `render_panel()`
- Console instance management
- Abstract methods for subclasses
- Error handling patterns

### 5. UI Components Library
**File**: `LLM/dashboard/ui_components.py` (~150 lines)
- Panel wrapper functions
- Table wrapper functions
- Prompt wrapper functions
- Status indicators (✅ ⚠️ 🔴 🟢 🟡)
- Color-coded text helpers
- Consistent styling constants

### 6. Helper Utilities
**File**: `LLM/dashboard/utils.py` (~50 lines)
- Path resolution helpers
- String formatting utilities
- Time/date formatting
- Common validation functions

### 7. Test Suite
**Directory**: `tests/LLM/dashboard/` (new)
**Files**:
- `test_base_dashboard.py` (~80 lines)
- `test_ui_components.py` (~120 lines)
- `test_utils.py` (~60 lines)

**Coverage Target**: >80% for all dashboard modules

---

## 🏗️ Approach

### Phase 1: Foundation Setup (30 minutes)

**1.1 Install Rich Library**:
- Add `rich>=13.0.0` to `requirements.txt`
- Run `pip install rich>=13.0.0`
- Verify installation: `python -c "from rich.console import Console; print('✓ Rich installed')"`

**1.2 Create Directory Structure**:
```bash
mkdir -p LLM/dashboard
touch LLM/dashboard/__init__.py
touch LLM/dashboard/base_dashboard.py
touch LLM/dashboard/ui_components.py
touch LLM/dashboard/utils.py

mkdir -p tests/LLM/dashboard
touch tests/LLM/dashboard/__init__.py
touch tests/LLM/dashboard/test_base_dashboard.py
touch tests/LLM/dashboard/test_ui_components.py
touch tests/LLM/dashboard/test_utils.py
```

**1.3 Create Entry Point**:
- Create `LLM/main.py` with basic structure
- Add argparse for --help flag
- Add placeholder for future dashboard routing

---

### Phase 2: Base Dashboard Implementation (45 minutes)

**2.1 Implement BaseDashboard Class** (`base_dashboard.py`):

```python
from rich.console import Console
from rich.panel import Panel
from abc import ABC, abstractmethod
from typing import Optional

class BaseDashboard(ABC):
    """Base class for all dashboard implementations.
    
    Provides core functionality for:
    - Console management
    - Screen clearing
    - Panel rendering
    - Common UI patterns
    
    Subclasses must implement show() method.
    """
    
    def __init__(self, console: Optional[Console] = None):
        """Initialize dashboard with console.
        
        Args:
            console: Rich Console instance (creates if None)
        """
        self.console = console or Console()
    
    @abstractmethod
    def show(self):
        """Show dashboard (must be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement show()")
    
    def clear(self):
        """Clear console screen."""
        self.console.clear()
    
    def render_panel(
        self, 
        content, 
        title: str = "", 
        border_style: str = "blue",
        **kwargs
    ) -> Panel:
        """Render Rich panel with consistent styling.
        
        Args:
            content: Panel content (Text, str, or renderable)
            title: Panel title
            border_style: Border color (blue, green, red, yellow, etc.)
            **kwargs: Additional Rich Panel arguments
        
        Returns:
            Rich Panel object
        """
        return Panel(
            content, 
            title=title, 
            border_style=border_style,
            **kwargs
        )
    
    def print(self, *args, **kwargs):
        """Wrapper for console.print()."""
        self.console.print(*args, **kwargs)
```

**Key Design Decisions**:
- Abstract base class (ABC) ensures subclasses implement show()
- Optional Console parameter for testing (dependency injection)
- Consistent method signatures for UI rendering
- Wrapper methods for common operations

---

### Phase 3: UI Components Library (60 minutes)

**3.1 Implement UI Components** (`ui_components.py`):

**Panel Helpers**:
```python
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm
from typing import List, Dict, Optional

# Status indicators
STATUS_APPROVED = "✅"
STATUS_WARNING = "⚠️"
STATUS_ERROR = "🔴"
STATUS_SUCCESS = "🟢"
STATUS_IN_PROGRESS = "🟡"
STATUS_NOT_STARTED = "⚪"

def create_panel(
    content, 
    title: str = "", 
    border_style: str = "blue"
) -> Panel:
    """Create Rich panel with consistent styling."""
    return Panel(content, title=title, border_style=border_style)

def create_info_panel(content, title: str = "Info") -> Panel:
    """Create info panel (blue border)."""
    return Panel(content, title=title, border_style="blue")

def create_success_panel(content, title: str = "Success") -> Panel:
    """Create success panel (green border)."""
    return Panel(content, title=title, border_style="green")

def create_warning_panel(content, title: str = "Warning") -> Panel:
    """Create warning panel (yellow border)."""
    return Panel(content, title=title, border_style="yellow")

def create_error_panel(content, title: str = "Error") -> Panel:
    """Create error panel (red border)."""
    return Panel(content, title=title, border_style="red")
```

**Table Helpers**:
```python
def create_table(
    title: str = "",
    show_header: bool = True,
    header_style: str = "bold cyan"
) -> Table:
    """Create Rich table with consistent styling."""
    return Table(
        title=title,
        show_header=show_header,
        header_style=header_style
    )

def create_simple_table(columns: List[str]) -> Table:
    """Create simple table with specified columns."""
    table = create_table()
    for col in columns:
        table.add_column(col)
    return table
```

**Text Formatting**:
```python
def format_status(status: str, label: str) -> Text:
    """Format status with emoji and label.
    
    Args:
        status: Status type (approved, warning, error, etc.)
        label: Status label text
    
    Returns:
        Rich Text object with formatted status
    """
    status_map = {
        'approved': (STATUS_APPROVED, 'green'),
        'warning': (STATUS_WARNING, 'yellow'),
        'error': (STATUS_ERROR, 'red'),
        'success': (STATUS_SUCCESS, 'green'),
        'in_progress': (STATUS_IN_PROGRESS, 'yellow'),
        'not_started': (STATUS_NOT_STARTED, 'dim'),
    }
    
    emoji, color = status_map.get(status, (STATUS_NOT_STARTED, 'dim'))
    
    text = Text()
    text.append(f"{emoji} {label}", style=color)
    return text

def format_header(text: str) -> Text:
    """Format header text (bold cyan)."""
    return Text(text, style="bold cyan")

def format_error(text: str) -> Text:
    """Format error text (red)."""
    return Text(text, style="red")

def format_success(text: str) -> Text:
    """Format success text (green)."""
    return Text(text, style="green")
```

**Prompt Wrappers**:
```python
def prompt_choice(
    message: str, 
    choices: List[str], 
    default: Optional[str] = None
) -> str:
    """Prompt user for choice from list.
    
    Args:
        message: Prompt message
        choices: List of valid choices
        default: Default choice (optional)
    
    Returns:
        User's choice
    """
    return Prompt.ask(message, choices=choices, default=default)

def prompt_confirm(message: str, default: bool = False) -> bool:
    """Prompt user for yes/no confirmation.
    
    Args:
        message: Confirmation message
        default: Default value (True/False)
    
    Returns:
        User's confirmation
    """
    return Confirm.ask(message, default=default)

def prompt_text(message: str, default: str = "") -> str:
    """Prompt user for text input.
    
    Args:
        message: Prompt message
        default: Default value
    
    Returns:
        User's input
    """
    return Prompt.ask(message, default=default)
```

---

### Phase 4: Utilities and Testing (45 minutes)

**4.1 Implement Helper Utilities** (`utils.py`):

```python
from pathlib import Path
from datetime import datetime
from typing import Optional

def format_timestamp(dt: datetime) -> str:
    """Format datetime as HH:MM:SS."""
    return dt.strftime('%H:%M:%S')

def format_date(dt: datetime) -> str:
    """Format datetime as YYYY-MM-DD."""
    return dt.strftime('%Y-%m-%d')

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def validate_plan_name(name: str) -> bool:
    """Validate plan name format."""
    return bool(name and len(name) > 0 and not name.startswith('.'))
```

**4.2 Write Tests**:

**`test_base_dashboard.py`**:
- Test BaseDashboard initialization
- Test console management
- Test panel rendering
- Test abstract method enforcement
- Test clear() method

**`test_ui_components.py`**:
- Test panel creation functions
- Test table creation functions
- Test status formatting
- Test text formatting
- Test prompt wrappers (with mocked input)

**`test_utils.py`**:
- Test timestamp formatting
- Test date formatting
- Test text truncation
- Test plan name validation

**Testing Strategy**:
- Use pytest fixtures for console mocking
- Mock user input for prompt tests
- Test edge cases (empty strings, None values)
- Validate return types and formats

---

## 🔄 Execution Strategy

**Type**: Single EXECUTION

**Rationale**:
- All components are interdependent (base class → UI components → utils)
- Small scope (2-3 hours total)
- Foundation work best done atomically
- Single test pass validates entire foundation

**Execution Order**:
1. Phase 1: Foundation Setup (creates structure)
2. Phase 2: Base Dashboard (core abstraction)
3. Phase 3: UI Components (builds on base)
4. Phase 4: Utilities and Testing (validates all)

**Not Parallel**: Components have clear dependencies (base → components → tests)

---

## 🧪 Testing Strategy

### Unit Tests (Priority)

**Location**: `tests/LLM/dashboard/`

**Test Files**:
1. `test_base_dashboard.py` (~80 lines)
   - Test initialization with/without console
   - Test abstract method enforcement
   - Test render_panel() method
   - Test clear() method
   - Test console wrapper methods

2. `test_ui_components.py` (~120 lines)
   - Test all panel creation functions
   - Test table creation functions
   - Test status formatting (all statuses)
   - Test text formatting (colors, styles)
   - Test prompt wrappers (mocked input)

3. `test_utils.py` (~60 lines)
   - Test timestamp formatting
   - Test date formatting
   - Test text truncation (various lengths)
   - Test plan name validation (valid/invalid cases)

**Coverage Target**: >80%

**Mocking Strategy**:
- Mock Rich Console for testing
- Mock user input for prompt tests
- Use pytest fixtures for common setups

### Manual Verification

**Checklist**:
- [ ] Rich library imports without error
- [ ] `python LLM/main.py --help` shows help message
- [ ] Dashboard directory structure created
- [ ] All files have correct imports
- [ ] No circular import issues
- [ ] Tests run with pytest
- [ ] Test coverage >80%
- [ ] No linter errors (ruff/flake8)

---

## 📊 Expected Results

### Files Created (7 new files)

**Source Files**:
1. `LLM/main.py` (~50 lines)
2. `LLM/dashboard/__init__.py` (~10 lines)
3. `LLM/dashboard/base_dashboard.py` (~100 lines)
4. `LLM/dashboard/ui_components.py` (~150 lines)
5. `LLM/dashboard/utils.py` (~50 lines)

**Test Files**:
6. `tests/LLM/dashboard/test_base_dashboard.py` (~80 lines)
7. `tests/LLM/dashboard/test_ui_components.py` (~120 lines)
8. `tests/LLM/dashboard/test_utils.py` (~60 lines)

**Total Lines**: ~620 lines (source + tests)

### Files Modified (1 file)

1. `requirements.txt` (+1 line: `rich>=13.0.0`)

### Test Results

**Expected**:
- All tests pass (pytest exit code 0)
- Coverage >80%
- No linter errors
- All imports resolve

---

## ✅ Success Criteria

1. **Functionality**:
   - ✅ Rich library installed and importable
   - ✅ Dashboard directory structure exists
   - ✅ BaseDashboard class implemented with all methods
   - ✅ UI components library complete (panels, tables, prompts, text)
   - ✅ Utilities implemented
   - ✅ Entry point exists (`LLM/main.py`)

2. **Quality**:
   - ✅ Test coverage >80%
   - ✅ All tests pass
   - ✅ No linter errors
   - ✅ No circular imports
   - ✅ Type hints present

3. **Documentation**:
   - ✅ All functions have docstrings
   - ✅ README comments in `__init__.py`
   - ✅ Usage examples in docstrings

4. **Integration**:
   - ✅ Can import from `LLM.dashboard`
   - ✅ BaseDashboard is subclassable
   - ✅ UI components are reusable

---

## 🔗 Dependencies

**External**:
- Rich library (>=13.0.0)
- Python 3.8+ (for type hints)
- pytest (for testing)

**Internal**:
- None (this is foundation work)

**Blocks**:
- Achievement 0.2 (Plan Discovery - needs base dashboard)
- Achievement 0.3 (Main Dashboard - needs base dashboard + UI components)

---

## 📚 References

**Rich Library Documentation**:
- Official Docs: https://rich.readthedocs.io/
- Console API: https://rich.readthedocs.io/en/stable/console.html
- Panel API: https://rich.readthedocs.io/en/stable/panel.html
- Table API: https://rich.readthedocs.io/en/stable/tables.html

**Project Patterns**:
- `LLM/scripts/generation/LIBRARY_INTEGRATION_GUIDE.md` - Library patterns
- `LLM/docs/ERROR_HANDLING_PATTERNS.md` - Error handling
- `tests/LLM/scripts/generation/` - Existing test patterns

**Methodology**:
- `LLM/templates/SUBPLAN-TEMPLATE.md` - SUBPLAN structure
- `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` - Workflow guidance

---

## 🎯 Implementation Notes

**Key Design Principles**:
1. **Simplicity**: Keep base classes simple, defer complexity to subclasses
2. **Reusability**: UI components should be usable by all dashboard types
3. **Consistency**: Standardize styling (colors, borders, formatting)
4. **Testability**: Design for dependency injection (optional Console parameter)

**Common Pitfalls to Avoid**:
- ❌ Over-engineering base class (keep it simple)
- ❌ Hardcoding styles (use constants)
- ❌ Not testing with mocked console (use fixtures)
- ❌ Circular imports (dashboard → ui_components → dashboard)

**Success Indicators During Implementation**:
- Can create simple panel in <5 lines of code
- Can create table in <10 lines of code
- UI components are intuitive to use
- Tests are easy to write and understand

---

**Status**: 📋 Ready for Execution  
**Next**: Execute EXECUTION_TASK_LLM-DASHBOARD-CLI_01_01.md


