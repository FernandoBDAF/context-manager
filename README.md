# LLM Methodology: Structured Development Framework

**Version**: 2.0  
**Status**: 🚀 Production Ready  
**Last Updated**: November 15, 2025

A comprehensive framework for structured, LLM-assisted software development with real-time progress tracking, parallel execution support, and production-ready libraries.

---

## 🎯 Overview

The **LLM Methodology** is a battle-tested framework for managing complex software development with AI assistance. It provides:

- **5-Tier Planning Hierarchy**: From strategic vision (NORTH_STAR) to executable tasks (EXECUTION_TASK)
- **Real-Time Dashboard**: Rich terminal UI for tracking progress across multiple plans
- **Production Libraries**: Logging, metrics, error handling, caching, and more
- **Parallel Execution**: Intelligent dependency analysis and batch execution
- **Automated Workflows**: Scripts for generation, validation, and archiving

Perfect for teams building complex systems with LLM assistance, or solo developers managing ambitious projects.

---

## ✨ Key Features

### 📊 Interactive Dashboard

```bash
python LLM/main.py
```

Rich terminal dashboard showing:
- **Active Plans**: Visual progress tracking (11/18 achievements, 61%)
- **Parallel Opportunities**: Automatic detection with time savings (67% faster)
- **Real-Time Updates**: Filesystem monitoring with auto-refresh
- **Quick Actions**: One-key shortcuts for common operations
- **Health Scores**: Plan health metrics (0-100) with component breakdown

### 📐 5-Tier Planning Hierarchy

```
NORTH_STAR (800-2,000 lines)    Strategic vision, principles
    ↓
GRAMMAPLAN (600-1,500 lines)    Coordinates 4-6 PLANs
    ↓
PLAN (300-900 lines)            Feature/project scope
    ↓
SUBPLAN (200-600 lines)         Single achievement design
    ↓
EXECUTION_TASK (<200 lines)     Executable work unit
```

Each tier has:
- **Size Limits**: Enforced via validation scripts
- **Templates**: Copy-paste ready structures
- **Protocols**: Step-by-step workflows
- **Guides**: Comprehensive how-tos

### 🔄 Parallel Execution

Automatically detect and execute independent achievements in parallel:

```bash
# Dashboard shows parallel opportunities
Level 0 Group (3 achievements):
  ├─ 3.1: Performance Optimization
  ├─ 3.2: Error Handling Enhancement
  └─ 3.3: Documentation Update
  
  Time: 3.5h parallel vs 10.5h sequential
  Savings: 7.0h (67%)
```

Batch creation with dependency tracking:
```bash
python LLM/scripts/generation/batch_subplan.py --plan-path work-space/plans/MY-PLAN --level 0
python LLM/scripts/generation/batch_execution.py --plan-path work-space/plans/MY-PLAN --level 0
```

### 🏗️ Production-Ready Libraries

**Core Libraries** (`LLM/core/libraries/`):
- **Logging**: Structured JSON logging with context, Loki integration
- **Metrics**: Prometheus-compatible counters, histograms, gauges
- **Error Handling**: Structured exceptions with context and suggestions
- **Retry**: Exponential backoff with configurable policies
- **Caching**: LRU cache with TTL and mtime-based invalidation
- **Validation**: Rule-based validation with clear error messages
- **Serialization**: Pydantic-based serialization with custom encoders
- **Rate Limiting**: Token bucket rate limiter
- **Concurrency**: Async execution with TPM tracking
- **Database**: MongoDB operations with error handling

All libraries are:
- ✅ Fully tested (>90% coverage)
- ✅ Type-hinted
- ✅ Documented with examples
- ✅ Production-proven

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone <repository-url>
cd context_manager

# Install dependencies
pip install -r requirements.txt
```

**Dependencies**:
- Python 3.8+
- pydantic>=2.7.0 (data validation)
- pymongo>=4.7.0 (MongoDB)
- openai>=1.42.0 (LLM integration)
- pyyaml>=6.0 (configuration)
- rich>=13.0.0 (terminal UI)

### Launch Dashboard

```bash
# Main dashboard (all plans)
python LLM/main.py

# Specific plan
python LLM/main.py --plan 1
```

### Create Your First Plan

```bash
# 1. Read the methodology
cat LLM/LLM-METHODOLOGY.md

# 2. Use the template
cp LLM/templates/PLAN-TEMPLATE.md work-space/plans/PLAN_MY-FEATURE.md

# 3. Follow the start protocol
cat LLM/protocols/IMPLEMENTATION_START_POINT.md
```

### Generate Prompts

```bash
# Interactive mode (auto-detects workflow state)
python LLM/scripts/generation/generate_prompt.py @MY-PLAN

# Create SUBPLAN for achievement 1.2
python LLM/scripts/generation/generate_prompt.py @MY-PLAN --achievement 1.2 --interactive

# Continue execution
python LLM/scripts/generation/generate_prompt.py continue @EXECUTION_TASK_MY-PLAN_12_01.md
```

---

## 📁 Project Structure

```
context_manager/
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── LLM-METHODOLOGY.md              # Complete methodology reference
│
├── LLM/                            # Core framework
│   ├── main.py                     # Dashboard entry point
│   ├── README.md                   # LLM folder documentation
│   │
│   ├── core/                       # Production libraries
│   │   └── libraries/              # Reusable libraries
│   │       ├── logging/            # Structured logging
│   │       ├── metrics/            # Prometheus metrics
│   │       ├── error_handling/     # Exception framework
│   │       ├── retry/              # Retry policies
│   │       ├── caching/            # LRU cache
│   │       ├── validation/         # Rule-based validation
│   │       ├── serialization/      # JSON serialization
│   │       ├── rate_limiting/      # Rate limiter
│   │       ├── concurrency/        # Async execution
│   │       └── database/           # MongoDB operations
│   │
│   ├── dashboard/                  # Interactive dashboard
│   │   ├── main_dashboard.py      # Main dashboard UI
│   │   ├── plan_dashboard.py      # Plan-specific UI
│   │   ├── state_detector.py      # State analysis
│   │   ├── parallel_detector.py   # Parallel detection
│   │   ├── workflow_executor.py   # Action execution
│   │   └── metrics.py             # Dashboard metrics
│   │
│   ├── scripts/                    # Automation tools
│   │   ├── generation/            # Prompt generation
│   │   │   ├── generate_prompt.py         # Main orchestrator
│   │   │   ├── batch_subplan.py          # Batch SUBPLAN creation
│   │   │   └── batch_execution.py        # Batch EXECUTION creation
│   │   ├── validation/            # Size & structure validation
│   │   │   ├── check_plan_size.py
│   │   │   ├── validate_achievement_completion.py
│   │   │   └── validate_subplan_executions.py
│   │   └── archiving/             # Archive completed work
│   │       └── manual_archive.py
│   │
│   ├── templates/                  # Copy-paste templates
│   │   ├── NORTH_STAR-TEMPLATE.md
│   │   ├── GRAMMAPLAN-TEMPLATE.md
│   │   ├── PLAN-TEMPLATE.md
│   │   ├── SUBPLAN-TEMPLATE.md
│   │   ├── EXECUTION_TASK-TEMPLATE.md
│   │   └── PROMPTS.md             # Ready-to-use prompts
│   │
│   ├── guides/                     # How-to guides
│   │   ├── NORTH-STAR-GUIDE.md
│   │   ├── GRAMMAPLAN-GUIDE.md
│   │   ├── SUBPLAN-WORKFLOW-GUIDE.md
│   │   └── FOCUS-RULES.md
│   │
│   ├── protocols/                  # Workflow protocols
│   │   ├── IMPLEMENTATION_START_POINT.md
│   │   ├── CREATE_SUBPLAN.md
│   │   ├── CREATE_EXECUTION.md
│   │   ├── IMPLEMENTATION_RESUME.md
│   │   └── IMPLEMENTATION_END_POINT.md
│   │
│   ├── tests/                      # Comprehensive tests
│   │   ├── dashboard/             # Dashboard tests (232+ tests)
│   │   └── scripts/               # Script tests
│   │
│   └── docs/                       # Additional documentation
│       ├── ERROR_HANDLING_PATTERNS.md
│       ├── PERFORMANCE_OPTIMIZATION_GUIDE.md
│       └── FEEDBACK_SYSTEM_GUIDE.md
│
└── work-space/                     # Active work directory
    ├── north-stars/               # Strategic vision documents
    ├── grammaplans/               # Multi-plan coordination
    ├── plans/                     # Active plans (17+)
    │   └── PLAN_NAME/
    │       ├── PLAN_NAME.md
    │       ├── subplans/         # Achievement designs
    │       ├── execution/        # Execution tasks
    │       │   └── feedbacks/    # APPROVED/FIX files
    │       └── parallel.json     # Parallel execution config
    ├── analyses/                  # Strategic analyses (125+)
    ├── knowledge/                 # Learnings & patterns
    └── archive/                   # Completed work
```

---

## 🎓 Learning Path

### 1. Understand the Methodology (30 min)

Start with the core concepts:

```bash
# Read the methodology overview
cat LLM-METHODOLOGY.md

# Understand the 4-phase workflow
cat LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md
```

**Key Concepts**:
- 5-tier hierarchy (NORTH_STAR → EXECUTION_TASK)
- 4-phase workflow (Design → Plan → Execute → Synthesize)
- Context budgets (what each agent reads)
- Filesystem-first tracking (no manual updates)

### 2. Explore the Dashboard (15 min)

```bash
# Launch and explore
python LLM/main.py

# Try different views
# - Main dashboard (all plans)
# - Plan dashboard (detailed view)
# - Actions menu (execute, create, review)
```

**Dashboard Features**:
- Press `1-6` to select actions
- Press `r` to refresh state
- Press `b` to go back
- Press `s` for settings (themes, auto-copy)

### 3. Create a Sample Plan (1 hour)

Follow the complete workflow:

```bash
# 1. Copy template
cp LLM/templates/PLAN-TEMPLATE.md work-space/plans/PLAN_SAMPLE-FEATURE.md

# 2. Edit plan (define 3-5 achievements)
# Add Achievement Index with clear goals

# 3. Create SUBPLAN for first achievement
python LLM/scripts/generation/generate_prompt.py @SAMPLE-FEATURE --achievement 1.1 --interactive

# 4. Review SUBPLAN in work-space/plans/SAMPLE-FEATURE/subplans/

# 5. Create EXECUTION_TASK
python LLM/scripts/generation/generate_prompt.py @SAMPLE-FEATURE --achievement 1.1 --continue

# 6. Execute work following EXECUTION_TASK instructions

# 7. Request review (create APPROVED or FIX feedback file)
```

### 4. Try Parallel Execution (30 min)

```bash
# 1. Create parallel.json for your plan
cat work-space/plans/PARALLEL-EXECUTION-AUTOMATION/parallel.json

# 2. Define achievements with dependencies
{
  "plan": "SAMPLE-FEATURE",
  "achievements": [
    {"id": "2.1", "dependencies": []},
    {"id": "2.2", "dependencies": []},
    {"id": "2.3", "dependencies": ["2.1", "2.2"]}
  ]
}

# 3. Dashboard shows parallel opportunities automatically
python LLM/main.py --plan SAMPLE-FEATURE

# 4. Execute parallel group
# Select action 2 (Execute Parallel Group)
```

---

## 📚 Documentation

### For New Users

1. **[LLM-METHODOLOGY.md](LLM-METHODOLOGY.md)** - Start here (complete reference)
2. **[LLM/README.md](LLM/README.md)** - LLM folder structure and contents
3. **[LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md](LLM/guides/SUBPLAN-WORKFLOW-GUIDE.md)** - Core workflow (4 phases)
4. **[LLM/QUICK-START.md](LLM/QUICK-START.md)** - Fast-track introduction

### For Developers

- **Core Libraries**: See `LLM/core/libraries/*/README.md` in each module
- **Dashboard**: See `LLM/dashboard/README.md` (architecture, components)
- **Scripts**: See `LLM/scripts/README.md` (automation tools)
- **Tests**: See `LLM/tests/` (232+ tests with examples)

### For Advanced Users

- **[LLM/guides/GRAMMAPLAN-GUIDE.md](LLM/guides/GRAMMAPLAN-GUIDE.md)** - Multi-plan coordination
- **[LLM/guides/NORTH-STAR-GUIDE.md](LLM/guides/NORTH-STAR-GUIDE.md)** - Strategic vision documents
- **[LLM/guides/EXECUTION-ANALYSIS-GUIDE.md](LLM/guides/EXECUTION-ANALYSIS-GUIDE.md)** - Strategic analysis
- **[work-space/analyses/](work-space/analyses/)** - 125+ real-world analyses

---

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
python -m pytest LLM/tests/ -v

# Run dashboard tests (232+ tests)
python -m pytest LLM/tests/dashboard/ -v

# Run script tests
python -m pytest LLM/tests/scripts/ -v

# Run specific test file
python -m pytest LLM/tests/dashboard/test_plan_dashboard.py -v

# Check coverage
python -m pytest LLM/tests/ --cov=LLM --cov-report=html
```

**Test Statistics**:
- **Total Tests**: 280+ tests
- **Dashboard Tests**: 232+ tests (100% pass rate)
- **Script Tests**: 48+ tests
- **Coverage**: >90% for core libraries

---

## 🛠️ Common Workflows

### Starting New Work

```bash
# 1. Check active work
cat work-space/plans/*/PLAN_*.md

# 2. Create new PLAN
cp LLM/templates/PLAN-TEMPLATE.md work-space/plans/PLAN_MY-FEATURE.md

# 3. Follow start protocol
cat LLM/protocols/IMPLEMENTATION_START_POINT.md
```

### Continuing Existing Work

```bash
# 1. Launch dashboard to see status
python LLM/main.py

# 2. Navigate to plan, see next achievements

# 3. Generate prompts for next achievement
python LLM/scripts/generation/generate_prompt.py @MY-PLAN --achievement 2.1 --interactive
```

### Reviewing Achievement

```bash
# 1. Follow review instructions in EXECUTION_TASK

# 2. Create feedback file
# If approved: work-space/plans/MY-PLAN/execution/feedbacks/APPROVED_21.md
# If fixes needed: work-space/plans/MY-PLAN/execution/feedbacks/FIX_21.md

# 3. Dashboard automatically updates status
```

### Archiving Completed Work

```bash
# Manual archive (on-demand)
python LLM/scripts/archiving/manual_archive.py --plan MY-PLAN

# Or follow end protocol
cat LLM/protocols/IMPLEMENTATION_END_POINT.md
```

---

## 📊 Statistics & Metrics

### Active Work

- **North Stars**: 4 strategic visions
- **GrammaPlans**: 6 coordination plans
- **Active Plans**: 17+ feature/project plans
- **Active SUBPLANs**: 30+ achievement designs
- **Active EXECUTION_TASKs**: 31+ work units
- **Archived Work**: 100+ completed documents

### Code Metrics

- **Core Libraries**: 13 production-ready modules
- **Dashboard Components**: 17 UI/logic modules
- **Scripts**: 50+ automation tools
- **Tests**: 280+ comprehensive tests
- **Documentation**: 100+ guides, templates, protocols

### Dashboard Features

- **Real-Time Updates**: Auto-refresh after actions
- **Parallel Detection**: Automatic dependency analysis
- **Health Scores**: 5 component metrics (0-100)
- **Multi-Instance Detection**: Safe concurrent access
- **Theme Support**: 3 color schemes (default, dark, light)

---

## 🔧 Configuration

### Dashboard Settings

Edit `LLM/dashboard/config.yaml`:

```yaml
theme: default              # default, dark, light
refresh_interval: 1         # seconds (1-60)
show_stats: true           # show quick stats section
show_parallel: true        # show parallel opportunities
auto_copy_commands: false  # auto-copy commands to clipboard
```

Or use interactive settings menu:
```bash
python LLM/main.py
# Press 's' for settings
```

### Logging

Configure in your scripts:

```python
from LLM.core.libraries.logging import setup_logging, get_logger

# Setup logging
setup_logging(
    log_level="INFO",
    log_file="my_app.log",
    format="json"  # or "colored", "compact"
)

# Get logger
logger = get_logger(__name__)
logger.info("Application started", extra={"version": "1.0"})
```

### Metrics

```python
from LLM.core.libraries.metrics import Counter, Histogram, MetricRegistry

# Define metrics
requests_total = Counter(
    "requests_total",
    "Total requests",
    labels=["method", "status"]
)

# Register
registry = MetricRegistry.get_instance()
registry.register(requests_total)

# Use
requests_total.inc(labels={"method": "GET", "status": "200"})

# Export (Prometheus format)
from LLM.core.libraries.metrics import export_prometheus_text
print(export_prometheus_text())
```

---

## 🤝 Contributing

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# Run tests
python -m pytest LLM/tests/ -v

# Check linting
# (project uses consistent style, no explicit linter config)
```

### Adding New Libraries

1. Create module in `LLM/core/libraries/YOUR_LIBRARY/`
2. Add `__init__.py` with public API
3. Write comprehensive tests (>90% coverage)
4. Document with examples
5. Update `LLM/core/libraries/README.md`

### Adding Dashboard Features

1. Review `LLM/dashboard/README.md` for architecture
2. Add feature to appropriate module
3. Write tests in `LLM/tests/dashboard/`
4. Update `LLM/dashboard/metrics.py` for tracking
5. Document in `LLM/docs/`

---

## 📞 Support & Resources

### Need Help?

- **Methodology Questions**: See [LLM-METHODOLOGY.md](LLM-METHODOLOGY.md)
- **Dashboard Help**: Press `h` in dashboard or see [LLM/dashboard/README.md](LLM/dashboard/README.md)
- **Script Usage**: See [LLM/scripts/README.md](LLM/scripts/README.md)
- **Templates**: See [LLM/templates/PROMPTS.md](LLM/templates/PROMPTS.md)

### Troubleshooting

**Dashboard doesn't start**:
```bash
# Check dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+

# Check error logs
python LLM/main.py 2>&1 | tee debug.log
```

**Tests failing**:
```bash
# Run specific test for details
python -m pytest LLM/tests/path/to/test.py -v -s

# Check imports
python -c "from LLM.dashboard import plan_dashboard"
```

**State not updating**:
```bash
# Manual refresh in dashboard
# Press 'r' to refresh state

# Or clear lock file
rm LLM/dashboard/.dashboard.lock
```

---

## 📝 License

[Specify your license here]

---

## 🙏 Acknowledgments

Built with:
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal UI
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [PyMongo](https://pymongo.readthedocs.io/) - MongoDB driver
- [OpenAI Python](https://github.com/openai/openai-python) - LLM integration

---

## 📈 Version History

### v2.0 (November 2025) - Current
- ✅ 5-tier hierarchy (added NORTH_STAR, GRAMMAPLAN)
- ✅ Interactive dashboard with real-time updates
- ✅ Parallel execution support
- ✅ Production-ready core libraries
- ✅ Comprehensive testing (280+ tests)

### v1.0 (Earlier)
- 4-tier hierarchy (PLAN → SUBPLAN → EXECUTION)
- Command-line tools
- Basic libraries

---

**Last Updated**: November 15, 2025  
**Version**: 2.0  
**Status**: 🚀 Production Ready

For detailed version changes, see [LLM/METHODOLOGY-EVOLUTION-v2.0.md](LLM/METHODOLOGY-EVOLUTION-v2.0.md)

