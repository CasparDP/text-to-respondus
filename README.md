# 📝 Text to Respondus Converter

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Poetry](https://img.shields.io/badge/dependency-poetry-blue.svg)](https://python-poetry.org/)

A Python tool to convert Canvas-style quiz text files into Respondus CSV format for easy import into learning management systems like ANS.

## ✨ Features

- **🔄 Easy Conversion**: Transform text-based quiz files to Respondus CSV format
- **🎯 Multiple Choice Support**: Handle questions with 2-10 answer options  
- **📝 Rich Feedback**: Preserve detailed explanations and feedback
- **🔍 Smart Parsing**: Automatic detection of correct answers marked with `*`
- **📊 Statistics**: Get insights about your quiz before conversion
- **🖥️ CLI Interface**: User-friendly command line interface
- **🐍 Python API**: Programmatic access for advanced users
- **✅ Validation**: Built-in validation and error checking

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Poetry (for dependency management)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/CasparDP/text-to-respondus.git
   cd text-to-respondus
   ```

2. **Install dependencies with Poetry:**
   ```bash
   poetry install
   ```

3. **Activate the virtual environment:**
   ```bash
   poetry shell
   ```

### Basic Usage

A generic sample file is included at `data/example_quiz.txt` so you can try the tool right away.

**Convert a quiz file:**
```bash
poetry run text-to-respondus convert data/example_quiz.txt output/example_respondus.csv --topic "Example"
```

**Convert every quiz file in a folder (batch):**
```bash
poetry run text-to-respondus batch data/ output/
```

## 📋 Input Format

The tool expects text files with questions in this format:

```
Title: Question Category Name
Points: 1
1. What is the question text?
... Detailed explanation of the answer goes here
a) First option
*b) Correct option (marked with *)
c) Third option
d) Fourth option
```

**Key points:**
- Questions start with `Title:` and `Points:`
- Question text begins with a number and period
- Explanations start with `...`
- Answer options use letters a), b), c), etc.
- Correct answers are marked with `*` before the letter

## 📤 Output Format

Generates CSV files compatible with Respondus import:
- Standard Respondus column structure with 34 columns
- Comma-separated values with proper escaping
- Support for up to 10 answer choices
- Metadata fields for topic, difficulty, etc.

## 🛠️ Development

### Project Structure
```
text-to-respondus/
├── src/
│   └── text_to_respondus/
│       ├── __init__.py
│       ├── converter.py      # Main conversion logic
│       ├── parser.py         # Quiz text parsing
│       └── cli.py           # Command line interface
├── tests/                   # Unit tests
├── data/                    # Example input files
├── output/                  # Generated CSV files
├── pyproject.toml          # Poetry configuration
└── README.md
```

### Running Tests
```bash
poetry run pytest
```

### Code Formatting
```bash
poetry run black src/ tests/
```

### Type Checking
```bash
poetry run mypy src/
```

## 📖 API Documentation

### Python API

```python
from text_to_respondus import QuizConverter

# Create converter
converter = QuizConverter()

# Convert a file
converter.convert_file(
    "input_quiz.txt", 
    "output_quiz.csv", 
    topic="Week 1"
)

# Get statistics
stats = converter.get_conversion_stats("input_quiz.txt")
print(f"Found {stats['total_questions']} questions")

# Validate input
if converter.validate_input_file("input_quiz.txt"):
    print("File is valid!")
```

### CLI Commands

```bash
# Convert a quiz file
text-to-respondus convert input.txt output.csv --topic "Week 1"

# Convert every *.txt quiz file in a folder
text-to-respondus batch input_dir/ output_dir/

# Validate without converting
text-to-respondus validate input.txt

# Preview first few questions
text-to-respondus preview input.txt --num-questions 3

# Show conversion statistics
text-to-respondus convert input.txt output.csv --stats

# Get help
text-to-respondus --help
```

## 🔧 Advanced Features

### Preview Before Converting
```bash
text-to-respondus convert quiz.txt output.csv --preview --stats
```

### Custom Topics and Difficulty
```bash
text-to-respondus convert quiz.txt output.csv --topic "Advanced Topics" --difficulty "Hard"
```

### Verbose Output
```bash
text-to-respondus --verbose convert quiz.txt output.csv
```

## 📊 Example Output

The converter produces CSV files like this:

| Question Type | Question Title/Id | Points | Question Wording | Correct Answer | Choice 1 | Choice 2 | Choice 3 | ... |
|---------------|-------------------|--------|------------------|----------------|----------|----------|----------|-----|
| mc | Deal Terminology | 1.0 | Which type of transaction... | A | Merger | Asset deal | Carve-out | ... |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run tests (`poetry run pytest`)
6. Format code (`poetry run black src/ tests/`)
7. Commit changes (`git commit -m 'Add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## 📋 Requirements

- **Input**: Canvas-style quiz text files
- **Output**: Respondus-compatible CSV files
- **Python**: 3.8 or higher
- **Dependencies**: pandas, click (managed by Poetry)

## 🐛 Troubleshooting

**Import Error in ANS?**
- Ensure your CSV uses comma separators (not semicolons)
- Check that all required columns are present
- Verify the file encoding is UTF-8

**Parsing Issues?**
- Ensure correct answers are marked with `*`
- Check that question format matches the expected structure
- Use the `validate` command to check for issues

**Missing Questions?**
- Verify the `Title:` and `Points:` format
- Ensure explanations start with `...`
- Check for proper line endings

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔄 Changelog

See [CHANGES.md](CHANGES.md) for version history and updates.

## 🙏 Acknowledgments

- Built for converting educational content to Respondus format
- Supports ANS and other learning management systems
- Designed with educator workflows in mind

---

**Made with ❤️ for educators and course creators**
