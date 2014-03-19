from PySide import QtCore, QtGui, QtUiTools


def load_ui_widget(ui_filename, parent=None):
    loader = QtUiTools.QUiLoader()
    ui_file = QtCore.QFile(ui_filename)
    ui_file.open(QtCore.QFile.ReadOnly)
    ui = loader.load(ui_file, parent)
    ui_file.close()
    return ui


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = load_ui_widget("ui/form.ui")
    MainWindow.show()
    sys.exit(app.exec_())