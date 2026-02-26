"""
Main entry point for Master Agent System V4.0-B
"""

import os
from dotenv import load_dotenv
from src.core.master_agent import MasterAgent


def main():
    """Run a complete research project."""
    # Load environment variables
    load_dotenv()
    
    # Initialize Master Agent
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")
    
    master = MasterAgent(api_key=api_key)
    
    # Example query
    user_query = input("Enter research query: ")
    project_id = input("Enter project ID: ")
    
    print(f"\n🚀 Starting project: {project_id}")
    print(f"📝 Query: {user_query}\n")
    
    # Phase 1: Information Gathering
    print("⚡ Phase 1: Information Gathering...")
    phase1_result = master.start_project(user_query, project_id)
    
    # Phase 2: Strategic Analysis
    print("⚡ Phase 2: Strategic Analysis...")
    phase2_result = master.execute_phase_with_lifecycle(2, phase1_result)
    
    # Phase 3: Report Synthesis
    print("⚡ Phase 3: Report Synthesis...")
    phase3_result = master.execute_phase_with_lifecycle(3, phase2_result)
    
    # Finalize with L3 validation
    print("\n✅ Finalizing project with L3 IAM-SDAI validation...")
    final_report = master.complete_project()
    
    print("\n" + "="*80)
    print("📊 FINAL REPORT")
    print("="*80)
    print(final_report)
    print("="*80)


if __name__ == "__main__":
    main()