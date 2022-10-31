from re import S
from Search import *
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.search = Search()
        self.search.prepare_texts()
        self.request = ''

        self.setFixedSize(QSize(800, 600))
        self.layout = QGridLayout()

        self.search_bar = QTextEdit()
        self.search_bar.setFixedSize(700, 30)

        self.response_bar = QTextEdit()
        self.response_bar.setFixedSize(700, 350)

        self.link_bar = QTextBrowser()
        self.link_bar.setOpenExternalLinks(True)
        self.link_bar.setFixedSize(700, 150)

        self.search_button = QPushButton("Search")
        self.search_button.setCheckable(True)
        self.search_button.clicked.connect(self.get_request)

        self.layout.addWidget(self.search_bar, 0, 0)
        self.layout.addWidget(self.link_bar, 1, 0)
        self.layout.addWidget(self.search_button, 0, 2)
        self.layout.addWidget(self.response_bar, 2, 0)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("My App")


    def get_request(self):
        response = self.search.get_similar_articles(self.search_bar.toPlainText())
        if response is not None:
            self.link_bar.clear()
            html = """<a href="{url}">{url}</a>""".format(url=response[1])
            self.link_bar.append(html)
            key_words = self.search.get_key_words()
            self.link_bar.append('\nKEY WORDS: ')
            self.link_bar.append(', '.join(key_words))
            summarization = self.search.summarize()
            self.response_bar.setText(summarization)
        else:
            self.response_bar.setText("No results were found")    
  
        self.search.clean()  


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()