"""
L2 Quality Validation: Cross-Validation
Master Agent checks for contradictions between Workers.
"""

from typing import List, Dict
import re


class CrossValidator:
    """
    L2 validation performed by Master Agent.
    Detects contradictions between Worker outputs.
    """
    
    def validate(self, worker_results: List[Dict]) -> Dict:
        """Cross-validate multiple Worker outputs."""
        contradictions = []
        
        # Check for numerical contradictions
        num_contradictions = self._check_numerical_contradictions(worker_results)
        if num_contradictions:
            contradictions.extend(num_contradictions)
        
        # Check for claim contradictions
        claim_contradictions = self._check_claim_contradictions(worker_results)
        if claim_contradictions:
            contradictions.extend(claim_contradictions)
        
        # Aggregate validated results
        aggregated = {
            "workers": [r["worker_type"] for r in worker_results],
            "results": [r["result"] for r in worker_results],
            "contradictions": contradictions,
            "validation_passed": len(contradictions) == 0
        }
        
        return aggregated
    
    def _check_numerical_contradictions(self, results: List[Dict]) -> List[str]:
        """Find conflicting numbers across Workers."""
        contradictions = []
        
        # Extract all numbers with context
        all_numbers = []
        for result in results:
            text = result["result"]
            numbers = re.findall(r'(\d+\.?\d*)\s*([%MKBT$]?)', text)
            all_numbers.append({
                "worker": result["worker_type"],
                "numbers": numbers
            })
        
        # Compare overlapping metrics
        # (Simplified - production would have sophisticated logic)
        if len(all_numbers) > 1:
            for i, a in enumerate(all_numbers):
                for b in all_numbers[i+1:]:
                    # Check if same metric has vastly different values
                    pass  # Placeholder for complex logic
        
        return contradictions
    
    def _check_claim_contradictions(self, results: List[Dict]) -> List[str]:
        """Find contradictory claims across Workers."""
        contradictions = []
        
        # Extract key claims (simplified)
        claims = []
        for result in results:
            text = result["result"]
            # Look for definitive statements
            sentences = text.split('. ')
            for sent in sentences:
                if any(word in sent.lower() for word in ['will', 'is', 'are', 'will be']):
                    claims.append({
                        "worker": result["worker_type"],
                        "claim": sent
                    })
        
        # Check for negation contradictions
        # (Simplified - production would use NLP)
        
        return contradictions