# Changelog

All notable changes to AI Prompt Generator Pro will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-03-25

### Added
- Complete rewrite with PyQt6 desktop application
- Modern dark theme UI with glassmorphism effects
- Tab-based interface with 5 main sections:
  - Input Source: Multiple file type support
  - Prompt Builder: Interactive wizard with guided questions
  - Generated Prompt: Output display with quality scoring
  - Prompt Library: Save, search, and filter prompts
  - Settings: Configure defaults and templates
- Advanced prompt engineering techniques:
  - Role Prompting
  - Chain of Thought
  - Few-shot Prompting
  - Structured Output
  - Constraints
  - Context Injection
  - Quality Scoring (0-100%)
- Multiple input type support:
  - Text (direct entry or paste)
  - PDF Documents
  - CSV Data Files
  - JSON Data Files
  - Website URLs
  - Other file formats (.txt, .md)
- Prompt library with search and filtering
- Export in multiple formats:
  - TXT (plain text)
  - Markdown
  - JSON
- Template management system
- Windows installer with Inno Setup
- Version management system

### Changed
- Migrated from CLI to modern GUI
- Completely redesigned user interface
- Improved prompt generation algorithm
- Enhanced file processing capabilities

### Fixed
- Unicode handling in file processing
- Memory management for large files
- Thread safety for background operations

## [1.0.0] - 2026-03-23

### Added
- Initial release with basic CLI interface
- Text and PDF input support
- Simple prompt generation
- Basic user preferences
- CSV and JSON file processing
- Template system with placeholders
- Multi-language support (planned)

### Known Issues
- Limited file type support
- No GUI interface
- Basic prompt generation only

---

## Upcoming Features

### Version 2.1.0 (Planned)
- [ ] Voice input support
- [ ] Image OCR integration
- [ ] Direct AI API integration
- [ ] Prompt versioning
- [ ] Cloud sync for prompts

### Version 2.2.0 (Planned)
- [ ] Light theme option
- [ ] Customizable layouts
- [ ] Keyboard shortcuts
- [ ] Batch processing
- [ ] Prompt testing with AI

### Version 3.0.0 (Future)
- [ ] Web application version
- [ ] Mobile companion app
- [ ] Team collaboration features
- [ ] Marketplace for prompts
- [ ] AI-powered prompt optimization