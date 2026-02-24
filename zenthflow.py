

"""
ZenithFlow IDE 
"""

import sys
import os
import subprocess
import threading
import time
import re
from pathlib import Path
from typing import Optional, List

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QTreeView, QSplitter, QTabWidget, QToolBar,
    QStatusBar, QLabel, QPushButton, QLineEdit, QDialog,
    QFileDialog, QInputDialog, QMessageBox, QMenu, QMenuBar,
    QPlainTextEdit, QCompleter, QCheckBox, QDialogButtonBox,
    QFrame, QScrollArea, QListWidget, QListWidgetItem, QGroupBox,
    QSpinBox, QComboBox, QSplashScreen
)
from PyQt6.QtGui import (
    QAction, QFont, QColor, QPalette, QSyntaxHighlighter,
    QTextCharFormat, QTextCursor, QKeySequence, QPainter,
    QPixmap, QShortcut, QTextFormat, QFileSystemModel
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QSettings, QSize, QPoint,
    QPropertyAnimation, QEasingCurve, QRegularExpression,
    QDateTime, QModelIndex
)



class ThemeManager:
  
    
    DARK_THEME = {
        'bg': '#1e1e2e',
        'bg_light': '#2d2d3a',
        'fg': '#cdd6f4',
        'primary': '#89b4fa',
        'secondary': '#cba6f7',
        'success': '#a6e3a1',
        'error': '#f38ba8',
        'border': '#45475a',
        'line_bg': '#313244',
        'syntax': {
            'keyword': '#cba6f7',
            'string': '#a6e3a1',
            'comment': '#6c7086',
            'function': '#89b4fa',
            'number': '#fab387',
            'operator': '#89dceb'
        }
    }
    
    def __init__(self):
        self.theme = self.DARK_THEME
        
    def apply_theme(self, app):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(self.theme['bg']))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(self.theme['fg']))
        palette.setColor(QPalette.ColorRole.Base, QColor(self.theme['bg_light']))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(self.theme['bg']))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(self.theme['bg']))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(self.theme['fg']))
        palette.setColor(QPalette.ColorRole.Text, QColor(self.theme['fg']))
        palette.setColor(QPalette.ColorRole.Button, QColor(self.theme['bg_light']))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(self.theme['fg']))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(self.theme['fg']))
        palette.setColor(QPalette.ColorRole.Link, QColor(self.theme['primary']))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(self.theme['primary']))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(self.theme['bg']))
        app.setPalette(palette)
        
        app.setStyleSheet(f"""
            QMainWindow, QDialog {{
                background: {self.theme['bg']};
            }}
            QMenuBar {{
                background: {self.theme['bg_light']};
                color: {self.theme['fg']};
                border-bottom: 1px solid {self.theme['border']};
            }}
            QMenuBar::item:selected {{
                background: {self.theme['line_bg']};
            }}
            QMenu {{
                background: {self.theme['bg_light']};
                color: {self.theme['fg']};
                border: 1px solid {self.theme['border']};
                border-radius: 4px;
                padding: 5px;
            }}
            QMenu::item:selected {{
                background: {self.theme['line_bg']};
            }}
            QToolBar {{
                background: {self.theme['bg_light']};
                border: none;
                spacing: 5px;
                padding: 5px;
            }}
            QToolButton {{
                background: transparent;
                color: {self.theme['fg']};
                border: none;
                border-radius: 4px;
                padding: 5px;
                min-width: 30px;
                min-height: 30px;
            }}
            QToolButton:hover {{
                background: {self.theme['line_bg']};
            }}
            QStatusBar {{
                background: {self.theme['bg_light']};
                color: {self.theme['fg']};
                border-top: 1px solid {self.theme['border']};
            }}
            QTabWidget::pane {{
                background: {self.theme['bg']};
                border: 1px solid {self.theme['border']};
                border-radius: 4px;
            }}
            QTabBar::tab {{
                background: {self.theme['bg_light']};
                color: {self.theme['fg']};
                border: 1px solid {self.theme['border']};
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 15px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background: {self.theme['bg']};
                border-bottom: 2px solid {self.theme['primary']};
            }}
            QTabBar::tab:hover:!selected {{
                background: {self.theme['line_bg']};
            }}
            QScrollBar:vertical {{
                background: {self.theme['bg']};
                width: 14px;
                border-radius: 7px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.theme['border']};
                min-height: 20px;
                border-radius: 7px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {self.theme['primary']};
            }}
            QScrollBar:horizontal {{
                background: {self.theme['bg']};
                height: 14px;
                border-radius: 7px;
            }}
            QScrollBar::handle:horizontal {{
                background: {self.theme['border']};
                min-width: 20px;
                border-radius: 7px;
                margin: 2px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {self.theme['primary']};
            }}
            QLineEdit, QTextEdit, QPlainTextEdit {{
                background: {self.theme['bg_light']};
                color: {self.theme['fg']};
                border: 1px solid {self.theme['border']};
                border-radius: 4px;
                padding: 5px;
                selection-background-color: {self.theme['primary']};
                selection-color: {self.theme['bg']};
            }}
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
                border-color: {self.theme['primary']};
            }}
            QTreeView {{
                background: {self.theme['bg_light']};
                color: {self.theme['fg']};
                border: 1px solid {self.theme['border']};
                border-radius: 4px;
                outline: none;
            }}
            QTreeView::item:selected {{
                background: {self.theme['line_bg']};
                color: {self.theme['primary']};
            }}
            QTreeView::item:hover {{
                background: {self.theme['line_bg']};
            }}
            QHeaderView::section {{
                background: {self.theme['bg']};
                color: {self.theme['fg']};
                border: 1px solid {self.theme['border']};
                padding: 5px;
            }}
            QPushButton {{
                background: {self.theme['bg_light']};
                color: {self.theme['fg']};
                border: 1px solid {self.theme['border']};
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background: {self.theme['line_bg']};
                border-color: {self.theme['primary']};
            }}
            QPushButton:pressed {{
                background: {self.theme['primary']};
                color: {self.theme['bg']};
            }}
            QSplitter::handle {{
                background: {self.theme['border']};
            }}
            QSplitter::handle:hover {{
                background: {self.theme['primary']};
            }}
            QProgressBar {{
                background: {self.theme['bg_light']};
                border: 1px solid {self.theme['border']};
                border-radius: 3px;
                text-align: center;
                color: {self.theme['fg']};
            }}
            QProgressBar::chunk {{
                background: {self.theme['primary']};
                border-radius: 3px;
            }}
            QCheckBox {{
                color: {self.theme['fg']};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 1px solid {self.theme['border']};
                border-radius: 3px;
            }}
            QCheckBox::indicator:checked {{
                background: {self.theme['primary']};
            }}
            QRadioButton {{
                color: {self.theme['fg']};
            }}
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                border: 1px solid {self.theme['border']};
                border-radius: 9px;
            }}
            QRadioButton::indicator:checked {{
                background: {self.theme['primary']};
            }}
            QComboBox {{
                background: {self.theme['bg_light']};
                color: {self.theme['fg']};
                border: 1px solid {self.theme['border']};
                border-radius: 4px;
                padding: 5px;
            }}
            QComboBox:hover {{
                border-color: {self.theme['primary']};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QSpinBox {{
                background: {self.theme['bg_light']};
                color: {self.theme['fg']};
                border: 1px solid {self.theme['border']};
                border-radius: 4px;
                padding: 5px;
            }}
            QSpinBox:hover {{
                border-color: {self.theme['primary']};
            }}
            QGroupBox {{
                color: {self.theme['fg']};
                border: 1px solid {self.theme['border']};
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QDialogButtonBox QPushButton {{
                min-width: 80px;
            }}
            QToolTip {{
                background: {self.theme['bg_light']};
                color: {self.theme['fg']};
                border: 1px solid {self.theme['border']};
                border-radius: 4px;
                padding: 5px;
            }}
        """)




class PythonHighlighter(QSyntaxHighlighter):
  
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = ThemeManager().theme['syntax']
        self.rules = []
        self.setup_rules()
        
    def setup_rules(self):

        keywords = [
            'and', 'or', 'not', 'if', 'elif', 'else', 'for', 'while',
            'break', 'continue', 'pass', 'return', 'def', 'class',
            'import', 'from', 'as', 'with', 'try', 'except', 'finally',
            'raise', 'assert', 'lambda', 'yield', 'None', 'True', 'False',
            'async', 'await', 'nonlocal', 'global', 'del', 'in', 'is'
        ]
        
        keyword_fmt = QTextCharFormat()
        keyword_fmt.setForeground(QColor(self.theme['keyword']))
        keyword_fmt.setFontWeight(QFont.Weight.Bold)
        
        for word in keywords:
            pattern = rf'\b{word}\b'
            self.rules.append((re.compile(pattern), keyword_fmt))
        
      
        string_fmt = QTextCharFormat()
        string_fmt.setForeground(QColor(self.theme['string']))
        self.rules.extend([
            (re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), string_fmt),
            (re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), string_fmt),
            (re.compile(r'""".*?"""', re.DOTALL), string_fmt),
            (re.compile(r"'''.*?'''", re.DOTALL), string_fmt)
        ])
        
     
        comment_fmt = QTextCharFormat()
        comment_fmt.setForeground(QColor(self.theme['comment']))
        comment_fmt.setFontItalic(True)
        self.rules.append((re.compile(r'#[^\n]*'), comment_fmt))
        
     
        number_fmt = QTextCharFormat()
        number_fmt.setForeground(QColor(self.theme['number']))
        self.rules.extend([
            (re.compile(r'\b[0-9]+\b'), number_fmt),
            (re.compile(r'\b0[xX][0-9a-fA-F]+\b'), number_fmt),
            (re.compile(r'\b0[bB][01]+\b'), number_fmt),
            (re.compile(r'\b0[oO][0-7]+\b'), number_fmt)
        ])
        
      
        func_fmt = QTextCharFormat()
        func_fmt.setForeground(QColor(self.theme['function']))
        self.rules.append((re.compile(r'\b[A-Za-z_][A-Za-z0-9_]*(?=\()'), func_fmt))
        
     
        decorator_fmt = QTextCharFormat()
        decorator_fmt.setForeground(QColor(self.theme['function']))
        self.rules.append((re.compile(r'@[A-Za-z_][A-Za-z0-9_]*'), decorator_fmt))
        
     
        op_fmt = QTextCharFormat()
        op_fmt.setForeground(QColor(self.theme['operator']))
        operators = ['+', '-', '*', '/', '%', '=', '==', '!=', '<', '>',
                    '<=', '>=', '+=', '-=', '*=', '/=', '//', '**', '&',
                    '|', '^', '~', '<<', '>>']
        for op in operators:
            self.rules.append((re.compile(re.escape(op)), op_fmt))
    
    def highlightBlock(self, text):
        for pattern, format in self.rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), format)



class PythonEditor(QPlainTextEdit):
   
    
    cursorChanged = pyqtSignal(int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = None
        self.setup_editor()
        self.setup_highlighter()
        
    def setup_editor(self):
      
        font = QFont("Courier New", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        
        
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(' '))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        
        
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        
        self.update_line_number_width()
        self.highlight_current_line()
        
       
        self.cursorPositionChanged.connect(self.emit_cursor_position)
        
    def setup_highlighter(self):
        self.highlighter = PythonHighlighter(self.document())
        
    def line_number_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 5 + self.fontMetrics().horizontalAdvance('9') * digits
        
    def update_line_number_width(self):
        self.setViewportMargins(self.line_number_width(), 0, 0, 0)
        
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), 
                                        self.line_number_area.width(), rect.height())
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            cr.left(), cr.top(), self.line_number_width(), cr.height()
        )
        
    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(ThemeManager().theme['bg']))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(ThemeManager().theme['border']))
                painter.drawText(0, int(top), 
                                self.line_number_area.width() - 5,
                                self.fontMetrics().height(),
                                Qt.AlignmentFlag.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
            
    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(ThemeManager().theme['line_bg'])
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)
        
    def emit_cursor_position(self):
        cursor = self.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.cursorChanged.emit(line, col)
        
    def load_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.setPlainText(f.read())
            self.file_path = path
            self.document().setModified(False)
            return True
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در باز کردن فایل: {str(e)}")
            return False
            
    def save_file(self, path=None):
        if path:
            self.file_path = path
        if self.file_path:
            try:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    f.write(self.toPlainText())
                self.document().setModified(False)
                return True
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ذخیره فایل: {str(e)}")
        return False

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        
    def sizeHint(self):
        return QSize(self.editor.line_number_width(), 0)
        
    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)



class PythonTerminal(QWidget):

    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_dir = os.getcwd()
        self.history = []
        self.history_index = -1
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
   
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Courier New", 10))
        layout.addWidget(self.output)
        
       
        input_layout = QHBoxLayout()
        self.prompt = QLabel(f"{self.current_dir}>")
        self.prompt.setFont(QFont("Courier New", 10))
        input_layout.addWidget(self.prompt)
        
        self.input = QLineEdit()
        self.input.setFont(QFont("Courier New", 10))
        self.input.returnPressed.connect(self.execute_command)
        input_layout.addWidget(self.input)
        
    
        clear_btn = QPushButton("🗑️")
        clear_btn.setFixedSize(30, 30)
        clear_btn.clicked.connect(self.clear_output)
        input_layout.addWidget(clear_btn)
        
        layout.addLayout(input_layout)
        self.setLayout(layout)
        

        QShortcut(QKeySequence("Ctrl+Up"), self.input, self.history_up)
        QShortcut(QKeySequence("Ctrl+Down"), self.input, self.history_down)
        
    def execute_command(self):
        cmd = self.input.text().strip()
        if not cmd:
            return
            
        self.history.append(cmd)
        self.history_index = len(self.history)
        
        self.output.appendPlainText(f"{self.current_dir}> {cmd}")
        self.input.clear()
        
        if cmd.startswith('cd '):
            self.change_dir(cmd[3:].strip())
        elif cmd == 'pwd':
            self.output.appendPlainText(self.current_dir)
        elif cmd == 'ls' or cmd == 'dir':
            self.list_files()
        elif cmd == 'clear':
            self.clear_output()
        elif cmd.startswith('python '):
            self.run_python(cmd[7:].strip())
        elif cmd == 'help':
            self.show_help()
        else:
            self.run_system(cmd)
            
    def change_dir(self, path):
        try:
            if path.startswith('~'):
                path = os.path.expanduser(path)
            new_path = os.path.abspath(os.path.join(self.current_dir, path))
            if os.path.exists(new_path) and os.path.isdir(new_path):
                self.current_dir = new_path
                self.prompt.setText(f"{self.current_dir}>")
            else:
                self.output.appendPlainText(f"دایرکتوری یافت نشد: {path}")
        except Exception as e:
            self.output.appendPlainText(f"خطا: {str(e)}")
            
    def list_files(self):
        try:
            files = os.listdir(self.current_dir)
            for f in sorted(files):
                path = os.path.join(self.current_dir, f)
                if os.path.isdir(path):
                    self.output.appendPlainText(f"📁 {f}/")
                else:
                    self.output.appendPlainText(f"📄 {f}")
        except Exception as e:
            self.output.appendPlainText(f"خطا: {str(e)}")
            
    def run_python(self, script):
        script_path = os.path.join(self.current_dir, script)
        if os.path.exists(script_path):
            self.output.appendPlainText(f"در حال اجرای {script}...")
            thread = threading.Thread(target=self._run_python_thread, args=(script_path,))
            thread.daemon = True
            thread.start()
        else:
            self.output.appendPlainText(f"فایل یافت نشد: {script}")
            
    def _run_python_thread(self, script_path):
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                cwd=self.current_dir,
                capture_output=True,
                text=True
            )
            if result.stdout:
                self.output.appendPlainText(result.stdout)
            if result.stderr:
                self.output.appendPlainText(f"خطا:\n{result.stderr}")
        except Exception as e:
            self.output.appendPlainText(f"خطا: {str(e)}")
            
    def run_system(self, cmd):
        thread = threading.Thread(target=self._run_system_thread, args=(cmd,))
        thread.daemon = True
        thread.start()
        
    def _run_system_thread(self, cmd):
        try:
            result = subprocess.run(
                cmd,
                cwd=self.current_dir,
                capture_output=True,
                text=True,
                shell=True
            )
            if result.stdout:
                self.output.appendPlainText(result.stdout)
            if result.stderr:
                self.output.appendPlainText(f"خطا:\n{result.stderr}")
        except Exception as e:
            self.output.appendPlainText(f"خطا: {str(e)}")
            
    def clear_output(self):
        self.output.clear()
        
    def show_help(self):
        help_text = """
        دستورات موجود:
        cd <path>    - تغییر دایرکتوری
        pwd          - نمایش دایرکتوری جاری
        ls/dir       - لیست فایل‌ها
        clear        - پاک کردن صفحه
        python <file>- اجرای فایل پایتون
        help         - نمایش این راهنما
        
        کلیدهای میانبر:
        Ctrl+Up      - دستور قبلی
        Ctrl+Down    - دستور بعدی
        """
        self.output.appendPlainText(help_text)
        
    def history_up(self):
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self.input.setText(self.history[self.history_index])
            
    def history_down(self):
        if self.history and self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.input.setText(self.history[self.history_index])
        else:
            self.history_index = len(self.history)
            self.input.clear()



class FileExplorer(QWidget):

    
    file_open_request = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        toolbar = QToolBar()
        refresh_btn = QPushButton("🔄")
        refresh_btn.setFixedSize(30, 30)
        refresh_btn.clicked.connect(self.refresh)
        toolbar.addWidget(refresh_btn)
        
        new_file_btn = QPushButton("📄")
        new_file_btn.setFixedSize(30, 30)
        new_file_btn.clicked.connect(self.new_file)
        toolbar.addWidget(new_file_btn)
        
        new_folder_btn = QPushButton("📁")
        new_folder_btn.setFixedSize(30, 30)
        new_folder_btn.clicked.connect(self.new_folder)
        toolbar.addWidget(new_folder_btn)
        
        layout.addWidget(toolbar)
        

        self.tree = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(os.getcwd()))
        self.tree.setHeaderHidden(True)
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        self.tree.doubleClicked.connect(self.on_double_click)
        
        layout.addWidget(self.tree)
        self.setLayout(layout)
        
    def set_root(self, path):
        self.tree.setRootIndex(self.model.index(path))
        
    def refresh(self):
        self.model.setRootPath(os.getcwd())
        
    def new_file(self):
        path, ok = QInputDialog.getText(self, "فایل جدید", "نام فایل:")
        if ok and path:
            if not path.endswith('.py'):
                path += '.py'
            full_path = os.path.join(self.model.rootPath(), path)
            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write('# -*- coding: utf-8 -*-\n\n')
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "خطا", str(e))
                
    def new_folder(self):
        name, ok = QInputDialog.getText(self, "پوشه جدید", "نام پوشه:")
        if ok and name:
            try:
                os.mkdir(os.path.join(self.model.rootPath(), name))
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "خطا", str(e))
                
    def on_double_click(self, index):
        path = self.model.filePath(index)
        if os.path.isfile(path) and path.endswith('.py'):
            self.file_open_request.emit(path)



class OutputPanel(QWidget):
   
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Courier New", 10))
        layout.addWidget(self.output)
        
        clear_btn = QPushButton("🗑️ پاک کردن")
        clear_btn.clicked.connect(self.output.clear)
        layout.addWidget(clear_btn)
        
        self.setLayout(layout)
        
    def append(self, text):
        self.output.appendPlainText(text)



class SettingsDialog(QDialog):
  
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("تنظیمات")
        self.resize(400, 300)
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        

        font_group = QGroupBox("فونت")
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("اندازه:"))
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        font_layout.addWidget(self.font_size)
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
    
        theme_group = QGroupBox("تم")
        theme_layout = QHBoxLayout()
        self.dark_theme = QCheckBox("تم تاریک")
        self.dark_theme.setChecked(True)
        theme_layout.addWidget(self.dark_theme)
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
      
        auto_group = QGroupBox("ذخیره خودکار")
        auto_layout = QHBoxLayout()
        self.auto_save = QCheckBox("فعال")
        auto_layout.addWidget(self.auto_save)
        self.auto_interval = QSpinBox()
        self.auto_interval.setRange(10, 300)
        self.auto_interval.setSuffix(" ثانیه")
        auto_layout.addWidget(self.auto_interval)
        auto_group.setLayout(auto_layout)
        layout.addWidget(auto_group)
        
      
        line_group = QGroupBox("شماره خط")
        line_layout = QHBoxLayout()
        self.show_line_numbers = QCheckBox("نمایش شماره خطوط")
        self.show_line_numbers.setChecked(True)
        line_layout.addWidget(self.show_line_numbers)
        line_group.setLayout(line_layout)
        layout.addWidget(line_group)
        
        layout.addStretch()
        
       
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_settings)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
        
    def load_settings(self):
        settings = QSettings("ZenithFlow", "IDE")
        self.font_size.setValue(settings.value("font_size", 11, type=int))
        self.dark_theme.setChecked(settings.value("dark_theme", True, type=bool))
        self.auto_save.setChecked(settings.value("auto_save", True, type=bool))
        self.auto_interval.setValue(settings.value("auto_interval", 30, type=int))
        self.show_line_numbers.setChecked(settings.value("show_line_numbers", True, type=bool))
        
    def save_settings(self):
        settings = QSettings("ZenithFlow", "IDE")
        settings.setValue("font_size", self.font_size.value())
        settings.setValue("dark_theme", self.dark_theme.isChecked())
        settings.setValue("auto_save", self.auto_save.isChecked())
        settings.setValue("auto_interval", self.auto_interval.value())
        settings.setValue("show_line_numbers", self.show_line_numbers.isChecked())
        self.accept()



class MainWindow(QMainWindow):
  
    
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        self.theme_manager.apply_theme(QApplication.instance())
        
        self.settings = QSettings("ZenithFlow", "IDE")
        self.current_file = None
        
        self.setup_window()
        self.create_menubar()
        self.setup_ui()
        self.setup_statusbar()
        self.setup_shortcuts()
        
    
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        auto_interval = self.settings.value("auto_interval", 30, type=int)
        self.auto_save_timer.start(auto_interval * 1000)
        
       
        self.show_splash()
        
    def setup_window(self):
        self.setWindowTitle("ZenithFlow IDE - Python IDE")
        self.setGeometry(100, 100, 1200, 800)
        
    def setup_ui(self):
        
        central = QWidget()
        self.setCentralWidget(central)
        
       
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
       
        self.explorer = FileExplorer()
        self.explorer.file_open_request.connect(self.open_file)
        self.explorer.setMaximumWidth(250)
        layout.addWidget(self.explorer)
        
        
        center = QWidget()
        center_layout = QVBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        
        
        toolbar = self.create_toolbar()
        center_layout.addWidget(toolbar)
        
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        center_layout.addWidget(self.tabs, 1)
        
        
        self.bottom_panel = QTabWidget()
        
        self.output = OutputPanel()
        self.bottom_panel.addTab(self.output, "📟 خروجی")
        
        self.terminal = PythonTerminal()
        self.bottom_panel.addTab(self.terminal, "💻 ترمینال")
        
        self.bottom_panel.setMaximumHeight(250)
        center_layout.addWidget(self.bottom_panel)
        
        center.setLayout(center_layout)
        layout.addWidget(center, 1)
        
        central.setLayout(layout)
        
        
        self.new_file()
        
    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(20, 20))
        
        
        new_btn = QAction("📄 جدید", self)
        new_btn.triggered.connect(self.new_file)
        toolbar.addAction(new_btn)
        
        open_btn = QAction("📂 باز", self)
        open_btn.triggered.connect(self.open_file_dialog)
        toolbar.addAction(open_btn)
        
        save_btn = QAction("💾 ذخیره", self)
        save_btn.triggered.connect(self.save_file)
        toolbar.addAction(save_btn)
        
        save_all_btn = QAction("💾 ذخیره همه", self)
        save_all_btn.triggered.connect(self.save_all_files)
        toolbar.addAction(save_all_btn)
        
        toolbar.addSeparator()
        
        
        run_btn = QAction("▶️ اجرا", self)
        run_btn.triggered.connect(self.run_file)
        toolbar.addAction(run_btn)
        
        stop_btn = QAction("⏹️ توقف", self)
        stop_btn.triggered.connect(self.stop_execution)
        toolbar.addAction(stop_btn)
        
        toolbar.addSeparator()
        
        
        settings_btn = QAction("⚙️ تنظیمات", self)
        settings_btn.triggered.connect(self.show_settings)
        toolbar.addAction(settings_btn)
        
        return toolbar
        
    def create_menubar(self):
        menubar = self.menuBar()
        
        
        file_menu = menubar.addMenu("فایل")
        
        new_action = QAction("جدید", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("باز کردن...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        
        open_folder_action = QAction("باز کردن پوشه...", self)
        open_folder_action.triggered.connect(self.open_folder_dialog)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("ذخیره", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("ذخیره با نام...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        save_all_action = QAction("ذخیره همه", self)
        save_all_action.triggered.connect(self.save_all_files)
        file_menu.addAction(save_all_action)
        
        file_menu.addSeparator()
        
        close_action = QAction("بستن", self)
        close_action.setShortcut("Ctrl+W")
        close_action.triggered.connect(self.close_current_tab)
        file_menu.addAction(close_action)
        
        exit_action = QAction("خروج", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
       
        edit_menu = menubar.addMenu("ویرایش")
        
        undo_action = QAction("واگرد", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("جلوگرد", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("برش", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("کپی", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("چسباندن", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        find_action = QAction("جستجو", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.find)
        edit_menu.addAction(find_action)
        
        replace_action = QAction("جایگزینی", self)
        replace_action.setShortcut("Ctrl+H")
        replace_action.triggered.connect(self.replace)
        edit_menu.addAction(replace_action)
        
        
        view_menu = menubar.addMenu("نمایش")
        
        toggle_explorer_action = QAction("فایل اکسپلورر", self)
        toggle_explorer_action.setShortcut("Ctrl+B")
        toggle_explorer_action.triggered.connect(self.toggle_explorer)
        view_menu.addAction(toggle_explorer_action)
        
        toggle_terminal_action = QAction("ترمینال", self)
        toggle_terminal_action.setShortcut("Ctrl+`")
        toggle_terminal_action.triggered.connect(self.toggle_terminal)
        view_menu.addAction(toggle_terminal_action)
        
        view_menu.addSeparator()
        
        zoom_in_action = QAction("بزرگنمایی +", self)
        zoom_in_action.setShortcut("Ctrl+=")
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("بزرگنمایی -", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        
        run_menu = menubar.addMenu("اجرا")
        
        run_action = QAction("اجرا", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_file)
        run_menu.addAction(run_action)
        
        stop_action = QAction("توقف", self)
        stop_action.setShortcut("Shift+F5")
        stop_action.triggered.connect(self.stop_execution)
        run_menu.addAction(stop_action)
        
        
        tools_menu = menubar.addMenu("ابزارها")
        
        settings_action = QAction("تنظیمات", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
       
        help_menu = menubar.addMenu("راهنما")
        
        about_action = QAction("درباره", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_statusbar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        
        self.position_label = QLabel("خط: 1, ستون: 1")
        self.status.addPermanentWidget(self.position_label)
        
        self.encoding_label = QLabel("UTF-8")
        self.status.addPermanentWidget(self.encoding_label)
        
        python_version = f"Python {sys.version_info.major}.{sys.version_info.minor}"
        self.version_label = QLabel(python_version)
        self.status.addPermanentWidget(self.version_label)
        
    def setup_shortcuts(self):
        
        QShortcut(QKeySequence("Ctrl+`"), self, self.toggle_terminal)
        QShortcut(QKeySequence("Ctrl+B"), self, self.toggle_explorer)
        
    def show_splash(self):
        pixmap = QPixmap(400, 200)
        pixmap.fill(QColor(ThemeManager().theme['bg']))
        
        splash = QSplashScreen(pixmap)
        splash.show()
        
        QApplication.processEvents()
        time.sleep(1)
        
        splash.close()
        
    def get_current_editor(self):
        return self.tabs.currentWidget()
        
    def new_file(self):
        editor = PythonEditor()
        editor.cursorChanged.connect(self.update_status)
        index = self.tabs.addTab(editor, "بدون نام")
        self.tabs.setCurrentIndex(index)
        
    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "باز کردن فایل", "", "Python Files (*.py);;All Files (*)"
        )
        if path:
            self.open_file(path)
            
    def open_file(self, path):
       
        for i in range(self.tabs.count()):
            editor = self.tabs.widget(i)
            if hasattr(editor, 'file_path') and editor.file_path == path:
                self.tabs.setCurrentIndex(i)
                return
                
        editor = PythonEditor()
        if editor.load_file(path):
            editor.cursorChanged.connect(self.update_status)
            self.tabs.addTab(editor, os.path.basename(path))
            self.tabs.setCurrentIndex(self.tabs.count() - 1)
            self.explorer.set_root(os.path.dirname(path))
            
    def open_folder_dialog(self):
        path = QFileDialog.getExistingDirectory(self, "باز کردن پوشه")
        if path:
            self.explorer.set_root(path)
            
    def save_file(self):
        editor = self.get_current_editor()
        if editor:
            if editor.file_path:
                if editor.save_file():
                    self.tabs.setTabText(self.tabs.currentIndex(), 
                                        os.path.basename(editor.file_path))
            else:
                self.save_file_as()
                
    def save_file_as(self):
        editor = self.get_current_editor()
        if editor:
            path, _ = QFileDialog.getSaveFileName(
                self, "ذخیره فایل", "", "Python Files (*.py)"
            )
            if path:
                if not path.endswith('.py'):
                    path += '.py'
                if editor.save_file(path):
                    self.tabs.setTabText(self.tabs.currentIndex(), 
                                        os.path.basename(path))
                    
    def save_all_files(self):
        for i in range(self.tabs.count()):
            editor = self.tabs.widget(i)
            if editor.document().isModified():
                if editor.file_path:
                    editor.save_file()
                else:
                    self.tabs.setCurrentIndex(i)
                    self.save_file_as()
                    
    def auto_save(self):
        if self.settings.value("auto_save", True, type=bool):
            self.save_all_files()
                    
    def close_tab(self, index):
        editor = self.tabs.widget(index)
        if editor.document().isModified():
            reply = QMessageBox.question(
                self, "ذخیره فایل",
                f"فایل ذخیره نشده است. ذخیره شود؟",
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No |
                QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Cancel:
                return
            elif reply == QMessageBox.StandardButton.Yes:
                if editor.file_path:
                    editor.save_file()
                else:
                    self.tabs.setCurrentIndex(index)
                    self.save_file_as()
                    
        self.tabs.removeTab(index)
        
    def close_current_tab(self):
        self.close_tab(self.tabs.currentIndex())
        
    def run_file(self):
        editor = self.get_current_editor()
        if editor and editor.file_path:
            self.output.append(f"در حال اجرای {os.path.basename(editor.file_path)}...")
            self.terminal.run_python(os.path.basename(editor.file_path))
            self.bottom_panel.setCurrentIndex(1)  
        else:
            QMessageBox.warning(self, "خطا", "لطفاً فایل را ذخیره کنید")
            
    def stop_execution(self):
        self.output.append("⏹️ توقف اجرا")
        
    def toggle_terminal(self):
        if self.bottom_panel.isVisible():
            self.bottom_panel.hide()
        else:
            self.bottom_panel.show()
            
    def toggle_explorer(self):
        if self.explorer.isVisible():
            self.explorer.hide()
        else:
            self.explorer.show()
            
    def update_status(self, line, col):
        self.position_label.setText(f"خط: {line}, ستون: {col}")
        
    def undo(self):
        editor = self.get_current_editor()
        if editor:
            editor.undo()
            
    def redo(self):
        editor = self.get_current_editor()
        if editor:
            editor.redo()
            
    def cut(self):
        editor = self.get_current_editor()
        if editor:
            editor.cut()
            
    def copy(self):
        editor = self.get_current_editor()
        if editor:
            editor.copy()
            
    def paste(self):
        editor = self.get_current_editor()
        if editor:
            editor.paste()
            
    def find(self):
        editor = self.get_current_editor()
        if editor:
            QMessageBox.information(self, "جستجو", "این قابلیت در حال توسعه است")
            
    def replace(self):
        editor = self.get_current_editor()
        if editor:
            QMessageBox.information(self, "جایگزینی", "این قابلیت در حال توسعه است")
            
    def zoom_in(self):
        editor = self.get_current_editor()
        if editor:
            font = editor.font()
            font.setPointSize(font.pointSize() + 1)
            editor.setFont(font)
            
    def zoom_out(self):
        editor = self.get_current_editor()
        if editor:
            font = editor.font()
            if font.pointSize() > 8:
                font.setPointSize(font.pointSize() - 1)
                editor.setFont(font)
            
    def show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec():
        
            font_size = self.settings.value("font_size", 11, type=int)
            editor = self.get_current_editor()
            if editor:
                font = editor.font()
                font.setPointSize(font_size)
                editor.setFont(font)
                
         
            interval = self.settings.value("auto_interval", 30, type=int)
            self.auto_save_timer.setInterval(interval * 1000)
                
    def show_about(self):
        QMessageBox.about(
            self, 
            "درباره ZenithFlow",
            """<h2>⚡ ZenithFlow IDE</h2>
            <p>یک IDE حرفه‌ای برای پایتون</p>
            <p>نسخه 1.0.0</p>
            <p>توسعه یافته با PyQt6</p>
            <br>
            <p>ویژگی‌ها:</p>
            <ul>
                <li>ویرایشگر با syntax highlighting</li>
                <li>ترمینال داخلی</li>
                <li>مدیریت فایل</li>
                <li>اجرای مستقیم فایل‌ها</li>
                <li>تم تاریک حرفه‌ای</li>
                <li>ذخیره خودکار</li>
            </ul>"""
        )
        
    def closeEvent(self, event):
     
        modified = False
        for i in range(self.tabs.count()):
            editor = self.tabs.widget(i)
            if editor.document().isModified():
                modified = True
                break
                
        if modified:
            reply = QMessageBox.question(
                self, "خروج",
                "فایل‌های ذخیره نشده وجود دارد. خارج می‌شوید؟",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
                
        event.accept()



def main():
    app = QApplication(sys.argv)
    
  
    font = QFont("Courier New", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()