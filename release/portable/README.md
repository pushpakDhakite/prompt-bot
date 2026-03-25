# AI Prompt Generator Bot

This bot helps you generate AI prompts from various input types including text, images, audio, PDFs, and other files.

## Features

- Accepts multiple input types: text, images, audio, PDFs, and other files
- Asks for user preferences to tailor the generated prompt
- Generates customized prompts based on your input and requirements
- Option to save the generated prompt to a file

## Usage

1. Run the bot: `python prompt_bot.py`
2. Follow the prompts to:
   - Select your input type
   - Provide your input (either directly or via file path)
   - Specify your preferences (goal, style, length, additional instructions)
   - Receive your generated prompt
   - Optionally save the prompt to a file

## Requirements

- Python 3.x
- PyPDF2 (for PDF processing) - installed via requirements.txt

## Installing Dependencies

```bash
pip install -r requirements.txt
```

## Supported Input Types

- **Text**: Direct entry or from .txt, .md, etc. files
- **Image**: Description-based (since direct image processing isn't available in this environment)
- **Audio**: Description-based (since direct audio processing isn't available in this environment)
- **PDF**: Text extraction using PyPDF2
- **Other**: Attempts text reading or description-based input

## Example Workflow

1. Choose input type (e.g., PDF)
2. Provide PDF file path
3. Bot extracts text from PDF
4. Specify goal (e.g., "generate a summary")
5. Choose style (e.g., "concise and professional")
6. Select length (e.g., "short")
7. Add any additional instructions
8. Receive your customized prompt
9. Optionally save to file

## Notes

- For image and audio inputs, since direct processing isn't available in this CLI environment, you'll be asked to describe the content
- PDF processing requires PyPDF2, which is included in requirements.txt
- The bot handles various text encodings and provides fallbacks for file reading errors