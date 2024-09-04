import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

# Define the main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stock Tracker")
        self.setGeometry(300, 300, 400, 300)  # x, y, width, height

        # Create a central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Add a label
        self.label = QLabel("Welcome to the Stock Tracker", self)
        layout.addWidget(self.label)

        # Add a button
        button = QPushButton("Click Me", self)
        button.clicked.connect(self.on_button_click)
        layout.addWidget(button)

        # Set the layout to the central widget
        central_widget.setLayout(layout)

    def on_button_click(self):
        self.label.setText("Button Clicked!")

# Main function to run the application
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()