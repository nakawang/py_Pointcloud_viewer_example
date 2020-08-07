from PyQt5 import QtCore
from PyQt5.QtWidgets import QTreeView
class Tree(QTreeView):
    def __init__(self,parent):
        QTreeView.__init__(self,parent)
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            print("ignore")
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            print("ignore")
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            # to get a list of files:
            drop_list = []
            for url in event.mimeData().urls():
                drop_list.append(str(url.toLocalFile()))
                print(url)
            # handle the list here
        else:
            print("ignore")
            event.ignore()