from pyqtgraph.Qt import QtGui, QtCore
import sys, os, random
import ruamel.yaml
import numpy as np
import pyqtgraph as pg
from modematching import Optical_Path as OP



class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):

        # buttons
        self.qbtn = QtGui.QPushButton('Quit', self)
        self.qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.run_catlab_rp2 = QtGui.QPushButton("catlab2")
        self.run_catlab_rp3 = QtGui.QPushButton("catlab3_SHGLock")
        self.config_file_path = TextDropper()
        self.config_file_path.textChanged.connect(self.read_config_file_action)
        #
        self.plot_button=QtGui.QPushButton("plot modematching")
        self.plot_button.clicked.connect(self.start_mode_matching_plot)
        #
        self.yml_display=QtGui.QTextEdit("hehe")

        # yml reading layout
        yml_layoutH=QtGui.QHBoxLayout()
        yml_layoutH.addWidget(self.config_file_path)
        yml_layoutH.addWidget(self.plot_button)
        yml_layoutV = QtGui.QVBoxLayout()
        yml_layoutV.addLayout(yml_layoutH)
        yml_layoutV.addWidget(self.yml_display)

        # buttons layout
        Buttons_layout_V = QtGui.QVBoxLayout()
        #Buttons_layout_V.addWidget(self.run_catlab_rp2)
        #Buttons_layout_V.addWidget(self.run_catlab_rp3)
        Buttons_layout_V.addLayout(yml_layoutV)
        Buttons_layout_V.addWidget(self.qbtn)
        #
        Buttons_layout_H = QtGui.QHBoxLayout()
        #Buttons_layout_H.addStretch(1)
        Buttons_layout_H.addLayout(Buttons_layout_V)
        #Buttons_layout_H.addStretch(1)
        #
        Center_Widget = QtGui.QWidget()
        Center_Widget.setLayout(Buttons_layout_H)
        #
        self.setCentralWidget(Center_Widget)

        # center windows and message bar
        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('Guassian Beam Mode-Matching tools')
        self.center()
        self.show()


    def read_config_file_action(self):
        _path = self.config_file_path.text()
        if os.path.isfile( _path ):
            if _path.split('.')[-1] == 'yml':
                with open(_path) as f:
                    _config = ruamel.yaml.load(f, ruamel.yaml.RoundTripLoader)
                _config_text= ruamel.yaml.dump(_config, Dumper= ruamel.yaml.RoundTripDumper)
                self.yml_display.setText(_config_text)
            else:
                self.yml_display.setText(_path+'  WTF?')
        else:
            self.yml_display.setText("WTF?")

    def start_mode_matching_plot(self):
        a = OP.load_yml_from_full_path(filepath=self.config_file_path.text())
        b = a.plotdata_OP()
        plotWidget = pg.plot(title="Three plot curves")
        #for i in range(3):
        #    plotWidget.plot(x, y[i], pen=(i, 3))
        ## setting pen=(i,3) automaticaly creates three different-colored pens
        for yn in b[1]:
            _color = (random.random() * 255,
                      random.random() * 255,
                      random.random() * 255)
            a=plotWidget.plot(b[0], yn)
            ng_yn= [-x for x in yn]
            c=plotWidget.plot(b[0], ng_yn)
            a.setPen(color=_color, width=2)
            c.setPen(color=_color, width=2)





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
            filepath = '/'+str(urls[0].path())[1:]
            self.setText(filepath)


def main():
    app = QtGui.QApplication([])
    ex = Example()
    sys.exit(app.exec())

main()






