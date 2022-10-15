from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from MedianFilter import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.median_filter = MedianFilter()
        self.filename = ''

        self.windows = [3, 5, 7, 9, 11]

        self.window_size = 3

        self.setFixedSize(QSize(800, 600))
        self.layout = QGridLayout()

        self.origin_image_label = QLabel()
        self.edit_image_label = QLabel()

        self.select_button = QPushButton("Select image")
        self.select_button.setCheckable(True)
        self.select_button.clicked.connect(self.get_file)

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply) 

        self.combo_box = QComboBox()
        self.combo_box.addItems(['3*3', '5*5', '7*7', '9*9', '11*11'])

        self.noise_spin = QSlider()
        self.noise_spin.setOrientation(Qt.Orientation.Horizontal)
        self.noise_spin.setMinimum(0)
        self.noise_spin.setFixedWidth(350)
        self.noise_spin.valueChanged.connect(self.change_noise)
        self.combo_box.currentIndexChanged.connect(self.window_changed)

        self.layout.addWidget(self.noise_spin, 3, 0)
        self.layout.addWidget(self.select_button, 4, 0)
        self.layout.addWidget(self.apply_button, 4, 2)
        self.layout.addWidget(self.origin_image_label, 0, 0)
        self.layout.addWidget(self.edit_image_label, 0, 2)
        self.layout.addWidget(self.combo_box, 3, 2)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("Median Filter")


    def window_changed(self):
        key = self.combo_box.currentIndex()
        self.window_size = self.windows[key]


    def change_noise(self):
        noise = self.noise_spin.value()
        self.median_filter.add_noise(noise)
        self.origin_image_label.setPixmap(QPixmap('noised_temp'))


    def apply(self):
        self.median_filter.apply(self.window_size)
        self.median_filter.add_zero_padding(math.floor(self.window_size / 2))
        self.edit_image_label.setPixmap(QPixmap('edited_temp'))


    def get_file(self):
        self.filename, _ = QFileDialog.getOpenFileName(None, 'Open File', './', "Image (*.png *.jpg *jpeg)") 
        self.median_filter.open_image(self.filename)
        if self.filename:
            self.origin_image_label.setPixmap(QPixmap(self.filename))

        noise_max = self.median_filter.size()[0] * self.median_filter.size()[1]
        self.noise_spin.setMaximum(noise_max)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()