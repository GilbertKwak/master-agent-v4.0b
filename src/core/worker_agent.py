"""
Worker Agent Base Class - Specialized executors
Performs actual research and analysis tasks.
"""

from typing import Dict, List
import anthropic


class WorkerAgent:
    """
    Base class for all specialized Workers.
    Each Worker has a specific skill (market research, tech analysis, etc.)
    """
    
    def __init__(self, api_key: str, worker_type: str, model: str = "claude-opus-4-20250514"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.temperature = 0.3  # Higher creativity for Workers
        self.worker_type = worker_type
        
    def execute_task(self, task: Dict, project_memory: str) -> Dict:
        """Execute assigned task with L1 Self-Check."""
        # Load Worker-specific prompt
        worker_prompt = self._load_prompt()
        
        # Perform task
        result = self._call_claude(
            system_prompt=worker_prompt,
            user_message=f"Task: {task}\n\nProject Context: {project_memory}"
        )
        
        # L1 Self-Check
        validated_result = self._self_check(result)
        
        return {
            "worker_type": self.worker_type,
            "result": validated_result,
            "citations": self._extract_citations(validated_result)
        }
    
    def _self_check(self, result: str) -> str:
        """L1: Validate own output before submission."""
        from ..quality.l1_self_check import SelfChecker
        
        checker = SelfChecker()
        return checker.check(result, self.worker_type)
    
    def _extract_citations(self, text: str) -> List[str]:
        """Extract [cite:X] citations from output."""
        import re
        return re.findall(r'\[cite:\d+\]', text)
    
    def _call_claude(self, system_prompt: str, user_message: str) -> str:
        """Call Claude API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8192,
            temperature=self.temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        return response.content[0].text
    
    def _load_prompt(self) -> str:
        """Load Worker-specific prompt from file."""
        with open(f"prompts/worker_prompts/{self.worker_type}.md", "r") as f:
            return f.read()