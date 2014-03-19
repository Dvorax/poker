from PySide import QtCore, QtGui, QtUiTools


def loadUiWidget(uifilename, parent=None):
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = loadUiWidget("ui/form.ui")
    MainWindow.cards
    MainWindow.show()
    sys.exit(app.exec_())