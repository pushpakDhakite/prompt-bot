"""
Test script to demonstrate the prompt bot functionality
without requiring interactive input.
"""

def simulate_prompt_generation():
    print("=== AI Prompt Generator Bot (Demo) ===")
    print("This is a demonstration of how the bot works.\n")
    
    # Simulate user inputs
    print("Simulating user interaction:")
    print("- Input type: PDF")
    print("- File path: sample.pdf (contains text about renewable energy)")
    print("- Goal: Generate an educational presentation outline")
    print("- Style: Engaging and informative")
    print("- Length: Medium")
    print("- Additional instructions: Include 3 key sections with sub-points\n")
    
    # Simulated extracted content from PDF
    content = """Renewable energy sources are becoming increasingly important in the fight against climate change. 
    Solar power harnesses energy from the sun using photovoltaic cells or solar thermal systems. 
    Wind energy captures kinetic energy from air movement using turbines. 
    Hydroelectric power generates electricity from flowing water in rivers and dams. 
    Geothermal energy utilizes heat from the Earth's interior. 
    Biomass energy comes from organic materials like plants and waste."""
    
    # User preferences (simulated)
    goal = "Generate an educational presentation outline"
    style = "Engaging and informative"
    length = "Medium"
    additional = "Include 3 key sections with sub-points"
    
    # Generate prompt (same logic as in the bot)
    print("=== Generating Prompt ===\n")
    
    prompt_parts = []
    if content:
        prompt_parts.append(f"Input content: {content}")
    
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
    
    final_prompt = "Based on the following information, generate an appropriate prompt:\n\n"
    final_prompt += "\n".join(prompt_parts)
    final_prompt += "\n\nGenerated Prompt:"
    
    print(final_prompt)
    print("\n" + "="*50)
    
    # Show what a good generated prompt might look like
    print("\nExample of what the AI might generate:")
    print("Create an educational presentation outline about renewable energy sources that is engaging and informative. "
          "The presentation should have medium detail (approximately one paragraph per section) and include exactly "
          "three key sections: 1) Solar and Wind Energy technologies, 2) Hydroelectric and Geothermal power systems, "
          "and 3) Biomass energy and future innovations. Each section should contain 2-3 sub-points with specific "
          "examples, benefits, and current applications.")
    
    print("\n" + "="*50)
    print("Demo complete!")

if __name__ == "__main__":
    simulate_prompt_generation()