# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-06-10

### Added
- Initial release of text-to-respondus converter
- Support for Canvas-style quiz text format parsing
- Conversion to standard Respondus CSV format
- Command line interface for easy file conversion
- Python API for programmatic use
- Support for multiple choice questions with 2-10 options
- Automatic detection of correct answers marked with *
- Preservation of question titles and detailed explanations
- Proper CSV escaping for long text fields
- Poetry-based package management and dependency handling

### Features
- **QuizConverter**: Main conversion engine with robust text parsing
- **Parser**: Dedicated quiz text format parser with error handling  
- **CLI**: User-friendly command line interface with click
- **Respondus Format**: Full compatibility with Respondus import requirements
- **Topic Support**: Configurable topic assignment for categorization
- **Clean Architecture**: Modular design for easy maintenance and extension

### Technical Details
- Python 3.8+ compatibility
- Pandas for efficient data manipulation
- Click for CLI functionality
- Comprehensive test suite with pytest
- Code formatting with Black
- Type checking with mypy
- Proper error handling and validation

### Examples
- Included a generic sample quiz (`data/example_quiz.txt`) demonstrating the input format
- Generated properly formatted Respondus CSV files
- Verified import compatibility with ANS systems
