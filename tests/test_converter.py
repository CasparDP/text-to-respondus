"""
Tests for text-to-respondus converter.
"""

import pytest
import tempfile
import os
from pathlib import Path

from text_to_respondus import QuizConverter, QuizParser


@pytest.fixture
def sample_quiz_content():
    """Sample quiz content for testing."""
    return '''
Title: Test Question 1
Points: 1
1. What is the capital of France?
... Paris is the capital and most populous city of France.
a) London
*b) Paris
c) Berlin
d) Madrid

Title: Test Question 2
Points: 2
2. Which of the following are programming languages?
... Programming languages are used to write computer programs.
*a) Python
*b) Java
c) HTML
d) CSS
'''


@pytest.fixture
def temp_files():
    """Create temporary files for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test_quiz.txt")
        output_file = os.path.join(tmpdir, "test_output.csv")
        yield input_file, output_file


class TestQuizParser:
    """Test the QuizParser class."""
    
    def test_parse_content(self, sample_quiz_content):
        """Test parsing of quiz content."""
        parser = QuizParser()
        questions = parser.parse_content(sample_quiz_content)
        
        assert len(questions) == 2
        
        # Test first question
        q1 = questions[0]
        assert q1['title'] == 'Test Question 1'
        assert q1['points'] == 1.0
        assert 'capital of France' in q1['question_text']
        assert q1['correct_answer'] == 'B'
        assert len(q1['options']) == 4
        assert 'Paris' in q1['options']
        
        # Test second question
        q2 = questions[1]
        assert q2['title'] == 'Test Question 2'
        assert q2['points'] == 2.0
        assert q2['correct_answer'] == 'A'  # First correct option


class TestQuizConverter:
    """Test the QuizConverter class."""
    
    def test_convert_file(self, sample_quiz_content, temp_files):
        """Test file conversion."""
        input_file, output_file = temp_files
        
        # Write sample content to input file
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(sample_quiz_content)
        
        # Convert file
        converter = QuizConverter()
        success = converter.convert_file(input_file, output_file, topic="test_topic")
        
        assert success
        assert os.path.exists(output_file)
        
        # Check output content
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'Question Type' in content
            assert 'test_topic' in content
            assert 'capital of France' in content
    
    def test_validation(self, sample_quiz_content, temp_files):
        """Test input file validation."""
        input_file, _ = temp_files
        
        # Write sample content
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(sample_quiz_content)
        
        converter = QuizConverter()
        assert converter.validate_input_file(input_file)
        
        # Test invalid file
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("Invalid content")
        
        assert not converter.validate_input_file(input_file)
    
    def test_statistics(self, sample_quiz_content, temp_files):
        """Test conversion statistics."""
        input_file, _ = temp_files
        
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(sample_quiz_content)
        
        converter = QuizConverter()
        stats = converter.get_conversion_stats(input_file)
        
        assert "error" not in stats
        assert stats["total_questions"] == 2
        assert stats["min_options"] == 4
        assert stats["max_options"] == 4
        assert stats["questions_with_explanations"] == 2


if __name__ == "__main__":
    pytest.main([__file__])
