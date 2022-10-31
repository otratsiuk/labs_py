from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
from googletrans import Translator

languages = {
    'belarusian': 'be',
    'russian': 'ru',
    'english': 'en'
    }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.input_text = ''
        self.input_lang = 'english'
        self.output_lang = 'russian'
        self.setFixedSize(QSize(600, 400))
        self.layout = QGridLayout()

        self.text_bar1 = QTextEdit()
        self.text_bar1.setFixedSize(250, 200)

        self.text_bar1.textChanged.connect(self.translate)

        self.text_bar2 = QTextEdit()
        self.text_bar2.setFixedSize(250, 200)

        self.lang_button1 = QComboBox()
        self.lang_button1.addItems(['english', 'russian', 'belarusian'])
        self.lang_button1.currentIndexChanged.connect(self.get_input_lang)
        self.lang_button1.setFixedSize(QSize(250, 30))

        self.lang_button2 = QComboBox()
        self.lang_button2.addItems(['russian', 'english', 'belarusian'])
        self.lang_button2.currentIndexChanged.connect(self.get_output_lang)
        self.lang_button2.setFixedSize(QSize(250, 30))

        self.open_button = QPushButton('open text')
        self.open_button.clicked.connect(self.get_text)
        self.open_button.setFixedSize(QSize(130, 30))

        self.layout.addWidget(self.lang_button1, 0, 0)
        self.layout.addWidget(self.lang_button2, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.text_bar1, 1, 0)
        self.layout.addWidget(self.text_bar2, 1, 1)
        self.layout.addWidget(self.open_button, 2, 0)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("langident")

    def get_text(self):
        self.filename, _ = QFileDialog.getOpenFileName(None, 'Open File', './') 
        with open(self.filename) as f:
            self.input_text = f.read()
 
        self.text_bar1.setText(self.input_text)

    def get_input_lang(self):
        self.input_lang = self.lang_button1.currentText()
        self.translate()

    def get_output_lang(self):
        self.output_lang = self.lang_button2.currentText()
        self.translate()

    def translate(self):
        translator = Translator()
        text = self.text_bar1.toPlainText()
        if text and text.strip():
            translation = translator.translate(self.text_bar1.toPlainText(), 
                                            dest=languages[self.output_lang], 
                                            src=languages[self.input_lang])
            self.text_bar2.setText(translation.text)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()