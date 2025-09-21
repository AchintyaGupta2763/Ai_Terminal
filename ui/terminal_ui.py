# ui/terminal_ui.py
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit, QCompleter
from PyQt5.QtGui import QFont, QTextCharFormat, QTextCursor, QColor
from PyQt5.QtCore import Qt
from backend.commands import CommandExecutor
from ai.ai_agent import interpret_natural_command
import os, sys

class TerminalUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeMate Terminal")
        self.setGeometry(100, 100, 1200, 700)
        self.executor = CommandExecutor()

        # Command history
        self.history = []
        self.history_index = -1

        # Commands for autocomplete
        self.commands = ["ls", "cd", "pwd", "mkdir", "rm", "cpu", "mem", "ps", "exit", "clear", "help", "ai:"]
        for path in os.environ.get("PATH", "").split(os.pathsep):
            if os.path.isdir(path):
                for exe in os.listdir(path):
                    if os.access(os.path.join(path, exe), os.X_OK):
                        self.commands.append(exe)

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Output area
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 12))
        self.output.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                border: 2px solid #333;
                padding: 5px;
            }
        """)
        layout.addWidget(self.output)

        # Input line
        self.input = QLineEdit()
        self.input.setFont(QFont("Consolas", 12))
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: white;
                border-top: 2px solid #333;
                padding: 5px;
            }
        """)
        self.input.setPlaceholderText("Type command here...")
        layout.addWidget(self.input)

        # Autocomplete
        completer = QCompleter(self.commands)
        completer.setCaseSensitivity(False)
        self.input.setCompleter(completer)

        # Signals
        self.input.returnPressed.connect(self.run_command)
        self.input.installEventFilter(self)

        # Welcome
        self._append_output("Welcome to Python Terminal 🚀\nType commands below.\nThis is the basic list of commands[ls, cd, pwd, mkdir, rm, cpu, mem, ps, cls, clear,help, ai:]", color="#34e2e2")
        self._append_output(self._get_prompt(), color="white")

    def _append_output(self, text, color="green"):
        fmt = QTextCharFormat()
        if color == "green":
            fmt.setForeground(QColor("#00ff00"))
        elif color == "red":
            fmt.setForeground(QColor("#ff5555"))
        elif color == "white":
            fmt.setForeground(QColor("white"))
        elif color == "cyan":
            fmt.setForeground(QColor("#00ffff"))
        else:
            fmt.setForeground(QColor(color))

        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.setCharFormat(fmt)
        cursor.insertText(text + "\n")
        cursor.movePosition(QTextCursor.End)
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()

    def _get_prompt(self):
        # Show current working directory
        cwd = self.executor.cwd if hasattr(self.executor, "cwd") else os.getcwd()
        return f"{cwd} > "

    def run_command(self):
        cmd = self.input.text().strip()
        if not cmd:
            return

        # Show prompt + user command in white
        self._append_output(f"{self._get_prompt()}{cmd}", color="white")

        # Save to history
        self.history.append(cmd)
        self.history_index = len(self.history)

        try:
            # AI command placeholder
            if cmd.lower().startswith("ai:"):
                ai_cmd = interpret_natural_command(cmd[3:].strip())
                output = self.executor.run(ai_cmd)
                if output:
                    self._append_output(output, color="cyan")
                # Always show cwd after AI commands
                self._append_output(str(self.executor.cwd), color="white")

            else:
                output = self.executor.run(cmd)
                if output:
                    self._append_output(output, color="green")
                # Always show cwd after normal commands
                self._append_output(str(self.executor.cwd), color="white")

        except Exception as e:
            self._append_output(str(e), color="red")

        # Clear input
        self.input.clear()


    def eventFilter(self, obj, event):
        if obj == self.input:
            if event.type() == event.KeyPress:
                key = event.key()
                # History
                if key == Qt.Key_Up and self.history:
                    self.history_index = max(0, self.history_index - 1)
                    self.input.setText(self.history[self.history_index])
                    return True
                elif key == Qt.Key_Down and self.history:
                    self.history_index = min(len(self.history), self.history_index + 1)
                    if self.history_index < len(self.history):
                        self.input.setText(self.history[self.history_index])
                    else:
                        self.input.clear()
                    return True
        return super().eventFilter(obj, event)

    def run(self):
        self.show()
