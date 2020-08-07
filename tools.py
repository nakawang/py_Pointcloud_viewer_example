import pandas as pd
import open3d as o3d
import numpy,time
import vtk
from vtk.util import numpy_support
from vtkPointCloud import VtkPointCloud
import json
def getVtkPointCloud(path,downsampling=0):
    print(time.time())
    isNotOk = True
    while isNotOk:
        try:
            f=open(path)
            isNotOk = False
        except:
            isNotOk = True
    pd_xyzrgb = pd.read_csv(f,header=None,delim_whitespace=True,dtype=float,usecols=[0,1,2])
    print(time.time())
    #rgb = pd.read_csv(path,header=None,delim_whitespace=True,dtype=float,usecols=[3,4,5])
    pd_xyzrgb = pd_xyzrgb.values
    xyz = pd_xyzrgb[:,[0,1,2]]
    #rgb = pd_xyzrgb[:,[3,4,5]]
    #print(xyz)
    #Create open3d pcd format========================
    p3d = o3d.geometry.PointCloud()
    p3d.points=o3d.utility.Vector3dVector(xyz)
    #================================================
    '''
    downsample by open3d
    '''
    if downsampling==1:
        print("donwsample by open3d")
        p3d = o3d.geometry.PointCloud()
        p3d.points=o3d.utility.Vector3dVector(xyz)
        print("np to open3d")
        downpcd = p3d.voxel_down_sample(voxel_size=0.5)
        print("voxel down sample")
        cl,ind=downpcd.remove_statistical_outlier(nb_neighbors=50,std_ratio=3.0)
        #print(cl,ind)
        #downpcd = downpcd.select_by_index(ind)
        xyz=numpy.asarray(cl.points)
        print("numpy array")
    
    #================================================
    print(time.time())
    '''
    print(xyz)
    theta1=numpy.radians(35)
    theta2=numpy.radians(5)
    c1,c2,s1,s2=numpy.cos(theta1),numpy.cos(theta2),numpy.sin(theta1),numpy.sin(theta2)
    rx=numpy.array(((1,0,0),(0,c1,-s1),(0,s1,c1)))
    ry=numpy.array(((c2,0,s2),(0,1,0),(-s2,0,c2)))
    xyz=xyz.dot(rx)
    print(xyz)
    xyz=xyz.dot(ry)
    '''
    #rgb = rgb.values
    #print(xyz,rgb)
    #xyz = loadtxt(self.fileName,dtype=float,usecols=[0,1,2])
    minH=xyz[:,2].min()
    maxH=xyz[:,2].max()
    #print("minh,maxh:",minH,maxH)
    count = len(xyz)
    #print(len(xyz.shape))
    pcd=VtkPointCloud(minH,maxH,count)
    pcd.clearPoints()
    counter=numpy.size(xyz,0)
    #print(counter)
    #test np to vtk array
    nCoords = xyz.shape[0]
    nElem = xyz.shape[1]
    #print("c,e",nCoords,nElem)
    #print("xyz",xyz)
    depth = xyz[:,2]
    #print("depth",depth)
    #colors = numpy_support.numpy_to_vtk(rgb)
    vtkDepth = numpy_support.numpy_to_vtk(depth)
    cells_npy = numpy.vstack([numpy.ones(nCoords,dtype=numpy.int64),
                           numpy.arange(nCoords,dtype=numpy.int64)]).T.flatten()
    #print("cells_npy",cells_npy)
    cells = vtk.vtkCellArray()
    cells.SetCells(nCoords,numpy_support.numpy_to_vtkIdTypeArray(cells_npy))
    #print("cells",cells)
    vtkArray=numpy_support.numpy_to_vtk(xyz)
    verts = vtk.vtkPoints()
    verts.SetData(vtkArray)
    #print(vtkArray)
    pcd.setPoints(vtkArray,nCoords,numpy_support.numpy_to_vtkIdTypeArray(cells_npy),vtkDepth)

    '''
    for k in range(size(xyz,0)):
        self.signalNow.emit(k)
        point = xyz[k]
        pcd.addPoint(point)
    '''
    print(time.time())
    data = [pcd,p3d]
    return data
def o3dp3dTovtkPCD(p3d):
    xyz=numpy.asarray(p3d.points)
    minH=xyz[:,2].min()
    maxH=xyz[:,2].max()
    #print("minh,maxh:",minH,maxH)
    count = len(xyz)
    #print(len(xyz.shape))
    pcd=VtkPointCloud(minH,maxH,count)
    pcd.clearPoints()
    counter=numpy.size(xyz,0)
    #print(counter)
    #test np to vtk array
    nCoords = xyz.shape[0]
    nElem = xyz.shape[1]
    #print("c,e",nCoords,nElem)
    #print("xyz",xyz)
    depth = xyz[:,2]
    #print("depth",depth)
    #colors = numpy_support.numpy_to_vtk(rgb)
    vtkDepth = numpy_support.numpy_to_vtk(depth)
    cells_npy = numpy.vstack([numpy.ones(nCoords,dtype=numpy.int64),
                           numpy.arange(nCoords,dtype=numpy.int64)]).T.flatten()
    #print("cells_npy",cells_npy)
    cells = vtk.vtkCellArray()
    cells.SetCells(nCoords,numpy_support.numpy_to_vtkIdTypeArray(cells_npy))
    #print("cells",cells)
    vtkArray=numpy_support.numpy_to_vtk(xyz)
    verts = vtk.vtkPoints()
    verts.SetData(vtkArray)
    #print(vtkArray)
    pcd.setPoints(vtkArray,nCoords,numpy_support.numpy_to_vtkIdTypeArray(cells_npy),vtkDepth)
    return pcd
def calcO3DRT(target,picked_id_target,source,picked_id_source):
    print("source points: ",picked_id_source)
    print("target points: ",picked_id_target)
    assert(len(picked_id_source)>=3 and len(picked_id_target)>=3)
    assert(len(picked_id_source) == len(picked_id_target))
    corr = numpy.zeros((len(picked_id_source),2))
    corr[:,0] = picked_id_source
    corr[:,1] = picked_id_target
    print(corr)
    # estimate rough transformation using correspondences
    print("Compute a rough transform using the correspondences given by user")
    p2p = o3d.registration.TransformationEstimationPointToPoint(with_scaling=False)
    trans_init = p2p.compute_transformation(source, target,
             o3d.utility.Vector2iVector(corr))
    print(trans_init)
    return trans_init
def manualRegistration(target,source,trans_init):
    threshold = 0.001 # 1cm distance threshold
    #reg_p2p = o3d.registration.registration_icp(source, target, threshold, trans_init,o3d.registration.TransformationEstimationPointToPoint(),o3d.registration.ICPConvergenceCriteria(max_iteration = 500))
    #source.transform(reg_p2p.transformation)
    source.transform(trans_init)
    fin=source+target
    #downfin=o3d.geometry.PointCloud.voxel_down_sample(fin,voxel_size=0.5)
    #o3d.io.write_point_cloud("D:\\testMerged.xyz",fin)
    return fin
def loadTrans_init(fpath):
    np_trans_init = []
    with open(fpath,'r') as f:
        trans_init_list = json.load(f)
        for i in trans_init_list:
            np_trans_init.append(numpy.array(i))
    #print(np_trans_init[0])
    return np_trans_init
def saveTrans_init(fpath,trans_init):
    trans_init_list = []
    for i in trans_init:
        trans_init_list.append(i.tolist())
    with open(fpath,'w') as f:
        json.dump(trans_init_list,f)
    return
def downsample(p3d,voxel_size=0.3):
    downpcd = p3d.voxel_down_sample(voxel_size)
    print("voxel down sample ", downpcd)
    cl,ind=downpcd.remove_statistical_outlier(nb_neighbors=50,std_ratio=3.0)
    print(cl,ind)
    #downpcd = downpcd.select_by_index(ind)
    return cl
def applyTransform(target,source,trans_init):
    target = target[1][1]
    #target = downsample(target)
    source = source[1][1]
    #source = downsample(source)
    threshold = 0.01
    #re calc icp registration
    #reg_p2p = o3d.registration.registration_icp(source, target, threshold, trans_init,o3d.registration.TransformationEstimationPointToPoint(),o3d.registration.ICPConvergenceCriteria(max_iteration = 2000))
    #source.transform(reg_p2p.transformation)
    source=source.transform(trans_init)
    mergedP3D=target+source
    #mergedP3D = downsample(mergedP3D)
    vtkPCD = o3dp3dTovtkPCD(mergedP3D)
    d = [vtkPCD,mergedP3D]
    #o3d.io.write_point_cloud("D:\\Testdata\\test0606.xyz",mergedP3D)
    return d
if __name__=="__main__":
    path="D:\\3.db"
    loadTrans_init(path)
