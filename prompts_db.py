"""
Prompts Database - Manages storage and retrieval of prompts
Uses JSON file storage for simplicity
"""

import json
import os
from datetime import datetime
from pathlib import Path

class PromptsDB:
    def __init__(self, db_path="data/prompts.json"):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure the database file exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            self._save_data({
                "prompts": [],
                "templates": [],
                "history": []
            })
    
    def _load_data(self):
        """Load data from JSON file"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "prompts": [],
                "templates": [],
                "history": []
            }
    
    def _save_data(self, data):
        """Save data to JSON file"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def save_prompt(self, prompt_data):
        """Save a prompt to the database"""
        data = self._load_data()
        
        # Check if prompt with same ID exists
        existing_idx = next((i for i, p in enumerate(data["prompts"]) if p["id"] == prompt_data["id"]), None)
        
        if existing_idx is not None:
            # Update existing
            data["prompts"][existing_idx] = prompt_data
        else:
            # Add new
            data["prompts"].append(prompt_data)
        
        # Add to history
        history_entry = {
            "id": prompt_data["id"],
            "title": prompt_data["title"],
            "timestamp": prompt_data["created_at"],
            "action": "create" if existing_idx is None else "update"
        }
        data["history"].insert(0, history_entry)
        
        # Keep only last 100 history items
        data["history"] = data["history"][:100]
        
        self._save_data(data)
        return prompt_data["id"]
    
    def get_prompts(self, category="all", search=""):
        """Get all prompts, optionally filtered"""
        data = self._load_data()
        prompts = data["prompts"]
        
        # Filter by category
        if category != "all":
            prompts = [p for p in prompts if p.get("category") == category]
        
        # Filter by search term
        if search:
            search_lower = search.lower()
            prompts = [
                p for p in prompts 
                if search_lower in p.get("title", "").lower() or 
                   search_lower in p.get("prompt", "").lower() or
                   any(search_lower in tag.lower() for tag in p.get("tags", []))
            ]
        
        # Sort by creation date (newest first)
        prompts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return prompts
    
    def get_prompt(self, prompt_id):
        """Get a specific prompt by ID"""
        data = self._load_data()
        prompt = next((p for p in data["prompts"] if p["id"] == prompt_id), None)
        
        # Increment usage count if found
        if prompt:
            prompt["usage_count"] = prompt.get("usage_count", 0) + 1
            self._save_data(data)
        
        return prompt
    
    def delete_prompt(self, prompt_id):
        """Delete a prompt"""
        data = self._load_data()
        data["prompts"] = [p for p in data["prompts"] if p["id"] != prompt_id]
        self._save_data(data)
    
    def get_categories(self):
        """Get all unique categories"""
        data = self._load_data()
        categories = set()
        for prompt in data["prompts"]:
            if prompt.get("category"):
                categories.add(prompt["category"])
        return sorted(list(categories))
    
    def get_stats(self):
        """Get usage statistics"""
        data = self._load_data()
        
        total_prompts = len(data["prompts"])
        total_usage = sum(p.get("usage_count", 0) for p in data["prompts"])
        
        # Calculate average quality score
        scores = [p.get("quality_score", 0) for p in data["prompts"] if p.get("quality_score")]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Get category distribution
        categories = {}
        for prompt in data["prompts"]:
            cat = prompt.get("category", "uncategorized")
            categories[cat] = categories.get(cat, 0) + 1
        
        # Get recent activity (last 7 days)
        recent_count = 0
        now = datetime.now()
        for prompt in data["prompts"]:
            try:
                created = datetime.fromisoformat(prompt.get("created_at", ""))
                if (now - created).days <= 7:
                    recent_count += 1
            except (ValueError, TypeError):
                continue
        
        return {
            "total_prompts": total_prompts,
            "total_usage": total_usage,
            "average_quality_score": round(avg_score, 1),
            "categories": categories,
            "recent_activity": recent_count,
            "history_count": len(data.get("history", []))
        }
    
    def save_template(self, template_data):
        """Save a template"""
        data = self._load_data()
        
        existing_idx = next((i for i, t in enumerate(data["templates"]) if t["id"] == template_data["id"]), None)
        
        if existing_idx is not None:
            data["templates"][existing_idx] = template_data
        else:
            data["templates"].append(template_data)
        
        self._save_data(data)
    
    def get_templates(self):
        """Get all templates"""
        data = self._load_data()
        return data.get("templates", [])