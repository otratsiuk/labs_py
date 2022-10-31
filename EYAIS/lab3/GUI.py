from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
import cld3

dir = {'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian',
       'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian',
       'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)',
       'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish',
       'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish',
       'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati',
       'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian',
       'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese',
       'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao',
       'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay',
       'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali',
       'no': 'norwegian', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian',
       'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi',
       'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili',
       'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu',
       'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu', 'fil': 'Filipino', 'he': 'Hebrew'}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text = ''
        self.setFixedSize(QSize(600, 400))
        self.layout = QGridLayout()

        self.text_bar = QTextEdit()
        self.text_bar.setFixedSize(400, 200)

        self.open_button = QPushButton("open text")
        self.open_button.clicked.connect(self.get_text)
        self.open_button.setFixedSize(QSize(130, 30))

        self.identificate_button = QPushButton('define language')
        self.identificate_button.clicked.connect(self.identificate)
        self.identificate_button.setFixedSize(QSize(130, 30))

        self.language = QLabel('language')
        self.probability = QLabel('probability')
        self.language_text = QLabel(' ')
        self.probability_text = QLabel(' ')

        self.v_layout = QVBoxLayout()
        self.v_layout.addSpacing(80)
        self.v_layout.addWidget(self.open_button)
        self.v_layout.addWidget(self.identificate_button)
        self.v_layout.addStretch()
        self.v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.v_layout1 = QVBoxLayout()
        self.v_layout1.addWidget(self.language)
        self.v_layout1.addSpacing(10)
        self.v_layout1.addWidget(self.probability)
        self.v_layout1.addSpacing(10)

        self.v_layout2 = QVBoxLayout()
        self.v_layout2.addWidget(self.language_text)
        self.v_layout2.addWidget(self.probability_text)

        self.layout.addWidget(self.text_bar, 0, 0)
        self.layout.addLayout(self.v_layout, 0, 1)
        self.layout.addLayout(self.v_layout1, 1, 0)
        self.layout.addLayout(self.v_layout2, 1, 1)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("langident")


    def get_text(self):
        self.filename, _ = QFileDialog.getOpenFileName(None, 'Open File', './') 
        with open(self.filename) as f:
            self.text = f.read()
 
        self.text_bar.setText(self.text)
    

    def identificate(self):
        res = cld3.get_language(self.text)
        self.language_text.setText(dir[res[0]])
        self.probability_text.setText(str(res[1]))


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()