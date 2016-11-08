from pyqtgraph.Qt import QtGui, QtCore
import sys
import numpy as np
import pyqtgraph as pg



class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):

        # buttons
        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        run_catlab_rp2 = QtGui.QPushButton("catlab2")
        run_catlab_rp3 = QtGui.QPushButton("catlab3_SHGLock")
        config_file_display = TextDropper()
        read_config_file_button=QtGui.QPushButton("read .yml")
        read_config_file_button.clicked.connect(self.read_config_file_action)
        yml_display=QtGui.QTextEdit("hehe")

        # yml reading layout
        yml_layoutH=QtGui.QHBoxLayout()
        yml_layoutH.addWidget(config_file_display)
        yml_layoutH.addWidget(read_config_file_button)
        yml_layoutV = QtGui.QVBoxLayout()
        yml_layoutV.addLayout(yml_layoutH)
        yml_layoutV.addWidget(yml_display)

        # buttons layout
        Buttons_layout_V = QtGui.QVBoxLayout()
        Buttons_layout_V.addWidget(run_catlab_rp2)
        Buttons_layout_V.addWidget(run_catlab_rp3)
        Buttons_layout_V.addWidget(qbtn)
        Buttons_layout_V.addLayout(yml_layoutV)
        #
        Buttons_layout_H = QtGui.QHBoxLayout()
        Buttons_layout_H.addStretch(1)
        Buttons_layout_H.addLayout(Buttons_layout_V)
        Buttons_layout_H.addStretch(1)
        #
        Buttons_Widget = QtGui.QWidget()
        Buttons_Widget.setLayout(Buttons_layout_H)
        #
        self.setCentralWidget(Buttons_Widget)

        # center windows and message bar
        self.setGeometry(300, 300, 320, 240)
        self.setWindowTitle('Guassian Beam Mode-Matching tools')
        self.center()
        self.show()


    def read_config_file_action(self):
        pass



    def closeEvent(self, event):

        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class TextDropper(QtGui.QLineEdit):
# here defines a QTextEdit which can drop a config file with .yml

    def __init__(self):
        super(TextDropper, self).__init__()
        self.setDragEnabled(True)


    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'file'):
            event.acceptProposedAction()


    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'file'):
            event.acceptProposedAction()


    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'file'):
        # for some reason, this doubles up the intro slash
            filepath = str(urls[0].path())[1:]
            self.setText(filepath)


def main():
    app = QtGui.QApplication([])
    ex = Example()
    sys.exit(app.exec())

main()






