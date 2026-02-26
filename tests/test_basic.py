"""
Basic unit tests for Master Agent V4.0-B
"""

import pytest
from src.core.master_agent import MasterAgent
from src.memory.project_memory import ProjectMemory
from src.quality.l1_self_check import SelfChecker


def test_project_memory_creation():
    """Test PROJECT_MEMORY.md creation."""
    memory = ProjectMemory("test_project_001")
    assert memory.file_path.exists()
    memory.file_path.unlink()  # Cleanup


def test_project_memory_write_read():
    """Test writing and reading sections."""
    memory = ProjectMemory("test_project_002")
    
    memory.write_section("test_section", "Test content")
    content = memory.read_section("test_section")
    
    assert content == "Test content"
    memory.file_path.unlink()  # Cleanup


def test_l1_self_check_citations():
    """Test L1 citation validation."""
    checker = SelfChecker()
    
    # Text with sufficient citations
    good_text = "Market size is $10B [cite:1]. Growth rate is 15% [cite:2]."
    result = checker.check(good_text, "market_research")
    assert "L1 Validation Warnings" not in result
    
    # Text with insufficient citations
    bad_text = "Market size is $10B."
    result = checker.check(bad_text, "market_research")
    assert "Insufficient citations" in result


def test_l1_self_check_ranges():
    """Test L1 numerical range validation."""
    checker = SelfChecker()
    
    # Valid range
    good_text = "Growth rate: 10-20% [cite:1] [cite:2]"
    result = checker._validate_ranges(good_text)
    assert result is True
    
    # Invalid range
    bad_text = "Growth rate: 20-10%"
    result = checker._validate_ranges(bad_text)
    assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])