"""
Quiz converter for transforming parsed quiz data to Respondus CSV format.
"""

import pandas as pd
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from .parser import QuizParser

logger = logging.getLogger(__name__)


class QuizConverter:
    """Convert quiz data to Respondus CSV format."""
    
    # Respondus CSV column structure
    RESPONDUS_COLUMNS = [
        'Question Type', 'Question Title/Id', 'Points', 'Question Wording', 
        'Correct Answer', 'Choice 1', 'Choice 2', 'Choice 3', 'Choice 4', 
        'Choice 5', 'Choice 6', 'Choice 7', 'Choice 8', 'Choice 9', 'Choice 10',
        'General Feedback', 'Correct Feedback', 'Incorrect Feedback',
        'Feedback 1', 'Feedback 2', 'Feedback 3', 'Feedback 4', 'Feedback 5',
        'Feedback 6', 'Feedback 7', 'Feedback 8', 'Feedback 9', 'Feedback 10',
        'Topic', 'Difficulty Level', 'Meta 1', 'Meta 2', 'Meta 3', 'Meta 4'
    ]
    
    def __init__(self) -> None:
        self.parser = QuizParser()
    
    def convert_file(
        self, 
        input_file: str, 
        output_file: str, 
        topic: str = "",
        difficulty: str = ""
    ) -> bool:
        """Convert a quiz file to Respondus CSV format."""
        try:
            # Parse the input file
            questions = self.parser.parse_file(input_file)
            
            if not questions:
                logger.error("No questions found in input file")
                return False
            
            # Convert to Respondus format
            df = self._questions_to_dataframe(questions, topic, difficulty)
            
            # Save to CSV
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            logger.info(f"Successfully converted {len(questions)} questions to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error converting file: {e}")
            return False
    
    def convert_questions(
        self, 
        questions: List[Dict[str, Any]], 
        output_file: str,
        topic: str = "",
        difficulty: str = ""
    ) -> bool:
        """Convert question data to Respondus CSV format."""
        try:
            df = self._questions_to_dataframe(questions, topic, difficulty)
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            logger.info(f"Successfully converted {len(questions)} questions to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error converting questions: {e}")
            return False
    
    def _questions_to_dataframe(
        self, 
        questions: List[Dict[str, Any]], 
        topic: str,
        difficulty: str
    ) -> pd.DataFrame:
        """Convert question list to Respondus DataFrame."""
        rows = []
        
        for question in questions:
            row = self._question_to_row(question, topic, difficulty)
            rows.append(row)
        
        return pd.DataFrame(rows, columns=self.RESPONDUS_COLUMNS)
    
    def _question_to_row(
        self, 
        question: Dict[str, Any], 
        topic: str,
        difficulty: str
    ) -> Dict[str, Any]:
        """Convert a single question to a Respondus row."""
        # Initialize row with empty values
        row = {col: "" for col in self.RESPONDUS_COLUMNS}
        
        # Fill in the basic question data
        row['Question Type'] = 'mc'  # Multiple choice
        row['Question Title/Id'] = question.get('title', '')
        row['Points'] = question.get('points', 1.0)
        row['Question Wording'] = question.get('question_text', '')
        row['Correct Answer'] = question.get('correct_answer', '')
        row['General Feedback'] = question.get('explanation', '')
        row['Topic'] = topic
        row['Difficulty Level'] = difficulty
        
        # Fill in the answer choices
        options = question.get('options', [])
        choice_columns = [f'Choice {i}' for i in range(1, 11)]
        
        for i, option in enumerate(options[:10]):  # Limit to 10 choices
            if i < len(choice_columns):
                row[choice_columns[i]] = option
        
        return row
    
    def preview_conversion(
        self, 
        input_file: str, 
        topic: str = "", 
        num_questions: int = 3
    ) -> Optional[pd.DataFrame]:
        """Preview the first few questions in Respondus format."""
        try:
            questions = self.parser.parse_file(input_file)
            
            if not questions:
                logger.error("No questions found in input file")
                return None
            
            # Limit to requested number of questions
            preview_questions = questions[:num_questions]
            df = self._questions_to_dataframe(preview_questions, topic, "")
            
            return df
            
        except Exception as e:
            logger.error(f"Error creating preview: {e}")
            return None
    
    def validate_input_file(self, input_file: str) -> bool:
        """Validate that the input file can be parsed."""
        try:
            questions = self.parser.parse_file(input_file)
            return len(questions) > 0
        except Exception as e:
            logger.error(f"Input file validation failed: {e}")
            return False
    
    def get_conversion_stats(self, input_file: str) -> Dict[str, Any]:
        """Get statistics about the conversion."""
        try:
            questions = self.parser.parse_file(input_file)
            
            if not questions:
                return {"error": "No questions found"}
            
            # Collect stats
            total_questions = len(questions)
            option_counts = [len(q.get('options', [])) for q in questions]
            
            stats = {
                "total_questions": total_questions,
                "min_options": min(option_counts) if option_counts else 0,
                "max_options": max(option_counts) if option_counts else 0,
                "avg_options": sum(option_counts) / len(option_counts) if option_counts else 0,
                "questions_with_explanations": sum(1 for q in questions if q.get('explanation')),
                "unique_titles": len(set(q.get('title', '') for q in questions))
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting conversion stats: {e}")
            return {"error": str(e)}


def create_output_directory(output_path: str) -> None:
    """Create output directory if it doesn't exist."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
