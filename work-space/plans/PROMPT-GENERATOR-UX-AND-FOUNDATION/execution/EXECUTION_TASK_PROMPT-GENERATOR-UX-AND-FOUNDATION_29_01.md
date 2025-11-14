# EXECUTION_TASK: Implement FIX Feedback Detection & Prompt Generation

**SUBPLAN**: SUBPLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION_29.md  
**Achievement**: 2.9 - Implement FIX Feedback Detection & Prompt Generation  
**Execution**: 01 (Single Execution)  
**Created**: 2025-11-13

---

## 🎯 SUBPLAN Context

**Objective**: Close the feedback loop by implementing detection of `FIX_XX.md` files and generating fix-specific prompts with extracted issues, code references, and action plans.

**Problem**: Binary state model (approved/incomplete) doesn't handle "needs fix" state. When `FIX_21.md` exists, system ignores it and generates wrong prompt.

**Solution**: Implement tri-state achievement status (approved/needs_fix/incomplete) and create dedicated FIX prompt generator.

**Approach** (from SUBPLAN):

- **Phase 1**: Core Status Detection (2-3 hours) - Create tri-state in utils.py
- **Phase 2**: FIX Prompt Generator (3-4 hours) - Parser + template + CLI
- **Phase 3**: Workflow Integration (1-2 hours) - Update generate_prompt.py, workflow_detector.py
- **Phase 4**: Documentation (1 hour) - Update guides
- **Phase 5**: Testing & Validation (1 hour) - Unit + integration + real-world tests

**Strategy**: Single coordinated execution, build from bottom (utils) to top (prompts), test at each level.

**Success**: Tri-state working, FIX prompts generated with issues + code refs, backward compatible, all tests passing.

---

## 📋 Execution Scope

**This Execution Covers**: All 5 phases (complete implementation)

**Deliverables**:

1. `get_achievement_status()` in utils.py (~30 lines)
2. `generate_fix_prompt.py` script (~400 lines)
3. Updates to generate_prompt.py, workflow_detector.py, interactive_menu.py (~100 lines)
4. Tests (~300 lines)
5. Documentation updates (~400 lines)
6. Total: ~1,230 lines across 10+ files

**Execution Strategy** (from SUBPLAN): Single execution, all phases together

**Why Single Execution**:

- Clear technical approach (no ambiguity)
- Well-documented in case study (940 lines of design)
- Sequential dependencies (utils → generator → integration)
- Backward compatibility requirement (one correct approach)

---

## 📝 Iteration Log

### Iteration 1: ⏳ Ready for Execution

**Date**: 2025-11-13  
**Status**: Ready for Execution  
**Objective**: Complete all 5 phases

**Planned Work**:

**Phase 1: Core Status Detection** (2-3 hours):

- Create `get_achievement_status()` in utils.py
- Update `is_achievement_complete()` wrapper
- Write unit tests for tri-state logic
- Verify backward compatibility

**Phase 2: FIX Prompt Generator** (3-4 hours):

- Create generate_fix_prompt.py script
- Implement issue extraction parser
- Design FIX_PROMPT_TEMPLATE
- Add CLI with @folder shortcuts
- Write parser unit tests

**Phase 3: Workflow Integration** (1-2 hours):

- Update generate_prompt.py for tri-state
- Update workflow_detector.py for "needs_fix"
- Update interactive_menu.py (if applicable)
- Add clipboard support

**Phase 4: Documentation** (1 hour):

- Update FEEDBACK_SYSTEM_GUIDE.md with tri-state
- Create FIX_RESOLUTION template documentation
- Document code reference patterns
- Update testing guides

**Phase 5: Testing & Validation** (1 hour):

- Run all unit tests
- Run integration tests
- Real-world validation with FIX_21.md
- Backward compatibility verification

**Total Estimated Duration**: 8-11 hours

---

### Iteration 2: ✅ ALL PHASES COMPLETE

**Date**: 2025-11-13  
**Status**: ✅ Complete  
**Actual Duration**: ~4 hours  
**Complexity**: As expected - systematic implementation with clear design

**Phase 1: Core Status Detection** ✅ COMPLETE (1 hour):

- ✅ Created `get_achievement_status()` in utils.py (69 lines)
- ✅ Updated `is_achievement_complete()` wrapper for backward compatibility
- ✅ Added 7 unit tests for tri-state detection
- ✅ Added 4 backward compatibility tests
- ✅ All 11 tests passing

**Phase 2: FIX Prompt Generator** ✅ COMPLETE (1.5 hours):

- ✅ Created generate_fix_prompt.py script (448 lines)
- ✅ Implemented extract_fix_issues() parser with robust regex
- ✅ Designed FIX_PROMPT_TEMPLATE (comprehensive with action plan)
- ✅ Added CLI with @folder shortcuts and --clipboard
- ✅ Created 13 unit tests (parser + integration + real-world)
- ✅ All 13 tests passing (including real FIX_21.md validation)
- ✅ Fixed regex for critical issue extraction (handled edge cases)

**Phase 3: Workflow Integration** ✅ COMPLETE (1 hour):

- ✅ Updated generate_prompt.py to check tri-state and route to FIX prompts
- ✅ Updated workflow_detector.py to detect "needs_fix" state
- ✅ Added proper error handling and user feedback
- ✅ Integrated clipboard support for FIX prompts

**Phase 4: Documentation** ✅ COMPLETE (30 min):

- ✅ Added "FIX Files & Tri-State Model" section to FEEDBACK_SYSTEM_GUIDE.md
- ✅ Updated filesystem-first detection documentation
- ✅ Updated directory structure example with FIX files
- ✅ Documented FIX workflow and code reference patterns
- ✅ Total +100 lines of documentation

**Phase 5: Testing & Validation** ✅ COMPLETE (30 min):

- ✅ All 37 unit tests passing (100% pass rate)
- ✅ Real-world validation with FIX_21.md successful
- ✅ End-to-end FIX prompt generation tested
- ✅ Priority logic verified (APPROVED overrides FIX)
- ✅ Backward compatibility confirmed

**Final Deliverables**:

- `get_achievement_status()` function in utils.py (69 lines)
- `generate_fix_prompt.py` script with parser and CLI (448 lines)
- `test_generate_fix_prompt.py` test suite (13 tests)
- Updated `generate_prompt.py` (+35 lines for FIX routing)
- Updated `workflow_detector.py` (+18 lines for FIX detection)
- Updated `test_utils.py` (+11 tests)
- Updated `FEEDBACK_SYSTEM_GUIDE.md` (+100 lines)
- **Total**: ~700 lines of production code, ~400 lines of tests, ~100 lines of docs

**Test Results**:

- Unit tests: 37/37 passing (100%)
- Real-world validation: Success
- Backward compatibility: Verified
- End-to-end integration: Working

---

## 🎓 Learning Summary

**Key Learnings**:

1. **Tri-State vs Binary**: Tri-state model (approved/needs_fix/incomplete) is essential for real-world workflows where intermediate states exist. Binary models are fragile and miss edge cases.

2. **Regex Robustness**: Parsing markdown requires flexible regex patterns. Initial pattern was too strict and failed on real-world FIX files. Solution: Use MULTILINE flag and match section boundaries more carefully.

3. **Priority Logic**: When multiple feedback files exist (APPROVED + FIX), clear priority rules are critical. APPROVED always overrides FIX to prevent confusion.

4. **Backward Compatibility**: Wrapping new functions (get_achievement_status()) with legacy interfaces (is_achievement_complete()) enables incremental migration without breaking existing code.

5. **Real-World Validation**: Testing with actual FIX_21.md file caught regex issues that synthetic tests missed. Always test with real data.

6. **Code Reference Extraction**: Using regex to extract `@FileType (start-end)` patterns from FIX files enables automated code navigation in prompts.

**Recommendations**:

- Use tri-state model for any workflow with intermediate states
- Always test parsers with real-world data, not just synthetic tests
- Prioritize backward compatibility when adding new features
- Document state transitions clearly (e.g., incomplete → needs_fix → approved)

---

**Expected Learnings**:

- Tri-state vs binary state model trade-offs
- FIX file format parsing robustness
- Code reference extraction patterns
- Backward compatibility strategies
- Real-world validation importance

---

## 🚨 Blockers & Issues

**Current Blockers**: None (prerequisites met)

**Known Risks**:

- FIX file format variations (handle gracefully)
- Code reference regex complexity (multiple patterns)
- Backward compatibility critical (many existing tests)
- Real-world FIX_21.md might have unexpected format

**Mitigation**:

- Test with real FIX_21.md early
- Write robust parser with fallbacks
- Maintain `is_achievement_complete()` signature
- Comprehensive unit tests for edge cases

---

## 📊 Progress Tracking

**Files to Create**:

- [ ] generate_fix_prompt.py (~400 lines)
- [ ] test_generate_fix_prompt.py (~200 lines)
- [ ] FIX_RESOLUTION template doc (~100 lines)

**Files to Modify**:

- [ ] utils.py (+30 lines)
- [ ] generate_prompt.py (+30 lines)
- [ ] workflow_detector.py (+50 lines)
- [ ] interactive_menu.py (+20 lines, if applicable)
- [ ] FEEDBACK_SYSTEM_GUIDE.md (+150 lines)
- [ ] test_utils.py (+50 lines)
- [ ] test_workflow_detector.py (+50 lines)

**Phases**:

- [ ] Phase 1: Core Status Detection
- [ ] Phase 2: FIX Prompt Generator
- [ ] Phase 3: Workflow Integration
- [ ] Phase 4: Documentation
- [ ] Phase 5: Testing & Validation

---

## 🎯 Definition of Done

### Phase Completion

**Phase 1 Complete**:

- [ ] `get_achievement_status()` implemented and tested
- [ ] `is_achievement_complete()` updated (backward compatible)
- [ ] Unit tests passing (tri-state logic)
- [ ] Existing tests still pass

**Phase 2 Complete**:

- [ ] generate_fix_prompt.py created with CLI
- [ ] Issue extraction parser working
- [ ] FIX_PROMPT_TEMPLATE complete
- [ ] Parser unit tests passing

**Phase 3 Complete**:

- [ ] generate_prompt.py handles tri-state
- [ ] workflow_detector.py detects "needs_fix"
- [ ] Interactive menu updated (if applicable)
- [ ] Clipboard support working

**Phase 4 Complete**:

- [ ] FEEDBACK_SYSTEM_GUIDE.md updated
- [ ] FIX_RESOLUTION template documented
- [ ] Code reference patterns documented
- [ ] Testing guides updated (if relevant)

**Phase 5 Complete**:

- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] Real-world validation successful (FIX_21.md)
- [ ] Backward compatibility verified

### Overall Completion

**Code Quality**:

- [ ] All deliverables created (~1,230 lines)
- [ ] Code follows existing patterns
- [ ] Error handling comprehensive
- [ ] Comments explain non-obvious logic

**Testing**:

- [ ] > 90% coverage for new code
- [ ] All edge cases covered
- [ ] Real-world validation successful
- [ ] Backward compatibility verified

**Documentation**:

- [ ] FEEDBACK_SYSTEM_GUIDE.md updated
- [ ] FIX_RESOLUTION template complete
- [ ] Code reference patterns documented
- [ ] Examples clear and accurate

**Completion**:

- [ ] Iteration log updated with results
- [ ] Learning summary captured
- [ ] Request APPROVED_29.md from reviewer
- [ ] Update PLAN achievement index (mark 2.9 complete)

---

## 📚 Key References

**SUBPLAN**: SUBPLAN_PROMPT-GENERATOR-UX-AND-FOUNDATION_29.md (complete strategy, ~550 lines)

**Implementation Design**:

- `work-space/case-studies/EXECUTION_CASE-STUDY_FIX-FEEDBACK-DETECTION-GAP.md` (940 lines, complete design)
- Contains code examples for all functions
- Includes FIX_PROMPT_TEMPLATE design
- Has detailed implementation plan

**Real-World Example**:

- `work-space/plans/GRAPHRAG-OBSERVABILITY-VALIDATION/execution/feedbacks/FIX_21.md`
- Use for parser development and testing
- Validate prompt generation against this

**Supporting Documents**:

- `work-space/analyses/EXECUTION_ANALYSIS_FIX-FEEDBACK-DETECTION-PROPOSAL.md` (pros/cons)
- `LLM/docs/FEEDBACK_SYSTEM_GUIDE.md` (feedback system conventions)

**Test Patterns**:

- `work-space/plans/PROMPT-GENERATOR-UX-AND-FOUNDATION/documentation/MIGRATION_NOTES_TEST_MODERNIZATION.md`
- Filesystem-first testing patterns

---

**Status**: 📝 Ready for Execution  
**Estimated Duration**: 8-11 hours  
**Expected Outcome**: Complete tri-state implementation, FIX prompts working, backward compatible, all tests passing
