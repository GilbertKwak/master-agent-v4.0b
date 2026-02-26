"""
L3 Quality Validation: IAM-SDAI Framework
Final 6-dimensional quality assessment.
"""

from typing import Dict
import re


class IAMSDAI:
    """
    L3 validation: 6-dimensional quality framework
    - Impact: Practical value
    - Accuracy: Factual correctness
    - Comprehensiveness: Topic coverage
    - Diversity: Perspective variety
    - Depth: Analysis thoroughness
    - Integration: Synthesis quality
    """
    
    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
    
    def validate(self, final_report: str) -> Dict[str, float]:
        """Calculate all 6 IAM-SDAI scores."""
        scores = {
            "impact": self._score_impact(final_report),
            "accuracy": self._score_accuracy(final_report),
            "coverage": self._score_coverage(final_report),
            "diversity": self._score_diversity(final_report),
            "depth": self._score_depth(final_report),
            "integration": self._score_integration(final_report)
        }
        
        # Calculate overall score
        scores["overall"] = sum(scores.values()) / 6
        scores["passed"] = scores["overall"] >= self.threshold
        
        return scores
    
    def _score_impact(self, text: str) -> float:
        """Measure practical business value."""
        # Count actionable recommendations
        actions = len(re.findall(r'(should|must|recommend|suggest)', text, re.IGNORECASE))
        
        # Count concrete examples
        examples = len(re.findall(r'(for example|such as|specifically)', text, re.IGNORECASE))
        
        score = min(1.0, (actions * 0.05 + examples * 0.1))
        return round(score, 2)
    
    def _score_accuracy(self, text: str) -> float:
        """Measure factual correctness via citations."""
        citations = len(re.findall(r'\[cite:\d+\]', text))
        
        # More citations = higher confidence in accuracy
        score = min(1.0, citations * 0.02)
        return round(score, 2)
    
    def _score_coverage(self, text: str) -> float:
        """Measure comprehensiveness of analysis."""
        word_count = len(text.split())
        
        # Longer reports = more comprehensive
        score = min(1.0, word_count / 5000)
        return round(score, 2)
    
    def _score_diversity(self, text: str) -> float:
        """Measure variety of perspectives."""
        # Count different viewpoints mentioned
        viewpoints = len(re.findall(r'(however|alternatively|on the other hand|conversely)', text, re.IGNORECASE))
        
        score = min(1.0, viewpoints * 0.15)
        return round(score, 2)
    
    def _score_depth(self, text: str) -> float:
        """Measure analytical depth."""
        # Count analytical phrases
        analysis = len(re.findall(r'(because|therefore|consequently|thus|implies)', text, re.IGNORECASE))
        
        score = min(1.0, analysis * 0.05)
        return round(score, 2)
    
    def _score_integration(self, text: str) -> float:
        """Measure synthesis quality."""
        # Check for cross-references
        references = len(re.findall(r'(as mentioned|as discussed|referring to)', text, re.IGNORECASE))
        
        score = min(1.0, references * 0.1)
        return round(score, 2)