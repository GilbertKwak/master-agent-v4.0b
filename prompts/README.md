# Worker Prompts Directory

This directory contains specialized prompts for each Worker type in the Master Agent System V4.0-B.

## Available Workers

### Phase 1: Information Gathering
1. **market_research.md** - Market size, trends, growth projections
2. **tech_analysis.md** - Technology assessment and feasibility
3. **competition.md** - Competitive landscape analysis
4. **patent_analysis.md** - IP landscape and patent research

### Phase 2: Strategic Analysis
5. **risk_analysis.md** - Risk identification and mitigation
6. **future_prediction.md** - Trend forecasting and scenarios
7. **new_business.md** - Business model and opportunity analysis

### Phase 3: Report Synthesis
8. **report_writer.md** - Executive report compilation

## Prompt Structure

Each Worker prompt follows this standard structure:

```markdown
# [Worker Name] - System Prompt

## Role
[Worker's specific role and purpose]

## Core Responsibilities
[List of key tasks]

## Quality Standards (L1 Self-Check)
[Validation criteria]

## Output Format
[Expected output structure]

## Context Awareness
[How to use PROJECT_MEMORY]

## Important Constraints
[Limitations and guidelines]
```

## Customization

To customize a Worker prompt:

1. Copy the template from an existing prompt
2. Modify the responsibilities and output format
3. Adjust quality standards as needed
4. Test with sample tasks
5. Deploy to production

## Best Practices

- ✅ Keep prompts focused on specific expertise
- ✅ Include clear L1 validation criteria
- ✅ Specify exact output format
- ✅ Reference PROJECT_MEMORY for context
- ❌ Avoid overlapping responsibilities between Workers
- ❌ Don't make prompts too general