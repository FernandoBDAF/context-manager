# EXECUTION_TASK: Color Themes & Customization

**Type**: EXECUTION_TASK  
**Subplan**: SUBPLAN_LLM-DASHBOARD-CLI_31.md  
**Mother Plan**: PLAN_LLM-DASHBOARD-CLI.md  
**Plan**: LLM-DASHBOARD-CLI  
**Achievement**: 3.1 (Color Themes & Customization)  
**Iteration**: 1  
**Execution Number**: 01 (first attempt)  
**Previous Execution**: N/A  
**Circular Debug Flag**: No  
**Started**: 2025-11-14 23:00 UTC  
**Status**: Planning

**Metadata Tags**: `#dashboard #themes #customization #configuration`

**File Location**: `work-space/plans/LLM-DASHBOARD-CLI/execution/EXECUTION_TASK_LLM-DASHBOARD-CLI_31_01.md`

---

## 📏 Size Limit

**⚠️ HARD LIMIT**: 200 lines maximum

**Current**: ~140 lines (within limit)

---

## 🎯 SUBPLAN Context

**Objective** (from SUBPLAN_LLM-DASHBOARD-CLI_31.md):

Create a flexible theme system and user customization framework that allows users to personalize their dashboard experience with color themes, configurable display options, and persistent preferences. Provides three pre-built themes (default, dark, light) along with a settings menu accessible from the dashboard.

**Approach Summary**:

Build simple file-based configuration using YAML with Theme class for color mappings. Implementation phases:
1. Theme system with 3 built-in themes (default, dark, light)
2. DashboardConfig class for YAML management
3. Create default config.yaml file
4. Integrate theme into dashboards (base, main, plan)
5. Add settings menu with theme switching
6. Write comprehensive tests (~27 tests)
7. Polish and integrate

**Key Decision**: Use YAML (human-readable), built-in themes (simpler), global configuration (all dashboards share).

---

## 📝 Execution Instructions

### Phase 1: Theme System (45 min)
Create `LLM/dashboard/theme.py`: Theme class with 3 themes (default, dark, light), _load_colors() with color mappings (primary, success, warning, error, info), get_color() method, preview() for theme preview Panel.

### Phase 2: Configuration System (45 min)
Create `LLM/dashboard/config.py`: DashboardConfig class, load/save YAML methods, default values (theme: default, refresh_interval: 1, show_stats: true, show_parallel: true, auto_copy_commands: true), validation, get/set methods.

### Phase 3: Default Config File (15 min)
Create `LLM/dashboard/config.yaml`: YAML file with default values and comments explaining each setting.

### Phase 4: Dashboard Integration (1 hour)
Modify `LLM/dashboard/base_dashboard.py`: Add theme and config support, get_color() utility. Modify `LLM/dashboard/plan_dashboard.py` and `main_dashboard.py`: Load config in __init__, apply theme colors to all render methods (replace hardcoded "cyan", "green", etc. with theme.get_color()).

### Phase 5: Settings Menu (45 min)
Add to `LLM/dashboard/plan_dashboard.py`: show_settings() method with interactive menu, theme switching (_change_theme()), setting toggles (_toggle_setting()), 's' or '7' key handler in handle_action().

### Phase 6: Tests (1 hour)
Create `tests/LLM/dashboard/test_theme.py` (~12 tests): theme loading, color retrieval, previews. Create `tests/LLM/dashboard/test_config.py` (~15 tests): YAML loading/saving, validation, persistence. Mock file operations.

### Phase 7: Polish (15 min)
Verify theme applied consistently, test settings menu, ensure configuration persists, fix any issues.

---

## ✅ Deliverables Checklist

**Files to Create**:
- [ ] `LLM/dashboard/theme.py` (200-250 lines)
- [ ] `LLM/dashboard/config.py` (150-200 lines)
- [ ] `LLM/dashboard/config.yaml` (20-30 lines)
- [ ] `tests/LLM/dashboard/test_theme.py` (200-250 lines)
- [ ] `tests/LLM/dashboard/test_config.py` (200-250 lines)

**Files to Modify**:
- [ ] `LLM/dashboard/base_dashboard.py` (add theme support)
- [ ] `LLM/dashboard/plan_dashboard.py` (apply theme, add settings menu)
- [ ] `LLM/dashboard/main_dashboard.py` (apply theme)

**Tests**:
- [ ] ~27 tests written
- [ ] All tests passing
- [ ] >90% coverage for new code
- [ ] No linter errors

**Functional**:
- [ ] User can change theme from settings
- [ ] Theme persists to config.yaml
- [ ] Theme applies to all dashboard elements
- [ ] Settings menu accessible via 's' or '7'
- [ ] Configuration toggles work

---

## 🧪 Verification Steps

1. Run theme tests: `pytest tests/LLM/dashboard/test_theme.py -v`
2. Run config tests: `pytest tests/LLM/dashboard/test_config.py -v`
3. Run all dashboard tests: `pytest tests/LLM/dashboard/ -v`
4. Manual test: Open settings ('s'), change theme, verify colors update
5. Manual test: Restart dashboard, verify theme persists
6. Manual test: Toggle settings, verify config.yaml updates
7. Check linter errors

---

## 📊 Success Criteria

**This EXECUTION_TASK is complete when**:

- [ ] All 7 phases complete
- [ ] All deliverables created/modified
- [ ] ~27 tests written and passing
- [ ] No linter errors
- [ ] Manual testing confirms theme switching works
- [ ] Configuration persists correctly
- [ ] Settings menu accessible and functional
- [ ] Ready for review (request APPROVED_31.md or FIX_31.md)

**Total Estimated Time**: 2-3 hours

---

## 📝 Notes

**Important Considerations**:

- **PyYAML Dependency**: Verify pyyaml is installed, add to requirements if needed
- **Color Names**: Use Rich standard color names (see Rich color docs)
- **Configuration Path**: Use relative path for portability
- **Theme Preview**: Help users visualize theme before applying

**Reference Implementations**:

- Existing dashboard rendering methods for color usage patterns
- Rich Panel examples for theme preview

**Quick Wins**:

- Start with color constants, systematically replace
- Reuse existing settings menu patterns from action menu
- YAML is self-documenting with comments

---

**Ready to Execute**: All phases defined, approach clear, ready for implementation ✅

