# Master Agent V4.0-B Integration Guide

## Quick Start (10 minutes)

### 1. Prerequisites
```bash
# Python 3.10+
python --version

# Clone repository
git clone https://github.com/GilbertKwak/master-agent-v4.0b.git
cd master-agent-v4.0b
```

### 2. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 4. Run First Project
```bash
python src/main.py
```

---

## Architecture Overview

```
Master Agent (Leader)
├── Phase 1: Information Gathering
│   ├── Market Research Worker ⚡
│   ├── Tech Analysis Worker ⚡
│   ├── Competition Worker ⚡
│   └── Patent Analysis Worker ⚡
├── Phase 2: Strategic Analysis
│   ├── Risk Analysis Worker ⚡
│   ├── Future Prediction Worker ⚡
│   └── New Business Worker ⚡
└── Phase 3: Report Synthesis
    └── Report Writer Worker ⚡

PROJECT_MEMORY.md (Persistent Storage)
```

---

## Key Patterns

### Pattern 1: Leader Memory Preservation
Master Agent NEVER performs actual work - only delegates to Workers.

```python
# ✅ Correct: Master delegates
master.execute_phase_with_lifecycle(phase_num=1, plan=plan)

# ❌ Wrong: Master does work directly
master.do_market_research()  # Don't do this!
```

### Pattern 2: External Memory (PROJECT_MEMORY.md)
All decisions stored externally to bypass context limits.

```python
# Write to external memory
project_memory.write_section("phase1_plan", plan_content)

# Read from external memory
previous_plan = project_memory.read_section("phase1_plan")
```

### Pattern 3: Ephemeral Workers
Workers are created fresh for each phase and destroyed after use.

```python
# ✅ Automatic lifecycle management
lifecycle_mgr.execute_phase(phase_num=1, plan=plan)
# Workers are summoned, execute, then retired automatically
```

### Pattern 5: 3-Tier Quality Validation
Sequential validation for maximum reliability.

```
L1: Worker Self-Check (citations, ranges, sources)
      ↓
L2: Cross-Validation (contradictions between Workers)
      ↓
L3: IAM-SDAI (6-dimensional final validation)
```

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_basic.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

---

## Troubleshooting

### Issue: "Context window exceeded"
**Solution**: PROJECT_MEMORY is too verbose. Reduce summary length in `config.yaml`:
```yaml
memory:
  summary_max_chars: 500  # Reduce from 1000
```

### Issue: "Worker execution timeout"
**Solution**: Increase timeout in `config.yaml`:
```yaml
performance:
  timeouts:
    worker_execution: 120  # Increase from 60
```

### Issue: "Low IAM-SDAI score"
**Solution**: Check individual dimension scores to identify weakness:
```python
scores = l3_validator.validate(final_report)
print(scores)  # See which dimension is low
```

---

## Migration from V3.1

1. **Backup existing system**
2. **Install V4.0-B** (see Quick Start)
3. **Migrate PROJECT_MEMORY format** (automatic converter included)
4. **Update Worker prompts** (use new template)
5. **Test with sample project**
6. **Deploy to production**

Full migration guide: `/docs/Migration_V31_to_V40B.md`

---

## Performance Benchmarks

| Metric | V3.1 | V4.0-B | Improvement |
|--------|------|--------|-------------|
| Response Time | 70s | 47s | -33% ⚡ |
| IAM-SDAI Score | 0.74 | 0.87 | +18% 📈 |
| API Cost | 100% | 60% | -40% 💰 |
| Bug Rate | 5% | 0.5% | -90% 🐛 |

---

## Support & Community

- **Issues**: [GitHub Issues](https://github.com/GilbertKwak/master-agent-v4.0b/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GilbertKwak/master-agent-v4.0b/discussions)
- **Documentation**: [Full Docs](https://github.com/GilbertKwak/master-agent-v4.0b/tree/main/docs)

---

**Ready to deploy?** See `/docs/Production_Deployment.md` for Docker setup and monitoring.