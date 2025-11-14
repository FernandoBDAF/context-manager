# SUBPLAN: Performance Optimization + Library Integration

**Type**: SUBPLAN  
**Mother Plan**: PLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION.md  
**Plan**: PROMPT-GENERATOR-UX-AND-FOUNDATION  
**Achievement Addressed**: Achievement 3.2 (Performance Optimization + Library Integration)  
**Achievement**: 3.2  
**Status**: Not Started  
**Created**: 2025-11-13 22:00 UTC  
**Estimated Effort**: 2 hours

**Metadata Tags**: See `LLM/guides/METADATA-TAGS.md` for virtual organization system

**File Location**: `work-space/plans/PROMPT-GENERATOR-UX-AND-FOUNDATION/subplans/SUBPLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION_32.md`

**Size**: ~580 lines

**Note**: This SUBPLAN operates independently - Designer creates design, plans execution(s), then Executor(s) execute. See `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` for complete workflow.

---

## 🎯 Objective

Achieve <3s prompt generation through intelligent caching and comprehensive performance monitoring, while integrating production-ready `caching` and `metrics` libraries from `core/libraries/` to establish observable performance patterns for production deployment.

**Context**: Current implementation parses PLAN files on every run (1-2s overhead) with no caching or performance visibility. Users experience slow response times, and we have no data on bottlenecks or optimization opportunities.

**Goal**: Implement caching for hot paths (PLAN parsing, directory listings, regex patterns) and comprehensive metrics collection, achieving 70% performance improvement (1-2s → 100-200ms for cached operations) while establishing observable performance patterns.

---

## 📋 What Needs to Be Created

### Files to Create

1. **`LLM/docs/PERFORMANCE_OPTIMIZATION_GUIDE.md`** (~150 lines):
   - Caching patterns and strategies
   - Performance metrics reference
   - Benchmarking methodology
   - Optimization recommendations

### Files to Modify

1. **`LLM/scripts/generation/plan_parser.py`**:

   - Add `@cached` decorator to `parse_plan_file()`
   - Cache with file modification time as key component
   - Add cache hit/miss logging
   - Add performance metrics

2. **`LLM/scripts/generation/utils.py`**:

   - Cache directory listing functions
   - Compile regex patterns at module level
   - Add performance profiling
   - Add metrics instrumentation

3. **`LLM/scripts/generation/workflow_detector.py`**:

   - Cache feedback file listings
   - Optimize filesystem scanning
   - Add performance metrics

4. **`LLM/scripts/generation/generate_prompt.py`**:

   - Add metrics collection (counters, histograms, timers)
   - Instrument main workflow with Timer context manager
   - Add profiling decorators to hot paths
   - Track cache statistics

5. **`LLM/scripts/generation/path_resolution.py`**:
   - Cache folder lookups
   - Compile regex patterns once
   - Add performance logging

### Tests to Create/Modify

1. **`tests/LLM/scripts/generation/test_performance.py`** (~100 lines):

   - Test cache hit rates (>80% target)
   - Test generation time (<3s target)
   - Test cache invalidation on file changes
   - Test memory usage limits
   - Integration performance tests

2. **Update existing tests** (~50 lines):
   - Mock caching for deterministic tests
   - Add performance assertions
   - Test metrics collection

---

## 📝 Approach

**Strategy**: Systematic performance optimization starting with profiling to identify bottlenecks, then apply caching to hot paths, integrate metrics for observability, and validate improvements through benchmarking.

**Method**:

1. **Phase 1 - Integrate Caching Library** (30 min):

   - Add `@cached` decorator to PLAN parsing (biggest bottleneck)
   - Cache key: `{plan_path}:{mtime}` for automatic invalidation
   - Cache directory listings with `@lru_cache`
   - Compile regex patterns at module level (one-time cost)
   - Test cache hit rates and invalidation

2. **Phase 2 - Integrate Metrics Library** (30 min):

   - Define Prometheus-compatible metrics (Counter, Histogram, Timer)
   - Counter: prompt_generation_total (by workflow, status)
   - Histogram: prompt_generation_duration_seconds
   - Counter: plan_cache_hits_total
   - Register metrics with MetricRegistry
   - Instrument workflow functions with Timer context manager

3. **Phase 3 - Profile Hot Paths** (30 min):

   - Create profiling decorator with perf_counter
   - Profile critical functions: parse_plan(), detect_workflow_state(), generate_prompt()
   - Log duration for each function call
   - Identify remaining bottlenecks
   - Document findings in benchmarking report

4. **Phase 4 - Optimize Based on Metrics** (30 min):
   - Apply targeted optimizations based on profiling data
   - Lazy load SUBPLAN content (defer until needed)
   - Batch filesystem operations where possible
   - Create performance tests (<3s target, >80% cache hit rate)
   - Generate before/after benchmarking report
   - Document optimization patterns

**Key Considerations**:

- **Cache Invalidation**: Use file mtime in cache key for automatic invalidation
- **Memory Limits**: Set reasonable cache sizes (50 PLANs, 100 directory listings)
- **TTL**: 5-minute TTL for caches (balance freshness vs performance)
- **Metrics Overhead**: Ensure metrics collection doesn't degrade performance
- **Testing**: Performance tests should be deterministic (mock time-sensitive operations)

---

## 🔄 Execution Strategy

**Execution Count**: Single

**Rationale**: This is a systematic performance optimization task with clear sequential phases. All work builds on profiling data and requires coordinated implementation across multiple files. No experimentation needed - optimization targets are well-defined from analysis.

**EXECUTION_TASK**: `EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_32_01.md`

**Decision Guidance**: Single execution chosen because:

- Clear technical approach (profile → cache → measure → optimize)
- Well-documented in supporting analysis (EXECUTION_ANALYSIS_LIBRARY-INTEGRATION-OPPORTUNITIES-PRIORITY-3.md)
- Sequential dependencies (profiling → optimization → validation)
- Coordinated changes across multiple files
- Quantifiable success criteria (<3s, 70% improvement, >80% cache hit rate)

---

## 🧪 Tests Required

### Test File

- **Path**: `tests/LLM/scripts/generation/test_performance.py`
- **Naming Convention**: `test_<module_name>.py`
- **Test Infrastructure**: Use existing pytest fixtures

### Test Cases to Cover

**Caching Tests**:

1. Test cache hit on repeated PLAN parse (same file)
2. Test cache miss on first PLAN parse
3. Test cache invalidation when file modified (mtime changes)
4. Test cache size limits (max_size=50)
5. Test cache TTL expiration (after 5 minutes)
6. Test directory listing cache
7. Test cache key generation (includes mtime)

**Performance Tests**:

1. Test PLAN parsing time <3s (uncached)
2. Test PLAN parsing time <200ms (cached, >80% hits)
3. Test full prompt generation <3s
4. Test cache hit rate >80% after 10 repeated runs
5. Test memory usage within limits

**Metrics Tests**:

1. Test counter increments (prompt_generation_total)
2. Test histogram records duration (prompt_generation_duration_seconds)
3. Test cache hit counter increments
4. Test metrics registered with registry
5. Test Timer context manager records duration

**Integration Tests**:

1. Test end-to-end performance (parse → detect → generate) <3s
2. Test cache persistence across multiple calls
3. Test metrics collection doesn't degrade performance (overhead <5%)
4. Test profiling decorator doesn't affect results

### Coverage Requirements

- **Target Coverage**: >90% for caching and metrics integration code
- **Required Test Types**:
  - Unit tests for cache behavior
  - Performance benchmarks for optimization validation
  - Integration tests for end-to-end performance
  - Metrics collection tests

---

## ✅ Expected Results

### Functional Changes

- **Caching**: PLAN parsing cached with automatic invalidation on file changes
- **Metrics**: Comprehensive Prometheus-compatible metrics for all workflows
- **Profiling**: Performance logging for hot paths with duration tracking
- **Optimization**: 70% faster for repeated runs, <3s for all operations

### Performance Changes

- **PLAN Parsing**: 1-2s → 100-200ms (cached, >80% hit rate)
- **Directory Listings**: ~50ms → <5ms (cached)
- **Regex Compilation**: ~10ms → <1ms (one-time, module-level)
- **Overall**: 70% improvement for typical workflows

### Observable Outcomes

**Before** (No Caching):

```bash
$ time python generate_prompt.py @FEATURE --next
# First run: 1.8s
# Second run: 1.8s (full reparse)
# No visibility into bottlenecks
```

**After** (Cached + Metrics):

```bash
$ time python generate_prompt.py @FEATURE --next
# First run: 1.8s (cache miss)
# Second run: 0.5s (cache hit - 72% faster!)
# Metrics show: cache_hit_rate=85%, parse_time=120ms

# Performance summary available:
$ python -c "from LLM.scripts.generation import generate_prompt; print(generate_prompt.get_performance_stats())"
{
  "cache_hit_rate": 0.85,
  "avg_parse_time": 0.12,
  "avg_generation_time": 0.48,
  "total_calls": 20
}
```

**User Experience**:

- ✅ Instant response for repeated operations
- ✅ Transparent caching (no user config needed)
- ✅ Automatic cache invalidation (no stale data)
- ✅ Observable performance (metrics endpoint ready)

---

## 🔍 Conflict Analysis with Other Subplans

**Review Existing Subplans**:

- SUBPLAN_01 - 31: Completed or approved
- No conflicts identified

**Check for**:

- **Overlap**: No overlap - this adds performance layer to existing functionality
- **Conflicts**: No conflicts - caching is transparent to existing code
- **Dependencies**: Builds on Achievement 3.1 (logging integration)
- **Integration**: Works alongside existing features without breaking changes

**Analysis**:

- **No conflicts detected**: This achievement adds caching and metrics without modifying core logic
- **Backward Compatible**: Caching is transparent - existing function signatures unchanged
- **Library Available**: `core/libraries/caching` and `core/libraries/metrics` exist
- **Clean Integration**: Decorators and metrics wrap existing code

**Result**: Safe to proceed ✅

---

## 🔗 Dependencies

### Other Subplans

- **Achievement 3.1**: Provides logging infrastructure (logger instances)
- **No blocking dependencies**: Can proceed independently

### External Dependencies

- **Python**: 3.7+ (for functools.lru_cache)
- **Libraries**: `core/libraries/caching`, `core/libraries/metrics` (already exist)
- **pytest**: For performance testing (already installed)
- **time**: perf_counter for profiling (stdlib)

### Prerequisite Knowledge

- Understand current performance bottlenecks
- Familiarity with caching strategies (TTL, LRU, invalidation)
- Knowledge of Prometheus metrics (Counter, Histogram, Timer)
- Understanding of Python decorators and context managers

### Reference Documents

- **`work-space/analyses/EXECUTION_ANALYSIS_LIBRARY-INTEGRATION-OPPORTUNITIES-PRIORITY-3.md`**: Complete performance analysis and optimization strategy (lines 337-522)
- **`core/libraries/caching/`**: Caching library documentation
- **`core/libraries/metrics/`**: Metrics library documentation

---

## 🔄 Execution Task Reference

**Execution Tasks** (created during execution):

_None yet - will be created when execution starts_

**First Execution**: `EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_32_01.md`

---

## 📊 Success Criteria

**This Subplan is Complete When**:

- [ ] PLAN parsing cached with mtime-based invalidation
- [ ] Directory listings cached with LRU cache
- [ ] Regex patterns compiled at module level
- [ ] Metrics integrated (Counter, Histogram, Timer)
- [ ] Profiling decorators added to hot paths
- [ ] Performance improvement validated (70% faster)
- [ ] Target achieved (<3s for all operations)
- [ ] Cache hit rate verified (>80% for repeated runs)
- [ ] Performance tests passing (all assertions met)
- [ ] Benchmarking report created (before/after comparison)
- [ ] Documentation complete (PERFORMANCE_OPTIMIZATION_GUIDE.md)
- [ ] EXECUTION_TASK complete
- [ ] **Achievement feedback received** (see Completion Workflow below)
- [ ] Ready for archive

**Specific Criteria**:

1. **Performance**: <3s for prompt generation, 70% faster for cached operations
2. **Caching**: >80% hit rate, automatic invalidation on file changes
3. **Metrics**: All workflows instrumented, Prometheus-compatible
4. **Profiling**: Hot paths identified and logged
5. **Tests**: Performance tests validate targets (<3s, >80% hit rate)

---

## ✅ Completion Workflow (Filesystem-First)

**After All Work Complete**:

1. **Request Review**: Ask reviewer to assess achievement completion
2. **Reviewer Creates Feedback File**:
   - **If Approved**: Create `execution/feedbacks/APPROVED_32.md` (32 = achievement number without dot)
   - **If Fixes Needed**: Create `execution/feedbacks/FIX_32.md` with detailed issues
3. **Filesystem = Source of Truth**: Achievement completion tracked by APPROVED file existence, not PLAN markdown

**Achievement Index in PLAN**:

- Defines structure (list of all achievements)
- NOT updated with checkmarks or status manually
- Filesystem (`APPROVED_32.md` file) indicates completion status

**Do NOT**:

- ❌ Manually update PLAN markdown with "✅ Achievement complete"
- ❌ Add checkmarks to Achievement Index
- ❌ Update "Current Status & Handoff" to mark achievement done

**DO**:

- ✅ Request reviewer feedback after work complete
- ✅ Wait for `APPROVED_32.md` or `FIX_32.md` file creation
- ✅ If FIX required: Address issues, request re-review

**Why Filesystem-First**:

- Single source of truth (files, not markdown parsing)
- Automated detection by scripts (`generate_prompt.py`)
- Clear audit trail (feedback files are timestamped, contain rationale)
- Prevents markdown parsing issues

**Reference**: See `LLM/docs/FEEDBACK_SYSTEM_GUIDE.md` for complete guidance

---

## 📝 Notes

**Common Pitfalls**:

- **Cache Invalidation**: Don't forget to include mtime in cache key
- **Memory Leaks**: Set appropriate cache size limits
- **Metrics Overhead**: Ensure metrics don't degrade performance >5%
- **Testing**: Use mocks for deterministic performance tests
- **Documentation**: Benchmark before AND after for accurate comparison

**Resources**:

- **Analysis Document**: `work-space/analyses/EXECUTION_ANALYSIS_LIBRARY-INTEGRATION-OPPORTUNITIES-PRIORITY-3.md` (lines 337-522 - complete performance analysis)
- **Library Docs**: `core/libraries/caching/`, `core/libraries/metrics/`
- **Profiling**: Python `time.perf_counter()` for accurate timing

**Implementation Notes**:

- Start with profiling to identify actual bottlenecks (don't assume)
- Cache at the function level (PLAN parsing, directory listings)
- Use decorators for clean integration (@cached, @profile)
- Metrics should be Prometheus-compatible for future observability stack

---

## 📖 What to Read (Focus Rules)

**When working on this SUBPLAN**, follow these focus rules to minimize context:

**✅ READ ONLY**:

- This SUBPLAN file (complete file)
- Parent PLAN Achievement 3.2 section (203 lines)
- Active EXECUTION_TASKs (if any exist)
- Parent PLAN "Current Status & Handoff" section (14 lines)
- Supporting analysis document (lines 337-522 for performance details)

**❌ DO NOT READ**:

- Parent PLAN full content
- Other achievements in PLAN
- Other SUBPLANs
- Completed EXECUTION_TASKs (unless needed for context)
- Completed work

**Context Budget**: ~800 lines (this SUBPLAN + achievement section + handoff + analysis snippets)

**Independent Operation**: This SUBPLAN operates independently:

- **Designer Phase**: Create SUBPLAN, design approach, plan execution(s) ✅
- **Executor Phase**: Execute EXECUTION_TASK(s) according to plan
- **Synthesis Phase**: Review results, synthesize learnings, complete SUBPLAN

**Executor Context**: Executor reads SUBPLAN objective (~2 sentences) and approach section only, not full SUBPLAN.

**Why**: SUBPLAN defines HOW to achieve one achievement. Reading other achievements or full PLAN adds scope and confusion.

**📖 See**: `LLM/guides/FOCUS-RULES.md` for complete focus rules and `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` for workflow.

---

## 🔄 Active EXECUTION_TASKs

**Real-Time Tracking** (update as EXECUTIONs progress):

| EXECUTION                                               | Status   | Progress | Notes          |
| ------------------------------------------------------- | -------- | -------- | -------------- |
| EXECUTION_TASK_PROMPT-GENERATOR-UX-AND-FOUNDATION_32_01 | Planning | 0%       | Ready to start |

**Status Options**:

- **Planning**: EXECUTION_TASK created, not yet executing
- **Executing**: Work in progress
- **Complete**: Execution finished, deliverables verified
- **Failed**: Execution encountered issues (document in notes)

**Update Frequency**: Update this table as EXECUTIONs progress

**For Single Execution**: Single row in table

---

## 📊 Execution Results Synthesis

**Review All Results** (complete after all EXECUTIONs finish):

**EXECUTION Summary**:

- **EXECUTION_01 Results**: [Summary of what was achieved, learnings, outcomes]

**Learnings**:

- [What worked?]
- [What didn't work?]
- [What patterns emerged?]
- [What should be adopted?]

**For Single Execution**: Document learnings from that execution

**When to Complete**: After EXECUTION finishes, before marking SUBPLAN complete

---

**Ready to Execute**:

- **Designer**: Complete SUBPLAN design ✅, plan execution ✅, now create EXECUTION_TASK ✅
- **Executor**: Read SUBPLAN objective, execute according to plan
- **Reference**: `LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md` for complete workflow, `LLM/protocols/IMPLEMENTATION_START_POINT.md` for execution workflows
