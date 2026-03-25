"""
Advanced Prompt Engine - Core Logic for Generating Professional AI Prompts
Implements advanced prompt engineering techniques
"""

import json
import re

def load_template(template_name):
    """Load a prompt template from the templates directory"""
    from pathlib import Path
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
    from pathlib import Path
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

def apply_template(template_str, replacements):
    """Apply replacements to a template string"""
    result = template_str
    for key, value in replacements.items():
        placeholder = "{" + key + "}"
        result = result.replace(placeholder, value)
    return result


# Template definitions for different prompt styles
TEMPLATES = {
    "creative": {
        "name": "Creative Writing",
        "role": "Expert creative writer",
        "techniques": ["role_prompting", "chain_of_thought", "few_shot"],
        "structure": "creative"
    },
    "technical": {
        "name": "Technical Documentation",
        "role": "Senior technical writer",
        "techniques": ["role_prompting", "structured_output", "constraints"],
        "structure": "technical"
    },
    "coding": {
        "name": "Code Generation",
        "role": "Senior software engineer",
        "techniques": ["role_prompting", "chain_of_thought", "step_by_step"],
        "structure": "coding"
    },
    "marketing": {
        "name": "Marketing Copy",
        "role": "Marketing strategist",
        "techniques": ["role_prompting", "audience_aware", "constraints"],
        "structure": "marketing"
    },
    "academic": {
        "name": "Academic Research",
        "role": "Academic researcher",
        "techniques": ["role_prompting", "chain_of_thought", "structured_output"],
        "structure": "academic"
    },
    "general": {
        "name": "General Purpose",
        "role": "Helpful assistant",
        "techniques": ["role_prompting", "clarity"],
        "structure": "general"
    }
}

def generate_prompt(content, answers, style="professional"):
    """
    Generate a professional prompt using advanced techniques.
    
    Args:
        content (str): The input content (from text, file, etc.)
        answers (dict): User answers to questions
        style (str): Prompt style template name
    
    Returns:
        dict: Contains 'prompt', 'quality_score', 'techniques_used'
    """
    
    # Determine template based on style
    template = TEMPLATES.get(style, TEMPLATES["general"])
    
    # Build prompt components
    components = []
    techniques_used = []
    
    # 1. Role Assignment (Role Prompting Technique)
    role = _determine_role(answers)
    components.append(f"# Role\nYou are {role}.")
    techniques_used.append("Role Prompting")
    
    # 2. Context (if provided)
    if content and content.strip():
        components.append(f"\n# Context\n{content}")
        techniques_used.append("Context Injection")
    
    # 3. Task Description
    task = _build_task_description(answers)
    components.append(f"\n# Task\n{task}")
    
    # 4. Output Format Instructions
    output_format = _build_output_format(answers)
    components.append(f"\n# Output Format\n{output_format}")
    techniques_used.append("Structured Output")
    
    # 5. Constraints
    constraints = _build_constraints(answers)
    if constraints:
        components.append(f"\n# Constraints\n{constraints}")
        techniques_used.append("Constraints")
    
    # 6. Examples (Few-shot prompting)
    if answers.get("include_examples"):
        examples = _build_examples(answers)
        if examples:
            components.append(f"\n# Examples\n{examples}")
            techniques_used.append("Few-shot Prompting")
    
    # 7. Chain of Thought (if step-by-step requested)
    if answers.get("step_by_step"):
        components.append("\n# Instructions\nThink step-by-step before providing your response. Break down your reasoning process clearly.")
        techniques_used.append("Chain of Thought")
    
    # 8. Quality Improvement Instructions
    quality_instructions = _build_quality_instructions(answers)
    components.append(f"\n# Quality Guidelines\n{quality_instructions}")
    
    # Combine all components
    full_prompt = "\n".join(components)
    
    # Calculate quality score
    quality_score = _calculate_quality_score(full_prompt, techniques_used)
    
    return {
        "prompt": full_prompt,
        "quality_score": quality_score,
        "techniques_used": techniques_used,
        "word_count": len(full_prompt.split())
    }

def _determine_role(answers):
    """Determine the appropriate role based on answers"""
    goal = answers.get("goal", "").lower()
    output_type = answers.get("output_type", "").lower()
    
    if "code" in goal or "code" in output_type or "script" in output_type:
        return "an expert software engineer"
    elif "creative" in goal or "story" in output_type:
        return "a professional creative writer"
    elif "technical" in output_type or "documentation" in output_type:
        return "a senior technical writer"
    elif "marketing" in goal or "marketing" in output_type:
        return "an experienced marketing strategist"
    elif "research" in goal or "academic" in output_type:
        return "a seasoned academic researcher"
    elif "translate" in goal:
        return "a professional translator"
    elif "summarize" in goal or "extract" in goal:
        return "an expert analyst"
    else:
        return "a knowledgeable and helpful assistant"

def _build_task_description(answers):
    """Build the main task description"""
    parts = []
    
    goal = answers.get("goal", "")
    output_type = answers.get("output_type", "")
    
    parts.append(f"Your task is to help me {goal.lower() if goal else 'generate content'}.")
    
    if output_type:
        parts.append(f"The desired output is: {output_type}.")
    
    if answers.get("audience"):
        parts.append(f"Tailor your response for: {answers['audience']}.")
    
    if answers.get("tone"):
        tone_map = {
            "Professional": "Use a professional tone.",
            "Casual and friendly": "Use a casual and friendly tone.",
            "Formal and academic": "Use a formal and academic tone.",
            "Creative and engaging": "Use a creative and engaging tone.",
            "Technical and precise": "Use a technical and precise tone.",
            "Persuasive": "Use a persuasive tone.",
            "Neutral and objective": "Use a neutral and objective tone."
        }
        parts.append(tone_map.get(answers.get("tone"), "Use an appropriate tone."))
    
    return " ".join(parts)

def _build_output_format(answers):
    """Build output format instructions"""
    parts = []
    
    length = answers.get("length", "")
    if "Brief" in length:
        parts.append("Keep your response concise (1-2 paragraphs).")
    elif "Moderate" in length:
        parts.append("Provide a moderate-length response (3-5 paragraphs).")
    elif "Detailed" in length:
        parts.append("Provide a detailed response covering all aspects.")
    elif "Comprehensive" in length:
        parts.append("Provide a comprehensive and in-depth response.")
    
    format_reqs = answers.get("format_requirements", "")
    if format_reqs:
        parts.append(f"Follow these formatting guidelines: {format_reqs}")
    else:
        parts.append("Use clear structure with appropriate headings and formatting.")
    
    return " ".join(parts)

def _build_constraints(answers):
    """Build constraint instructions"""
    parts = []
    
    if answers.get("constraints"):
        parts.append(answers["constraints"])
    
    # Add default constraints based on output type
    output_type = answers.get("output_type", "")
    if "Code" in output_type or "script" in output_type:
        parts.append("Ensure code is well-commented and follows best practices.")
        parts.append("Include error handling where appropriate.")
    
    if not parts:
        return ""
    
    return "\n".join(f"- {part}" for part in parts)

def _build_examples(answers):
    """Build example section"""
    output_type = answers.get("output_type", "")
    
    if "Code" in output_type:
        return """Example format:
```python
def example_function():
    # Comment explaining the purpose
    result = some_operation()
    return result
```"""
    elif "Article" in output_type:
        return """Example structure:
# Title
## Introduction
Brief overview of the topic
## Main Section 1
Detailed explanation
## Main Section 2
Further details
## Conclusion
Summary and key takeaways"""
    
    return ""

def _build_quality_instructions(answers):
    """Build quality improvement instructions"""
    parts = [
        "Ensure your response is accurate and factually correct.",
        "Provide clear and actionable information.",
        "Avoid unnecessary repetition.",
        "Use appropriate terminology for the target audience."
    ]
    
    if answers.get("include_examples"):
        parts.append("Include relevant examples to illustrate your points.")
    
    if answers.get("ai_tool"):
        parts.append(f"Optimize your response for {answers['ai_tool']}.")
    
    return "\n".join(f"- {part}" for part in parts)

def _calculate_quality_score(prompt, techniques_used):
    """Calculate prompt quality score"""
    score = 60  # Base score
    
    # Add points for techniques used
    score += len(techniques_used) * 5
    
    # Add points for structure
    if "# Role" in prompt:
        score += 5
    if "# Context" in prompt:
        score += 5
    if "# Constraints" in prompt:
        score += 5
    if "# Output Format" in prompt:
        score += 5
    
    # Cap at 100
    return min(score, 100)

def improve_prompt(prompt, improvement_type="general"):
    """Improve an existing prompt"""
    changes = []
    improved = prompt
    
    # Check for common issues and improve
    if len(prompt.split()) < 50:
        improved += "\n\nPlease provide a comprehensive and detailed response."
        changes.append("Added detail request")
    
    if "step" not in prompt.lower() and "chain" not in prompt.lower():
        improved += "\n\nThink step-by-step before providing your answer."
        changes.append("Added Chain of Thought")
    
    if "# Role" not in prompt:
        role_line = "# Role\nYou are an expert assistant.\n"
        improved = role_line + improved
        changes.append("Added role assignment")
    
    if "# Constraints" not in prompt:
        improved += "\n\n# Constraints\n- Be accurate and factual\n- Avoid unnecessary repetition"
        changes.append("Added constraints")
    
    return {
        "prompt": improved,
        "changes": changes
    }