"""
Demo script to test the enhanced prompt bot functionality
without requiring interactive input.
"""

import os
import sys
import re
import json
from pathlib import Path

# Copy the essential functions from prompt_bot.py for demonstration

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
    """Get user preferences for prompt generation (simulated for demo)"""
    # Simulated user preferences
    goal = "Generate a sales report summary"
    style = "professional and concise"
    length = "medium"
    additional = "Focus on trends and actionable insights"
    return goal, style, length, additional

def apply_template(template_str, replacements):
    """Apply replacements to a template string"""
    result = template_str
    for key, value in replacements.items():
        placeholder = "{" + key + "}"
        result = result.replace(placeholder, value)
    return result

def demo_enhanced_features():
    print("=== AI Prompt Generator Bot - Enhanced Features Demo ===\n")
    
    # Demo 1: Template System
    print("1. TEMPLATE SYSTEM DEMO")
    print("-" * 30)
    available_templates = list_available_templates()
    print(f"Available templates: {available_templates}")
    
    if available_templates:
        template_name = available_templates[0]  # Use first template
        template_content = load_template(template_name)
        print(f"\nLoaded template '{template_name}':")
        print(template_content)
        
        # Extract placeholders and simulate user input
        placeholders = re.findall(r'\{([^}]+)\}', template_content)
        if placeholders:
            print(f"\nTemplate placeholders: {placeholders}")
            # Simulate providing values for placeholders
            replacements = {}
            for placeholder in placeholders:
                if placeholder == "language":
                    replacements[placeholder] = "Python"
                elif placeholder == "function_name":
                    replacements[placeholder] = "calculate_sales_tax"
                elif placeholder == "description":
                    replacements[placeholder] = "calculates sales tax based on purchase amount and location"
                elif placeholder == "parameters":
                    replacements[placeholder] = "amount (float), location (str)"
                elif placeholder == "return_value":
                    replacements[placeholder] = "the calculated tax amount (float)"
                elif placeholder == "error_cases":
                    replacements[placeholder] = "negative amounts and invalid locations"
                elif placeholder == "standards":
                    replacements[placeholder] = "PEP 8 with type hints"
                elif placeholder == "additional_instructions":
                    replacements[placeholder] = "Include docstring and examples"
                else:
                    replacements[placeholder] = f"sample_value_for_{placeholder}"
            
            # Apply template
            filled_template = apply_template(template_content, replacements)
            print(f"\nFilled template:")
            print(filled_template)
    print()
    
    # Demo 2: CSV Processing
    print("2. CSV PROCESSING DEMO")
    print("-" * 30)
    csv_content = process_csv_file("sample_data.csv")
    print("Processing sample_data.csv:")
    print(csv_content)
    print()
    
    # Demo 3: JSON Processing (create a sample JSON file)
    print("3. JSON PROCESSING DEMO")
    print("-" * 30)
    sample_json = {
        "company": "TechCorp Inc.",
        "employees": [
            {"name": "John Doe", "position": "Software Engineer", "salary": 90000},
            {"name": "Jane Smith", "position": "Product Manager", "salary": 95000},
            {"name": "Bob Johnson", "position": "Designer", "salary": 85000}
        ],
        "departments": ["Engineering", "Product", "Design"],
        "founded": 2020,
        "location": "San Francisco"
    }
    
    with open("sample_data.json", "w") as f:
        json.dump(sample_json, f, indent=2)
    
    json_content = process_json_file("sample_data.json")
    print("Processing sample_data.json:")
    print(json_content)
    print()
    
    # Demo 4: Enhanced Prompt Generation
    print("4. ENHANCED PROMPT GENERATION DEMO")
    print("-" * 30)
    goal, style, length, additional = get_user_preferences()
    
    # Use CSV content as input
    input_content = csv_content
    
    # Build prompt parts
    prompt_parts = []
    if input_content:
        prompt_parts.append(f"Input content: {input_content}")
    
    if goal:
        prompt_parts.append(f"Goal: {goal}")
    
    if style:
        prompt_parts.append(f"Style/Tone: {style}")
    
    length_guidance = {
        'short': "Keep the prompt concise (1-2 sentences)",
        'medium': "Provide a moderate level of detail (one paragraph)",
        'long': "Provide comprehensive details and context"
    }
    if length in length_guidance:
        prompt_parts.append(f"Length: {length_guidance[length]}")
    
    if additional:
        prompt_parts.append(f"Additional Instructions: {additional}")
    
    # Combine into final prompt
    final_prompt = "Based on the following information, generate an appropriate prompt:\n\n"
    final_prompt += "\n".join(prompt_parts)
    final_prompt += "\n\nGenerated Prompt:"
    
    print("Generated Prompt:")
    print(final_prompt)
    print()
    
    # Show what a good generated prompt might look like
    print("Example of what the AI might generate:")
    print("Create a professional and concise sales report summary based on the following CSV data: [data description]. "
          "The summary should be of medium detail (approximately one paragraph) and focus on trends and actionable insights. "
          "Include analysis of salary distributions across departments, identify highest/lowest earning departments, "
          "and provide recommendations for budget allocation based on the data.")
    
    print("\n" + "="*60)
    print("Demo complete! The enhanced prompt bot now includes:")
    print("* Template system with customizable placeholders")
    print("* Advanced CSV processing with data summarization")
    print("* Advanced JSON processing with structure analysis")
    print("* Enhanced user preference collection")
    print("* Integrated prompt generation with all features")

if __name__ == "__main__":
    demo_enhanced_features()