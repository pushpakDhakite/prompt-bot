"""
Advanced AI Prompt Generator - PyQt6 Desktop Application
Modern GUI for generating professional AI prompts
"""

import sys
import os
import json
import uuid
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox,
    QGroupBox, QFormLayout, QRadioButton, QButtonGroup, QCheckBox,
    QListWidget, QListWidgetItem, QFileDialog, QMessageBox,
    QProgressBar, QSpinBox, QSplitter, QScrollArea, QFrame,
    QStackedWidget, QGridLayout, QSizePolicy, QToolButton
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QAction, QPixmap, QCursor

# Import core modules
from prompt_core import (
    load_template, list_available_templates, process_csv_file, 
    process_json_file, apply_template, generate_prompt
)


class PromptEngineThread(QThread):
    """Thread for generating prompts without freezing UI"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, context, answers, style):
        super().__init__()
        self.context = context
        self.answers = answers
        self.style = style
    
    def run(self):
        try:
            result = generate_prompt(self.context, self.answers, self.style)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class InputProcessorThread(QThread):
    """Thread for processing input files"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, filepath, input_type):
        super().__init__()
        self.filepath = filepath
        self.input_type = input_type
    
    def run(self):
        try:
            if self.input_type == "csv":
                content = process_csv_file(self.filepath)
            elif self.input_type == "json":
                content = process_json_file(self.filepath)
            elif self.input_type == "pdf":
                # Use PyPDF2
                import PyPDF2
                with open(self.filepath, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    content = ""
                    for page in reader.pages:
                        content += page.extract_text() + "\n"
            else:
                # Text file
                with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            self.finished.emit(content)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window with modern dark theme"""
    
    def __init__(self):
        super().__init__()
        self.current_context = ""
        self.current_answers = {}
        self.saved_prompts = []
        self.initUI()
        self.load_settings()
        self.apply_dark_theme()
    
    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle("AI Prompt Generator Pro")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create main content with tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.setStyleSheet(self.get_tab_style())
        
        # Add tabs
        self.tab_widget.addTab(self.create_input_tab(), "Input Source")
        self.tab_widget.addTab(self.create_builder_tab(), "Prompt Builder")
        self.tab_widget.addTab(self.create_output_tab(), "Generated Prompt")
        self.tab_widget.addTab(self.create_library_tab(), "Prompt Library")
        self.tab_widget.addTab(self.create_settings_tab(), "Settings")
        
        main_layout.addWidget(self.tab_widget)
        
        # Create status bar
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("color: #a0a0a0; background-color: #1a1a2e;")
        
        # Connect signals
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
    
    def create_header(self):
        """Create application header"""
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1a2e, stop:1 #16213e);
                border-bottom: 2px solid #0f3460;
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Logo/Title
        title_label = QLabel("AI Prompt Generator Pro")
        title_label.setStyleSheet("""
            QLabel {
                color: #e94560;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # Quick actions
        new_btn = QPushButton("New Prompt")
        new_btn.setStyleSheet(self.get_button_style("#e94560"))
        new_btn.clicked.connect(self.new_prompt)
        layout.addWidget(new_btn)
        
        load_btn = QPushButton("Load File")
        load_btn.setStyleSheet(self.get_button_style("#0f3460"))
        load_btn.clicked.connect(self.load_file)
        layout.addWidget(load_btn)
        
        return header
    
    def create_input_tab(self):
        """Create input source tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Provide Input Source")
        title.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # Input type selection
        type_group = QGroupBox("Input Type")
        type_group.setStyleSheet(self.get_group_style())
        type_layout = QVBoxLayout(type_group)
        
        self.input_type_group = QButtonGroup()
        
        types = [
            ("text", "Direct Text Input"),
            ("pdf", "PDF Document"),
            ("csv", "CSV Data File"),
            ("json", "JSON Data File"),
            ("url", "Website URL"),
            ("other", "Other File (txt, md, etc.)")
        ]
        
        for i, (value, label) in enumerate(types):
            radio = QRadioButton(label)
            radio.setProperty("type", value)
            radio.setStyleSheet(self.get_radio_style())
            if i == 0:
                radio.setChecked(True)
            self.input_type_group.addButton(radio)
            type_layout.addWidget(radio)
        
        layout.addWidget(type_group)
        
        # Content area
        content_group = QGroupBox("Input Content")
        content_group.setStyleSheet(self.get_group_style())
        content_layout = QVBoxLayout(content_group)
        
        # Text input
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter your text here, or paste content from files, websites, etc.")
        self.text_input.setStyleSheet(self.get_text_edit_style())
        self.text_input.setMaximumHeight(200)
        content_layout.addWidget(self.text_input)
        
        # File selection area
        file_layout = QHBoxLayout()
        
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setStyleSheet("color: #a0a0a0;")
        file_layout.addWidget(self.file_path_label)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.setStyleSheet(self.get_button_style("#0f3460"))
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        content_layout.addLayout(file_layout)
        
        layout.addWidget(content_group)
        
        # Context display
        context_group = QGroupBox("Extracted Context")
        context_group.setStyleSheet(self.get_group_style())
        context_layout = QVBoxLayout(context_group)
        
        self.context_display = QTextEdit()
        self.context_display.setReadOnly(True)
        self.context_display.setPlaceholderText("Context will be extracted here from your input...")
        self.context_display.setStyleSheet(self.get_text_edit_style())
        self.context_display.setMaximumHeight(150)
        context_layout.addWidget(self.context_display)
        
        # Process button
        process_btn = QPushButton("Process Input")
        process_btn.setStyleSheet(self.get_button_style("#e94560"))
        process_btn.clicked.connect(self.process_input)
        context_layout.addWidget(process_btn)
        
        layout.addWidget(context_group)
        
        layout.addStretch()
        
        # Next button
        next_btn = QPushButton("Next: Build Prompt →")
        next_btn.setStyleSheet(self.get_button_style("#0f3460"))
        next_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(1))
        layout.addWidget(next_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        return widget
    
    def create_builder_tab(self):
        """Create prompt builder wizard tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Prompt Builder")
        title.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # Scroll area for questions
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #1a1a2e;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #0f3460;
                min-height: 30px;
                border-radius: 5px;
            }
        """)
        
        questions_widget = QWidget()
        questions_layout = QVBoxLayout(questions_widget)
        questions_layout.setSpacing(20)
        
        # Core questions
        core_group = QGroupBox("Core Requirements")
        core_group.setStyleSheet(self.get_group_style())
        core_layout = QFormLayout(core_group)
        core_layout.setSpacing(15)
        
        # Goal
        self.goal_combo = QComboBox()
        self.goal_combo.addItems([
            "Generate creative content",
            "Analyze or explain something",
            "Write code or technical content",
            "Summarize or extract information",
            "Translate or convert content",
            "Get recommendations or advice",
            "Create marketing content",
            "Research and explore topics"
        ])
        self.goal_combo.setStyleSheet(self.get_combo_style())
        core_layout.addRow("What is your goal?", self.goal_combo)
        
        # AI Tool
        self.ai_tool_combo = QComboBox()
        self.ai_tool_combo.addItems([
            "ChatGPT",
            "Claude",
            "Gemini",
            "Midjourney",
            "DALL-E",
            "GitHub Copilot",
            "Other AI"
        ])
        self.ai_tool_combo.setStyleSheet(self.get_combo_style())
        core_layout.addRow("Which AI tool will you use?", self.ai_tool_combo)
        
        # Output type
        self.output_combo = QComboBox()
        self.output_combo.addItems([
            "Article or blog post",
            "Code or script",
            "Report or analysis",
            "Creative story",
            "Email or message",
            "List or bullet points",
            "Step-by-step guide",
            "Q&A format"
        ])
        self.output_combo.setStyleSheet(self.get_combo_style())
        core_layout.addRow("What type of output?", self.output_combo)
        
        questions_layout.addWidget(core_group)
        
        # Style and Tone
        style_group = QGroupBox("Style & Tone")
        style_group.setStyleSheet(self.get_group_style())
        style_layout = QFormLayout(style_group)
        style_layout.setSpacing(15)
        
        # Tone
        self.tone_combo = QComboBox()
        self.tone_combo.addItems([
            "Professional",
            "Casual and friendly",
            "Formal and academic",
            "Creative and engaging",
            "Technical and precise",
            "Persuasive",
            "Neutral and objective"
        ])
        self.tone_combo.setStyleSheet(self.get_combo_style())
        style_layout.addRow("What tone should it have?", self.tone_combo)
        
        # Prompt style
        self.prompt_style_combo = QComboBox()
        self.prompt_style_combo.addItems([
            "creative",
            "technical",
            "coding",
            "marketing",
            "academic",
            "general"
        ])
        self.prompt_style_combo.setStyleSheet(self.get_combo_style())
        style_layout.addRow("Prompt style template:", self.prompt_style_combo)
        
        questions_layout.addWidget(style_group)
        
        # Audience and Length
        audience_group = QGroupBox("Audience & Detail Level")
        audience_group.setStyleSheet(self.get_group_style())
        audience_layout = QFormLayout(audience_group)
        audience_layout.setSpacing(15)
        
        # Audience
        self.audience_input = QLineEdit()
        self.audience_input.setPlaceholderText("e.g., Business professionals, Students, General public")
        self.audience_input.setStyleSheet(self.get_input_style())
        audience_layout.addRow("Target audience:", self.audience_input)
        
        # Length
        self.length_combo = QComboBox()
        self.length_combo.addItems([
            "Brief (1-2 paragraphs)",
            "Moderate (3-5 paragraphs)",
            "Detailed (full article)",
            "Comprehensive (in-depth guide)"
        ])
        self.length_combo.setStyleSheet(self.get_combo_style())
        audience_layout.addRow("Response detail level:", self.length_combo)
        
        questions_layout.addWidget(audience_group)
        
        # Advanced Options
        advanced_group = QGroupBox("Advanced Options")
        advanced_group.setStyleSheet(self.get_group_style())
        advanced_layout = QVBoxLayout(advanced_group)
        advanced_layout.setSpacing(10)
        
        self.include_examples_check = QCheckBox("Include examples in the prompt")
        self.include_examples_check.setStyleSheet(self.get_check_style())
        advanced_layout.addWidget(self.include_examples_check)
        
        self.step_by_step_check = QCheckBox("Request step-by-step explanations")
        self.step_by_step_check.setStyleSheet(self.get_check_style())
        advanced_layout.addWidget(self.step_by_step_check)
        
        # Constraints
        constraints_label = QLabel("Additional constraints or requirements:")
        constraints_label.setStyleSheet("color: #a0a0a0;")
        advanced_layout.addWidget(constraints_label)
        
        self.constraints_input = QTextEdit()
        self.constraints_input.setPlaceholderText("e.g., Use simple language, Include statistics, Avoid jargon")
        self.constraints_input.setStyleSheet(self.get_text_edit_style())
        self.constraints_input.setMaximumHeight(100)
        advanced_layout.addWidget(self.constraints_input)
        
        # Format requirements
        format_label = QLabel("Format requirements:")
        format_label.setStyleSheet("color: #a0a0a0;")
        advanced_layout.addWidget(format_label)
        
        self.format_input = QTextEdit()
        self.format_input.setPlaceholderText("e.g., Use markdown headers, Include code blocks, Add bullet points")
        self.format_input.setStyleSheet(self.get_text_edit_style())
        self.format_input.setMaximumHeight(100)
        advanced_layout.addWidget(self.format_input)
        
        questions_layout.addWidget(advanced_group)
        
        scroll.setWidget(questions_widget)
        layout.addWidget(scroll)
        
        # Generate button
        generate_btn = QPushButton("Generate Prompt")
        generate_btn.setStyleSheet(self.get_button_style("#e94560"))
        generate_btn.setFixedHeight(50)
        generate_btn.clicked.connect(self.generate_prompt)
        layout.addWidget(generate_btn)
        
        return widget
    
    def create_output_tab(self):
        """Create output tab for generated prompts"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title and quality score
        header_layout = QHBoxLayout()
        
        title = QLabel("Generated Prompt")
        title.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: bold;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.quality_label = QLabel("Quality Score: --")
        self.quality_label.setStyleSheet("""
            QLabel {
                color: #4ade80;
                font-size: 16px;
                font-weight: bold;
                padding: 5px 15px;
                background-color: #1a1a2e;
                border-radius: 5px;
            }
        """)
        header_layout.addWidget(self.quality_label)
        
        layout.addLayout(header_layout)
        
        # Techniques used
        self.techniques_label = QLabel("Techniques used: --")
        self.techniques_label.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        layout.addWidget(self.techniques_label)
        
        # Prompt display
        self.prompt_output = QTextEdit()
        self.prompt_output.setPlaceholderText("Your generated prompt will appear here...")
        self.prompt_output.setStyleSheet(self.get_text_edit_style())
        layout.addWidget(self.prompt_output)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        copy_btn = QPushButton("Copy to Clipboard")
        copy_btn.setStyleSheet(self.get_button_style("#0f3460"))
        copy_btn.clicked.connect(self.copy_prompt)
        button_layout.addWidget(copy_btn)
        
        improve_btn = QPushButton("Improve Prompt")
        improve_btn.setStyleSheet(self.get_button_style("#0f3460"))
        improve_btn.clicked.connect(self.improve_prompt)
        button_layout.addWidget(improve_btn)
        
        regenerate_btn = QPushButton("Regenerate")
        regenerate_btn.setStyleSheet(self.get_button_style("#e94560"))
        regenerate_btn.clicked.connect(self.generate_prompt)
        button_layout.addWidget(regenerate_btn)
        
        layout.addLayout(button_layout)
        
        # Export options
        export_group = QGroupBox("Export Options")
        export_group.setStyleSheet(self.get_group_style())
        export_layout = QHBoxLayout(export_group)
        
        export_txt_btn = QPushButton("Export as TXT")
        export_txt_btn.setStyleSheet(self.get_button_style("#16213e"))
        export_txt_btn.clicked.connect(lambda: self.export_prompt("txt"))
        export_layout.addWidget(export_txt_btn)
        
        export_md_btn = QPushButton("Export as Markdown")
        export_md_btn.setStyleSheet(self.get_button_style("#16213e"))
        export_md_btn.clicked.connect(lambda: self.export_prompt("md"))
        export_layout.addWidget(export_md_btn)
        
        export_json_btn = QPushButton("Export as JSON")
        export_json_btn.setStyleSheet(self.get_button_style("#16213e"))
        export_json_btn.clicked.connect(lambda: self.export_prompt("json"))
        export_layout.addWidget(export_json_btn)
        
        save_btn = QPushButton("Save to Library")
        save_btn.setStyleSheet(self.get_button_style("#4ade80"))
        save_btn.clicked.connect(self.save_to_library)
        export_layout.addWidget(save_btn)
        
        layout.addWidget(export_group)
        
        return widget
    
    def create_library_tab(self):
        """Create prompt library tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Prompt Library")
        title.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # Search and filter
        filter_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search prompts...")
        self.search_input.setStyleSheet(self.get_input_style())
        self.search_input.textChanged.connect(self.filter_prompts)
        filter_layout.addWidget(self.search_input)
        
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "All Categories",
            "Creative",
            "Technical",
            "Marketing",
            "Academic",
            "General"
        ])
        self.category_combo.setStyleSheet(self.get_combo_style())
        self.category_combo.currentTextChanged.connect(self.filter_prompts)
        filter_layout.addWidget(self.category_combo)
        
        layout.addLayout(filter_layout)
        
        # Prompts list
        self.prompts_list = QListWidget()
        self.prompts_list.setStyleSheet("""
            QListWidget {
                background-color: #1a1a2e;
                border: 2px solid #0f3460;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 15px;
                border-bottom: 1px solid #0f3460;
            }
            QListWidget::item:selected {
                background-color: #e94560;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #16213e;
            }
        """)
        self.prompts_list.itemClicked.connect(self.load_prompt_from_library)
        layout.addWidget(self.prompts_list)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        load_btn = QPushButton("Load Selected")
        load_btn.setStyleSheet(self.get_button_style("#0f3460"))
        load_btn.clicked.connect(self.load_selected_prompt)
        action_layout.addWidget(load_btn)
        
        delete_btn = QPushButton("Delete Selected")
        delete_btn.setStyleSheet(self.get_button_style("#e94560"))
        delete_btn.clicked.connect(self.delete_selected_prompt)
        action_layout.addWidget(delete_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet(self.get_button_style("#16213e"))
        refresh_btn.clicked.connect(self.refresh_library)
        action_layout.addWidget(refresh_btn)
        
        layout.addLayout(action_layout)
        
        # Stats
        self.stats_label = QLabel("Library Stats: Loading...")
        self.stats_label.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        layout.addWidget(self.stats_label)
        
        return widget
    
    def create_settings_tab(self):
        """Create settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Settings")
        title.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # General settings
        general_group = QGroupBox("General Settings")
        general_group.setStyleSheet(self.get_group_style())
        general_layout = QFormLayout(general_group)
        general_layout.setSpacing(15)
        
        # Default AI tool
        self.default_ai_combo = QComboBox()
        self.default_ai_combo.addItems(["ChatGPT", "Claude", "Gemini", "Other"])
        self.default_ai_combo.setStyleSheet(self.get_combo_style())
        general_layout.addRow("Default AI Tool:", self.default_ai_combo)
        
        # Default style
        self.default_style_combo = QComboBox()
        self.default_style_combo.addItems(["creative", "technical", "coding", "marketing", "academic", "general"])
        self.default_style_combo.setStyleSheet(self.get_combo_style())
        general_layout.addRow("Default Prompt Style:", self.default_style_combo)
        
        # Auto-save
        self.autosave_check = QCheckBox("Auto-save generated prompts")
        self.autosave_check.setChecked(True)
        self.autosave_check.setStyleSheet(self.get_check_style())
        general_layout.addRow("", self.autosave_check)
        
        layout.addWidget(general_group)
        
        # Template management
        template_group = QGroupBox("Template Management")
        template_group.setStyleSheet(self.get_group_style())
        template_layout = QVBoxLayout(template_group)
        
        template_info = QLabel("Manage your prompt templates for quick generation.")
        template_info.setStyleSheet("color: #a0a0a0;")
        template_layout.addWidget(template_info)
        
        # Templates list
        self.templates_list = QListWidget()
        self.templates_list.setMaximumHeight(200)
        self.templates_list.setStyleSheet("""
            QListWidget {
                background-color: #1a1a2e;
                border: 2px solid #0f3460;
                border-radius: 8px;
                color: #ffffff;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #0f3460;
            }
        """)
        template_layout.addWidget(self.templates_list)
        
        template_btn_layout = QHBoxLayout()
        
        refresh_templates_btn = QPushButton("Refresh Templates")
        refresh_templates_btn.setStyleSheet(self.get_button_style("#0f3460"))
        refresh_templates_btn.clicked.connect(self.refresh_templates)
        template_btn_layout.addWidget(refresh_templates_btn)
        
        template_layout.addLayout(template_btn_layout)
        
        layout.addWidget(template_group)
        
        # About
        about_group = QGroupBox("About")
        about_group.setStyleSheet(self.get_group_style())
        about_layout = QVBoxLayout(about_group)
        
        about_text = QLabel("""
        <h3>AI Prompt Generator Pro</h3>
        <p>Version 2.0</p>
        <p>A professional tool for generating high-quality AI prompts using advanced prompt engineering techniques.</p>
        <p><b>Features:</b></p>
        <ul>
            <li>Multiple input sources (text, PDF, CSV, JSON)</li>
            <li>Interactive prompt builder</li>
            <li>Advanced prompt engineering techniques</li>
            <li>Prompt library and management</li>
            <li>Export in multiple formats</li>
        </ul>
        """)
        about_text.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        about_text.setWordWrap(True)
        about_layout.addWidget(about_text)
        
        layout.addWidget(about_group)
        
        layout.addStretch()
        
        return widget
    
    # Style methods
    def get_button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
            QPushButton:pressed {{
                background-color: {color}99;
            }}
        """
    
    def get_group_style(self):
        return """
            QGroupBox {
                background-color: #1a1a2e;
                border: 2px solid #0f3460;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }
        """
    
    def get_input_style(self):
        return """
            QLineEdit {
                background-color: #16213e;
                border: 2px solid #0f3460;
                border-radius: 8px;
                padding: 10px;
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #e94560;
            }
        """
    
    def get_text_edit_style(self):
        return """
            QTextEdit {
                background-color: #16213e;
                border: 2px solid #0f3460;
                border-radius: 8px;
                padding: 10px;
                color: #ffffff;
                font-size: 14px;
            }
            QTextEdit:focus {
                border-color: #e94560;
            }
        """
    
    def get_combo_style(self):
        return """
            QComboBox {
                background-color: #16213e;
                border: 2px solid #0f3460;
                border-radius: 8px;
                padding: 10px;
                color: #ffffff;
                font-size: 14px;
            }
            QComboBox:hover {
                border-color: #e94560;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #16213e;
                color: #ffffff;
                selection-background-color: #e94560;
            }
        """
    
    def get_radio_style(self):
        return """
            QRadioButton {
                color: #ffffff;
                font-size: 14px;
                spacing: 10px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:checked {
                background-color: #e94560;
                border: 2px solid #ffffff;
                border-radius: 9px;
            }
        """
    
    def get_check_style(self):
        return """
            QCheckBox {
                color: #ffffff;
                font-size: 14px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #0f3460;
                border-radius: 4px;
                background-color: #16213e;
            }
            QCheckBox::indicator:checked {
                background-color: #e94560;
                border-color: #e94560;
            }
        """
    
    def get_tab_style(self):
        return """
            QTabWidget::pane {
                border: none;
                background-color: #0f0f23;
            }
            QTabBar::tab {
                background-color: #1a1a2e;
                color: #a0a0a0;
                padding: 15px 25px;
                margin-right: 5px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #e94560;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #16213e;
                color: #ffffff;
            }
        """
    
    def apply_dark_theme(self):
        """Apply dark theme to the application"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(15, 15, 35))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(22, 33, 62))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(26, 26, 46))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(15, 52, 96))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Link, QColor(233, 69, 96))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(233, 69, 96))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        QApplication.setPalette(palette)
    
    # Action methods
    def on_tab_changed(self, index):
        """Handle tab change"""
        if index == 2:  # Output tab
            if not self.prompt_output.toPlainText():
                self.statusBar().showMessage("No prompt generated yet. Go to Prompt Builder tab to create one.")
        elif index == 3:  # Library tab
            self.refresh_library()
    
    def browse_file(self):
        """Open file browser dialog"""
        file_filter = "All Files (*);;PDF Files (*.pdf);;CSV Files (*.csv);;JSON Files (*.json);;Text Files (*.txt);;Markdown Files (*.md)"
        filepath, _ = QFileDialog.getOpenFileName(self, "Select Input File", "", file_filter)
        
        if filepath:
            self.file_path_label.setText(filepath)
            # Detect file type
            ext = os.path.splitext(filepath)[1].lower()
            type_map = {
                '.pdf': 'pdf',
                '.csv': 'csv',
                '.json': 'json',
                '.txt': 'text',
                '.md': 'text'
            }
            input_type = type_map.get(ext, 'text')
            
            # Select corresponding radio button
            for button in self.input_type_group.buttons():
                if button.property("type") == input_type:
                    button.setChecked(True)
                    break
    
    def load_file(self):
        """Load file action from header"""
        self.browse_file()
    
    def process_input(self):
        """Process the selected input"""
        selected_button = self.input_type_group.checkedButton()
        if not selected_button:
            QMessageBox.warning(self, "Warning", "Please select an input type.")
            return
        
        input_type = selected_button.property("type")
        
        if input_type == "text":
            self.current_context = self.text_input.toPlainText()
            self.context_display.setPlainText(self.current_context)
            self.statusBar().showMessage("Text input processed successfully")
        
        elif input_type == "url":
            # Simple URL handling
            url = self.text_input.toPlainText()
            if url.startswith("http"):
                self.current_context = f"Content from URL: {url}\n\n[URL content would be extracted here in production]"
                self.context_display.setPlainText(self.current_context)
                self.statusBar().showMessage("URL processed (simulated)")
            else:
                QMessageBox.warning(self, "Warning", "Please enter a valid URL starting with http:// or https://")
        
        else:
            # File processing
            filepath = self.file_path_label.text()
            if not filepath or filepath == "No file selected":
                QMessageBox.warning(self, "Warning", "Please select a file first.")
                return
            
            # Start processing in thread
            self.statusBar().showMessage(f"Processing {input_type.upper()} file...")
            self.processor_thread = InputProcessorThread(filepath, input_type)
            self.processor_thread.finished.connect(self.on_input_processed)
            self.processor_thread.error.connect(self.on_input_error)
            self.processor_thread.start()
    
    def on_input_processed(self, content):
        """Handle successful input processing"""
        self.current_context = content
        self.context_display.setPlainText(content[:2000] + "..." if len(content) > 2000 else content)
        self.statusBar().showMessage("Input processed successfully")
    
    def on_input_error(self, error):
        """Handle input processing error"""
        QMessageBox.critical(self, "Error", f"Failed to process input: {error}")
        self.statusBar().showMessage("Input processing failed")
    
    def generate_prompt(self):
        """Generate prompt based on current settings"""
        if not self.current_context and not self.text_input.toPlainText():
            reply = QMessageBox.question(
                self, "No Input", 
                "No input context provided. Generate prompt without context?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        # Gather answers
        answers = {
            "goal": self.goal_combo.currentText(),
            "ai_tool": self.ai_tool_combo.currentText(),
            "output_type": self.output_combo.currentText(),
            "tone": self.tone_combo.currentText(),
            "audience": self.audience_input.text(),
            "length": self.length_combo.currentText(),
            "include_examples": self.include_examples_check.isChecked(),
            "step_by_step": self.step_by_step_check.isChecked(),
            "constraints": self.constraints_input.toPlainText(),
            "format_requirements": self.format_input.toPlainText()
        }
        
        style = self.prompt_style_combo.currentText()
        context = self.current_context or self.text_input.toPlainText()
        
        # Start generation in thread
        self.statusBar().showMessage("Generating prompt...")
        self.generator_thread = PromptEngineThread(context, answers, style)
        self.generator_thread.finished.connect(self.on_prompt_generated)
        self.generator_thread.error.connect(self.on_generation_error)
        self.generator_thread.start()
    
    def on_prompt_generated(self, result):
        """Handle successful prompt generation"""
        self.prompt_output.setPlainText(result["prompt"])
        self.quality_label.setText(f"Quality Score: {result.get('quality_score', 0)}%")
        
        techniques = result.get("techniques_used", [])
        if techniques:
            self.techniques_label.setText(f"Techniques used: {', '.join(techniques)}")
        
        # Switch to output tab
        self.tab_widget.setCurrentIndex(2)
        self.statusBar().showMessage("Prompt generated successfully")
    
    def on_generation_error(self, error):
        """Handle prompt generation error"""
        QMessageBox.critical(self, "Error", f"Failed to generate prompt: {error}")
        self.statusBar().showMessage("Prompt generation failed")
    
    def copy_prompt(self):
        """Copy prompt to clipboard"""
        prompt = self.prompt_output.toPlainText()
        if prompt:
            clipboard = QApplication.clipboard()
            clipboard.setText(prompt)
            self.statusBar().showMessage("Prompt copied to clipboard")
        else:
            QMessageBox.warning(self, "Warning", "No prompt to copy.")
    
    def improve_prompt(self):
        """Improve the current prompt"""
        current_prompt = self.prompt_output.toPlainText()
        if not current_prompt:
            QMessageBox.warning(self, "Warning", "No prompt to improve.")
            return
        
        # Simple improvement by adding common enhancements
        improved = current_prompt
        
        if "# Role" not in improved:
            improved = "# Role\nYou are an expert assistant.\n\n" + improved
        
        if "step-by-step" not in improved.lower():
            improved += "\n\nThink step-by-step before providing your answer."
        
        if "# Constraints" not in improved:
            improved += "\n\n# Constraints\n- Be accurate and factual\n- Avoid unnecessary repetition"
        
        self.prompt_output.setPlainText(improved)
        self.statusBar().showMessage("Prompt improved")
    
    def export_prompt(self, format_type):
        """Export prompt to file"""
        prompt = self.prompt_output.toPlainText()
        if not prompt:
            QMessageBox.warning(self, "Warning", "No prompt to export.")
            return
        
        default_name = f"generated_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if format_type == "txt":
            filepath, _ = QFileDialog.getSaveFileName(self, "Save as Text", f"{default_name}.txt", "Text Files (*.txt)")
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(prompt)
        
        elif format_type == "md":
            filepath, _ = QFileDialog.getSaveFileName(self, "Save as Markdown", f"{default_name}.md", "Markdown Files (*.md)")
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# Generated Prompt\n\n{prompt}")
        
        elif format_type == "json":
            filepath, _ = QFileDialog.getSaveFileName(self, "Save as JSON", f"{default_name}.json", "JSON Files (*.json)")
            if filepath:
                data = {
                    "prompt": prompt,
                    "generated_at": datetime.now().isoformat(),
                    "context": self.current_context[:500] if self.current_context else ""
                }
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
        
        if filepath:
            self.statusBar().showMessage(f"Prompt exported to {filepath}")
    
    def save_to_library(self):
        """Save current prompt to library"""
        prompt = self.prompt_output.toPlainText()
        if not prompt:
            QMessageBox.warning(self, "Warning", "No prompt to save.")
            return
        
        # Get title from user
        title, ok = QInputDialog.getText(self, "Save Prompt", "Enter a title for this prompt:", text="My Prompt")
        if not ok or not title:
            return
        
        # Create prompt data
        prompt_data = {
            "id": str(uuid.uuid4()),
            "title": title,
            "prompt": prompt,
            "context": self.current_context[:500] if self.current_context else "",
            "style": self.prompt_style_combo.currentText(),
            "category": self.prompt_style_combo.currentText(),
            "tags": [],
            "created_at": datetime.now().isoformat(),
            "quality_score": int(self.quality_label.text().replace("Quality Score: ", "").replace("%", "") or 0),
            "usage_count": 0
        }
        
        # Save to file
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        prompts_file = data_dir / "prompts.json"
        prompts = []
        if prompts_file.exists():
            try:
                with open(prompts_file, 'r', encoding='utf-8') as f:
                    prompts = json.load(f)
            except:
                prompts = []
        
        prompts.append(prompt_data)
        
        with open(prompts_file, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, indent=2)
        
        self.statusBar().showMessage(f"Prompt saved to library: {title}")
        self.refresh_library()
    
    def refresh_library(self):
        """Refresh the prompts library list"""
        self.prompts_list.clear()
        
        data_dir = Path("data")
        prompts_file = data_dir / "prompts.json"
        
        if not prompts_file.exists():
            self.stats_label.setText("Library Stats: No prompts saved yet")
            return
        
        try:
            with open(prompts_file, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
        except:
            prompts = []
        
        # Filter based on search and category
        search_text = self.search_input.text().lower()
        category = self.category_combo.currentText()
        
        filtered = []
        for p in prompts:
            # Category filter
            if category != "All Categories" and p.get("category", "").lower() != category.lower():
                continue
            
            # Search filter
            if search_text and search_text not in p.get("title", "").lower() and search_text not in p.get("prompt", "").lower():
                continue
            
            filtered.append(p)
        
        # Add to list
        for prompt in filtered:
            item = QListWidgetItem()
            item.setText(f"{prompt['title']} ({prompt['created_at'][:10]})")
            item.setData(Qt.ItemDataRole.UserRole, prompt)
            self.prompts_list.addItem(item)
        
        self.stats_label.setText(f"Library Stats: {len(filtered)} prompts shown (of {len(prompts)} total)")
    
    def filter_prompts(self):
        """Filter prompts based on search and category"""
        self.refresh_library()
    
    def load_prompt_from_library(self, item):
        """Handle prompt selection from library"""
        pass  # Will be called on double-click or selection
    
    def load_selected_prompt(self):
        """Load selected prompt from library"""
        selected = self.prompts_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select a prompt from the list.")
            return
        
        prompt_data = selected.data(Qt.ItemDataRole.UserRole)
        self.prompt_output.setPlainText(prompt_data["prompt"])
        
        # Update quality score
        if "quality_score" in prompt_data:
            self.quality_label.setText(f"Quality Score: {prompt_data['quality_score']}%")
        
        # Switch to output tab
        self.tab_widget.setCurrentIndex(2)
        self.statusBar().showMessage(f"Loaded prompt: {prompt_data['title']}")
    
    def delete_selected_prompt(self):
        """Delete selected prompt from library"""
        selected = self.prompts_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select a prompt to delete.")
            return
        
        prompt_data = selected.data(Qt.ItemDataRole.UserRole)
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{prompt_data['title']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Load prompts
            data_dir = Path("data")
            prompts_file = data_dir / "prompts.json"
            
            if prompts_file.exists():
                try:
                    with open(prompts_file, 'r', encoding='utf-8') as f:
                        prompts = json.load(f)
                    
                    # Remove the prompt
                    prompts = [p for p in prompts if p.get("id") != prompt_data.get("id")]
                    
                    # Save back
                    with open(prompts_file, 'w', encoding='utf-8') as f:
                        json.dump(prompts, f, indent=2)
                    
                    self.statusBar().showMessage(f"Deleted prompt: {prompt_data['title']}")
                    self.refresh_library()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to delete prompt: {str(e)}")
    
    def refresh_templates(self):
        """Refresh available templates"""
        self.templates_list.clear()
        templates = list_available_templates()
        for template in templates:
            self.templates_list.addItem(template)
    
    def new_prompt(self):
        """Start a new prompt"""
        self.text_input.clear()
        self.context_display.clear()
        self.prompt_output.clear()
        self.current_context = ""
        self.file_path_label.setText("No file selected")
        self.quality_label.setText("Quality Score: --")
        self.techniques_label.setText("Techniques used: --")
        self.tab_widget.setCurrentIndex(0)
        self.statusBar().showMessage("Ready for new prompt")
    
    def load_settings(self):
        """Load application settings"""
        # Initialize defaults
        self.refresh_templates()
        self.refresh_library()
    
    def save_settings(self):
        """Save application settings"""
        pass  # Implement settings persistence if needed


# Import QInputDialog
from PyQt6.QtWidgets import QInputDialog


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better cross-platform look
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()