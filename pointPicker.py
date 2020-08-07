import vtk 
class testStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self,cbFunc,rbFunc,rtFunc,parent):
        #parent = interactor, need to get hotkey from interactor
        self.parent=parent
        self.AddObserver("KeyPressEvent",self.keyPressEvent)
        self.LastPickedActor = None
        self.LastPickedProperty = vtk.vtkProperty()
        self.cbFunc=cbFunc
        self.rbFunc=rbFunc
        self.rtFunc=rtFunc
        self.isPickerMode=True
        if self.isPickerMode == True:
            self.__startObserver()
    def __startObserver(self):
        self.AddObserver("LeftButtonPressEvent",self.leftButtonPressEvent)
        self.AddObserver("RightButtonPressEvent",self.rightButtonPressEvent)
    def __removeObserver(self):
        self.RemoveObservers("LeftButtonPressEvent")
        self.RemoveObservers("RightButtonPressEvent")
        #self.RemoveObserver(self.rightButtonPressEvent)
    def leftButtonPressEvent(self,obj,event):
        print(obj)
        clickPos = self.GetInteractor().GetEventPosition()
        print("click position: ",clickPos)
        #picker = self.GetInteractor().GetPicker()
        #print("Get current picker: ", picker)
        picker = vtk.vtkPointPicker()
        picker.SetTolerance(0.001)
        ren = self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer()
        picker.Pick(clickPos[0],clickPos[1],0,ren)
        print("picked id: ",picker.GetPointId())
        if(picker.GetPointId()==-1):
            return
        self.cbFunc(picker.GetPointId())
    def rightButtonPressEvent(self,obj,event):
        print(obj)
        self.rbFunc()
    def setPickingMode(self,mode):
        if (mode==0):
            if (self.isPickerMode):
                self.isPickerMode=False
                self.__removeObserver()
        elif (mode==1):
            if not (self.isPickerMode):
                self.isPickerMode=True
                self.__startObserver()
    def keyPressEvent(self,obj,event):
        key = self.parent.GetKeySym()
        print("Key pressed: ",key)
        if(key=="F1"):
            if not (self.isPickerMode):
                print("start picking")
                self.isPickerMode=True
                self.__startObserver()
            else:
                print("stop picking")
                self.isPickerMode=False
                self.__removeObserver()
        elif(key=="F2"):
            self.rtFunc()
if __name__=="__main__":
    #a=testStyle()
    print("testStyle")
