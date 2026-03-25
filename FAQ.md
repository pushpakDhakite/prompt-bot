# Frequently Asked Questions

## General Questions

### What is AI Prompt Generator Pro?

AI Prompt Generator Pro is a desktop application that helps you create professional-quality prompts for AI tools like ChatGPT, Claude, Gemini, Midjourney, and more. It uses advanced prompt engineering techniques to generate optimized prompts from your input.

### What makes this different from other prompt tools?

- **Advanced Engineering**: Uses techniques like Role Prompting, Chain of Thought, Few-shot Prompting
- **Quality Scoring**: Automatically evaluates prompt quality (0-100%)
- **Multiple Input Types**: Supports text, PDF, CSV, JSON, and more
- **Library Management**: Save and organize your prompts
- **Modern Interface**: Professional dark theme UI

### Is it free?

Yes! AI Prompt Generator Pro is free and open-source under the MIT License.

### What platforms are supported?

Currently, we support Windows 10/11 (64-bit). macOS and Linux versions are planned for future releases.

## Installation

### Do I need Python installed?

- **Installer version**: No, Python is bundled
- **Source version**: Yes, Python 3.8 or higher

### How much disk space is needed?

- Application: ~50 MB
- Templates: ~5 MB
- Prompts library: Varies (typically <10 MB)

### Can I install it on a USB drive?

Yes, use the source version on a portable Python installation.

### How do I update?

1. Download the new installer
2. Run it (it will update existing installation)
3. Your prompts library is preserved

## Input Types

### What file types are supported?

- **Text**: .txt, .md
- **PDF**: .pdf (extracts text)
- **Data**: .csv, .json (with analysis)
- **Other**: Any text-based file

### Can I use images?

Image OCR support is planned for version 2.1. For now, you can describe images in text.

### Can I input from websites?

Yes, enter a URL in the text field. Basic content extraction is supported.

### What's the maximum file size?

There's no hard limit, but very large files (>100 MB) may be slow to process.

## Prompt Generation

### How does the quality scoring work?

The score is calculated based on:
- Number of prompt engineering techniques used
- Structure and completeness
- Presence of key elements (Role, Context, Constraints)

A score of 80%+ indicates a professional-quality prompt.

### What are the prompt engineering techniques?

1. **Role Prompting**: Assigns expert roles to AI
2. **Chain of Thought**: Step-by-step reasoning
3. **Few-shot Prompting**: Includes examples
4. **Structured Output**: Clear formatting
5. **Constraints**: Specific limitations
6. **Context Injection**: Uses your input

### Can I customize the prompts?

Yes! You can:
- Edit generated prompts directly
- Use "Improve Prompt" for AI enhancements
- Create custom templates
- Save and modify prompts in your library

### How do I get better results?

1. Provide detailed input/context
2. Answer all builder questions completely
3. Use advanced options (examples, constraints)
4. Choose the right style for your task
5. Review and edit the generated prompt

## Library Management

### Where are my prompts saved?

Prompts are saved in:
- Windows: `%APPDATA%\AI Prompt Generator Pro\prompts.json`
- Or in the `data` folder in the application directory

### Can I export my library?

Yes, export individual prompts as TXT, MD, or JSON. Full library export is planned.

### How many prompts can I save?

There's no limit. The library uses a JSON file that can grow as needed.

### Can I search my prompts?

Yes, use the search bar in the Prompt Library tab to search by title or content.

## Troubleshooting

### The application won't start

1. Check Python installation (for source version)
2. Verify all dependencies are installed
3. Run from command line to see errors
4. Check Windows Event Viewer for crashes

### File processing fails

1. Check file permissions
2. Ensure file isn't corrupted
3. Try a different file format
4. Check file encoding (UTF-8 recommended)

### UI looks strange

1. Update graphics drivers
2. Try different display scaling
3. Check for Windows updates
4. Disable high DPI scaling in compatibility settings

### Export doesn't work

1. Check write permissions to target folder
2. Ensure enough disk space
3. Try a different export format
4. Close the file if it's open in another program

### Prompt quality is low

1. Provide more detailed input
2. Answer all questions completely
3. Use advanced options
4. Try different prompt style
5. Use "Improve Prompt" feature

## Advanced Usage

### Can I create my own templates?

Yes! Create .txt files in the `data/templates` folder with `{placeholder}` syntax.

Example:
```
Write a {tone} {output_type} about {topic} for {audience}.
```

### Can I use it programmatically?

The core modules (`prompt_core.py`) can be imported in Python scripts.

### Is there a command-line version?

Yes, `prompt_bot.py` is the original CLI version.

### Can I integrate with other tools?

The JSON export format is designed for easy integration with other applications.

## Future Features

### What's coming in version 2.1?

- Voice input support
- Image OCR integration
- Direct AI API integration
- Prompt versioning
- Cloud sync

### How can I contribute?

1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Join our Discord for discussion

### How do I report bugs?

Create an issue on GitHub with:
- Error message
- Steps to reproduce
- System information
- Screenshots if applicable

## Licensing

### Can I use it commercially?

Yes, the MIT License allows commercial use.

### Can I modify it?

Yes, you can modify and distribute under the same license.

### Do I need to give credit?

While not required, attribution is appreciated.

## Support

### Where can I get help?

- GitHub Issues: Report bugs and request features
- Documentation: Read the guides in this repository
- Discord: Join our community (link in README)

### Is there paid support?

Currently, support is community-based. Commercial support may be offered in the future.

### How do I stay updated?

- Watch the GitHub repository
- Subscribe to release notifications
- Join our Discord server