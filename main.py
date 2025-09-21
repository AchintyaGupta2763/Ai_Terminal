from PyQt5.QtWidgets import QApplication
from ui.terminal_ui import TerminalUI
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)     # Create QApplication first
    window = TerminalUI()            # Now it's safe to create QWidget
    window.show()
    sys.exit(app.exec_())            # Start the event loop
