"""
PROJECT_MEMORY.md Manager (Pattern 2: External Memory)
Persistent storage that bypasses context window limits.
"""

from pathlib import Path
from typing import Optional
from datetime import datetime


class ProjectMemory:
    """
    Manages PROJECT_MEMORY.md - the external memory for persistent project state.
    All decisions, results, and metadata stored here.
    """
    
    def __init__(self, project_id: str, base_dir: str = "./data/project_memories"):
        self.project_id = project_id
        self.file_path = Path(base_dir) / f"PROJECT_MEMORY_{project_id}.md"
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.file_path.exists():
            self._initialize_file()
    
    def _initialize_file(self):
        """Create new PROJECT_MEMORY.md with template."""
        template = f"""# PROJECT_MEMORY: {self.project_id}

**Created**: {datetime.now().isoformat()}
**Version**: V4.0-B

---

## User Query
[To be filled]

## Phase 1: Information Gathering
### Plan
[To be filled]

### Results
[To be filled]

## Phase 2: Strategic Analysis
### Plan
[To be filled]

### Results
[To be filled]

## Phase 3: Report Synthesis
### Plan
[To be filled]

### Results
[To be filled]

## Quality Metrics
### IAM-SDAI Scores
[To be filled]

---
**Last Updated**: {datetime.now().isoformat()}
"""
        self.file_path.write_text(template, encoding='utf-8')
    
    def write_section(self, section_name: str, content: str):
        """Write or update a specific section."""
        current = self.file_path.read_text(encoding='utf-8')
        
        # Replace section content
        section_marker = f"## {section_name}"
        if section_marker in current:
            # Update existing section
            lines = current.split('\n')
            new_lines = []
            in_section = False
            
            for line in lines:
                if line.startswith(section_marker):
                    in_section = True
                    new_lines.append(line)
                    new_lines.append(content)
                elif in_section and line.startswith('##'):
                    in_section = False
                    new_lines.append(line)
                elif not in_section:
                    new_lines.append(line)
            
            current = '\n'.join(new_lines)
        else:
            # Append new section
            current += f"\n\n## {section_name}\n{content}\n"
        
        # Update timestamp
        current = current.replace(
            "**Last Updated**:",
            f"**Last Updated**: {datetime.now().isoformat()}"
        )
        
        self.file_path.write_text(current, encoding='utf-8')
    
    def read_section(self, section_name: str) -> Optional[str]:
        """Read specific section."""
        content = self.file_path.read_text(encoding='utf-8')
        section_marker = f"## {section_name}"
        
        if section_marker not in content:
            return None
        
        lines = content.split('\n')
        section_lines = []
        in_section = False
        
        for line in lines:
            if line.startswith(section_marker):
                in_section = True
                continue
            elif in_section and line.startswith('##'):
                break
            elif in_section:
                section_lines.append(line)
        
        return '\n'.join(section_lines).strip()
    
    def read_all(self) -> str:
        """Read entire PROJECT_MEMORY.md."""
        return self.file_path.read_text(encoding='utf-8')
    
    def get_summary(self) -> str:
        """Get condensed summary for Master Agent context."""
        sections = ["user_query", "phase1_plan", "phase2_plan", "phase3_plan"]
        summary = []
        
        for section in sections:
            content = self.read_section(section)
            if content:
                summary.append(f"**{section}**: {content[:200]}...")
        
        return '\n'.join(summary)