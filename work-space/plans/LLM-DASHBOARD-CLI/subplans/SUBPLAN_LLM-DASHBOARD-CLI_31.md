# SUBPLAN: Color Themes & Customization

**Type**: SUBPLAN  
**Mother Plan**: PLAN_LLM-DASHBOARD-CLI.md  
**Plan**: LLM-DASHBOARD-CLI  
**Achievement Addressed**: Achievement 3.1 (Color Themes & Customization)  
**Achievement**: 3.1  
**Status**: Not Started  
**Created**: 2025-11-14 23:00 UTC  
**Estimated Effort**: 2-3 hours

**Metadata Tags**: `#dashboard #themes #customization #configuration #user-preferences`

**File Location**: `work-space/plans/LLM-DASHBOARD-CLI/subplans/SUBPLAN_LLM-DASHBOARD-CLI_31.md`

**Size**: 200-600 lines (within target range)

---

## 🎯 Objective

Create a flexible theme system and user customization framework that allows users to personalize their dashboard experience with color themes, configurable display options, and persistent preferences. This implements Achievement 3.1 (Color Themes & Customization) and provides three pre-built themes (default, dark, light) along with a settings menu accessible from the dashboard. This enhances user experience by allowing customization of visual appearance and dashboard behavior.

---

## 📋 What Needs to Be Created

### Files to Create

1. **`LLM/dashboard/theme.py`** (200-250 lines)
   - `Theme` class for color scheme management
   - Three built-in themes: default, dark, light
   - Color mapping for dashboard elements
   - Theme loading and application
   - Theme preview functionality

2. **`LLM/dashboard/config.py`** (150-200 lines)
   - `DashboardConfig` class for configuration management
   - Load/save configuration to YAML file
   - Default configuration values
   - Configuration validation
   - Type-safe configuration access

3. **`LLM/dashboard/config.yaml`** (20-30 lines)
   - Default configuration file
   - Theme setting
   - Refresh interval
   - Display toggles (stats, parallel, etc.)
   - User preferences

4. **`tests/LLM/dashboard/test_theme.py`** (200-250 lines)
   - Tests for Theme class
   - Tests for color loading
   - Tests for theme switching
   - Tests for invalid themes

5. **`tests/LLM/dashboard/test_config.py`** (200-250 lines)
   - Tests for DashboardConfig class
   - Tests for YAML loading/saving
   - Tests for configuration validation
   - Tests for default values

### Files to Modify

1. **`LLM/dashboard/plan_dashboard.py`**
   - Import `Theme` and `DashboardConfig`
   - Load configuration in `__init__`
   - Apply theme colors throughout rendering methods
   - Add settings menu action (key '7' or 's')
   - Update color references to use theme

2. **`LLM/dashboard/base_dashboard.py`**
   - Add theme support to base class
   - Add `get_color(color_name)` utility method
   - Make theme available to all dashboards

3. **`LLM/dashboard/main_dashboard.py`**
   - Apply theme to main dashboard rendering
   - Update color references to use theme

### Functions/Classes to Add

**Theme Class**:

```python
class Theme:
    """Dashboard color theme."""
    
    def __init__(self, name: str):
        """Initialize theme."""
        
    def _load_colors(self) -> Dict[str, str]:
        """Load theme colors."""
        
    def get_color(self, color_name: str) -> str:
        """Get color for element."""
        
    def preview(self) -> Panel:
        """Generate theme preview."""
```

**DashboardConfig Class**:

```python
class DashboardConfig:
    """Dashboard configuration manager."""
    
    def __init__(self, config_path: Path):
        """Initialize config."""
        
    def load(self) -> Dict:
        """Load configuration from YAML."""
        
    def save(self, config: Dict):
        """Save configuration to YAML."""
        
    def get(self, key: str, default=None):
        """Get configuration value."""
        
    def set(self, key: str, value):
        """Set configuration value."""
```

**PlanDashboard Additions**:

```python
def show_settings(self):
    """Show settings menu."""
    
def _toggle_setting(self, setting_name: str):
    """Toggle boolean setting."""
    
def _change_theme(self):
    """Show theme selection menu."""
    
def _preview_theme(self, theme_name: str):
    """Preview theme before applying."""
```

### Tests Required

**Test File 1**: `tests/LLM/dashboard/test_theme.py`

**Test Cases**:

1. **Theme Loading** (5 tests)
   - Test default theme loads
   - Test dark theme loads
   - Test light theme loads
   - Test invalid theme fallback to default
   - Test theme color retrieval

2. **Color Mapping** (4 tests)
   - Test get_color returns correct color
   - Test unknown color returns fallback
   - Test all standard colors present
   - Test color name validation

3. **Theme Preview** (3 tests)
   - Test preview generates Panel
   - Test preview shows all colors
   - Test preview formatting

**Test File 2**: `tests/LLM/dashboard/test_config.py`

**Test Cases**:

1. **Configuration Loading** (6 tests)
   - Test load from valid YAML
   - Test load with missing file (creates default)
   - Test load with invalid YAML
   - Test default values applied
   - Test configuration validation
   - Test type conversion

2. **Configuration Saving** (4 tests)
   - Test save to YAML
   - Test save creates file if missing
   - Test save preserves comments
   - Test save with invalid data

3. **Configuration Access** (5 tests)
   - Test get() with existing key
   - Test get() with missing key returns default
   - Test set() updates value
   - Test set() triggers save
   - Test configuration persistence

**Total**: ~27 tests (smaller scope, simpler feature)

---

## 📝 Approach

**Strategy**: Build a simple, file-based configuration system using YAML for human-readable settings, with a Theme class that provides color mappings for dashboard elements. Focus on simplicity and user-friendliness.

**Method**:

1. **Create Theme System** (45 min)
   - Define Theme class with 3 built-in themes
   - Map semantic color names to Rich color codes
   - Create color getters for dashboard elements
   - Add theme preview functionality

2. **Create Configuration System** (45 min)
   - Create DashboardConfig class for YAML management
   - Define default configuration with sensible defaults
   - Implement load/save with error handling
   - Add configuration validation

3. **Create Default Configuration File** (15 min)
   - Create config.yaml with default values
   - Add comments explaining each setting
   - Use YAML format for human readability

4. **Integrate Theme into Dashboards** (1 hour)
   - Update BaseDashboard to include theme
   - Update PlanDashboard to use theme colors
   - Update MainDashboard to use theme colors
   - Replace hardcoded colors with theme.get_color() calls

5. **Add Settings Menu** (45 min)
   - Add show_settings() method to PlanDashboard
   - Create interactive settings menu
   - Add theme switching functionality
   - Add toggle for display options
   - Add 's' or '7' key handler

6. **Write Tests** (1 hour)
   - Write ~27 tests for Theme and Config classes
   - Mock YAML file operations
   - Test theme switching and color retrieval
   - Test configuration persistence

7. **Polish and Integrate** (15 min)
   - Ensure theme applied consistently
   - Test settings menu works
   - Verify configuration persists
   - Fix any integration issues

**Key Considerations**:

- **YAML vs JSON**: YAML is more human-readable for configuration
  - **Decision**: Use YAML with PyYAML library
  
- **Theme Storage**: Built-in themes vs external files
  - **Decision**: Built-in themes (simpler, no external files needed)
  
- **Configuration Location**: User home directory vs project directory
  - **Decision**: Project directory (LLM/dashboard/config.yaml) for simplicity
  
- **Settings Scope**: Per-plan vs global
  - **Decision**: Global configuration (all dashboards share settings)

**Trade-offs**:

- **Built-in vs External Themes**:
  - Built-in: Simpler, no file management
  - External: More flexible, users can create custom themes
  - **Decision**: Built-in for now, can add custom themes later

- **YAML Dependency**: Requires PyYAML
  - **Decision**: Acceptable - PyYAML is lightweight and standard

**Risks to Watch For**:

- **YAML Parsing**: Invalid YAML could break configuration
  - **Mitigation**: Catch exceptions, fall back to defaults
  
- **Configuration File Corruption**: User edits could corrupt file
  - **Mitigation**: Validate on load, recreate if invalid
  
- **Theme Application**: Ensure all color references updated
  - **Mitigation**: Systematic search and replace of color strings

---

## 🔄 Execution Strategy

**Execution Count**: Single

**Rationale**: Single clear approach, straightforward implementation

- **Clear Requirements**: Achievement 3.1 has well-defined deliverables
- **Proven Pattern**: Configuration + Theme system is standard pattern
- **No Alternatives**: No competing approaches, single optimal design
- **Simple Scope**: Smaller than previous achievements (2-3 hours vs 3-4 hours)

**EXECUTION_TASK**: `EXECUTION_TASK_LLM-DASHBOARD-CLI_31_01.md`

**Implementation Flow**:

1. Theme system → 2. Configuration system → 3. Default config file → 4. Dashboard integration → 5. Settings menu → 6. Tests → 7. Polish

---

## 🧪 Tests Required

### Test File 1

- **Path**: `tests/LLM/dashboard/test_theme.py`
- **Test Cases**: ~12 tests covering theme loading, color mapping, previews
- **Approach**: Test each theme, verify colors, test edge cases

### Test File 2

- **Path**: `tests/LLM/dashboard/test_config.py`
- **Test Cases**: ~15 tests covering YAML loading/saving, validation, access patterns
- **Approach**: Mock YAML files, test error handling, verify persistence

### Coverage Requirements

- **Target Coverage**: >90% for new code
- **Required Test Types**:
  - Unit tests for Theme and Config classes
  - Integration tests for settings menu
  - Edge case tests for invalid input
  - Mock tests for file operations

### Test-First Requirement

- [ ] Tests written before implementation (TDD workflow)
- [ ] Initial test run shows all failing (red)
- [ ] Tests define success criteria
- [ ] Implementation makes tests pass (green)

---

## ✅ Expected Results

### Functional Changes

**After this SUBPLAN is complete, users will be able to**:

1. **Switch Themes**:
   - Press 's' or '7' in dashboard to open settings
   - Select theme from menu (default, dark, light)
   - See theme preview before applying
   - Theme applied immediately to all dashboard elements
   - Theme persists across dashboard restarts

2. **Customize Display Options**:
   - Toggle stats section visibility
   - Toggle parallel opportunities section visibility
   - Configure refresh interval
   - Enable/disable auto-copy commands
   - All settings persist to config.yaml

3. **See Theme Preview**:
   - View color samples for each theme
   - Compare themes side-by-side
   - Make informed choice before applying

4. **Persistent Configuration**:
   - Settings saved to LLM/dashboard/config.yaml
   - Configuration loads on dashboard start
   - Invalid configuration falls back to defaults
   - User can manually edit config.yaml

### Performance Changes

- **Minimal Impact**: Configuration loading adds <10ms to startup
- **Theme Application**: No runtime overhead (colors determined at init)

### Observable Outcomes

**Success Indicators**:

1. **User changes theme**:
   ```
   Dashboard displays
   User presses 's' (Settings)
   
   → Settings menu shows:
     "1. Theme: default
      2. Refresh Interval: 1s
      3. Show Stats: true
      4. Show Parallel: true
      5. Auto-Copy Commands: true
      6. Back"
   
   User presses '1' (Change Theme)
   
   → Theme menu shows:
     "1. default (current)
      2. dark
      3. light
      4. Preview
      5. Back"
   
   User presses '2' (Dark theme)
   
   → Theme applied, dashboard re-renders with bright colors
   → Settings saved to config.yaml
   ```

2. **Configuration persists**:
   ```bash
   $ cat LLM/dashboard/config.yaml
   
   theme: dark
   refresh_interval: 1
   show_stats: true
   show_parallel: true
   auto_copy_commands: true
   ```

3. **Tests verify all functionality**:
   ```bash
   $ python -m pytest tests/LLM/dashboard/test_theme.py -v
   $ python -m pytest tests/LLM/dashboard/test_config.py -v
   
   ========== 27 passed in 1.15s ==========
   ```

---

## 🔍 Conflict Analysis with Other Subplans

**Review Existing Subplans**:

From PLAN tracking:
- ✅ SUBPLAN_11 through SUBPLAN_23 - Complete
- 🆕 SUBPLAN_31 (Achievement 3.1 - Color Themes) - This SUBPLAN

**Check for Conflicts**:

- **Overlap**: None - This is new functionality (themes and configuration)
- **Conflicts**: None - Adds customization without changing existing functionality
- **Dependencies**: 
  - ✅ All Priority 1-2 achievements complete (dashboard foundation ready for customization)
- **Integration**:
  - Integrates with all dashboard classes (base, main, plan)
  - Adds configuration layer without breaking existing code

**Analysis**:

- **No conflicts detected**: This achievement adds customization layer on top of existing dashboard
- **Backward compatible**: Default theme matches current colors, no breaking changes
- **Global feature**: Benefits all dashboard views (main, plan)
- **Clean extension**: Configuration and theme systems are separate concerns

**Result**: Safe to proceed - No conflicts, dependencies met, clean extension

---

## 🔗 Dependencies

### Other Subplans

- **Depends on SUBPLAN_11-23** (All dashboard implementations): ✅ Complete
  - Dashboard structure established
  - Rendering methods defined
  - Ready for theme application

### External Dependencies

**Python Libraries**:
- `pyyaml`: For YAML configuration file parsing and saving
  - **Installation**: `pip install pyyaml` (likely already installed)
  - **Purpose**: Human-readable configuration format

**Dashboard Infrastructure** (already exists):
- `rich`: For color styling and theme preview
- `LLM/dashboard/base_dashboard.py`: Base class to add theme support
- `LLM/dashboard/plan_dashboard.py`: Integration point for settings menu
- `LLM/dashboard/main_dashboard.py`: Integration point for theme

**Check**: Verify PyYAML is in project dependencies

### Prerequisite Knowledge

- **Rich Color Styles**: Understanding Rich color naming (cyan, bright_cyan, etc.)
- **YAML Format**: Basic YAML syntax for configuration
- **Configuration Patterns**: Config file best practices
- **Python Dataclasses**: For type-safe configuration

**Documentation to Review**:
- Rich color documentation
- PyYAML documentation
- Python YAML module

---

## 🔄 Execution Task Reference

**Execution Tasks**:

- `EXECUTION_TASK_LLM-DASHBOARD-CLI_31_01.md` - Implement themes and customization (2-3 hours)

**Status**: Planning

---

## 📊 Success Criteria

**This Subplan is Complete When**:

- [ ] `Theme` class created with 3 themes
- [ ] `DashboardConfig` class created with YAML support
- [ ] `config.yaml` default file created
- [ ] Theme integrated into all dashboards
- [ ] Settings menu accessible from dashboard
- [ ] ~27 tests written and passing (>90% coverage)
- [ ] User can switch themes and see changes
- [ ] Configuration persists across restarts
- [ ] Theme preview works correctly
- [ ] Code documented with docstrings
- [ ] EXECUTION_TASK_31_01 complete
- [ ] Achievement feedback received (APPROVED_31.md or FIX_31.md)
- [ ] Ready for archive

**Specific Success Indicators**:

1. User can change theme from settings menu
2. Theme colors applied to all dashboard elements
3. Configuration saved to config.yaml
4. Configuration loads on dashboard restart
5. All 27 tests pass
6. No linter errors

---

## ✅ Completion Workflow (Filesystem-First)

**After All Work Complete**:

1. **Request Review**: Ask reviewer to assess achievement completion
2. **Reviewer Creates Feedback File**:
   - **If Approved**: Create `execution/feedbacks/APPROVED_31.md`
   - **If Fixes Needed**: Create `execution/feedbacks/FIX_31.md` with detailed issues
3. **Filesystem = Source of Truth**: Achievement completion tracked by APPROVED file existence

**Do NOT**:
- ❌ Manually update PLAN markdown with "✅ Achievement complete"
- ❌ Add checkmarks to Achievement Index
- ❌ Update "Current Status & Handoff"

**DO**:
- ✅ Request reviewer feedback after work complete
- ✅ Wait for `APPROVED_31.md` or `FIX_31.md` file creation
- ✅ If FIX required: Address issues, request re-review

---

## 📝 Notes

**Common Pitfalls**:

- **Color Names**: Rich color names are specific (e.g., "bright_cyan" not "light_cyan")
- **YAML Parsing**: Invalid YAML breaks configuration, need robust error handling
- **Theme Coverage**: Easy to miss color references, need systematic replacement
- **Configuration File Location**: Ensure file path is correct and accessible

**Resources**:

- Rich color documentation: https://rich.readthedocs.io/en/stable/appendix/colors.html
- PyYAML documentation: https://pyyaml.org/wiki/PyYAMLDocumentation
- Existing dashboard code for color usage patterns

**Design Notes**:

- **Theme Scope**: Global (all dashboards share theme)
- **Configuration Scope**: Global (all dashboards share configuration)
- **Theme Preview**: Important for user to see before applying
- **Default Values**: Ensure sensible defaults if config.yaml missing

---

## 🔄 Active EXECUTION_TASKs

**Real-Time Tracking**:

| EXECUTION                                       | Status   | Progress | Notes |
| ----------------------------------------------- | -------- | -------- | ----- |
| EXECUTION_TASK_LLM-DASHBOARD-CLI_31_01 | Planning | 0%       | -     |

---

## 📊 Execution Results Synthesis

**To be completed after execution finishes**

---

## 📖 What to Read (Focus Rules)

**When working on this SUBPLAN**, follow these focus rules:

**✅ READ ONLY**:

- This SUBPLAN file (complete file)
- Parent PLAN Achievement 3.1 section (~86 lines)
- Active EXECUTION_TASK (EXECUTION_TASK_LLM-DASHBOARD-CLI_31_01.md)
- `LLM/dashboard/plan_dashboard.py` (to identify color usage)
- `LLM/dashboard/base_dashboard.py` (integration point)

**❌ DO NOT READ**:

- Parent PLAN full content (3000+ lines)
- Other achievements in PLAN
- Other SUBPLANs
- Completed EXECUTION_TASKs

**Context Budget**: ~500 lines total

**Why**: SUBPLAN defines HOW to achieve Achievement 3.1. Reading other achievements adds unnecessary scope.

---

**Ready to Execute**:

- **Designer**: SUBPLAN design complete ✅
- **Next Step**: Create EXECUTION_TASK_LLM-DASHBOARD-CLI_31_01.md
- **Executor**: Will read SUBPLAN objective + approach, then execute
- **Reference**: `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` for workflow

