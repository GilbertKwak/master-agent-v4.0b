"""
L1 Quality Validation: Worker Self-Check
Workers validate their own outputs before submission.
"""

from typing import Dict
import re


class SelfChecker:
    """
    L1 validation performed by each Worker on their own output.
    Checks: Citations, numerical accuracy, range validity.
    """
    
    def check(self, output: str, worker_type: str) -> str:
        """Run L1 checks and return validated output."""
        issues = []
        
        # Check 1: Minimum citations
        citations = self._count_citations(output)
        if citations < 2:
            issues.append(f"Insufficient citations: {citations} (min: 2)")
        
        # Check 2: Numerical ranges
        if not self._validate_ranges(output):
            issues.append("Invalid numerical ranges detected")
        
        # Check 3: Source consistency
        if not self._validate_sources(output):
            issues.append("Inconsistent sources")
        
        if issues:
            # Append validation warnings
            output += "\n\n**L1 Validation Warnings:**\n"
            for issue in issues:
                output += f"- {issue}\n"
        
        return output
    
    def _count_citations(self, text: str) -> int:
        """Count [cite:X] citations."""
        return len(re.findall(r'\[cite:\d+\]', text))
    
    def _validate_ranges(self, text: str) -> bool:
        """Check if numerical ranges are logically valid."""
        # Find patterns like "10-20%" or "$5M-$10M"
        ranges = re.findall(r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)', text)
        
        for start, end in ranges:
            if float(start) > float(end):
                return False
        
        return True
    
    def _validate_sources(self, text: str) -> bool:
        """Check if sources are mentioned consistently."""
        # Look for source mentions
        sources = re.findall(r'(according to|based on|per|from)\s+([A-Z][\w\s]+)', text)
        
        # At least some sources should be mentioned
        return len(sources) >= 1