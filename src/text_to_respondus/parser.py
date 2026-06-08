"""
Quiz text parser for converting Canvas-style quiz files to structured data.
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class QuizParser:
    """Parser for Canvas-style quiz text files."""
    
    def __init__(self) -> None:
        self.questions: List[Dict[str, Any]] = []
    
    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse a quiz file and return structured question data."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return self.parse_content(content)
        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {e}")
            raise
    
    def parse_content(self, content: str) -> List[Dict[str, Any]]:
        """Parse quiz content string and return structured question data."""
        self.questions = []
        
        # Split content into question blocks
        question_blocks = self._split_into_questions(content)
        
        for i, block in enumerate(question_blocks, 1):
            try:
                question = self._parse_question_block(block, i)
                if question:
                    self.questions.append(question)
            except Exception as e:
                logger.warning(f"Error parsing question {i}: {e}")
                continue
        
        logger.info(f"Successfully parsed {len(self.questions)} questions")
        return self.questions
    
    def _split_into_questions(self, content: str) -> List[str]:
        """Split content into individual question blocks."""
        # Remove quiz header information
        lines = content.strip().split('\n')
        
        # Find where questions start (after description)
        start_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('Title:'):
                start_idx = i
                break
        
        # Split by "Title:" to get question blocks
        content_from_questions = '\n'.join(lines[start_idx:])
        blocks = re.split(r'\n(?=Title:)', content_from_questions)
        
        # Filter out empty blocks
        return [block.strip() for block in blocks if block.strip()]
    
    def _parse_question_block(self, block: str, question_number: int) -> Optional[Dict[str, Any]]:
        """Parse a single question block."""
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        
        if len(lines) < 4:  # Minimum: Title, Points, Question, Options
            logger.warning(f"Question {question_number}: Insufficient lines")
            return None
        
        # Parse title
        title_line = lines[0]
        if not title_line.startswith('Title:'):
            logger.warning(f"Question {question_number}: Missing title")
            return None
        title = title_line.replace('Title:', '').strip()
        
        # Parse points
        points_line = lines[1]
        if not points_line.startswith('Points:'):
            logger.warning(f"Question {question_number}: Missing points")
            return None
        try:
            points = float(points_line.replace('Points:', '').strip())
        except ValueError:
            points = 1.0
        
        # Find question text (starts with number)
        question_text = ""
        explanation = ""
        options_start_idx = -1
        
        for i, line in enumerate(lines[2:], 2):
            # Check if this is the question line (starts with number)
            if re.match(r'^\d+\.', line):
                question_text = re.sub(r'^\d+\.\s*', '', line)
                
                # Find explanation (starts with ...)
                for j, next_line in enumerate(lines[i+1:], i+1):
                    if next_line.startswith('...'):
                        explanation = next_line[3:].strip()
                        options_start_idx = j + 1
                        break
                    elif re.match(r'^[*]?[a-j]\)', next_line):
                        # Options start immediately, no explanation
                        options_start_idx = j
                        break
                break
        
        if not question_text:
            logger.warning(f"Question {question_number}: No question text found")
            return None
        
        if options_start_idx == -1:
            logger.warning(f"Question {question_number}: No options found")
            return None
        
        # Parse options
        options, correct_answer = self._parse_options(lines[options_start_idx:])
        
        if not options:
            logger.warning(f"Question {question_number}: No valid options found")
            return None
        
        return {
            'title': title,
            'points': points,
            'question_text': question_text,
            'explanation': explanation,
            'options': options,
            'correct_answer': correct_answer,
            'question_number': question_number
        }
    
    def _parse_options(self, option_lines: List[str]) -> Tuple[List[str], str]:
        """Parse answer options and identify correct answer."""
        options = []
        correct_answer = ""
        option_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        
        for line in option_lines:
            # Match pattern: optional *, letter, ), text
            match = re.match(r'^(\*)?([a-j])\)\s*(.+)$', line)
            if match:
                is_correct, letter, text = match.groups()
                options.append(text.strip())
                
                if is_correct and not correct_answer:
                    # Record the first correct option (output is single-answer mc)
                    letter_upper = letter.upper()
                    if letter_upper in option_letters:
                        correct_answer = letter_upper
        
        return options, correct_answer
    
    def get_questions(self) -> List[Dict[str, Any]]:
        """Return parsed questions."""
        return self.questions
    
    def get_question_count(self) -> int:
        """Return number of parsed questions."""
        return len(self.questions)
