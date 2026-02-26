"""
Master Agent V4.0-B - Leader Component
Handles strategic planning and Worker coordination only.
"""

from typing import Dict, List, Optional
from datetime import datetime
import anthropic


class MasterAgent:
    """
    Master Agent (Leader) that delegates all work to specialized Workers.
    Never performs actual research - only strategizes and coordinates.
    """
    
    def __init__(self, api_key: str, model: str = "claude-opus-4-20250514"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.temperature = 0.1
        self.project_memory = None
        
    def start_project(self, user_query: str, project_id: str) -> Dict:
        """Initialize project and create Phase 1 plan."""
        from ..memory.project_memory import ProjectMemory
        
        # Initialize PROJECT_MEMORY.md
        self.project_memory = ProjectMemory(project_id)
        self.project_memory.write_section("user_query", user_query)
        self.project_memory.write_section("start_time", str(datetime.now()))
        
        # Create Phase 1 plan (delegation to Workers)
        system_prompt = self._get_master_prompt()
        phase_plan = self._call_claude(
            system_prompt=system_prompt,
            user_message=f"Create Phase 1 plan for: {user_query}"
        )
        
        self.project_memory.write_section("phase1_plan", phase_plan)
        return {"phase": 1, "plan": phase_plan}
    
    def execute_phase_with_lifecycle(self, phase_num: int, plan: Dict) -> Dict:
        """Execute a phase using Ephemeral Workers."""
        from ..lifecycle.agent_lifecycle import AgentLifecycleManager
        
        lifecycle_mgr = AgentLifecycleManager(self.project_memory)
        
        # Summon Workers for this phase
        worker_results = lifecycle_mgr.execute_phase(
            phase_num=phase_num,
            plan=plan
        )
        
        # Aggregate results and perform L2 Cross-Validation
        validated_results = self._cross_validate(worker_results)
        
        # Store in PROJECT_MEMORY
        self.project_memory.write_section(
            f"phase{phase_num}_results",
            validated_results
        )
        
        return validated_results
    
    def complete_project(self) -> str:
        """Finalize project and run L3 IAM-SDAI validation."""
        from ..quality.l3_iam_sdai import IAMSDAI
        
        # Get final report from PROJECT_MEMORY
        final_report = self.project_memory.read_section("phase3_results")
        
        # L3 Validation
        l3_validator = IAMSDAI()
        scores = l3_validator.validate(final_report)
        
        self.project_memory.write_section("iam_sdai_scores", str(scores))
        self.project_memory.write_section("end_time", str(datetime.now()))
        
        return final_report
    
    def _cross_validate(self, worker_results: List[Dict]) -> Dict:
        """L2: Cross-validate Worker outputs for contradictions."""
        from ..quality.l2_cross_validation import CrossValidator
        
        validator = CrossValidator()
        return validator.validate(worker_results)
    
    def _call_claude(self, system_prompt: str, user_message: str) -> str:
        """Call Claude API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=self.temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        return response.content[0].text
    
    def _get_master_prompt(self) -> str:
        """Load Master prompt from file."""
        with open("prompts/master_prompt_v4.0b.md", "r") as f:
            return f.read()