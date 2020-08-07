#from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys,time,win32gui,subprocess,win32con,os
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
import copy
import registration_dialog
import tools
import vtkXYZviewer
"""
20200723 新增回上一步,下一步功能,增加檢查icp點數量是否一致
20200802 修正載入資料完成前就顯示在list上,修正外參index未清除
"""
class treeViewApp(QtWidgets.QDialog):
    def __init__(self):
        super(treeViewApp,self).__init__()
        self.ui=None
        self.model = QtGui.QStandardItemModel()
        self.__beHwnd=None
        self.info=dataCollection()
        self.loading = ""
        self.pcdListModel = pcdListModel()
        self.fileModel = ""
        self.m_flag = False
        print("initial")
        self.setup()
        # 設定窗體無邊框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # 設定背景透明
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #self.setWindowOpacity(0.5)
    def setup(self):
        print("setup ui")
        self.ui=registration_dialog.Ui_Dialog()
        self.frame=Qt.QFrame()
        self.viewerMerged = vtkXYZviewer.XYZviewer(self.frame,1)
        self.viewerMerged.setCubeAxesVisibility(False)
        self.viewerCurrent = vtkXYZviewer.XYZviewer(self.frame,1)
        self.viewerCurrent.setCubeAxesVisibility(False)
        self.ui.setupUi(self)
        self.ui.progressBar.hide()
        #call sdk exe and catch window to QT
        self.__addExe()
        self.__addViewer()
        self.__addFileTree()
        self.__addListView()
        #self.ui.addPickedID.setCheckable(True)
        self.ui.addPickedID.clicked.connect(self.__addPickedID)
        self.ui.save.clicked.connect(self.__saveTrans_inits)
        self.ui.load.clicked.connect(self.__loadTrans_inits)
        self.ui.clear.clicked.connect(self.__clearData)
        self.ui.addPickedID_2.clicked.connect(self.__changeRootPath)
        self.ui.btnTestMerged.clicked.connect(self.__mergedByTransInit)
        self.ui.selectPoints.clicked.connect(self.__setViewerSelectionMode)
        self.ui.selectPoints.setChecked(True)
        self.ui.btn_Previous.clicked.connect(self.showPrevious)
        self.ui.btn_Post.clicked.connect(self.showPost)
        #self.ui.load.clicked.connect(self.ui.comboBox.clear)
        self.ui.close.clicked.connect(self.close)
    def __addViewer(self):
        self.ui.verticalLayout_2.addWidget(self.viewerMerged)
        self.ui.verticalLayout_3.addWidget(self.viewerCurrent)
    def __addExe(self):
        return
        hwnd=win32gui.FindWindow(None,"BenanoSDKExample")
        try:
            command = 'taskkill /F /IM BenanoScanSDKExCS.exe'
            os.system(command)
        except:
            print("kill command error")
        exePath = r"C:\Program Files\Benano\BenanoScanSDK\Example\BenanoScanSDKExCS_test\Bin\Release\BenanoScanSDKExCS.exe"
        subprocess.Popen(exePath)
        time.sleep(0.2)
        while(hwnd==0x0):
            hwnd=win32gui.FindWindow(None,"BenanoSDKExample")
            print("%#x"%hwnd)
        window=QtGui.QWindow.fromWinId(hwnd)
        window.setGeometry(500,500,500,500)
        container = QtWidgets.QWidget.createWindowContainer(window, self)
        self.ui.verticalLayout.addWidget(container)
        self.ui.verticalLayout.setContentsMargins(0,0,0,0)
        self.__beHwnd = hwnd
    def __addFileTree(self,root="D:\\testdata"):
        model = QtWidgets.QFileSystemModel()
        model.setRootPath(root)
        #model.setFilter(QtCore.QDir.AllDirs|QtCore.QDir.NoDotAndDotDot)
        model.setNameFilters(["*.xyz"])
        model.setNameFilterDisables(False)
        self.ui.treeView.setModel(model)
        self.ui.treeView.setRootIndex(model.index("D:\\testdata"))
        self.ui.treeView.doubleClicked.connect(self.__doubleClickedFileTree)
        self.ui.treeView.setColumnHidden(1,True)
        self.ui.treeView.setColumnHidden(2,True)
        self.ui.treeView.setColumnHidden(3,True)
        self.fileModel=model
    def __addListView(self):
        self.ui.listView.setModel(self.pcdListModel)
        #self.ui.btn_Add.clicked.connect(self.__addInfo)
        #self.ui.btn_Remove.clicked.connect(self.__deleteInfo)
        self.ui.listView.doubleClicked.connect(self.__doubleClickedListView)
    def __doubleClickedFileTree(self,signal):
        file_path = self.ui.treeView.model().filePath(signal)
        path, name = os.path.split(file_path)
        if not "xyz" in name:
            return
        if not os.path.isdir(file_path):
            print("DoubleClicked: ",file_path)
            #self.viewerCurrent.load_data(file_path)
            self.loading = loading(file_path,self.info)
            self.info.isBusy = True
            self.loading.finished.connect(self.__loadingFinished)
            self.ui.progressBar.show()
            self.loading.start()
            #self.pcdListModel.pcdList.append((False,name))
        
    def __doubleClickedListView(self):
        if self.info.isBusy:
            return
        indexes = self.ui.listView.selectedIndexes()
        print("indexes",indexes)
        if indexes:
            index = indexes[0]
            print("index",index)
            row = index.row()
            print("row",row)
            status,text = self.pcdListModel.pcdList[row]
            if self.viewerMerged.ind =="":
                self.pcdListModel.pcdList[row] = (True, text)
                pcd = self.info.pcdCollection[row]
                self.viewerMerged.add_newData(pcd)
                self.info.addMergedData(pcd[1])
                self.pcdListModel.dataChanged.emit(index,index)
            else:
                self.viewerCurrent.add_newData(self.info.pcdCollection[row])
            return
    def __loadingFinished(self):
        self.info.isBusy = False
        self.ui.progressBar.hide()
        d=self.info.pcdCollection
        print("pcd data counts: ",len(d))
        self.showMessage("載入完成")
        #=====================================================
        '''
        if len(d):
            pcd = d[-1]
            print("cur pcd=",pcd)
            if self.viewerMerged.ind == "":
                print("merged viewer ind:",self.viewerMerged.ind)
                self.viewerMerged.add_newData(pcd)
                print("merged viewer ind:",self.viewerMerged.ind)
            else:
                self.viewerCurrent.add_newData(pcd)
        '''
        #=====================================================
        self.pcdListModel.pcdList.append((False,self.info.names[-1]))
        self.pcdListModel.layoutChanged.emit()
    def __setViewerSelectionMode(self):
        if self.ui.selectPoints.isChecked():
            self.viewerCurrent.changeMode(1)
            self.viewerMerged.changeMode(1)
        else:
            print("btn select 0")
            self.viewerCurrent.changeMode(0)
            self.viewerMerged.changeMode(0)
    def __addPickedID(self):
        source_pickedID=self.viewerCurrent.getPickedID()
        target_pickedID=self.viewerMerged.getPickedID()
        if len(source_pickedID)<3 or len(target_pickedID)<3:
            self.showMessage("選擇的點數少於3點")
            return
        elif len(source_pickedID) != len(target_pickedID):
            self.showMessage("兩邊選擇的點數不同")
            return
        ind = self.viewerCurrent.ind
        self.info.addPickedIDs(ind,target_pickedID)
        print("Add pickedIDs:",target_pickedID)
        targetID = self.viewerMerged.ind
        if self.info.curMergedPCDIndex>0:
            target = self.info.getCurMergedData()
            print("get current merged data")
        else:
            target = self.info.pcdCollection[targetID]
            print("get first target data")
        sourceID = self.viewerCurrent.ind
        print("get current viewer ind",sourceID)
        source = self.info.pcdCollection[sourceID]
        print(source[1][1])
        #計算初步旋轉矩陣
        trans_init = tools.calcO3DRT(target[1][1],target_pickedID,source[1][1],source_pickedID)
        #合併並且downsampling
        source_new = copy.deepcopy(source[1][1])
        target_new = copy.deepcopy(target[1][1])
        mergedP3D = tools.manualRegistration(target_new,source_new,trans_init)
        vtkPCD = tools.o3dp3dTovtkPCD(mergedP3D)
        d = [vtkPCD,mergedP3D]
        self.info.addMergedData(d)
        self.info.addTransInits(trans_init)
        self.viewerMerged.add_newData(self.info.getCurMergedData())
    def __changeRootPath(self):
        fpath =QtWidgets.QFileDialog.getExistingDirectory(self,"讀取參數","D:\\")
        if fpath=="":
            return
        #model = QtWidgets.QFileSystemModel()
        self.ui.treeView.setRootIndex(self.fileModel.index(fpath))
        
    def __loadTrans_inits(self):
        fpath,filetype =QtWidgets.QFileDialog.getOpenFileName(self,"讀取參數","D:\\","db files(*.db)")
        if fpath=="":
            return
        trans_inits = tools.loadTrans_init(fpath)
        self.info.trans_inits = trans_inits
        self.info.trans_ind = 0
        #print("load trans_inits:",trans_inits[0])
        count = len(self.info.trans_inits)
        text = "Load"+str(count)+"組參數"
        self.showMessage(text)
        '''
        if len(trans_inits) == len(self.info.pcdCollection)-1:
            for i in range(len(trans_inits)):
                if i==0:
                    mergedData = tools.manualRegistration(self.info.pcdCollection[0][1][0],self.info.pcdCollection[1][1][0],trans_inits[i])
                    self.info.addData(mergedData)
                else:
                    mergedData = tools.manualRegistration(self.info.pcdCollection[-1][1][0],self.info.pcdCollection[i+1][1][0],trans_inits[i])
                    self.info.addData(mergedData)
        '''
        self.ui.btnTestMerged.setEnabled(True)
    def showMessage(self,text):
        self.ui.textEdit.append(str(text))
    def showPrevious(self):
        self.viewerCurrent.removeAll()
        self.viewerMerged.removeAll()
        self.viewerCurrent.ind=""
        self.viewerMerged.ind=""
        pcd = self.info.getPreviousMergedPCD()
        print("return previous")
        if pcd ==-1:
            print("debug")
            return
        else:
            self.viewerMerged.add_newData(pcd)
            #ID = self.viewerCurrent.ind
            #curPCD = self.info.pcdCollection[ID]
            #self.viewerCurrent.add_newData(curPCD)
    def showPost(self):
        pcd = self.info.getPostMergedPCD()
        if  pcd is None:
            return
        else:
            self.viewerMerged.add_newData(pcd)
    def __selectTransInit(self):
        self.info.trans_ind = self.ui.comboBox.currentIndex()
    def __mergedByTransInit(self):
        if self.info.isBusy:
            self.showMessage("載入中,請稍後")
            return
        ind_target = self.viewerMerged.ind
        ind_source = self.viewerCurrent.ind
        if ind_target=="" or ind_source=="":
            return
        target = self.info.pcdCollection[ind_target]
        print("target:",target)
        source = self.info.pcdCollection[ind_source]
        print("source:",source)
        if self.info.trans_ind=="":
            self.info.trans_ind = 0
        trans_ind = self.info.trans_ind
        #要加入rt數量與點雲數量保護
        text = "套用第"+str(trans_ind)+"組參數"
        self.showMessage(text)
        print("trans_ind",trans_ind)
        d = tools.applyTransform(target,source,self.info.trans_inits[trans_ind])
        self.info.trans_ind=trans_ind+1
        self.info.addData(d)
        self.viewerMerged.add_newData(self.info.pcdCollection[-1])
        self.viewerCurrent.removeAll()
    def __saveTrans_inits(self):
        
        count = self.info.curMergedPCDIndex -1
        if count > 0:
            fpath,filetype =QtWidgets.QFileDialog.getSaveFileName(self,"儲存參數","D:\\","db files(*.db)")
            if fpath=="":
                return
            self.showMessage("清除不保存數據")
            self.info.delExtraData()
            count = len(self.info.trans_inits)
            tools.saveTrans_init(fpath,self.info.trans_inits)
            txt = "儲存"+str(count)+"組參數"
            self.showMessage(txt)
        else:
            self.showMessage("沒有足夠參數")
    def __clearData(self):
        if self.info.isBusy:
            self.showMessage("系統忙碌中")
            return
        self.showMessage("清除所有數據")
        self.info.clearData()
        self.viewerCurrent.removeAll()
        self.viewerMerged.removeAll()
        self.viewerCurrent.ind=""
        self.viewerMerged.ind=""
        self.ui.btnTestMerged.setEnabled(False)
        #=======================================
        #取得所有Qmodelindex,進行操作
        #indexes = self.pcdListModel.getTickInd()
        #for ind in indexes:
        #    row = ind.row()
        #    _ , text = self.pcdListModel.pcdList[row]
        #    self.pcdListModel.pcdList[row] = (False, text)
        #    self.pcdListModel.dataChanged.emit(ind,ind)
        #=======================================
        #移除所有list data
        ind = self.ui.listView.currentIndex()
        rowCount = self.pcdListModel.rowCount(ind)
        print("index count",rowCount)
        for i in range(rowCount):
            print("刪除第",i,"個")
            del self.pcdListModel.pcdList[0]
        self.pcdListModel.layoutChanged.emit()
    def __addInfo(self,signal):
        file_path = self.ui.treeView.model().filePath(signal)
        if not os.path.isdir(file_path):
            print("DoubleClicked: ",file_path)
            #self.viewerCurrent.load_data(file_path)
            self.loading = loading(file_path,self.info)
            self.dataSet.isBusy = True
            self.loading.finished.connect(self.__loadingFinished)
            self.ui.progressBar.show()
            self.loading.start()
            fname = os.path.basename(file_path)
            self.model.dataSet.append((False,fname))
            self.model.layoutChanged.emit()
    def __deleteInfo(self):
        indexes = self.info.selectedIndexes()
        if indexes:
            index = indexes[0]
            del self.model.info[index.row()]
            self.model.layoutChanged.emit()
            self.info.clearSelection()
    def mousePressEvent(self, event):
        if event.button()==QtCore.Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #獲取滑鼠相對視窗的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  #更改滑鼠圖示
            
    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改視窗位置
            QMouseEvent.accept()
            
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    def closeEvent(self,event):
        self.viewerCurrent.closeWindow()
        self.viewerMerged.closeWindow()
        win32gui.PostMessage(self.__beHwnd,win32con.WM_CLOSE,0,0)
        time.sleep(1)

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
        pcd = tools.getVtkPointCloud(self.file_path)
        self.data.names.append(os.path.basename(self.file_path))
        self.data.addData(pcd)
        
class dataCollection():
    def __init__(self):
        self.isBusy = 0
        self.pcdCollection  = []
        self.mergedPCDCollection = []
        self.names = []
        self.trans_inits = []
        self.trans_ind = 0
        self.curPCDIndex = 0
        self.curMergedPCDIndex = 0
    def getData(self):
        return self.pcdCollection
    def getPreviousMergedPCD(self):
        print("cur merged ind:", self.curMergedPCDIndex)
        if self.curMergedPCDIndex==1:
            return self.mergedPCDCollection[0]
        elif self.curMergedPCDIndex==0:
            return -1
        else:
            ind = self.curMergedPCDIndex-1
            self.curMergedPCDIndex=ind
            return self.mergedPCDCollection[ind-1]
    def getPostMergedPCD(self):
        maxCount = len(self.mergedPCDCollection)
        print("maxCount",maxCount)
        if self.curMergedPCDIndex==maxCount:
            return None
        elif maxCount==0:
            return None
        ind = self.curMergedPCDIndex+1
        self.curMergedPCDIndex=ind
        return self.mergedPCDCollection[ind-1]
    def addData(self,d,pickedIDs=[]):
        ind = len(self.pcdCollection)
        data = [ind,d,pickedIDs]
        self.pcdCollection.append(data)
    def addMergedData(self,d,pickedIDs=[]):
        self.delExtraData()
        ind = len(self.mergedPCDCollection)
        data = [ind,d,pickedIDs]
        self.curMergedPCDIndex+=1
        print("merged ind:",self.curMergedPCDIndex)
        self.mergedPCDCollection.append(data)
    def getCurMergedData(self):
        curPCD=self.mergedPCDCollection[self.curMergedPCDIndex-1]
        return curPCD
    def addPickedIDs(self,ind,pickedIDs):
        self.pcdCollection[ind][2].append(pickedIDs)
    def addTransInits(self,trans_init):
        self.delExtraData()
        self.trans_inits.append(trans_init)
    def delExtraData(self):
        ind = len(self.mergedPCDCollection)
        cutoff = ind-self.curMergedPCDIndex
        for i in range(cutoff):
            self.trans_inits=self.trans_inits[:-1]
            self.mergedPCDCollection=self.mergedPCDCollection[:-1]
        print("curent trans_inits:",self.trans_inits)
    def clearData(self):
        self.isBusy=0
        self.pcdCollection  = []
        self.names = []
        self.trans_inits = []
        
tick = QtGui.QImage('tick.png')

class pcdListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, pcdList=None, **kwargs):
        super(pcdListModel,self).__init__(*args,**kwargs)
        self.pcdList = pcdList or []
        self.TickInd = []
    def data(self,index,role):
        if role == QtCore.Qt.DisplayRole:
            _ ,text = self.pcdList[index.row()]
            return text
        if role == QtCore.Qt.DecorationRole:
            status, _ = self.pcdList[index.row()]
            self.TickInd.append(index)
            if status:
                return tick
    def rowCount(self,index):
        return len(self.pcdList)
    def getTickInd(self):
        return self.TickInd
        
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback) 
    sys.exit(1)        
     
if __name__=="__main__":
    qss = ".\\Diffnes\\Diffnes.qss"
    
    #appctxt=ApplicationContext()
    app = QtWidgets.QApplication(sys.argv)
    with open(qss,'r') as q:
        app.setStyleSheet(q.read())
    ex=treeViewApp()
    ex.show()
    #exit_code = appctxt.app.exec_()
    sys._excepthook = sys.excepthook 
    
    sys.excepthook = exception_hook 
    sys.exit(app.exec_())
    
