"""
Agent Lifecycle Manager (Pattern 3: Ephemeral Workers)
Manages Worker summoning, execution, and retirement.
"""

from typing import Dict, List
from ..core.worker_agent import WorkerAgent
from ..memory.project_memory import ProjectMemory


class AgentLifecycleManager:
    """
    Manages the complete lifecycle of Ephemeral Workers:
    1. Summon: Create fresh Workers for each Phase
    2. Execute: Run tasks with clean context
    3. Retire: Destroy Workers immediately after task completion
    """
    
    def __init__(self, project_memory: ProjectMemory):
        self.project_memory = project_memory
        self.active_workers = {}
        
    def execute_phase(self, phase_num: int, plan: Dict) -> List[Dict]:
        """Execute a complete phase with fresh Workers."""
        # Determine required Workers for this phase
        worker_types = self._get_phase_workers(phase_num)
        
        # Summon Workers
        workers = self._summon_workers(worker_types)
        
        # Execute tasks in parallel
        results = []
        for worker_type, worker in workers.items():
            task = plan.get(worker_type)
            if task:
                result = worker.execute_task(
                    task=task,
                    project_memory=self.project_memory.get_summary()
                )
                results.append(result)
        
        # Retire Workers immediately
        self._retire_workers(workers)
        
        return results
    
    def _get_phase_workers(self, phase_num: int) -> List[str]:
        """Define which Workers are needed for each phase."""
        phase_workers = {
            1: ["market_research", "tech_analysis", "competition", "patent_analysis"],
            2: ["risk_analysis", "future_prediction", "new_business"],
            3: ["report_writer"]
        }
        return phase_workers.get(phase_num, [])
    
    def _summon_workers(self, worker_types: List[str]) -> Dict[str, WorkerAgent]:
        """Create fresh Worker instances."""
        import os
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        workers = {}
        for worker_type in worker_types:
            workers[worker_type] = WorkerAgent(
                api_key=api_key,
                worker_type=worker_type
            )
            print(f"⚡ Summoned Worker: {worker_type}")
        
        return workers
    
    def _retire_workers(self, workers: Dict[str, WorkerAgent]):
        """Destroy Workers to free memory."""
        for worker_type in workers.keys():
            del workers[worker_type]
            print(f"💀 Retired Worker: {worker_type}")
        
        # Force garbage collection
        import gc
        gc.collect()