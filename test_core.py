"""
Test script for core functionality
"""

from prompt_core import generate_prompt, list_available_templates, improve_prompt

def test_prompt_generation():
    """Test prompt generation"""
    print("Testing prompt generation...")
    
    context = "A guide to machine learning basics for beginners."
    
    answers = {
        "goal": "Generate creative content",
        "ai_tool": "ChatGPT",
        "output_type": "Step-by-step guide",
        "tone": "Professional",
        "audience": "Computer science students",
        "length": "Detailed (full article)",
        "include_examples": True,
        "step_by_step": True,
        "constraints": "Use simple language, Include practical examples",
        "format_requirements": "Use markdown headers, Include code examples"
    }
    
    style = "technical"
    
    # Test using the new function signature
    result = generate_prompt(context, answers, style)
    
    print(f"\nGenerated Prompt ({len(result['prompt'])} characters):")
    print("=" * 60)
    print(result['prompt'][:500] + "...")
    print("=" * 60)
    print(f"Quality Score: {result.get('quality_score', 0)}%")
    print(f"Techniques Used: {result.get('techniques_used', [])}")
    print("\nTest passed!")

def test_templates():
    """Test template listing"""
    print("\nTesting template listing...")
    
    templates = list_available_templates()
    print(f"Found {len(templates)} templates: {templates}")
    
    if templates:
        print("Template test passed!")
    else:
        print("No templates found (this is OK if templates directory is empty)")

if __name__ == "__main__":
    print("=" * 60)
    print("AI Prompt Generator - Core Functionality Test")
    print("=" * 60)
    
    test_prompt_generation()
    test_templates()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)