# -*- coding: utf-8 -*-
import vtk,sys,numpy,os
from numpy import random,genfromtxt,size
from PyQt5 import QtCore, QtGui, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtCore import pyqtSlot, QThread
from vtkPointCloud import VtkPointCloud
from tools import getVtkPointCloud

class XYZviewer(QtWidgets.QFrame):
    def __init__(self, parent, pickingMode, dataPath=None):
        super(XYZviewer,self).__init__(parent)
        self.interactor = QVTKRenderWindowInteractor(self)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.interactor)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.pointCloud = VtkPointCloud()
        self.pcdCollection=[]
        self.actors = []
        self.pickedID=[]
        self.pickedPoints=[]
        self.ind=""
        self.scalarParam=[]
    # Renderer
        self.renderer = vtk.vtkRenderer()
        self.cubeAxesActor = vtk.vtkCubeAxesActor()
        self.setCubeAxesActor()
        self.cubeAxesActor.SetBounds(0,100,0,100,0,100)
        
        self.renderer.AddActor(self.cubeAxesActor)
        
    # Scalar Bar
    
        self.scalarBarActor = vtk.vtkScalarBarActor()
        self.setScalarBar()
        self.renderer.AddActor(self.scalarBarActor)
    
    #renderer.SetBackground(.2, .3, .4)
        #colors=vtk.vtkNamedColors()
        #colors.SetColor("BkgColor",[179,204,255,255])
        #renderer.SetBackground(colors.GetColor3d("BkgColor"))
        self.pointCloud.setLUTRange(0,10)
        #cam=self.renderer.GetActiveCamera()
        #cam.Azimuth(-45)
        #cam.Elevation(0)
        #cam.Roll(90)
        #cam.SetViewUp(0,0,1)
        #cam.SetPosition(0,1,0)
        #cam.SetParallelProjection(0)
        #cam.Elevation(-10)
        #self.renderer.SetActiveCamera(cam)
        #self.renderer.ResetCamera()
        #renderer.SetLayer(1)
     
    # Render Window
        renderWindow = self.interactor.GetRenderWindow()
        #renderWindow = vtk.vtkRenderWindow()
        #print(renderWindow)
        #renderWindow.SetNumberOfLayers(2)
        renderWindow.AddRenderer(self.renderer)
        #renderWindow.AddRenderer(self.addLogo())
        
    # Interactor
        #renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(renderWindow)
        self.__setInterActorModeAsPickerMode(pickingMode)
    # Scalar Bar
        #self.addScalarBar(self.pointCloud.getLUT())
        
        #renderWindow.SetInteractor(self.interactor)
    # Logo
        #self.addLogo()
    # orientation marker
        self.addAxisWidget()
        self.renderer.ResetCamera()
    # Begin Interaction
        renderWindow.Render()
        renderWindow.SetWindowName("XYZ Data Viewer:"+ "xyz")
        self.interactor.Start()
        #renderWindowInteractor.Start()
    # Pack to class
        #self.renderer=renderer
        #self.interactor=interactor
        if not (dataPath==None):
            self.load_data(dataPath)
                
    def start(self):
        self.interactor.Start()
    def load_data(self,dataPath):
        self.pointCloud=getVtkPointCloud(dataPath)
        self.addActor()
        self.refresh_renderer()
    def addLogo(self):
        imgReader = vtk.vtkPNGReader()
        imgReader.SetFileName("benano.png")
        imgReader.Update()
        #print(imgReader.GetOutput())
        imgActor = vtk.vtkImageActor()
        imgActor.SetInputData(imgReader.GetOutput())
        background_renderer = vtk.vtkRenderer()
        background_renderer.SetLayer(0)
        background_renderer.InteractiveOff()
        background_renderer.AddActor(imgActor)
        return background_renderer
    def setScalarBar(self,barRatio=0.06,height=100,max_width=40,max_height=250):
        if not (barRatio==0.06 and height==100 and max_width==40 and max_height==250):
            self.scalarParam=[barRatio,height,max_width,max_height]
        if len(self.scalarParam)>0:
            barRatio = self.scalarParam[0]
            height = self.scalarParam[1]
            max_width = self.scalarParam[2]
            max_height = self.scalarParam[3]
        lut=self.pointCloud.getLUT()
        scalarBar=self.scalarBarActor
        scalarBar.SetOrientationToVertical()
        scalarBar.SetLookupTable(lut)
        scalarBar.SetBarRatio(barRatio)
        scalarBar.SetTitleRatio(barRatio)
        scalarBar.SetMaximumWidthInPixels(max_width)
        scalarBar.SetMaximumHeightInPixels(max_height)
        #print(self.scalarBar.GetProperty().SetDisplayLocationToBackground())
        #self.scalarBar.SetDisplayPosition(750,250)
        scalarBar.SetDisplayPosition(5,height)
        textP = vtk.vtkTextProperty()
        textP.SetFontSize(1)
        scalarBar.SetLabelTextProperty(textP)
        scalarBar.SetTitleTextProperty(textP)
        scalarBar.SetNumberOfLabels(10)
        scalarBar.SetLabelFormat("%-#6.2f")#輸出格式
        #self.scalarBarWidget = vtk.vtkScalarBarWidget()
        #self.scalarBarWidget.SetInteractor(self.interactor)
        #self.scalarBarWidget.SetScalarBarActor(self.scalarBar)
        #self.scalarBarWidget.On()
        self.scalarBarActor=scalarBar
        self.refresh_renderer()
    def setCubeAxesActor(self):
        cubeAxesActor = self.cubeAxesActor
        #設定軸上下限
        bounds = self.pointCloud.getBounds()
        cubeAxesActor.SetBounds(bounds)
        #將RENDER CAMERA指定給軸
        cubeAxesActor.SetCamera(self.renderer.GetActiveCamera())
        #設定標題與標籤文字顏色
        cubeAxesActor.GetTitleTextProperty(0).SetColor(0.5,0.5,0.5)
        cubeAxesActor.GetLabelTextProperty(0).SetColor(0.5,0.5,0.5)
        cubeAxesActor.GetTitleTextProperty(1).SetColor(0.5,0.5,0.5)
        cubeAxesActor.GetLabelTextProperty(1).SetColor(0.5,0.5,0.5)
        cubeAxesActor.GetTitleTextProperty(2).SetColor(0.5,0.5,0.5)
        cubeAxesActor.GetLabelTextProperty(2).SetColor(0.5,0.5,0.5)
        #設定坐標軸線寬
        cubeAxesActor.GetXAxesLinesProperty().SetLineWidth(1)
        cubeAxesActor.GetYAxesLinesProperty().SetLineWidth(1)
        cubeAxesActor.GetZAxesLinesProperty().SetLineWidth(1)
        #開啟網格線
        cubeAxesActor.DrawXGridlinesOn()
        cubeAxesActor.DrawYGridlinesOn()
        cubeAxesActor.DrawZGridlinesOn()
        #內部網格線不畫
        cubeAxesActor.SetDrawXInnerGridlines(0)
        cubeAxesActor.SetDrawYInnerGridlines(0)
        cubeAxesActor.SetDrawZInnerGridlines(0)
        #cubeAxesActor.DrawXInnerGridlinesOn()
        #cubeAxesActor.DrawYInnerGridlinesOn()
        #cubeAxesActor.DrawZInnerGridlinesOn()
        #網格線顏色
        cubeAxesActor.GetXAxesGridlinesProperty().SetColor(0.5,0.5,0.5)
        cubeAxesActor.GetYAxesGridlinesProperty().SetColor(0.5,0.5,0.5)
        cubeAxesActor.GetZAxesGridlinesProperty().SetColor(0.5,0.5,0.5)
        #控制軸的繪製方式(外,最近,最遠,靜態最近,靜態外)
        cubeAxesActor.SetFlyMode(1)
        #設定刻度線的位置(內,外,兩側)
        cubeAxesActor.SetTickLocation(1)
        #網格線樣式(所有,最近,最遠)
        cubeAxesActor.SetGridLineLocation(1)
        cubeAxesActor.XAxisMinorTickVisibilityOn()
        cubeAxesActor.YAxisMinorTickVisibilityOn()
        cubeAxesActor.ZAxisMinorTickVisibilityOn()
        self.cubeAxesActor=cubeAxesActor
    def setCubeAxesVisibility(self,switch):
        if switch:
            self.cubeAxesActor.VisibilityOn()
        else:
            self.cubeAxesActor.VisibilityOff()
        self.refresh_renderer()
    def addAxisWidget(self):
        axes = vtk.vtkAxesActor()
        self.axisWidget = vtk.vtkOrientationMarkerWidget()
        self.axisWidget.SetOutlineColor(0.9,0.5,0.1)
        self.axisWidget.SetOrientationMarker(axes)
        self.axisWidget.SetInteractor(self.interactor)
        #self.axisWidget.SetViewport(0,0,0.4,0.4)
        self.axisWidget.EnabledOn()
        self.axisWidget.InteractiveOff()
    def add_newData(self,pcd):
        
        '''
        print("generate xyz")
        for k in range(size(data,0)):
            point = data[k] #20*(random.rand(3)-0.5)
            pcd.addPoint(point)
        self.renderer.AddActor(pcd.vtkActor)
        '''
        self.__removePickedPoints()
        self.ind = pcd[0]
        print("cur ind:", self.ind)
        self.pointCloud=pcd[1][0]
        self.addActor()
    def addActor(self):
        """
        self.pcdCollection.append(self.xyzLoader.pcd)
        print("Current pcd count: ", len(self.pcdCollection))
        #self.actors.append(self.pcdCollection[-1].vtkActor)
        #create each actor from xyz collection
        for i in self.pcdCollection:
            self.renderer.AddActor(i.vtkActor)
            #print(i.vtkActor)
        """
        print("start add actor")
        ind = self.ind
        self.removeAll()
        self.ind = ind
        bounds=self.pointCloud.getBounds()
        zMin=bounds[4]
        zMax=bounds[5]
        r=zMax-zMin
        self.pointCloud.setLUTRange(zMin,zMax)
        isMesh = False
        isDelaunay3D=False
        isSurfRecon=False
        isDelaunay2D=0
        if isMesh:
            self.pointCloud.generateMesh()
            #self.renderer.AddActor(self.pointCloud.vtkActor)
            self.mainActor=self.pointCloud.boundaryActor
        elif isDelaunay3D:
            self.mainActor=self.pointCloud.delaunay3D()
        elif isSurfRecon:
            self.mainActor=self.pointCloud.surfaceRecon()
        elif isDelaunay2D:
            self.delny2d()
        else:
            self.mainActor=self.pointCloud.vtkActor
        print(self.pointCloud)
        self.renderer.AddActor(self.mainActor)
        self.setCubeAxesActor()
        self.renderer.AddActor(self.cubeAxesActor)
        self.setScalarBar()
        self.renderer.AddActor(self.scalarBarActor)
        
        self.renderer.ResetCamera()
        self.refresh_renderer()
        self.pickedID=[]
        self.pickedPoints=[]
        cam = self.renderer.GetActiveCamera()
        self.oriMatrix = cam.GetExplicitProjectionTransformMatrix()
        print("Add actor done.")
    def delny2d(self):
        delny = vtk.vtkDelaunay2D()
        print("1")
        delny.SetInputData(self.pointCloud.vtkPolyData)
        print("1")
        delny.SetSourceData(self.pointCloud.vtkPolyData)
        print("1")
        delny.SetAlpha(1)
        #delny.SetTolerance(1)
        mapper = vtk.vtkPolyDataMapper()
        print("1")
        mapper.SetInputConnection(delny.GetOutputPort())
        mapper.SetColorModeToDefault()
        print("1")
        actor=vtk.vtkActor()
        print("1")
        actor.SetMapper(mapper)
        print("1")
        self.mainActor=actor
    def removeAll(self):
        actors = self.renderer.GetActors()
        #print(actors)
        for i in actors:
            self.renderer.RemoveActor(i)
        for i in range(len(self.pcdCollection)):
            #print(i)
            del self.pcdCollection[-1]
        #print(len(self.pcdCollection))
        self.ind=""
        self.pcdCollection=[]
        self.actors = []
        self.pickedID=[]
        self.pickedPoints=[]
        self.refresh_renderer()
    def reset_Camera(self):
        #print(self.oriMatrix)
        center_x,center_y,center_z=self.mainActor.GetCenter()
        cam = self.renderer.GetActiveCamera()
        cam.SetPosition(center_x,center_y,center_z+100)
        cam.SetViewUp(0,1,0)
        self.renderer.ResetCamera()
        self.refresh_renderer()
    def setCameraTop(self):
        center_x,center_y,center_z=self.mainActor.GetCenter()
        cam=self.renderer.GetActiveCamera()
        cam.SetPosition(center_x+100,center_y,center_z)
        cam.SetViewUp(0,0,1)
        cam.Azimuth(90)
        print(cam.GetPosition())
        #self.renderer.SetActiveCamera(cam)
        self.renderer.ResetCamera()
        self.refresh_renderer()
    def setCameraLeft(self):
        self.renderer.ResetCamera()
        cam=self.renderer.GetActiveCamera()
        #cam.SetPosition(0,0,0)
        #cam.SetViewUp(0,1,0)
        cam.Azimuth(-10)
        #self.renderer.SetActiveCamera(cam)
        self.renderer.ResetCamera()
        self.refresh_renderer()
    def setCameraRight(self):
        self.renderer.ResetCamera()
        cam=self.renderer.GetActiveCamera()
        #cam.SetPosition(0,0,0)
        #cam.SetViewUp(0,1,0)
        cam.Azimuth(10)
        #self.renderer.SetActiveCamera(cam)
        self.renderer.ResetCamera()
        self.refresh_renderer()
    def refresh_renderer(self):
        #self.renderer.ResetCamera()
        renderWindow = self.interactor.GetRenderWindow()
        renderWindow.Render()
    def applyXTransform(self,x):
        w = vtk.vtkTransform()
        w.RotateX(float(x))
        self.pointCloud.setRTFilter(w)
        self.addActor()
        self.refresh_renderer()
    def applyYTransform(self,y):
        w = vtk.vtkTransform()
        w.RotateX(float(y))
        self.pointCloud.setRTFilter(w)
        self.addActor()
        self.refresh_renderer()
    def applyZTransform(self,z):
        w = vtk.vtkTransform()
        w.RotateX(float(z))
        self.pointCloud.setRTFilter(w)
        self.addActor()
        self.refresh_renderer()
    def applyTransform(self,x,y,z):
        center_x,center_y,center_z=self.mainActor.GetCenter()
        w = vtk.vtkTransform()
        #w.Translate(-center_x,-center_y,-center_z)
        #vtk not auto change type from string to double
        w.RotateX(float(x))
        w.RotateY(float(y))
        w.RotateZ(float(z))
        #self.mainActor.SetUserTransform(w)
        #self.scalarBarActor.SetUserTransform(w)
        #self.cubeAxesActor.SetUserTransform(w)
        self.pointCloud.setRTFilter(w)
        self.addActor()
        self.refresh_renderer()
    def setParallelCamera(self,state):
        cam = self.renderer.GetActiveCamera()
        cam.SetParallelProjection(state)
        self.renderer.ResetCamera()
        self.refresh_renderer()
    def changeMode(self,mode):
        #change vtk picker mode
        self.__setInterActorModeAsPickerMode(mode)
    def __setInterActorModeAsPickerMode(self,pickingMode):
        import pointPicker as pStyle
        print(pStyle)
        print(pickingMode)
        if pickingMode==1:
            self.interactor.SetInteractorStyle(pStyle.testStyle(self.emitPickedPoint,self.__removePickedPoints,self.__setTransformMatrix,self.interactor))
        else:
            self.interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    def emitPickedPoint(self,pointId):
        self.pickedID.append(pointId)
        x,y,z=self.pointCloud.vtkPoints.GetPoint(pointId)
        p=(x,y,z)
        self.pickedPoints.append(p)
        print("emit:",pointId,x,y,z)
        px = "{:.3f}".format(x)
        py = "{:.3f}".format(y)
        pz = "{:.3f}".format(z)
        txt = "Picked:"+px+","+py+","+pz
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetCenter(x,y,z)
        sphereSource.SetRadius(1)
        sphereSource.SetThetaResolution(10)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphereSource.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1,0,0)
        #actor.GetProperty().SetRepresentationToWireframe()
        print(actor)
        actors = self.renderer.GetActors()
        print(actors)
        self.renderer.AddActor(actor)
        self.refresh_renderer()
    def getPickedID(self):
        return self.pickedID
    def __removePickedPoints(self):
        count = len(self.pickedID)
        print("picked count:",count)
        if count>0:
            for i in range(count):
                actors = self.renderer.GetActors()
                self.renderer.RemoveActor(actors.GetLastActor())
        self.pickedID=[]
        self.refresh_renderer()
    def __setTransformMatrix(self):
        if(len(self.pickedPoints)<3):
            return
        p0 = self.pickedPoints[0]
        p1 = self.pickedPoints[1]
        p2 = self.pickedPoints[2]
        a = numpy.array([p0[0],p0[1],p0[2]])
        b = numpy.array([p1[0],p1[1],p1[2]])
        c = numpy.array([p2[0],p2[1],p2[2]])
        print("norm: ",b-a,c-a)
        n = numpy.cross(b-a,c-a)
        nn = n/numpy.linalg.norm(n)
        print("normal: ",nn)
        z_axis= numpy.array([0,0,1])
        x_axis = numpy.array([1,0,0])
        y_axis = numpy.array([0,1,0])
        rad_z=numpy.arccos(numpy.dot(nn,z_axis))
        rad_x=numpy.arccos(numpy.dot(nn,x_axis))
        rad_y=numpy.arccos(numpy.dot(nn,y_axis))
        print("radian: ",rad_z)
        rot_axis = numpy.cross(nn,z_axis)
        print("rotation axis: ",rot_axis)
        angles = numpy.abs(numpy.arcsin(nn))
        degrees = numpy.degrees(angles)
        deg_z=numpy.degrees(rad_z)
        deg_y=numpy.degrees(rad_y)
        deg_x=numpy.degrees(rad_x)
        print("angles: ",angles)
        print("degrees: ",degrees)
        print("deg_: ", deg_x,deg_y,deg_z)
        self.applyXTransform(deg_x)
        self.applyYTransform(deg_y)
        self.applyZTransform(deg_z)
        #self.applyTransform(degrees[0],degrees[1],degrees[2])
    def projectionPlane(self):
        b=self.pointCloud.getBounds()
        print("get boundary",b)
        print("create projection plane")
        projectPoints =  projectXYplane(b[4]-1,self.pointCloud.vtkPoints)
        pPointsY=projectXZplane(b[2]-1,self.pointCloud.vtkPoints)
        pPointsX=projectYZplane(b[0]-1,self.pointCloud.vtkPoints)
        print("y boundary",b[2])
        '''
        pZ = vtk.vtkPlane()
        pZ.SetOrigin(0,0,b[4]-1)
        pZ.SetNormal(0,0,1)
        print("create projection points")
        projectPoints = vtk.vtkPoints()
        print("set projection points")
        for i in range(self.pointCloud.vtkPoints.GetNumberOfPoints()):
            p=self.pointCloud.vtkPoints.GetPoint(i)
            #print("pts:",p)
            projectedPoint=numpy.zeros(3)
            pZ.ProjectPoint(p,projectedPoint)
            #print("pts:",projectedPoint)
            projectPoints.InsertNextPoint(projectedPoint)
        '''
        print("Get projected points",projectPoints)
        aaa = vtk.vtkPolyData()
        print("Add point source",aaa)
        aaa.SetPoints(projectPoints)
        abc=vtk.vtkPolyData()
        abc.SetPoints(pPointsY)
        ccc=vtk.vtkPolyData()
        ccc.SetPoints(pPointsX)
        '''
        create 2d delaunay mesh
        delny = vtk.vtkDelaunay2D()
        delny.SetTolerance(0.01)
        delny.SetInputData(aaa)
        delny.SetSourceData(aaa)
        '''
        
        '''
        #create edges
        extract = vtk.vtkExtractEdges()
        extract.SetInputConnection(delny.GetOutputPort())
        '''
        vertexGlyphFilter = vtk.vtkVertexGlyphFilter()
        vertexGlyphFilter.SetInputData(aaa)
        vertexGlyphFilter.Update()
        vertexGlyphFilter1 = vtk.vtkVertexGlyphFilter()
        vertexGlyphFilter1.SetInputData(abc)
        vertexGlyphFilter1.Update()
        vertexGlyphFilter2 = vtk.vtkVertexGlyphFilter()
        vertexGlyphFilter2.SetInputData(ccc)
        vertexGlyphFilter2.Update()
        print("Add mapper")
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(vertexGlyphFilter.GetOutputPort())
        mapper1 = vtk.vtkPolyDataMapper()
        mapper1.SetInputConnection(vertexGlyphFilter1.GetOutputPort())
        mapper2 = vtk.vtkPolyDataMapper()
        mapper2.SetInputConnection(vertexGlyphFilter2.GetOutputPort())
        print("set Actor")
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0,0,1)
        actor1 = vtk.vtkActor()
        actor1.SetMapper(mapper1)
        actor1.GetProperty().SetColor(0,1,0)
        actor2 = vtk.vtkActor()
        actor2.SetMapper(mapper2)
        actor2.GetProperty().SetColor(1,0,0)
        print("Add Actor",actor)
        self.renderer.AddActor(actor)
        self.renderer.AddActor(actor1)
        self.renderer.AddActor(actor2)
        self.refresh_renderer()
        print("refresh renderer")
    def drawParametricSpline(self,IDList):
        points = vtk.vtkPoints()
        for i in IDList:
            p=self.pointCloud.vtkPoints.GetPoint(i)
            points.InsertNextPoint(p)
        spline = vtk.vtkParametricSpline()
        spline.SetPoints(points)
        functionSource = vtk.vtkParametricFunctionSource()
        functionSource.SetParametricFunction(spline)
        functionSource.Update()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(functionSource.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self.renderer.AddActor(actor)
        self.refresh_renderer()
    def drawKochanekSpline(self,IDList):
        points = vtk.vtkPoints()
        for i in IDList:
            p=self.pointCloud.vtkPoints.GetPoint(i)
            points.InsertNextPoint(p)
        xSpline = vtk.vtkKochanekSpline()
        ySpline = vtk.vtkKochanekSpline()
        zSpline = vtk.vtkKochanekSpline()
        spline = vtk.vtkParametricSpline()
        spline.SetXSpline(xSpline)
        spline.SetYSpline(ySpline)
        spline.SetZSpline(zSpline)
        spline.SetPoints(points)
        functionSource = vtk.vtkParametricFunctionSource()
        functionSource.SetParametricFunction(spline)
        functionSource.Update()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(functionSource.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self.renderer.AddActor(actor)
        self.refresh_renderer()
    def SurfaceReconstruction(self):
        pointSource=vtk.vtkProgrammableSource()
        def readPoints():
            output = pointSource.GetPolyDataOutput()
            points = vtk.vtkPoints()
            output.SetPoints(points)
            for i in IDList:
                p=self.pointCloud.vtkPoints.GetPoint(i)
                points.InsertNextPoint(p)
        pointSource.SetExecuteMethod(readPoints)
        surf = vtk.vtkSurfaceReconstructionFilter()
        surf.SetInputConnection(pointSource.GetOutputPort())
        cf = vtk.vtkContourFilter()
        cf.SetInputConnection(surf.GetOutputPort())
        cf.SetValue(0,0)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cf.GetOutputPort())
        mapper.ScalarVisibilityOff()
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetDiffuseColor(1,0.3882,0.2784)
        actor.GetProperty().SetSpecularColor(1,1,1)
        actor.GetProperty().SetSpecular(.4)
        actor.GetProperty().SetSpecularPower(50)
        self.renderer.AddActor(actor)
        self.refresh_renderer()
    def closeWindow(self):
        print("close vtk")
        renderWindow = self.interactor.GetRenderWindow()
        renderWindow.Finalize()
        self.interactor.TerminateApp()
        #del render_window, sefl.interactor
    def __del__(self):
        self.closeWindow()
        
if __name__=="__main__":
	print("xyz viewer")
