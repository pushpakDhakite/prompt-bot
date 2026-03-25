# AI Prompt Generator Pro

A modern desktop application for generating professional AI prompts using advanced prompt engineering techniques.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

## Features

### Input Sources
- **Text Input**: Direct text entry or paste
- **PDF Documents**: Extract text from PDF files
- **CSV Data**: Process and analyze CSV data
- **JSON Files**: Parse and summarize JSON structures
- **Website URLs**: Extract content from web pages (basic)
- **Other Files**: Support for .txt, .md, and other formats

### Interactive Prompt Builder
- Guided question-based workflow
- Dynamic questions based on context
- Multiple prompt styles:
  - Creative Writing
  - Technical Documentation
  - Code Generation
  - Marketing Copy
  - Academic Research
  - General Purpose

### Advanced Prompt Engineering
- **Role Prompting**: Assign expert roles to AI
- **Chain of Thought**: Step-by-step reasoning instructions
- **Few-shot Prompting**: Include examples when needed
- **Structured Output**: Clear formatting requirements
- **Constraints**: Add specific limitations and requirements
- **Quality Scoring**: Automatic prompt quality assessment

### Prompt Management
- **Library**: Save and organize prompts
- **Templates**: Use pre-built templates
- **History**: Track prompt usage
- **Export**: Save as TXT, Markdown, or JSON
- **Copy**: One-click copy to clipboard
- **Improve**: AI-assisted prompt enhancement

### Modern UI
- Dark theme with glassmorphism effects
- Responsive and intuitive interface
- Tab-based navigation
- Real-time feedback

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone or download the project**
   ```bash
   cd bot1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run_gui.py
   ```
   
   Or on Windows:
   ```bash
   start.bat
   ```

### Dependencies
- PyQt6 (GUI framework)
- PyPDF2 (PDF processing)
- pandas (Data analysis)
- numpy (Numerical operations)

## Usage Guide

### 1. Input Source Tab
1. Select your input type (text, PDF, CSV, JSON, etc.)
2. Enter text directly or browse for a file
3. Click "Process Input" to extract content
4. Review the extracted context
5. Click "Next: Build Prompt →"

### 2. Prompt Builder Tab
1. Answer the guided questions:
   - What is your goal?
   - Which AI tool will you use?
   - What type of output do you need?
   - What tone should it have?
   - Who is the target audience?
   - How detailed should it be?
2. Configure advanced options if needed
3. Click "Generate Prompt"

### 3. Generated Prompt Tab
1. Review your generated prompt
2. Check the quality score
3. Use action buttons:
   - **Copy to Clipboard**: Copy the prompt
   - **Improve Prompt**: Get AI-enhanced version
   - **Regenerate**: Create a new variation
4. Export in different formats:
   - TXT (plain text)
   - Markdown (with formatting)
   - JSON (structured data)
   - Save to Library

### 4. Prompt Library Tab
1. Browse saved prompts
2. Search by title or content
3. Filter by category
4. Load, edit, or delete prompts

### 5. Settings Tab
1. Configure default AI tool
2. Set default prompt style
3. Manage templates
4. View application info

## Prompt Engineering Techniques

The application implements these advanced techniques:

### Role Prompting
Assigns expert roles to the AI (e.g., "You are a senior software engineer...")

### Chain of Thought
Instructs AI to think step-by-step before responding

### Few-shot Prompting
Includes examples to guide AI output

### Structured Output
Specifies exact format requirements

### Constraints
Defines limitations and requirements

### Context Injection
Incorporates provided input into the prompt

## Architecture

```
bot1/
├── prompt_generator.py    # Main GUI application
├── prompt_core.py         # Core prompt generation logic
├── run_gui.py            # Application launcher
├── start.bat             # Windows launcher
├── requirements.txt      # Python dependencies
├── data/                 # User data storage
│   ├── prompts.json      # Saved prompts
│   └── uploads/          # Temporary uploads
└── templates/            # Prompt templates
```

## API Reference

### Core Functions

#### generate_prompt(context, answers, style)
Generate a professional prompt.

**Parameters:**
- `context` (str): Input content
- `answers` (dict): User answers to questions
- `style` (str): Prompt style template

**Returns:**
- `dict`: Contains 'prompt', 'quality_score', 'techniques_used'

#### process_csv_file(filepath)
Process CSV file and return summary.

#### process_json_file(filepath)
Process JSON file and return structure analysis.

### GUI Components

#### MainWindow
Main application window with:
- Input source tab
- Prompt builder wizard
- Output display
- Library management
- Settings panel

## Customization

### Adding New Templates

1. Create a new template file in `templates/` directory
2. Follow the existing template format
3. The application will automatically detect new templates

### Modifying Questions

Edit the `question_sets` dictionary in `prompt_core.py` to add or modify builder questions.

### Styling Changes

Modify the style methods in `prompt_generator.py`:
- `get_button_style()`
- `get_group_style()`
- `get_input_style()`
- `apply_dark_theme()`

## Troubleshooting

### Application won't start
- Check Python version: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Check for error messages in console

### PDF processing fails
- Ensure PyPDF2 is installed: `pip install PyPDF2`
- Check if PDF is encrypted or corrupted

### CSV/JSON processing fails
- Ensure pandas is installed: `pip install pandas`
- Check file encoding (UTF-8 recommended)

### GUI looks incorrect
- Update PyQt6: `pip install --upgrade PyQt6`
- Try running with different style: `app.setStyle('Windows')`

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- PyQt6 for the GUI framework
- PyPDF2 for PDF processing
- pandas for data analysis
- OpenAI for prompt engineering inspiration

## Version History

### v2.0 (Current)
- Complete rewrite with PyQt6
- Modern dark theme UI
- Advanced prompt engineering techniques
- Prompt library and templates
- Multiple export formats
- Quality scoring system

### v1.0
- Basic CLI interface
- Simple prompt generation
- Basic file support

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code documentation
3. Create an issue on the repository

---

**Made with ❤️ for the AI community**