# SUBPLAN: Achievement 1.3 - Quick Action Shortcuts

**PLAN**: LLM-DASHBOARD-CLI  
**Achievement**: 1.3  
**Estimated Time**: 3-4 hours  
**Created**: 2025-11-14  
**Status**: 📋 Design Phase

---

## 🎯 Objective

Implement one-key shortcuts for common actions in the plan dashboard, enabling users to execute next achievement, create SUBPLANs, create EXECUTIONs, and access documentation with a single keystroke. This completes the Priority 1 goals by transforming the dashboard from a read-only display to an interactive command center.

**Core Purpose**: Replace 80+ character commands with single-key actions, making the dashboard a full-featured command center that handles all common workflow operations directly from the UI.

**Success Definition**:
- Users can execute next achievement with one key press
- Users can create SUBPLANs and EXECUTIONs from dashboard
- Users can access documentation without leaving dashboard
- Action menu shows available options clearly
- Commands are built and executed correctly
- All actions handle errors gracefully

---

## 📦 Deliverables

### 1. Action Executor Module

**File**: `LLM/dashboard/action_executor.py` (~300 lines, NEW)

**Purpose**: Execute user actions by building and running commands

**Key Components**:

```python
class ActionExecutor:
    """
    Execute user actions from dashboard.
    
    Handles:
    - Command building for common operations
    - Subprocess execution
    - Error handling and reporting
    """
    
    def __init__(self, plan_path: Path, console: Console):
        self.plan_path = plan_path
        self.console = console
        self.plan_name = plan_path.name
    
    def execute_next(self):
        """Execute next achievement."""
        cmd = [
            "python",
            "LLM/scripts/generation/generate_prompt.py",
            f"@{self.plan_name}",
            "--next",
            "--interactive"
        ]
        self._run_command(cmd, "Execute Next")
    
    def create_subplan(self, achievement: str):
        """Create SUBPLAN for achievement."""
        cmd = [
            "python",
            "LLM/scripts/generation/generate_subplan_prompt.py",
            f"@{self.plan_name}",
            "--achievement", achievement
        ]
        self._run_command(cmd, "Create SUBPLAN")
    
    def create_execution(self, achievement: str):
        """Create EXECUTION for achievement."""
        cmd = [
            "python",
            "LLM/scripts/generation/generate_execution_prompt.py",
            f"@{self.plan_name}",
            "--achievement", achievement
        ]
        self._run_command(cmd, "Create EXECUTION")
    
    def _run_command(self, cmd: List[str], action_name: str):
        """Run command with error handling."""
        try:
            result = subprocess.run(cmd, check=True, capture_output=False)
            self.console.print(f"[green]✅ {action_name} completed[/green]")
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]❌ {action_name} failed: {e}[/red]")
        except FileNotFoundError:
            self.console.print(f"[red]❌ Command not found[/red]")
```

### 2. Action Menu Rendering

**Function**: `render_actions()` in `plan_dashboard.py` (~40 lines)

**Purpose**: Display available actions with emoji indicators

**Implementation**:

```python
from dataclasses import dataclass

@dataclass
class Action:
    """Dashboard action definition."""
    key: str      # Key to press (e.g., '1', '2')
    emoji: str    # Emoji indicator
    label: str    # Action label
    enabled: bool = True  # Whether action is available

def render_actions(self):
    """
    Render action menu.
    
    Shows:
    - Available actions with key bindings
    - Emoji indicators for each action
    - Enabled/disabled state
    """
    actions = self._get_available_actions()
    
    content = Text()
    content.append("🎯 Available Actions\n", style="bold green")
    content.append("\n")
    
    for action in actions:
        if action.enabled:
            content.append(f"{action.key}. {action.emoji} {action.label}\n")
        else:
            content.append(f"{action.key}. {action.emoji} {action.label} [dim](disabled)[/dim]\n", style="dim")
    
    panel = Panel(content, border_style="green", padding=(1, 2))
    self.console.print(panel)

def _get_available_actions(self) -> List[Action]:
    """
    Get list of available actions based on plan state.
    
    Returns:
        List of Action objects
    """
    actions = [
        Action('1', '▶️', 'Execute Next Achievement', enabled=len(self.state.next_achievements) > 0),
        Action('2', '📝', 'Create SUBPLAN', enabled=True),
        Action('3', '🔄', 'Create EXECUTION', enabled=True),
        Action('4', '📚', 'View Documentation', enabled=True),
        Action('5', '🔙', 'Back to Plans', enabled=True),
    ]
    return actions
```

### 3. Action Handler

**Function**: `handle_action()` in `plan_dashboard.py` (~80 lines)

**Purpose**: Route user input to appropriate action

**Implementation**:

```python
def handle_action(self, choice: str):
    """
    Handle user action choice.
    
    Args:
        choice: User's input (action key)
    """
    if choice == '1':
        self._action_execute_next()
    elif choice == '2':
        self._action_create_subplan()
    elif choice == '3':
        self._action_create_execution()
    elif choice == '4':
        self._action_view_documentation()
    elif choice == '5' or choice.lower() in ['b', 'back']:
        return  # Exit to main dashboard
    else:
        self.console.print("[red]Invalid choice[/red]")
        self.console.print("Press any key to continue...")
        self.get_user_input("")

def _action_execute_next(self):
    """Execute next achievement action."""
    if not self.state.next_achievements:
        self.console.print("[yellow]No achievements ready to execute[/yellow]")
        self.console.print("Press any key to continue...")
        self.get_user_input("")
        return
    
    executor = ActionExecutor(self.plan_path, self.console)
    executor.execute_next()

def _action_create_subplan(self):
    """Create SUBPLAN action."""
    # Prompt for achievement number
    ach_num = Prompt.ask("Enter achievement number (e.g., 1.2)")
    
    if not ach_num:
        return
    
    executor = ActionExecutor(self.plan_path, self.console)
    executor.create_subplan(ach_num)

def _action_create_execution(self):
    """Create EXECUTION action."""
    # Prompt for achievement number
    ach_num = Prompt.ask("Enter achievement number (e.g., 1.2)")
    
    if not ach_num:
        return
    
    executor = ActionExecutor(self.plan_path, self.console)
    executor.create_execution(ach_num)

def _action_view_documentation(self):
    """View documentation action."""
    self._show_documentation_menu()
```

### 4. Documentation Menu

**Function**: `_show_documentation_menu()` in `plan_dashboard.py` (~80 lines)

**Purpose**: Provide quick access to documentation files

**Implementation**:

```python
def _show_documentation_menu(self):
    """
    Show documentation menu with available docs.
    
    Displays:
    - List of available documentation files
    - Quick access to guides and references
    """
    docs = [
        ('1', 'SUBPLAN Workflow Guide', 'LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md'),
        ('2', 'EXECUTION Task Template', 'LLM/templates/EXECUTION_TASK-TEMPLATE.md'),
        ('3', 'SUBPLAN Template', 'LLM/templates/SUBPLAN-TEMPLATE.md'),
        ('4', 'Prompts Reference', 'LLM/templates/PROMPTS.md'),
        ('5', 'Dashboard README', 'LLM/dashboard/README.md'),
        ('6', 'Main README', 'README.md'),
    ]
    
    self.clear()
    
    content = Text()
    content.append("📚 Documentation\n\n", style="bold cyan")
    
    for num, title, path in docs:
        # Check if file exists
        doc_file = Path(path)
        if doc_file.exists():
            content.append(f"{num}. {title}\n")
        else:
            content.append(f"{num}. {title} [dim](not found)[/dim]\n", style="dim")
    
    content.append("\nb. Back to dashboard\n", style="dim")
    
    panel = Panel(content, title="Available Documentation", border_style="cyan", padding=(1, 2))
    self.console.print(panel)
    
    choice = Prompt.ask("\nSelect document (1-6) or 'b' for back", default="b")
    
    if choice.lower() == 'b':
        return
    
    if choice.isdigit() and 1 <= int(choice) <= 6:
        doc_path = docs[int(choice)-1][2]
        self._open_document(doc_path)

def _open_document(self, doc_path: str):
    """
    Open document in pager or print preview.
    
    Args:
        doc_path: Path to documentation file
    """
    doc_file = Path(doc_path)
    
    if not doc_file.exists():
        self.console.print(f"[red]Document not found: {doc_path}[/red]")
        self.console.print("Press any key to continue...")
        self.get_user_input("")
        return
    
    # Try to open in less (pager)
    try:
        import subprocess
        subprocess.run(['less', str(doc_file)])
    except (FileNotFoundError, OSError):
        # Fallback: print first 50 lines
        try:
            with open(doc_file, 'r') as f:
                lines = f.readlines()[:50]
                self.console.print(''.join(lines))
                
                total_lines = len(f.readlines()) + 50
                self.console.print(f"\n[cyan]Showing first 50 of {total_lines} lines[/cyan]")
                self.console.print(f"[cyan]Full doc: {doc_path}[/cyan]")
        except OSError as e:
            self.console.print(f"[red]Failed to read document: {e}[/red]")
        
        self.console.print("\nPress any key to continue...")
        self.get_user_input("")
```

### 5. Test Suite

**File**: `tests/LLM/dashboard/test_action_executor.py` (~400 lines, NEW)

**Purpose**: Comprehensive tests for action execution

**Test Coverage**:

```python
class TestActionExecutor:
    """Tests for ActionExecutor class."""
    
    def test_init(self):
        """Test ActionExecutor initialization."""
    
    def test_execute_next_command_building(self):
        """Test execute_next builds correct command."""
    
    def test_create_subplan_command_building(self):
        """Test create_subplan builds correct command."""
    
    def test_create_execution_command_building(self):
        """Test create_execution builds correct command."""
    
    def test_run_command_success(self):
        """Test successful command execution."""
    
    def test_run_command_failure(self):
        """Test command failure handling."""

class TestActionMenu:
    """Tests for action menu rendering."""
    
    def test_render_actions(self):
        """Test action menu rendering."""
    
    def test_get_available_actions(self):
        """Test available actions based on state."""
    
    def test_action_enabled_disabled_states(self):
        """Test actions show enabled/disabled correctly."""

class TestActionHandler:
    """Tests for action handling."""
    
    def test_handle_action_execute_next(self):
        """Test execute next action."""
    
    def test_handle_action_create_subplan(self):
        """Test create SUBPLAN action."""
    
    def test_handle_action_create_execution(self):
        """Test create EXECUTION action."""
    
    def test_handle_action_view_docs(self):
        """Test view documentation action."""
    
    def test_handle_action_invalid(self):
        """Test invalid action handling."""

class TestDocumentationMenu:
    """Tests for documentation menu."""
    
    def test_show_documentation_menu(self):
        """Test documentation menu display."""
    
    def test_open_document_exists(self):
        """Test opening existing document."""
    
    def test_open_document_not_found(self):
        """Test opening non-existent document."""
```

---

## 🔧 Approach

### Phase 1: Action Executor Module (90 min)

**Goal**: Create ActionExecutor class with command building and execution

**Steps**:

1. **Create `LLM/dashboard/action_executor.py`** (60 min):
   - Define ActionExecutor class
   - Implement `execute_next()` - Build command for next achievement
   - Implement `create_subplan()` - Build command for SUBPLAN creation
   - Implement `create_execution()` - Build command for EXECUTION creation
   - Implement `_run_command()` - Execute subprocess with error handling
   - Add logging for all actions

2. **Add command building logic** (30 min):
   - Build paths to scripts (generate_prompt.py, etc.)
   - Format plan name with @ prefix
   - Add appropriate flags (--next, --interactive, --achievement)
   - Test command building

**Verification**:
- ActionExecutor can build commands correctly
- Commands include all required arguments
- Error handling works for missing scripts

---

### Phase 2: Action Menu Integration (60 min)

**Goal**: Add action menu to plan dashboard

**Steps**:

1. **Add Action dataclass** (10 min):
   - Define Action with key, emoji, label, enabled
   - Import dataclasses

2. **Implement `render_actions()`** (20 min):
   - Get available actions based on state
   - Display with Rich Panel
   - Show enabled/disabled state

3. **Implement `_get_available_actions()`** (20 min):
   - Return list of Action objects
   - Set enabled based on plan state
   - Execute Next only enabled if next_achievements exist

4. **Update `show()` method** (10 min):
   - Add `render_actions()` call
   - Position between achievements and navigation prompt

**Verification**:
- Action menu displays correctly
- Actions show enabled/disabled state
- Layout is clean

---

### Phase 3: Action Handling (60 min)

**Goal**: Implement action routing and execution

**Steps**:

1. **Implement `handle_action()`** (20 min):
   - Route choice to appropriate action method
   - Handle invalid choices
   - Return to dashboard after action

2. **Implement action methods** (30 min):
   - `_action_execute_next()` - Call ActionExecutor.execute_next()
   - `_action_create_subplan()` - Prompt for achievement, call executor
   - `_action_create_execution()` - Prompt for achievement, call executor
   - `_action_view_documentation()` - Show documentation menu
   - Add user feedback after each action

3. **Update show() loop** (10 min):
   - Call `handle_action()` with user choice
   - Don't exit on action (loop back)
   - Only exit on 'b' or '5'

**Verification**:
- Actions execute correctly
- User returns to dashboard after action
- Invalid choices handled gracefully

---

### Phase 4: Documentation Menu & Testing (90 min)

**Goal**: Add documentation quick access and comprehensive tests

**Steps**:

1. **Implement documentation menu** (30 min):
   - `_show_documentation_menu()` - Display doc list
   - `_open_document()` - Open doc in pager or print
   - List 6 key documentation files
   - Check file existence before showing
   - Handle pager (less) or fallback to print

2. **Create test suite** (40 min):
   - Create `test_action_executor.py`
   - TestActionExecutor (6 tests)
   - TestActionMenu (3 tests)
   - TestActionHandler (5 tests)
   - TestDocumentationMenu (3 tests)

3. **Run tests and fix issues** (20 min):
   ```bash
   pytest tests/LLM/dashboard/test_action_executor.py -v
   pytest tests/LLM/dashboard/ -v
   ```
   - Fix any failures
   - Ensure >90% coverage
   - No linter errors

**Verification**:
- Documentation menu works
- All tests pass
- No regressions

---

## 🔄 Execution Strategy

### Type: Single EXECUTION (Recommended)

**Rationale**:

1. **Cohesive Feature**: All components work together (menu, handler, executor)
2. **Manageable Scope**: 3-4 hours, can be done in one session
3. **Sequential Dependencies**: Menu needs handler, handler needs executor
4. **Atomic Delivery**: Feature only useful when complete

**Execution**: Create single `EXECUTION_TASK_LLM-DASHBOARD-CLI_13_01.md`

**Alternative**: Could split into 2 EXECUTIONs (executor + menu, docs + testing), but overhead not worth it

---

## 🧪 Testing Strategy

### Unit Testing

**Scope**: Test each component in isolation

**Test Files**:
- `test_action_executor.py` - Action execution and command building

**Coverage Target**: >90% for new code

**Key Tests**:
- Command building (execute_next, create_subplan, create_execution)
- Action menu rendering
- Action handler routing
- Documentation menu
- Error handling

### Integration Testing

**Scope**: Test with real dashboard

**Test Cases**:
1. **Full Action Workflow**:
   - Display action menu
   - Select action
   - Execute action
   - Return to dashboard

2. **Documentation Access**:
   - Open documentation menu
   - Select document
   - Display or open document

3. **Edge Cases**:
   - Invalid action choice
   - Missing documentation files
   - Command execution failures

### Manual Testing

**Verification**:
- Test with LLM-DASHBOARD-CLI plan
- Execute real actions
- Verify commands are built correctly
- Test documentation access
- Verify error handling

---

## 📊 Expected Results

### Success Criteria

**Functional**:
- ✅ Action menu displays with 5 actions
- ✅ Actions execute correctly
- ✅ Commands are built with correct arguments
- ✅ Documentation menu provides quick access
- ✅ Error handling prevents crashes
- ✅ User returns to dashboard after actions

**Quality**:
- ✅ Test coverage >90% for new code
- ✅ All tests passing (17+ tests)
- ✅ No linter errors
- ✅ Clear error messages

**User Experience**:
- ✅ One-key shortcuts work smoothly
- ✅ Actions complete in <2 seconds
- ✅ Documentation is discoverable
- ✅ Dashboard feels responsive

### Deliverable Metrics

**Files Created**: 2 files (~700 lines total)
- New: 2 files (~700 lines)

**Test Metrics**:
- Total Tests: ~17 new tests
- Coverage: >90% for new code
- All tests passing

---

## 🚨 Risks & Mitigations

### Risk 1: Script Path Resolution

**Risk**: Scripts might not be found if dashboard run from different directory

**Impact**: MEDIUM - Actions fail

**Mitigation**:
- Use absolute paths for scripts
- Check script existence before executing
- Clear error messages if script not found
- Test from multiple directories

### Risk 2: Subprocess Execution Failures

**Risk**: Subprocess might fail for various reasons

**Impact**: MEDIUM - Action doesn't complete

**Mitigation**:
- Catch subprocess.CalledProcessError
- Display clear error messages
- Log failures for debugging
- Don't crash dashboard on failure

### Risk 3: Documentation Files Missing

**Risk**: Documentation files might not exist or be moved

**Impact**: LOW - Doc menu shows broken links

**Mitigation**:
- Check file existence before displaying
- Show "(not found)" for missing files
- Provide fallback message
- Don't crash on missing files

### Risk 4: User Confusion

**Risk**: Users might not understand what actions do

**Impact**: LOW - Users don't use actions

**Mitigation**:
- Clear action labels
- Emoji indicators for recognition
- Show which actions are available
- Documentation action provides help

---

## 💡 Design Decisions

### Decision 1: Subprocess vs Direct Import

**Chosen**: Use subprocess to run scripts

**Rationale**:
- Scripts expect to be run from command line
- Subprocess preserves script isolation
- Easier to test (mock subprocess)
- Matches user's mental model (runs same commands)

**Alternative Considered**: Import and call directly, but would require refactoring scripts

### Decision 2: Action Menu Always Visible

**Chosen**: Show action menu in every dashboard render

**Rationale**:
- Users always know what actions are available
- Quick reference for keyboard shortcuts
- Consistent UI (always in same place)
- Encourages action usage

**Alternative Considered**: Toggle with key press, but less discoverable

### Decision 3: Documentation Menu Separate

**Chosen**: Documentation as separate submenu (not inline in actions)

**Rationale**:
- Documentation list is long (6+ items)
- Separate menu keeps action menu focused
- Can expand documentation list easily
- Clear separation of concerns

**Alternative Considered**: Inline in actions, but clutters menu

### Decision 4: Enabled/Disabled Actions

**Chosen**: Show all actions, mark disabled if not available

**Rationale**:
- Users see what's possible
- Understand why action disabled
- Consistent action list (predictable)
- Better than hiding actions

**Alternative Considered**: Hide unavailable actions, but less informative

### Decision 5: Single EXECUTION

**Chosen**: One EXECUTION_TASK for all components

**Rationale**:
- 3-4 hours is manageable
- Components are tightly coupled
- Atomic feature delivery
- Less overhead than split

**Alternative Considered**: Split into 2 EXECUTIONs (executor, menu), but not needed

---

## 📝 Implementation Notes

### Command Building Patterns

**Execute Next**:
```bash
python LLM/scripts/generation/generate_prompt.py @PLAN_NAME --next --interactive
```

**Create SUBPLAN**:
```bash
python LLM/scripts/generation/generate_subplan_prompt.py @PLAN_NAME --achievement 1.2
```

**Create EXECUTION**:
```bash
python LLM/scripts/generation/generate_execution_prompt.py @PLAN_NAME --achievement 1.2
```

### Action Menu Layout

**Position**: After achievements table, before navigation prompt

**Format**:
```
🎯 Available Actions

1. ▶️ Execute Next Achievement
2. 📝 Create SUBPLAN
3. 🔄 Create EXECUTION
4. 📚 View Documentation
5. 🔙 Back to Plans
```

### Documentation Files

**Core Docs** (must exist):
- `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md`
- `LLM/templates/SUBPLAN-TEMPLATE.md`
- `LLM/templates/EXECUTION_TASK-TEMPLATE.md`
- `README.md`

**Optional Docs** (show if exist):
- `LLM/dashboard/README.md`
- `LLM/templates/PROMPTS.md`

---

## 🔗 Dependencies

### Requires (from previous achievements):

- Achievement 1.1: `PlanDashboard` class ✅
- Achievement 1.2: Achievement visualization ✅
- Achievement 0.2: State detection ✅

### Enables (for future achievements):

- Achievement 2.1: Parallel Execution Detection (will add parallel execution action)
- Achievement 2.2: Interactive Workflow Execution (will enhance actions)

### External Dependencies:

- Python 3.8+ (existing)
- Rich library (from Achievement 0.1)
- subprocess module (Python stdlib)
- No new external libraries needed

---

## ✅ Definition of Done

**Code Complete**:
- [ ] `action_executor.py` created (~300 lines)
- [ ] `render_actions()` implemented
- [ ] `handle_action()` implemented
- [ ] Action methods implemented (4 methods)
- [ ] Documentation menu implemented
- [ ] `test_action_executor.py` created (~400 lines)

**Tests Complete**:
- [ ] 17+ tests written and passing
- [ ] >90% coverage for new code
- [ ] Command building tested
- [ ] Action handling tested
- [ ] Documentation menu tested

**Quality Complete**:
- [ ] No linter errors
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] Error messages clear

**Integration Complete**:
- [ ] Integrated into plan dashboard
- [ ] Actions execute correctly
- [ ] Documentation menu works
- [ ] No performance issues

---

**Status**: 📋 Ready for Execution  
**Next Step**: Create `EXECUTION_TASK_LLM-DASHBOARD-CLI_13_01.md` and execute work  
**Executor**: Begin with Phase 1 (Action Executor Module)

