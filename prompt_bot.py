import os
import sys
import re
import json
from pathlib import Path

def load_template(template_name):
    """Load a prompt template from the templates directory"""
    template_path = Path("templates") / f"{template_name}.txt"
    if template_path.exists():
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading template: {e}")
            return None
    else:
        print(f"Template '{template_name}' not found.")
        return None

def list_available_templates():
    """List all available templates in the templates directory"""
    templates_dir = Path("templates")
    if not templates_dir.exists():
        return []
    
    templates = []
    for file in templates_dir.glob("*.txt"):
        templates.append(file.stem)
    return templates

def process_csv_file(filepath):
    """Process a CSV file and return a summary of its contents"""
    try:
        import pandas as pd
        df = pd.read_csv(filepath)
        
        # Get basic info
        info = f"CSV file with {len(df)} rows and {len(df.columns)} columns\n"
        info += f"Columns: {', '.join(df.columns.tolist())}\n\n"
        
        # Get sample data
        info += "First 3 rows:\n"
        info += df.head(3).to_string() + "\n\n"
        
        # Get column types
        info += "Column data types:\n"
        for col in df.columns:
            info += f"  {col}: {df[col].dtype}\n"
        
        # Get basic stats for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            info += "\nNumeric column statistics:\n"
            info += df[numeric_cols].describe().to_string()
        
        return info
    except Exception as e:
        return f"Error processing CSV file: {e}"

def process_json_file(filepath):
    """Process a JSON file and return a summary of its contents"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Basic info
        info = f"JSON file with {len(str(data))} characters\n"
        
        # If it's a dict, show top-level keys
        if isinstance(data, dict):
            info += f"Top-level keys: {', '.join(list(data.keys())[:10])}"
            if len(data.keys()) > 10:
                info += f" and {len(data.keys()) - 10} more"
            info += "\n\n"
            
            # Show structure of first few items if it's a list of dicts
            for key, value in list(data.items())[:3]:
                if isinstance(value, list) and len(value) > 0:
                    info += f"'{key}' is a list with {len(value)} items\n"
                    if isinstance(value[0], dict):
                        info += f"  First item keys: {', '.join(list(value[0].keys())[:5])}\n"
                elif isinstance(value, dict):
                    info += f"'{key}' is a dictionary with {len(value)} keys\n"
                    info += f"  Sample keys: {', '.join(list(value.keys())[:5])}\n"
                else:
                    info += f"'{key}': {type(value).__name__} = {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}\n"
        
        # If it's a list
        elif isinstance(data, list):
            info += f"JSON array with {len(data)} items\n"
            if len(data) > 0:
                info += f"First item type: {type(data[0]).__name__}\n"
                if isinstance(data[0], dict):
                    info += f"First item keys: {', '.join(list(data[0].keys())[:10])}\n"
        
        return info
    except Exception as e:
        return f"Error processing JSON file: {e}"

def get_user_preferences():
    """Get user preferences for prompt generation"""
    print("\n=== Prompt Preferences ===")
    print("Let's tailor the prompt to your needs.\n")
    
    # Goal/Purpose
    print("What is the goal or purpose of the prompt?")
    print("Examples: generate a story, answer a question, create artwork, write code, etc.")
    goal = input("\nEnter the goal: ").strip()
    
    # Style/Tone
    print("\nWhat style or tone should the prompt have?")
    print("Examples: formal, casual, poetic, technical, humorous, persuasive, etc.")
    style = input("\nEnter style/tone: ").strip()
    
    # Length
    print("\nWhat approximate length do you prefer for the generated prompt?")
    print("Options: short (1-2 sentences), medium (paragraph), long (detailed)")
    length = input("\nEnter length (short/medium/long): ").strip().lower()
    if length not in ['short', 'medium', 'long']:
        length = 'medium'  # default
    
    # Additional instructions
    print("\nAny additional instructions or constraints?")
    print("Examples: include specific keywords, avoid certain topics, format requirements, etc.")
    additional = input("\nEnter additional instructions (or leave blank): ").strip()
    
    return goal, style, length, additional

def apply_template(template_str, replacements):
    """Apply replacements to a template string"""
    result = template_str
    for key, value in replacements.items():
        placeholder = "{" + key + "}"
        result = result.replace(placeholder, value)
    return result
    print("=== AI Prompt Generator Bot ===")
    print("I can help you generate prompts from various input types.")
    print("Supported inputs: text, image, audio, PDF, and other files.\n")
    
    # Step 1: Get input type
    input_types = {
        '1': 'text (.txt, .md, etc.)',
        '2': 'image (.jpg, .png, .gif, etc.)',
        '3': 'audio (.mp3, .wav, etc.)',
        '4': 'PDF (.pdf)',
        '5': 'other file type'
    }
    
    print("What type of input do you have?")
    for key, value in input_types.items():
        print(f"  {key}. {value}")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    input_type = input_types.get(choice, 'text')
    if choice not in input_types:
        print("Invalid choice. Defaulting to text.\n")
    
    # Step 2: Get input content
    content = ""
    if choice == '1':  # Text
        print("\nYou can either:")
        print("  1. Enter text directly")
        print("  2. Provide a path to a text file")
        subchoice = input("Enter your choice (1 or 2): ").strip()
        
        if subchoice == '1':
            content = input("\nEnter your text: ").strip()
        elif subchoice == '2':
            filepath = input("\nEnter the path to your text file: ").strip()
            if os.path.isfile(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    print(f"Error reading file: {e}")
                    print("Falling back to manual entry.")
                    content = input("\nEnter your text: ").strip()
            else:
                print("File not found. Please enter text manually.")
                content = input("\nEnter your text: ").strip()
        else:
            print("Invalid choice. Please enter text manually.")
            content = input("\nEnter your text: ").strip()
    
    elif choice == '2':  # Image
        print("\nSince I cannot process images directly in this environment,")
        print("please provide a description of the image.")
        content = input("\nDescribe the image: ").strip()
    
    elif choice == '3':  # Audio
        print("\nSince I cannot process audio directly in this environment,")
        print("please provide a description of the audio content.")
        content = input("\nDescribe the audio: ").strip()
    
    elif choice == '4':  # PDF
        print("\nAttempting to extract text from PDF...")
        filepath = input("\nEnter the path to your PDF file: ").strip()
        if os.path.isfile(filepath):
            try:
                # Try to import PyPDF2
                import PyPDF2
                with open(filepath, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                    content = text.strip()
                    if not content:
                        print("No text extracted from PDF. Please provide a description.")
                        content = input("\nDescribe the PDF content: ").strip()
            except ImportError:
                print("PyPDF2 not installed. Please provide a description of the PDF.")
                content = input("\nDescribe the PDF content: ").strip()
            except Exception as e:
                print(f"Error processing PDF: {e}")
                print("Please provide a description of the PDF.")
                content = input("\nDescribe the PDF content: ").strip()
        else:
            print("File not found. Please provide a description.")
            content = input("\nDescribe the PDF content: ").strip()
    
    else:  # Other
        print("\nFor other file types, I'll try to read as text or you can provide a description.")
        filepath = input("\nEnter the path to your file (or leave blank to describe): ").strip()
        if filepath and os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if not content.strip():
                    print("File appears to be empty or binary. Please provide a description.")
                    content = input("\nDescribe the file content: ").strip()
            except Exception as e:
                print(f"Error reading file: {e}")
                print("Please provide a description.")
                content = input("\nDescribe the file content: ").strip()
        else:
            if not filepath:
                filepath = "no file provided"
            print(f"You chose to describe '{filepath}'.")
            content = input("\nDescribe the content: ").strip()
    
    # Step 3: Ask if user wants to use a template
    print("\n=== Template Options ===")
    available_templates = list_available_templates()
    if available_templates:
        print("Available templates:")
        for i, template in enumerate(available_templates, 1):
            print(f"  {i}. {template}")
        print("  0. Create prompt from scratch")
        
        template_choice = input("\nSelect a template (0 for custom): ").strip()
        template_used = False
        
        if template_choice.isdigit() and int(template_choice) != 0:
            template_index = int(template_choice) - 1
            if 0 <= template_index < len(available_templates):
                template_name = available_templates[template_index]
                template_content = load_template(template_name)
                if template_content:
                    print(f"\nLoaded template: {template_name}")
                    print("Template content:")
                    print("-" * 40)
                    print(template_content)
                    print("-" * 40)
                    
                    # Extract placeholders from template
                    placeholders = re.findall(r'\{([^}]+)\}', template_content)
                    if placeholders:
                        print(f"\nTemplate requires the following information: {', '.join(placeholders)}")
                        replacements = {}
                        for placeholder in placeholders:
                            value = input(f"Enter value for {{{placeholder}}}: ").strip()
                            replacements[placeholder] = value
                        
                        # Apply template
                        content = apply_template(template_content, replacements)
                        template_used = True
                        print(f"\nGenerated content from template:")
                        print("-" * 40)
                        print(content)
                        print("-" * 40)
                    else:
                        content = template_content
                        template_used = True
    
    # If not using template or template failed, get input content as before
    if not template_used:
        # Step 2: Get input content (restructured)
        if choice == '1':  # Text
            print("\nYou can either:")
            print("  1. Enter text directly")
            print("  2. Provide a path to a text file")
            subchoice = input("Enter your choice (1 or 2): ").strip()
            
            if subchoice == '1':
                content = input("\nEnter your text: ").strip()
            elif subchoice == '2':
                filepath = input("\nEnter the path to your text file: ").strip()
                if os.path.isfile(filepath):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except Exception as e:
                        print(f"Error reading file: {e}")
                        print("Falling back to manual entry.")
                        content = input("\nEnter your text: ").strip()
                else:
                    print("File not found. Please enter text manually.")
                    content = input("\nEnter your text: ").strip()
            else:
                print("Invalid choice. Please enter text manually.")
                content = input("\nEnter your text: ").strip()
        
        elif choice == '2':  # Image
            print("\nSince I cannot process images directly in this environment,")
            print("please provide a description of the image.")
            content = input("\nDescribe the image: ").strip()
        
        elif choice == '3':  # Audio
            print("\nSince I cannot process audio directly in this environment,")
            print("please provide a description of the audio content.")
            content = input("\nDescribe the audio: ").strip()
        
        elif choice == '4':  # PDF
            print("\nAttempting to extract text from PDF...")
            filepath = input("\nEnter the path to your PDF file: ").strip()
            if os.path.isfile(filepath):
                try:
                    # Try to import PyPDF2
                    import PyPDF2
                    with open(filepath, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text() + "\n"
                        content = text.strip()
                        if not content:
                            print("No text extracted from PDF. Please provide a description.")
                            content = input("\nDescribe the PDF content: ").strip()
                except ImportError:
                    print("PyPDF2 not installed. Please provide a description of the PDF.")
                    content = input("\nDescribe the PDF content: ").strip()
                except Exception as e:
                    print(f"Error processing PDF: {e}")
                    print("Please provide a description of the PDF.")
                    content = input("\nDescribe the PDF content: ").strip()
            else:
                print("File not found. Please provide a description.")
                content = input("\nDescribe the PDF content: ").strip()
        
        else:  # Other - now with CSV/JSON support
            print("\nFor other file types, I'll try to read as text or you can provide a description.")
            filepath = input("\nEnter the path to your file (or leave blank to describe): ").strip()
            if filepath and os.path.isfile(filepath):
                # Check file extension for special handling
                ext = os.path.splitext(filepath)[1].lower()
                if ext == '.csv':
                    print("\nProcessing CSV file...")
                    content = process_csv_file(filepath)
                elif ext == '.json':
                    print("\nProcessing JSON file...")
                    content = process_json_file(filepath)
                else:
                    # Try to read as text
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        if not content.strip():
                            print("File appears to be empty or binary. Please provide a description.")
                            content = input("\nDescribe the file content: ").strip()
                    except Exception as e:
                        print(f"Error reading file: {e}")
                        print("Please provide a description.")
                        content = input("\nDescribe the file content: ").strip()
            else:
                if not filepath:
                    filepath = "no file provided"
                print(f"You chose to describe '{filepath}'.")
                content = input("\nDescribe the content: ").strip()
    
    # Step 4: Get user preferences for prompt generation
    goal, style, length, additional = get_user_preferences()
    
    # Step 5: Generate the prompt
    print("\n=== Generating Prompt ===\n")
    
    # Base prompt from content
    prompt_parts = []
    if content:
        prompt_parts.append(f"Input content: {content}")
    
    # Add goal
    if goal:
        prompt_parts.append(f"Goal: {goal}")
    
    # Add style
    if style:
        prompt_parts.append(f"Style/Tone: {style}")
    
    # Add length guidance
    length_guidance = {
        'short': "Keep the prompt concise (1-2 sentences)",
        'medium': "Provide a moderate level of detail (one paragraph)",
        'long': "Provide comprehensive details and context"
    }
    if length in length_guidance:
        prompt_parts.append(f"Length: {length_guidance[length]}")
    
    # Add additional instructions
    if additional:
        prompt_parts.append(f"Additional Instructions: {additional}")
    
    # Combine into final prompt
    final_prompt = "Based on the following information, generate an appropriate prompt:\n\n"
    final_prompt += "\n".join(prompt_parts)
    final_prompt += "\n\nGenerated Prompt:"
    
    # Output the result
    print(final_prompt)
    print("\n" + "="*50)
    
    # Ask if user wants to save
    save_choice = input("\nWould you like to save this prompt to a file? (y/n): ").strip().lower()
    if save_choice == 'y':
        filename = input("Enter filename (default: generated_prompt.txt): ").strip()
        if not filename:
            filename = "generated_prompt.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(final_prompt)
            print(f"Prompt saved to {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")
    
    print("\nThank you for using the AI Prompt Generator Bot!")

def main():
    print("=== AI Prompt Generator Bot ===")
    print("I can help you generate prompts from various input types.")
    print("Supported inputs: text, image, audio, PDF, CSV, JSON, and other files.\n")
    
    # Step 1: Get input type
    input_types = {
        '1': 'text (.txt, .md, etc.)',
        '2': 'image (.jpg, .png, .gif, etc.)',
        '3': 'audio (.mp3, .wav, etc.)',
        '4': 'PDF (.pdf)',
        '5': 'CSV (.csv)',
        '6': 'JSON (.json)',
        '7': 'other file type'
    }
    
    print("What type of input do you have?")
    for key, value in input_types.items():
        print(f"  {key}. {value}")
    
    choice = input("\nEnter your choice (1-7): ").strip()
    
    input_type = input_types.get(choice, 'text')
    if choice not in input_types:
        print("Invalid choice. Defaulting to text.\n")
    
    # Step 2: Get input content
    content = ""
    if choice == '1':  # Text
        print("\nYou can either:")
        print("  1. Enter text directly")
        print("  2. Provide a path to a text file")
        subchoice = input("Enter your choice (1 or 2): ").strip()
        
        if subchoice == '1':
            content = input("\nEnter your text: ").strip()
        elif subchoice == '2':
            filepath = input("\nEnter the path to your text file: ").strip()
            if os.path.isfile(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    print(f"Error reading file: {e}")
                    print("Falling back to manual entry.")
                    content = input("\nEnter your text: ").strip()
            else:
                print("File not found. Please enter text manually.")
                content = input("\nEnter your text: ").strip()
        else:
            print("Invalid choice. Please enter text manually.")
            content = input("\nEnter your text: ").strip()
    
    elif choice == '2':  # Image
        print("\nSince I cannot process images directly in this environment,")
        print("please provide a description of the image.")
        content = input("\nDescribe the image: ").strip()
    
    elif choice == '3':  # Audio
        print("\nSince I cannot process audio directly in this environment,")
        print("please provide a description of the audio content.")
        content = input("\nDescribe the audio: ").strip()
    
    elif choice == '4':  # PDF
        print("\nAttempting to extract text from PDF...")
        filepath = input("\nEnter the path to your PDF file: ").strip()
        if os.path.isfile(filepath):
            try:
                # Try to import PyPDF2
                import PyPDF2
                with open(filepath, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                    content = text.strip()
                    if not content:
                        print("No text extracted from PDF. Please provide a description.")
                        content = input("\nDescribe the PDF content: ").strip()
            except ImportError:
                print("PyPDF2 not installed. Please provide a description of the PDF.")
                content = input("\nDescribe the PDF content: ").strip()
            except Exception as e:
                print(f"Error processing PDF: {e}")
                print("Please provide a description of the PDF.")
                content = input("\nDescribe the PDF content: ").strip()
        else:
            print("File not found. Please provide a description.")
            content = input("\nDescribe the PDF content: ").strip()
    
    elif choice == '5':  # CSV
        print("\nProcessing CSV file...")
        filepath = input("\nEnter the path to your CSV file: ").strip()
        if os.path.isfile(filepath):
            content = process_csv_file(filepath)
            if content.startswith("Error"):
                print(content)
                print("Falling back to description.")
                content = input("\nDescribe the CSV content: ").strip()
        else:
            print("File not found. Please provide a description.")
            content = input("\nDescribe the CSV content: ").strip()
    
    elif choice == '6':  # JSON
        print("\nProcessing JSON file...")
        filepath = input("\nEnter the path to your JSON file: ").strip()
        if os.path.isfile(filepath):
            content = process_json_file(filepath)
            if content.startswith("Error"):
                print(content)
                print("Falling back to description.")
                content = input("\nDescribe the JSON content: ").strip()
        else:
            print("File not found. Please provide a description.")
            content = input("\nDescribe the JSON content: ").strip()
    
    else:  # Other
        print("\nFor other file types, I'll try to read as text or you can provide a description.")
        filepath = input("\nEnter the path to your file (or leave blank to describe): ").strip()
        if filepath and os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if not content.strip():
                    print("File appears to be empty or binary. Please provide a description.")
                    content = input("\nDescribe the file content: ").strip()
            except Exception as e:
                print(f"Error reading file: {e}")
                print("Please provide a description.")
                content = input("\nDescribe the file content: ").strip()
        else:
            if not filepath:
                filepath = "no file provided"
            print(f"You chose to describe '{filepath}'.")
            content = input("\nDescribe the content: ").strip()
    
    # Step 3: Ask if user wants to use a template
    print("\n=== Template Options ===")
    available_templates = list_available_templates()
    if available_templates:
        print("Available templates:")
        for i, template in enumerate(available_templates, 1):
            print(f"  {i}. {template}")
        print("  0. Create prompt from scratch")
        
        template_choice = input("\nSelect a template (0 for custom): ").strip()
        template_used = False
        
        if template_choice.isdigit() and int(template_choice) != 0:
            template_index = int(template_choice) - 1
            if 0 <= template_index < len(available_templates):
                template_name = available_templates[template_index]
                template_content = load_template(template_name)
                if template_content:
                    print(f"\nLoaded template: {template_name}")
                    print("Template content:")
                    print("-" * 40)
                    print(template_content)
                    print("-" * 40)
                    
                    # Extract placeholders from template
                    placeholders = re.findall(r'\{([^}]+)\}', template_content)
                    if placeholders:
                        print(f"\nTemplate requires the following information: {', '.join(placeholders)}")
                        replacements = {}
                        for placeholder in placeholders:
                            value = input(f"Enter value for {{{placeholder}}}: ").strip()
                            replacements[placeholder] = value
                        
                        # Apply template
                        content = apply_template(template_content, replacements)
                        template_used = True
                        print(f"\nGenerated content from template:")
                        print("-" * 40)
                        print(content)
                        print("-" * 40)
                    else:
                        content = template_content
                        template_used = True
    
    # If not using template or template failed, get input content as before
    if not template_used:
        # Step 2: Get input content (restructured)
        if choice == '1':  # Text
            print("\nYou can either:")
            print("  1. Enter text directly")
            print("  2. Provide a path to a text file")
            subchoice = input("Enter your choice (1 or 2): ").strip()
            
            if subchoice == '1':
                content = input("\nEnter your text: ").strip()
            elif subchoice == '2':
                filepath = input("\nEnter the path to your text file: ").strip()
                if os.path.isfile(filepath):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except Exception as e:
                        print(f"Error reading file: {e}")
                        print("Falling back to manual entry.")
                        content = input("\nEnter your text: ").strip()
                else:
                    print("File not found. Please enter text manually.")
                    content = input("\nEnter your text: ").strip()
            else:
                print("Invalid choice. Please enter text manually.")
                content = input("\nEnter your text: ").strip()
        
        elif choice == '2':  # Image
            print("\nSince I cannot process images directly in this environment,")
            print("please provide a description of the image.")
            content = input("\nDescribe the image: ").strip()
        
        elif choice == '3':  # Audio
            print("\nSince I cannot process audio directly in this environment,")
            print("please provide a description of the audio content.")
            content = input("\nDescribe the audio: ").strip()
        
        elif choice == '4':  # PDF
            print("\nAttempting to extract text from PDF...")
            filepath = input("\nEnter the path to your PDF file: ").strip()
            if os.path.isfile(filepath):
                try:
                    # Try to import PyPDF2
                    import PyPDF2
                    with open(filepath, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text() + "\n"
                        content = text.strip()
                        if not content:
                            print("No text extracted from PDF. Please provide a description.")
                            content = input("\nDescribe the PDF content: ").strip()
                except ImportError:
                    print("PyPDF2 not installed. Please provide a description of the PDF.")
                    content = input("\nDescribe the PDF content: ").strip()
                except Exception as e:
                    print(f"Error processing PDF: {e}")
                    print("Please provide a description of the PDF.")
                    content = input("\nDescribe the PDF content: ").strip()
            else:
                print("File not found. Please provide a description.")
                content = input("\nDescribe the PDF content: ").strip()
        
        elif choice == '5':  # CSV
            print("\nProcessing CSV file...")
            filepath = input("\nEnter the path to your CSV file: ").strip()
            if os.path.isfile(filepath):
                content = process_csv_file(filepath)
                if content.startswith("Error"):
                    print(content)
                    print("Falling back to description.")
                    content = input("\nDescribe the CSV content: ").strip()
            else:
                print("File not found. Please provide a description.")
                content = input("\nDescribe the CSV content: ").strip()
        
        elif choice == '6':  # JSON
            print("\nProcessing JSON file...")
            filepath = input("\nEnter the path to your JSON file: ").strip()
            if os.path.isfile(filepath):
                content = process_json_file(filepath)
                if content.startswith("Error"):
                    print(content)
                    print("Falling back to description.")
                    content = input("\nDescribe the JSON content: ").strip()
            else:
                print("File not found. Please provide a description.")
                content = input("\nDescribe the JSON content: ").strip()
        
        else:  # Other - now with CSV/JSON support
            print("\nFor other file types, I'll try to read as text or you can provide a description.")
            filepath = input("\nEnter the path to your file (or leave blank to describe): ").strip()
            if filepath and os.path.isfile(filepath):
                # Check file extension for special handling
                ext = os.path.splitext(filepath)[1].lower()
                if ext == '.csv':
                    print("\nProcessing CSV file...")
                    content = process_csv_file(filepath)
                elif ext == '.json':
                    print("\nProcessing JSON file...")
                    content = process_json_file(filepath)
                else:
                    # Try to read as text
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        if not content.strip():
                            print("File appears to be empty or binary. Please provide a description.")
                            content = input("\nDescribe the file content: ").strip()
                    except Exception as e:
                        print(f"Error reading file: {e}")
                        print("Please provide a description.")
                        content = input("\nDescribe the file content: ").strip()
            else:
                if not filepath:
                    filepath = "no file provided"
                print(f"You chose to describe '{filepath}'.")
                content = input("\nDescribe the content: ").strip()
    
    # Step 4: Get user preferences for prompt generation
    goal, style, length, additional = get_user_preferences()
    
    # Step 5: Generate the prompt
    print("\n=== Generating Prompt ===\n")
    
    # Base prompt from content
    prompt_parts = []
    if content:
        prompt_parts.append(f"Input content: {content}")
    
    # Add goal
    if goal:
        prompt_parts.append(f"Goal: {goal}")
    
    # Add style
    if style:
        prompt_parts.append(f"Style/Tone: {style}")
    
    # Add length guidance
    length_guidance = {
        'short': "Keep the prompt concise (1-2 sentences)",
        'medium': "Provide a moderate level of detail (one paragraph)",
        'long': "Provide comprehensive details and context"
    }
    if length in length_guidance:
        prompt_parts.append(f"Length: {length_guidance[length]}")
    
    # Add additional instructions
    if additional:
        prompt_parts.append(f"Additional Instructions: {additional}")
    
    # Combine into final prompt
    final_prompt = "Based on the following information, generate an appropriate prompt:\n\n"
    final_prompt += "\n".join(prompt_parts)
    final_prompt += "\n\nGenerated Prompt:"
    
    # Output the result
    print(final_prompt)
    print("\n" + "="*50)
    
    # Ask if user wants to save
    save_choice = input("\nWould you like to save this prompt to a file? (y/n): ").strip().lower()
    if save_choice == 'y':
        filename = input("Enter filename (default: generated_prompt.txt): ").strip()
        if not filename:
            filename = "generated_prompt.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(final_prompt)
            print(f"Prompt saved to {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")
    
    print("\nThank you for using the AI Prompt Generator Bot!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please try again.")
        sys.exit(1)