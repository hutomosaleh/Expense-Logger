import sys
import json
import pandas as pd

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


directory = 'save/'
json_file = 'save.json'



"""
    Read and save json (To remember last used file)
"""


def read_json(filename):
    with open('{}{}'.format(directory, filename), 'r') as f:
        savefile = json.load(f)
    return savefile


def save_json(filename, file):
    with open('{}'.format(directory)+filename, 'w') as f:
        json.dump(file, f, indent=2, sort_keys=False)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('Expense Logger')
        self.setGeometry(50, 50, 350, 350)
        self.savefile = read_json('save.json')
        self.name = self.savefile
        self.UI()

        columns = self.input + ['Date']
        self.df = pd.DataFrame(columns=columns)

    def UI(self):

        """
            Menus
        """

        openFile = QAction('Open File', self)
        openFile.triggered.connect(self.file_open)
        newFile = QAction('New File', self)
        newFile.triggered.connect(self.getText)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(newFile)
        aboutMenu = mainMenu.addMenu('About')
        fileMenu.addAction(openFile)

        """
            Widgets
        """

        self.input = ['Info', 'Description', 'Cost']
        self.input_dict = {}

        for i in self.input:
            self.input_dict[i] = QTextEdit()
            self.input_dict[i+'_lbl'] = QLabel(i)

        self.label = QLabel(f'Current loaded file: {self.name}')

        self.date = QDateEdit()
        self.date.setDateTime(QDateTime.currentDateTime())
        self.date.setCalendarPopup(True)
        self.date.calendarWidget().installEventFilter(self)
        self.date.dateChanged.connect(self.onDateChanged)
        self.date_value = [self.date.dateTime().date().toString()[4:]]
        self.button = QPushButton('save')
        self.button.clicked.connect(self.save)

        """
            Layouts
        """

        main_l = QVBoxLayout()
        input_l_main = QHBoxLayout()
        save_l = QHBoxLayout()

        input_l = {}
        for i in self.input:
            input_l[i] = QVBoxLayout()
            input_l[i].addWidget(self.input_dict[i+'_lbl'])
            input_l[i].addWidget(self.input_dict[i])
            input_l_main.addLayout(input_l[i])


        save_l.addWidget(self.date)
        save_l.addWidget(self.button)

        main_l.addLayout(input_l_main)
        main_l.addLayout(save_l)
        main_l.addWidget(self.label)

        self.widget = QWidget()
        self.widget.setLayout(main_l)
        self.setCentralWidget(self.widget)

    def onDateChanged(self):
        self.date_value = [self.date.dateTime().date().toString()[4:]]

    def save(self):
        value = {}

        for i, val in enumerate(self.input):
            try:
                value[i] = self.input_dict[val].toPlainText()
            except KeyError:
                value[i] = {}
                value[i] = self.input_dict[val].toPlainText()
        if value[0] == value[0] == value[0] == '':
            pass
        else:
            self.df.loc[self.df.shape[0]] = [value[0]] + [value[1]] + [value[2]] + self.date_value
            writer = pd.ExcelWriter(self.name)
            self.df.to_excel(writer, 'Sheet1', index=False)
            writer.save()
            save_json(json_file, self.name)
            self.messageBox()

    def messageBox(self):
        QMessageBox.information(self, 'File saved', 'Expense has been logged!')

    def file_open(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        try:
            self.df = pd.read_excel(name)
            self.name = name
        except FileNotFoundError:
            print('No file chosen')
        self.updateText()

    def file_new(self):
        writer = pd.ExcelWriter(self.name)
        self.df.to_excel(writer, 'Sheet1', index=False)
        writer.save()

    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Make new file", "File name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            text = text + '.xlsx'
            self.name = text
            QMessageBox.information(self, 'File made', 'File successfully created!')
            self.file_new()
            self.updateText()

    def updateText(self):
        self.label.setText(f'Current loaded file: {self.name}')
        save_json(json_file, self.name)


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

