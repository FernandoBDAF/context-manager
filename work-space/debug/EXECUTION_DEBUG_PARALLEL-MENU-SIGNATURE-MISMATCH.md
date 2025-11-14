# EXECUTION_DEBUG: Parallel Menu Signature Mismatch

**Created**: 2025-11-14  
**Type**: EXECUTION_DEBUG  
**Category**: Function Signature Bug  
**Status**: 🔧 Fixed

---

## 🐛 Bug Report

### Error Message

```
TypeError: show_parallel_menu() takes 2 positional arguments but 3 were given
```

### Context

**When**: User selects option 6 "Access Parallel Execution Menu" from interactive menu  
**Where**: `interactive_menu.py` line 451  
**Plan**: GRAPHRAG-OBSERVABILITY-VALIDATION  
**Trigger**: Selecting option 6 after parallel.json detection

### Full Stack Trace

```
Traceback (most recent call last):
  File ".../generate_prompt.py", line 1795, in <module>
    main()
  File ".../generate_prompt.py", line 1294, in main
    menu.show_pre_execution_menu()
  File ".../interactive_menu.py", line 451, in show_pre_execution_menu
    menu_choice = show_parallel_menu(parallel_data, plan_name, plan_path.parent)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: show_parallel_menu() takes 2 positional arguments but 3 were given
```

---

## 🔍 Root Cause Analysis

### Function Signature Check

**File**: `parallel_workflow.py` line 163

```python
def show_parallel_menu(parallel_data: Dict, plan_name: str) -> str:
    """Show parallel execution menu."""
```

**Signature**: Takes 2 arguments: `parallel_data`, `plan_name`

### Function Call Check

**File**: `interactive_menu.py` line 451

```python
menu_choice = show_parallel_menu(parallel_data, plan_name, plan_path.parent)
```

**Call**: Passing 3 arguments: `parallel_data`, `plan_name`, `plan_path.parent` ❌

### Root Cause

**Mismatch**: Integration code passes 3 arguments but function only accepts 2.

**Why This Happened**:
- `show_parallel_menu()` only displays menu (doesn't need `plan_path`)
- `handle_parallel_menu_selection()` needs `plan_path` for batch operations
- Integration code incorrectly assumed both functions had same signature

---

## 🔧 Solution

### Fix: Remove Extra Argument

**File**: `interactive_menu.py` line 451

**Before**:
```python
menu_choice = show_parallel_menu(parallel_data, plan_name, plan_path.parent)
```

**After**:
```python
menu_choice = show_parallel_menu(parallel_data, plan_name)
```

**Reasoning**: `show_parallel_menu()` only displays menu and returns choice - doesn't need `plan_path`

---

## 🎓 Lessons Learned

1. **Verify function signatures** before calling
2. **Test integration points** not just individual functions
3. **Read error messages carefully** - TypeError clearly indicated the problem
4. **Simple fixes are often best** - removing one argument solved it

---

**Status**: ✅ Fixed  
**Effort**: 1 line change  
**Verified**: Tested with GRAPHRAG-OBSERVABILITY-VALIDATION

