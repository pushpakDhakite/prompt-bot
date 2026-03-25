# Project Structure

AI Prompt Generator Pro follows a modular structure for easy maintenance and deployment.

## Directory Layout

```
bot1/
├── prompt_generator.py     # Main GUI application (PyQt6)
├── prompt_core.py          # Core prompt generation engine
├── run_gui.py              # Application launcher
├── version_info.py         # Version information for PyInstaller
├── requirements.txt        # Python dependencies
├── requirements_deploy.txt # Pinned dependencies for deployment
├── PromptGeneratorPro.spec # PyInstaller configuration
│
├── assets/                 # Application assets
│   ├── icons/             # Application icons
│   ├── images/            # UI images and graphics
│   ├── license.txt        # License file
│   ├── readme_before.txt  # Installer pre-install message
│   └── readme_after.txt   # Installer post-install message
│
├── data/                   # Application data
│   ├── prompts.json       # Saved prompts database
│   ├── templates/         # Prompt templates
│   └── logs/              # Application logs
│
├── installer/              # Inno Setup installer files
│   ├── setup.iss          # Installer script
│   └── setup.ico          # Installer icon
│
├── dist/                   # Build output
│   ├── PromptGeneratorPro.exe  # Built executable
│   └── installer/         # Installer package
│
├── build/                  # PyInstaller build files
│
├── release/                # Release packages
│   └── v2.0.0/           # Versioned release
│
├── deploy/                 # Deployment packages
│   └── v2.0.0/           # Portable deployment
│
├── tests/                  # Test files
│   └── test_core.py       # Core functionality tests
│
├── docs/                   # Documentation
│   ├── INSTALL_GUIDE.md   # Installation instructions
│   ├── QUICK_START.md     # Getting started guide
│   ├── FAQ.md             # Frequently asked questions
│   └── PROJECT_STRUCTURE.md  # This file
│
├── scripts/                # Build and deployment scripts
│   ├── build.bat          # Build executable
│   ├── create_installer.bat  # Create installer
│   ├── build_all.bat      # Complete build process
│   └── deploy_simple.bat  # Create portable deployment
│
├── README.md               # Project overview
├── LICENSE                 # MIT License
├── CHANGELOG.md           # Version history
├── APP_README.md          # Application documentation
└── APPLICATION_SUMMARY.md # Technical summary
```

## Core Modules

### prompt_generator.py
Main GUI application using PyQt6. Contains:
- MainWindow class with all UI components
- Tab-based interface (Input, Builder, Output, Library, Settings)
- Modern dark theme styling
- File processing and prompt generation

### prompt_core.py
Core prompt generation engine. Contains:
- Template loading and processing
- CSV and JSON file analysis
- Advanced prompt generation with techniques:
  - Role Prompting
  - Chain of Thought
  - Few-shot Prompting
  - Structured Output
  - Constraints
  - Context Injection

### run_gui.py
Simple launcher that imports and runs the main application.

## Configuration Files

### requirements.txt
Python package dependencies:
- PyQt6 (GUI framework)
- PyPDF2 (PDF processing)
- pandas (Data analysis)
- numpy (Numerical operations)

### PromptGeneratorPro.spec
PyInstaller configuration for building executable:
- Bundles all dependencies
- Includes assets and data files
- Creates single-file executable

### version_info.py
Version information for executable metadata:
- Application name and version
- Company information
- File descriptions

## Build System

### Scripts
- **build.bat**: Creates executable using PyInstaller
- **create_installer.bat**: Creates Windows installer using Inno Setup
- **build_all.bat**: Complete build process
- **deploy_simple.bat**: Creates portable deployment

### Build Process
1. Install dependencies
2. Create application icon
3. Build executable with PyInstaller
4. Create installer with Inno Setup
5. Package release files

## Data Management

### prompts.json
User's saved prompts database. Format:
```json
[
  {
    "id": "uuid",
    "title": "Prompt Title",
    "prompt": "Generated prompt text",
    "context": "Input context",
    "style": "technical",
    "category": "coding",
    "tags": ["python", "api"],
    "created_at": "2026-03-25T10:00:00",
    "quality_score": 85,
    "usage_count": 5
  }
]
```

### templates/
Text files with placeholder syntax:
```
Write a {tone} {output_type} about {topic} for {audience}.
```

## Testing

### test_core.py
Tests core functionality:
- Prompt generation
- Template loading
- CSV/JSON processing
- Quality scoring

## Documentation

### User Documentation
- **INSTALL_GUIDE.md**: How to install and uninstall
- **QUICK_START.md**: Getting started tutorial
- **FAQ.md**: Common questions and answers

### Developer Documentation
- **PROJECT_STRUCTURE.md**: This file
- **CHANGELOG.md**: Version history
- **APPLICATION_SUMMARY.md**: Technical overview

## Dependencies

### Runtime Dependencies
- Python 3.8+
- PyQt6 6.10+
- PyPDF2 3.0+
- pandas 3.0+
- numpy 2.4+

### Build Dependencies
- PyInstaller 6.14+
- Inno Setup 6 (Windows)
- Pillow (for icon generation)

## Version Control

### Versioning Scheme
- Major.Minor.Patch (e.g., 2.0.0)
- Semantic versioning
- Changelog for each release

### Git Structure
```
main branch: Stable releases
develop branch: Development
feature/*: New features
bugfix/*: Bug fixes
release/*: Release preparation
```

## Deployment Options

### 1. Windows Installer
- Single .exe installer
- Creates shortcuts and file associations
- Includes uninstaller

### 2. Portable Version
- No installation required
- Run from any location
- Requires Python on system

### 3. From Source
- Clone repository
- Install dependencies
- Run directly with Python

## Extending the Application

### Adding New Templates
1. Create .txt file in `data/templates/`
2. Use `{placeholder}` syntax for variables
3. Application auto-detects new templates

### Adding New Input Types
1. Update `InputProcessorThread` in prompt_generator.py
2. Add file extension handling
3. Implement content extraction

### Adding New Prompt Techniques
1. Update `generate_prompt()` in prompt_core.py
2. Add technique to `techniques_used` list
3. Update quality scoring algorithm

## Performance Considerations

### Memory Management
- Background threads for file processing
- Lazy loading of templates
- Limited context size (10,000 chars)

### Startup Optimization
- Fast import of core modules
- Deferred loading of heavy libraries
- Cached template loading

## Security

### File Handling
- Sandboxed file access
- Input validation
- Error handling for corrupted files

### Data Privacy
- Local storage only
- No network transmission
- User data stays on machine

## Future Roadmap

### Version 2.1
- Voice input support
- Image OCR integration
- Cloud sync (optional)

### Version 2.2
- Light theme
- Keyboard shortcuts
- Batch processing

### Version 3.0
- Web application
- Team collaboration
- AI integration

## Support and Community

### Getting Help
- GitHub Issues for bugs
- Discord for discussion
- Documentation for guides

### Contributing
- Fork and submit PR
- Follow code style
- Add tests for new features