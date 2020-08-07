import sys,time,win32gui,subprocess,win32con,os
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
import icpRegistration_dialog
from mainWindow import Ui_MainWindow
import tools,numpy
import vtkXYZviewer
"""
20200723
新增縮小功能與關閉功能
"""

class main(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(main,self).__init__()
        self.ui = None
        self.monitorDir=""
        self.setupUI()
        #顯示無邊框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #顯示全螢幕
        self.showFullScreen()
        self.showMaximized()
        self.fileSystemWatcher = QtCore.QFileSystemWatcher()
        self.fileSystemWatcher.addPath(self.monitorDir)
        self.fileSystemWatcher.directoryChanged.connect(self.__autorun)
        self.xyzList=[]
        self.datas = dataCollection()
    def setupUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(self.__callRTDialog)
        self.setupViewer()
        self.ui.progressBar.setVisible(0)
        self.ui.verticalLayout_3.addWidget(self.viewer)
        self.ui.close.clicked.connect(self.close)
        self.ui.circleRed.clicked.connect(self.close)
        self.ui.circleYellow.clicked.connect(self.showMinimized)
        self.ui.automode.clicked.connect(self.__autorun)
        self.ui.loadsettings.clicked.connect(self.__loadsettings)
        self.ui.monPath.clicked.connect(self.__addMonitorDir)
        return
    def setupViewer(self):
        self.frame=Qt.QFrame()
        self.viewer = vtkXYZviewer.XYZviewer(self.frame,0)
        self.viewer.setCubeAxesVisibility(True)
        self.viewer.setScalarBar(0.2,400,60,400)
    def __callRTDialog(self):
        self.rtDg = icpRegistration_dialog.treeViewApp()
        self.rtDg.show()
        return
    
    def __autorun(self):
        if self.monitorDir=="":
            self.ui.information.append("尚未選擇自動路徑!")
            return
        if self.ui.automode.isChecked():
            d = self.monitorDir
            files = os.listdir(d)
            for i in files:
                if ".xyz" in i:
                    if not i in self.xyzList:
                        self.ui.information.append(i)
                        self.xyzList.append(i)
                        p = os.path.join(d,i)
                        self.__qThreadLoading(p)
                        #pcd = tools.getVtkPointCloud(path,1)
                        #self.datas.names.append(i)
                        #self.datas.addData(pcd)
                        #self.__mergedByTransInit()
    def __qThreadLoading(self,file_path):
        self.loading = loading(file_path,self.datas)
        self.datas.isBusy = True
        self.loading.finished.connect(self.__loadingFinished)
        self.ui.progressBar.show()
        self.loading.start()
    def __loadingFinished(self):
        self.datas.isBusy = False
        #self.__mergedByTransInit()
        self.ui.progressBar.hide()
        self.viewer.add_newData(self.datas.pcdCollection[-1])
        self.ui.information.append("載入完成")
    def __loadsettings(self):
        fpath,filetype =QtWidgets.QFileDialog.getOpenFileName(self,"讀取參數","D:\\","db files(*.db)")
        if fpath=="":
            return
        trans_inits = tools.loadTrans_init(fpath)
        self.datas.trans_inits = trans_inits
        text = "load "+str(len(self.datas.trans_inits))+ "組參數"
        print(text)
        print("Load trans_init: ",self.datas.trans_inits)
        self.ui.information.append(text)
        return
    def __addMonitorDir(self):
        fpath=QtWidgets.QFileDialog.getExistingDirectory(self,"Select","D:\\")
        if fpath=="":
            return
        files = os.listdir(fpath)
        for i in files:
            f = os.path.join(fpath,i)
            os.remove(f)
        self.monitorDir=fpath
        self.fileSystemWatcher.addPath(fpath)
        text = "Select monitor folder: "+fpath
        self.ui.information.append(text)
        return
    def __mergedByTransInit(self):
        #1.viewer裡面沒東西, 直接顯示
        #2. viewer裡面有點雲, a.判斷要套用哪一組RT b. 套用並合併 c. 只留下合併後點雲
        counter = self.datas.mergedCounter
        print(counter)
        rtCount = len(self.datas.trans_inits)
        rtInd = counter
        print("###############################################")
        print("current merged count:", rtInd,"Trans count: ",rtCount)
        print("###############################################")
        if self.viewer.ind=="" or rtCount==rtInd:
            self.viewer.add_newData(self.datas.pcdCollection[-1])
            self.datas.mergedCounter = 0
        else :
            print("start merged")
            trans=self.datas.trans_inits
            print(self.datas.pcdCollection[-2])
            print(self.datas.pcdCollection[-1])
            print(trans)
            d=tools.applyTransform(self.datas.pcdCollection[-2],self.datas.pcdCollection[-1],trans[0])
            self.datas.pcdCollection=[]
            self.datas.addData(d)
            self.viewer.add_newData(self.datas.pcdCollection[-1])
            self.datas.mergedCounter+=1
        print("mergedCounter:",self.datas.mergedCounter)
        
    def closeEvent(self,event):
        self.viewer.closeWindow()
        time.sleep(1)
def exception_hook(exctype, value, traceback):
    f = "log.txt"
    with open(f,"a") as logger:
        msg =str(exctype)+str(value)+str(traceback)
        print("msg",msg)
        logger.write(msg)
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback) 
    sys.exit(1)

class loading(QtCore.QThread):
    """
    run a counter for progressbar
    """
    countChanged = QtCore.pyqtSignal(int)
    def __init__(self,file_path,data):
        super().__init__()
        self.file_path=file_path
        self.data=data
    def run(self):
        pcd = tools.getVtkPointCloud(self.file_path,1)
        self.data.names.append(os.path.basename(self.file_path))
        self.data.addData(pcd)
        #1.viewer裡面沒東西, 直接顯示
        #2. viewer裡面有點雲, a.判斷要套用哪一組RT b. 套用並合併 c. 只留下合併後點雲
        counter = self.data.mergedCounter
        print(counter)
        rtCount = len(self.data.trans_inits)
        rtInd = counter
        print("current merged count:", rtInd)
        if rtCount==rtInd:
            self.data.mergedCounter = 0
        elif self.data.isFirst:
            self.data.mergedCounter = 0
            self.data.isFirst=False
        else :
            print("start merged:",rtInd)
            d=tools.applyTransform(self.data.pcdCollection[-2],self.data.pcdCollection[-1],self.data.trans_inits[rtInd])
            self.data.pcdCollection=[]
            self.data.addData(d)
            self.data.mergedCounter+=1
        print("mergedCounter:",self.data.mergedCounter)
        
class dataCollection():
    def __init__(self):
        self.isFirst = True
        self.isBusy = 0
        self.pcdCollection  = []
        self.names = []
        self.trans_inits = []
        self.trans_ind = 0
        self.mergedCounter=0
    def getData(self):
        return self.pcdCollection
    def addData(self,d,pickedIDs=[]):
        ind = len(self.pcdCollection)
        data = [ind,d,pickedIDs]
        self.pcdCollection.append(data)
    def addPickedIDs(self,ind,pickedIDs):
        self.pcdCollection[ind][2].append(pickedIDs)
    def addTransInits(self,trans_init):
        self.trans_inits.append(trans_init)
    def clearData(self):
        self.isBusy=0
        self.pcdCollection  = []
        self.names = []
        self.trans_inits = []
class Logger():
    def __init__(self, filename="log.log",stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename,"a")
    def write(self,message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass
if __name__=="__main__":
    qss = ".\\Diffnes\\Diffnes.qss"
    app = QtWidgets.QApplication(sys.argv)
    with open(qss,'r') as q:
        app.setStyleSheet(q.read())
    ex=main()
    ex.show()
    sys._excepthook = sys.excepthook 
    sys.excepthook = exception_hook
    sys.stdout=Logger("default.log",sys.stdout)
    sys.stderr=Logger("error.log",sys.stderr)
    sys.exit(app.exec_())
