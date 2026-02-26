"""
Master Agent System V4.0-B
Advanced AI Research System with Leader-Worker Architecture
"""

__version__ = "4.0-B"
__author__ = "GilbertKwak"
__license__ = "MIT"

from .core.master_agent import MasterAgent
from .core.worker_agent import WorkerAgent
from .memory.project_memory import ProjectMemory
from .lifecycle.agent_lifecycle import AgentLifecycleManager
from .quality.l1_self_check import SelfChecker
from .quality.l2_cross_validation import CrossValidator
from .quality.l3_iam_sdai import IAMSDAI

__all__ = [
    'MasterAgent',
    'WorkerAgent',
    'ProjectMemory',
    'AgentLifecycleManager',
    'SelfChecker',
    'CrossValidator',
    'IAMSDAI'
]