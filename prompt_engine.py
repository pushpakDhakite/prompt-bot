"""
Prompt Engine - Core Logic for Generating Professional AI Prompts
Implements advanced prompt engineering techniques
"""

import json
import re

class PromptEngine:
    def __init__(self):
        self.templates = self._load_templates()
        self.question_sets = self._load_question_sets()
        
    def _load_templates(self):
        """Load prompt templates"""
        return {
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
    
    def _load_question_sets(self):
        """Load question sets for different scenarios"""
        return {
            "base": [
                {
                    "id": "goal",
                    "question": "What is your primary goal with this prompt?",
                    "type": "select",
                    "options": [
                        "Generate creative content",
                        "Analyze or explain something",
                        "Write code or technical content",
                        "Summarize or extract information",
                        "Translate or convert content",
                        "Get recommendations or advice",
                        "Create marketing content",
                        "Research and explore topics"
                    ],
                    "required": True
                },
                {
                    "id": "ai_tool",
                    "question": "Which AI tool will you use?",
                    "type": "select",
                    "options": [
                        "ChatGPT",
                        "Claude",
                        "Gemini",
                        "Midjourney (Image)",
                        "DALL-E (Image)",
                        "GitHub Copilot",
                        "Notion AI",
                        "Other"
                    ],
                    "required": True
                },
                {
                    "id": "output_type",
                    "question": "What type of output do you need?",
                    "type": "select",
                    "options": [
                        "Article or blog post",
                        "Code or script",
                        "Report or analysis",
                        "Creative story",
                        "Email or message",
                        "List or bullet points",
                        "Step-by-step guide",
                        "Q&A format"
                    ],
                    "required": True
                },
                {
                    "id": "tone",
                    "question": "What tone should the output have?",
                    "type": "select",
                    "options": [
                        "Professional",
                        "Casual and friendly",
                        "Formal and academic",
                        "Creative and engaging",
                        "Technical and precise",
                        "Persuasive",
                        "Neutral and objective"
                    ],
                    "required": True
                },
                {
                    "id": "audience",
                    "question": "Who is the target audience?",
                    "type": "text",
                    "placeholder": "e.g., Business professionals, Students, General public",
                    "required": True
                },
                {
                    "id": "length",
                    "question": "How detailed should the response be?",
                    "type": "select",
                    "options": [
                        "Brief (1-2 paragraphs)",
                        "Moderate (3-5 paragraphs)",
                        "Detailed (full article)",
                        "Comprehensive (in-depth guide)"
                    ],
                    "required": True
                }
            ],
            "advanced": [
                {
                    "id": "include_examples",
                    "question": "Should examples be included?",
                    "type": "boolean",
                    "required": False
                },
                {
                    "id": "step_by_step",
                    "question": "Want step-by-step explanations?",
                    "type": "boolean",
                    "required": False
                },
                {
                    "id": "constraints",
                    "question": "Any specific constraints or requirements?",
                    "type": "textarea",
                    "placeholder": "e.g., Use simple language, Include statistics, Avoid jargon",
                    "required": False
                },
                {
                    "id": "format_requirements",
                    "question": "Any specific format requirements?",
                    "type": "textarea",
                    "placeholder": "e.g., Use markdown headers, Include code blocks, Add bullet points",
                    "required": False
                }
            ]
        }
    
    def get_dynamic_questions(self, context, previous_answers):
        """Generate dynamic questions based on context and previous answers"""
        questions = []
        
        # Add base questions
        questions.extend(self.question_sets["base"])
        
        # Add advanced questions
        questions.extend(self.question_sets["advanced"])
        
        # Add context-specific questions based on answers
        if previous_answers.get("ai_tool") == "Midjourney (Image)" or previous_answers.get("ai_tool") == "DALL-E (Image)":
            questions.append({
                "id": "image_style",
                "question": "What style should the image have?",
                "type": "select",
                "options": [
                    "Realistic photography",
                    "Digital art",
                    "Illustration",
                    "Abstract",
                    "3D render",
                    "Watercolor",
                    "Oil painting"
                ],
                "required": True
            })
        
        if previous_answers.get("output_type") == "Code or script":
            questions.append({
                "id": "programming_language",
                "question": "Which programming language?",
                "type": "text",
                "placeholder": "e.g., Python, JavaScript, SQL",
                "required": True
            })
        
        if "summarize" in previous_answers.get("goal", "").lower():
            questions.append({
                "id": "summary_focus",
                "question": "What aspects should the summary focus on?",
                "type": "textarea",
                "placeholder": "e.g., Key findings, Main arguments, Action items",
                "required": False
            })
        
        return questions
    
    def generate_prompt(self, context, answers, style="professional"):
        """Generate a professional prompt using advanced techniques"""
        
        # Determine template based on style
        template = self.templates.get(style, self.templates["general"])
        
        # Build prompt components
        components = []
        techniques_used = []
        
        # 1. Role Assignment (Role Prompting Technique)
        role = self._determine_role(answers)
        components.append(f"# Role\nYou are {role}.")
        techniques_used.append("Role Prompting")
        
        # 2. Context (if provided)
        if context and context.strip():
            components.append(f"\n# Context\n{context}")
            techniques_used.append("Context Injection")
        
        # 3. Task Description
        task = self._build_task_description(answers)
        components.append(f"\n# Task\n{task}")
        
        # 4. Output Format Instructions
        output_format = self._build_output_format(answers)
        components.append(f"\n# Output Format\n{output_format}")
        techniques_used.append("Structured Output")
        
        # 5. Constraints
        constraints = self._build_constraints(answers)
        if constraints:
            components.append(f"\n# Constraints\n{constraints}")
            techniques_used.append("Constraints")
        
        # 6. Examples (Few-shot prompting)
        if answers.get("include_examples"):
            examples = self._build_examples(answers)
            if examples:
                components.append(f"\n# Examples\n{examples}")
                techniques_used.append("Few-shot Prompting")
        
        # 7. Chain of Thought (if step-by-step requested)
        if answers.get("step_by_step"):
            components.append("\n# Instructions\nThink step-by-step before providing your response. Break down your reasoning process clearly.")
            techniques_used.append("Chain of Thought")
        
        # 8. Quality Improvement Instructions
        quality_instructions = self._build_quality_instructions(answers)
        components.append(f"\n# Quality Guidelines\n{quality_instructions}")
        
        # Combine all components
        full_prompt = "\n".join(components)
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(full_prompt, techniques_used)
        
        return {
            "prompt": full_prompt,
            "quality_score": quality_score,
            "techniques_used": techniques_used,
            "word_count": len(full_prompt.split())
        }
    
    def _determine_role(self, answers):
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
    
    def _build_task_description(self, answers):
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
    
    def _build_output_format(self, answers):
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
    
    def _build_constraints(self, answers):
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
    
    def _build_examples(self, answers):
        """Build example section (placeholder)"""
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
    
    def _build_quality_instructions(self, answers):
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
    
    def _calculate_quality_score(self, prompt, techniques_used):
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
    
    def improve_prompt(self, prompt, improvement_type="general"):
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
    
    def get_templates(self):
        """Return available templates"""
        return [
            {
                "id": key,
                "name": value["name"],
                "description": f"Template for {value['name'].lower()}",
                "techniques": value["techniques"]
            }
            for key, value in self.templates.items()
        ]