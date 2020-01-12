'''
Created on 09.03.2010

@author: andi

* reads current position, rotation from fbx file
* sets CE camera to the parsed values
Note: camera needs to be exported as single object. 
anim curves are not read, only camera transformation of current frame
fbx file needs to be ascii, version <= 2010, y-Up

'''
from scripting import *
import math

# get a CityEngine instance
ce = CE()



'''
parse lines and look for id
prepare cam data in array
non-generic, works for specific fbx part only
'''
def parseLine(lines, id):
    data = False
    for line in lines:
        if line.find(id) >=0 :
            data = line.partition(id)[2]
            break
    if data:
        data = data[:len(data)-1] # strip \n
        data = data.split(",")        
    return data

'''
parse lines from fbx file that store cam data
'''
def parseFbxCam(filename):
    f=open(filename)
    lines = f.readlines()
    cnt = 0
    loc =  parseLine(lines, 'Property: "Lcl Translation", "Lcl Translation", "A+",')
    rot =  parseLine(lines, 'Property: "Lcl Rotation", "Lcl Rotation", "A+",')
    return [loc,rot]



'''
helper functions
'''
def setCamPosV(v, vec):
    v.setCameraPosition(vec[0], vec[1], vec[2])
    
def setCamRotV(v, vec):
    v.setCameraRotation(vec[0], vec[1], vec[2])



'''
sets camera on first CE viewport
'''
def setCamData(data):
    v = ce.getObjectsFrom(ce.get3DViews(), ce.isViewport)[0]
    setCamPosV(v, data[0])
    setCamRotV(v, data[1])
    return v





'''
master function
'''

def degree_to_radian(d):
    return d*math.pi/180

def angle_transformation(x, y, height, angle):
    if angle == 90:
        return x, y, height, angle
    d = 2 * height * math.tan(degree_to_radian(7.5))    
    n_height = d * (math.cos(degree_to_radian(15))-math.cos(degree_to_radian(2*angle)))/(2*math.sin(degree_to_radian(15)))
    n_x =  x - (height-n_height) * math.tan(degree_to_radian(angle))
    n_y = y
    return n_x, n_y, n_height, angle

def importFbxCamera(fbxfile):
    x, y, height, angle = 0, 0, 652.2, 50
    x, y, height, angle = angle_transformation(x, y, height, angle)
    print(x)
    print(height)
    data = parseFbxCam(fbxfile)
    if(data[0] and data[1]) :
        #x, y, height = angle_transformation()
        data[0][0]= str(x)
        data[0][1] = str(height)
        data[0][2]= str(y)
        #data[1][0] = data[1][1]='-70'
        data[1][0] = '-' + str(angle)
        data[1][1] = '-90'
        v = setCamData(data)
        print "Camera set to "+str(data)
        return v
    else:
        print "No camera data found in file "+file

def exportImages(directory, v, Tag=""):
   path = directory + "\_" + Tag + "_RGB.png"
   v.snapshot(path, width=572, height=572)

def exportGroundtruths(directory, v, Tag=""):
   path = directory + "\_" + Tag + "_GT.png"
   v.snapshot(path, width=572, height=572)
   
if __name__ == '__main__':
    camfile = ce.toFSPath("data/camera.fbx")
    view = importFbxCamera(camfile)
    #exportImages(ce.toFSPath('images'), view, Tag='angle_change_tst1')
    #exportGroundtruths(ce.toFSPath('images'), view, Tag='random_city_6')