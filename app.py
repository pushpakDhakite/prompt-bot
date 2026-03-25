"""
Advanced AI Prompt Generator - Main Application
A modern web application for generating professional AI prompts
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime
import uuid
from prompt_engine import PromptEngine
from input_processor import InputProcessor
from prompts_db import PromptsDB

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize components
prompt_engine = PromptEngine()
input_processor = InputProcessor()
prompts_db = PromptsDB()

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html')

@app.route('/api/process-input', methods=['POST'])
def process_input():
    """Process different types of input (text, file, URL)"""
    try:
        input_type = request.form.get('input_type', 'text')
        context = ""
        
        if input_type == 'text':
            context = request.form.get('text_content', '')
        
        elif input_type == 'file':
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Save file temporarily
            filename = f"{uuid.uuid4()}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process file based on extension
            context = input_processor.process_file(filepath, file.filename)
            
            # Clean up
            os.remove(filepath)
        
        elif input_type == 'url':
            url = request.form.get('url', '')
            if url:
                context = input_processor.process_url(url)
        
        return jsonify({
            'success': True,
            'context': context[:5000] if len(context) > 5000 else context,
            'context_length': len(context)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-prompt', methods=['POST'])
def generate_prompt():
    """Generate a prompt based on user inputs and answers"""
    try:
        data = request.json
        
        # Extract data
        context = data.get('context', '')
        answers = data.get('answers', {})
        style = data.get('style', 'professional')
        
        # Generate prompt using the engine
        result = prompt_engine.generate_prompt(context, answers, style)
        
        return jsonify({
            'success': True,
            'prompt': result['prompt'],
            'quality_score': result.get('quality_score', 85),
            'techniques_used': result.get('techniques_used', [])
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/improve-prompt', methods=['POST'])
def improve_prompt():
    """Improve an existing prompt"""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        improvement_type = data.get('type', 'general')
        
        improved = prompt_engine.improve_prompt(prompt, improvement_type)
        
        return jsonify({
            'success': True,
            'improved_prompt': improved['prompt'],
            'changes': improved.get('changes', [])
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save-prompt', methods=['POST'])
def save_prompt():
    """Save a prompt to the library"""
    try:
        data = request.json
        prompt_data = {
            'id': str(uuid.uuid4()),
            'title': data.get('title', 'Untitled Prompt'),
            'prompt': data.get('prompt', ''),
            'context': data.get('context', ''),
            'style': data.get('style', 'professional'),
            'category': data.get('category', 'general'),
            'tags': data.get('tags', []),
            'created_at': datetime.now().isoformat(),
            'quality_score': data.get('quality_score', 0),
            'usage_count': 0
        }
        
        prompts_db.save_prompt(prompt_data)
        
        return jsonify({
            'success': True,
            'prompt_id': prompt_data['id']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-prompts', methods=['GET'])
def get_prompts():
    """Get all saved prompts"""
    try:
        category = request.args.get('category', 'all')
        search = request.args.get('search', '')
        
        prompts = prompts_db.get_prompts(category, search)
        
        return jsonify({
            'success': True,
            'prompts': prompts
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-prompt/<prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
    """Get a specific prompt by ID"""
    try:
        prompt = prompts_db.get_prompt(prompt_id)
        
        if prompt:
            return jsonify({
                'success': True,
                'prompt': prompt
            })
        else:
            return jsonify({'error': 'Prompt not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete-prompt/<prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
    """Delete a prompt from the library"""
    try:
        prompts_db.delete_prompt(prompt_id)
        
        return jsonify({
            'success': True,
            'message': 'Prompt deleted successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-templates', methods=['GET'])
def get_templates():
    """Get available prompt templates"""
    try:
        templates = prompt_engine.get_templates()
        
        return jsonify({
            'success': True,
            'templates': templates
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-questions', methods=['POST'])
def get_questions():
    """Get dynamic questions based on context"""
    try:
        data = request.json
        context = data.get('context', '')
        previous_answers = data.get('previous_answers', {})
        
        questions = prompt_engine.get_dynamic_questions(context, previous_answers)
        
        return jsonify({
            'success': True,
            'questions': questions
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-prompt', methods=['POST'])
def export_prompt():
    """Export prompt in different formats"""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        format_type = data.get('format', 'txt')
        title = data.get('title', 'generated_prompt')
        
        if format_type == 'txt':
            filename = f"{title}.txt"
            filepath = os.path.join('data', filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(prompt)
            return send_file(filepath, as_attachment=True)
        
        elif format_type == 'json':
            filename = f"{title}.json"
            filepath = os.path.join('data', filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({'prompt': prompt, 'title': title}, f, indent=2)
            return send_file(filepath, as_attachment=True)
        
        elif format_type == 'md':
            filename = f"{title}.md"
            filepath = os.path.join('data', filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n{prompt}")
            return send_file(filepath, as_attachment=True)
        
        else:
            return jsonify({'error': 'Unsupported format'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-stats', methods=['GET'])
def get_stats():
    """Get usage statistics"""
    try:
        stats = prompts_db.get_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)