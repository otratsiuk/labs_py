from ctypes import alignment
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
import enum
from AdressBook import *

class BookMode(enum.Enum):
    navigation_mode = 0
    adding_mode = 1
    editing_mode = 2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.book = AdressBook()
        self.old_name = ''
        self.old_adress = ''
        self.mode = BookMode

        self.setFixedSize(QSize(800, 600))
        self.layout = QGridLayout()

        self.name_label = QLabel('Name')
        self.name_label.setFixedSize(QSize(50, 30))
        self.adress_label = QLabel('Adress')
        self.adress_label.setFixedSize(QSize(50, 400))
        self.adress_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.name_edit = QLineEdit()
        self.name_edit.setFixedSize(QSize(600, 30))
        self.adress_edit = QTextEdit()
        self.adress_edit.setFixedSize(QSize(600, 400))

        self.v_buttons_layout = QVBoxLayout()
        self.add_button = QPushButton('Add')
        self.submit_button = QPushButton('Submit')
        self.submit_button.hide()
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.hide()
        self.edit_button = QPushButton('Edit')
        self.edit_button.hide()
        self.remove_button = QPushButton('Remove')
        self.remove_button.hide()
        self.find_button = QPushButton('Find')
        self.find_button.hide()
        self.load_button = QPushButton('Load')
        self.save_button = QPushButton('Save')
        self.save_button.hide()
        self.export_button = QPushButton('Export')
        self.export_button.hide()

        self.v_buttons_layout.addSpacing(56)
        self.v_buttons_layout.addWidget(self.add_button)
        self.v_buttons_layout.addWidget(self.submit_button)
        self.v_buttons_layout.addWidget(self.cancel_button)
        self.v_buttons_layout.addWidget(self.edit_button)
        self.v_buttons_layout.addWidget(self.remove_button)
        self.v_buttons_layout.addWidget(self.find_button)
        self.v_buttons_layout.addWidget(self.save_button)
        self.v_buttons_layout.addWidget(self.load_button)
        self.v_buttons_layout.addWidget(self.export_button)
        self.v_buttons_layout.addStretch()
        self.v_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.h_buttons_layout = QHBoxLayout()
        self.previous_button = QPushButton('Previous')
        self.previous_button.setEnabled(False)
        self.next_button = QPushButton('Next')
        self.next_button.setEnabled(False)
        
        self.h_buttons_layout.addWidget(self.previous_button)
        self.h_buttons_layout.addWidget(self.next_button)

        self.layout.addWidget(self.name_label, 0, 0)
        self.layout.addWidget(self.adress_label, 1, 0)
        self.layout.addWidget(self.name_edit, 0, 1)
        self.layout.addWidget(self.adress_edit, 1, 1)
        self.layout.addLayout(self.v_buttons_layout, 1, 2)
        self.layout.addLayout(self.h_buttons_layout, 2, 1)

        self.add_button.clicked.connect(self.add_person)
        self.submit_button.clicked.connect(self.submit)
        self.cancel_button.clicked.connect(self.cancel)
        self.edit_button.clicked.connect(self.edit)
        self.remove_button.clicked.connect(self.remove)
        self.find_button.clicked.connect(self.find)
        self.save_button.clicked.connect(self.save)
        self.load_button.clicked.connect(self.load)
        self.export_button.clicked.connect(self.export)

        self.previous_button.clicked.connect(self.previous)
        self.next_button.clicked.connect(self.next)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("Adress Book")


    def load(self):
        self.book.load_from_file()
        
        if (self.book.size() > 1):
            self.update_interface(BookMode.navigation_mode)

    def save(self):
        self.book.save_to_file()


    def export(self):
        filename = QFileDialog(self, 'Save file')
        filename = filename.getSaveFileName() 
        self.book.export(filename[0]) 
        print(filename[0])  


    def update_interface(self, mode):
        self.mode = mode

        if self.mode == BookMode.editing_mode:
            print('Edit')
            self.name_edit.setReadOnly(False)
            self.adress_edit.setReadOnly(False)

            self.add_button.setEnabled(False)
            self.edit_button.setEnabled(False)
            self.remove_button.setEnabled(False)

            self.next_button.setEnabled(False)
            self.previous_button.setEnabled(False)

            self.save_button.setEnabled(False)
            self.load_button.setEnabled(False)
            self.find_button.setEnabled(False)

            self.submit_button.show()
            self.cancel_button.show()
            self.find_button.show()

        if self.mode == BookMode.adding_mode:
            print('Add')
            self.name_edit.setReadOnly(False)
            self.adress_edit.setReadOnly(False)

            self.add_button.setEnabled(False)
            self.edit_button.setEnabled(False)
            self.remove_button.setEnabled(False)
            self.find_button.setEnabled(False)
            self.save_button.setEnabled(False)
            self.export_button.setEnabled(False)
            self.load_button.setEnabled(False)

            self.next_button.setEnabled(False)
            self.previous_button.setEnabled(False)

            self.submit_button.show()
            self.cancel_button.show()    

        if self.mode == BookMode.navigation_mode:
            print('Navigation')
            self.name_edit.setReadOnly(False)
            self.adress_edit.setReadOnly(False)
            self.add_button.setEnabled(True)
            self.remove_button.show()
            self.edit_button.show()

            size = self.book.size()
            self.edit_button.setEnabled(size >= 1)
            self.remove_button.setEnabled(size >= 1)
            self.next_button.setEnabled(size > 1)
            self.previous_button.setEnabled(size >1 )
            self.save_button.setEnabled(True)
            self.load_button.setEnabled(True)
            self.export_button.setEnabled(True)
            self.find_button.setEnabled(True)

            self.export_button.show()
            self.save_button.show()
            self.load_button.show()
            self.submit_button.hide()
            self.cancel_button.hide()  
            self.find_button.show()
            

    def find(self):
        search = self.name_edit.text()

        self.name_edit.clear()
        self.adress_edit.clear()

        name = self.book.get(search)

        if name is not None:
            self.name_edit.setText(name[0])
            self.adress_edit.setText(name[1])
        else:
            msg_box = QMessageBox()
            msg = str(search) + ' is not in adress book'
            msg_box.setText(msg)
            msg_box.exec()
             
              
    def edit(self):
        self.old_name = self.name_edit.text()
        self.old_adress = self.adress_edit.toPlainText()

        self.update_interface(BookMode.editing_mode)


    def remove(self):
        name = self.name_edit.text()
        self.book.remove_person(name) 
        self.name_edit.clear()
        self.adress_edit.clear() 
        self.update_interface(BookMode.navigation_mode)  


    def next(self):
        name = self.name_edit.text()    
        index = self.book.prev_and_next(name)

        next = self.book.get(index[1])

        self.name_edit.clear()
        self.adress_edit.clear()

        self.name_edit.setText(next[0])
        self.adress_edit.setText(next[1])

        self.name_edit.show()
        self.adress_edit.show()


    def previous(self):
        name = self.name_edit.text()    
        index = self.book.prev_and_next(name)

        prev = self.book.get(index[0])

        self.name_edit.clear()
        self.adress_edit.clear()

        self.name_edit.setText(prev[0])
        self.adress_edit.setText(prev[1])

        self.name_edit.show()
        self.adress_edit.show() 


    def cancel(self):
        self.name_edit.clear()
        self.adress_edit.clear()

        self.name_edit.setText(self.old_name)
        self.adress_edit.setText(self.old_adress)

        self.update_interface(BookMode.navigation_mode)


    def submit(self):
        name = self.name_edit.text()
        adress = self.adress_edit.toPlainText()

        if self.mode == BookMode.adding_mode:
            self.book.add_person(name, adress)
            self.name_edit.clear()
            self.adress_edit.clear()

            self.update_interface(BookMode.navigation_mode)

        elif self.mode == BookMode.editing_mode:
            if self.old_name != name or self.old_adress != adress:
                self.book.remove_person(self.old_name)
                self.book.add_person(name, adress)  

            self.update_interface(BookMode.navigation_mode)             


    def add_person(self):
        self.old_name = self.name_edit.text()
        self.old_adress = self.adress_edit.toPlainText()

        self.name_edit.setReadOnly(True)
        self.adress_edit.setReadOnly(True)
        self.add_button.setEnabled(False)
        self.submit_button.show()
        self.cancel_button.show()

        self.update_interface(BookMode.adding_mode)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()