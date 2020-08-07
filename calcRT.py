from math import sin,cos,asin,acos,atan,tan
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def calcTheta(p1,p2,p3):
    a = [p1,p2,p3]
    print(a)
    a=np.array(a)
    b = [0,0,0]
    b=np.array(b)
    x=np.linalg.solve(a,b)
    print(x)
    thetaX = asin(x[1])
    thetaY = atan(-x[0]/x[2])
    return thetaX,thetaY
def calcRTxy(x,y):
    r1=[cos(y),0,sin(y)]
    r2=[0,1,0]
    r3=[-sin(y),0,cos(y)]
    ry=np.array([r1,r2,r3])
    rr1=[1,0,0]
    rr2=[0,cos(x),-sin(x)]
    rr3=[0,sin(x),cos(x)]
    rx=np.array([rr1,rr2,rr3])
    return rx,ry
def calcPos(p,rx,ry):
    py=np.dot(p,ry)
    px=np.dot(py,rx)
    return px
def fitPlane(points):
    tmp_A = []
    tmp_b = []
    for i in range(len(points)):
        print(points[i])
        p=points[i]
        tmp_A.append([p[0], p[1], 1])
        tmp_b.append(p[2])
    b = np.matrix(tmp_b).T
    A = np.matrix(tmp_A)
    fit = (A.T * A).I * A.T * b
    errors = b - A * fit
    residual = np.linalg.norm(errors)
    
    print("solution:")
    print("%f x + %f y + %f = z" % (fit[0], fit[1], fit[2]))
    print("errors:")
    print(errors)
    print("residual:")
    print(residual)
    a=[[row[i] for row in points] for i in range(3)]
    # plot raw data
    plt.figure()
    ax = plt.subplot(111, projection='3d')
    ax.scatter(a[0], a[1], a[2], color='b')
    # plot plane
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    X,Y = np.meshgrid(np.arange(xlim[0], xlim[1]),np.arange(ylim[0], ylim[1]))
    Z = np.zeros(X.shape)
    for r in range(X.shape[0]):
        for c in range(X.shape[1]):
            Z[r,c] = fit[0] * X[r,c] + fit[1] * Y[r,c] + fit[2]
    ax.plot_wireframe(X,Y,Z, color='k')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()
    if fit[2]<0:
        fit=-fit
    return fit
def calcRTT(fit):
    xy_normal = np.array([0,0,1])
    print(xy_normal)
    normal = fit
    axis = np.cross(normal.T,xy_normal.T)
    theta = np.arccos(fit[2]/np.sqrt(fit[0]**2+fit[1]**2+fit[2]**2))
    print(theta)
    return theta
if __name__=="__main__":
    p1=[3,2,1]
    p2=[4,1,4]
    p3=[5,3,3]
    p=[p1,p2,p3]
    fit = fitPlane(p)
    print(fit.T)
    calcRTT(fit)
