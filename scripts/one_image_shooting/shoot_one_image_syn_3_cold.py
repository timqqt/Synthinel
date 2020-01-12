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
import random

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
def importFbxCamera(fbxfile):
   
    data = parseFbxCam(fbxfile)
    if(data[0] and data[1]) :
        data[0][0]='-300'
        data[0][1] = '5250'
        data[0][2]= '-100'
        data[1][0] = data[1][1]='-90'
        data[1][0] = data[1][1]='-90'
        v = setCamData(data)
        print "Camera set to "+str(data)
        return v
    else:
        print "No camera data found in file "+file

def exportImages(directory, v, Tag=""):
   path = directory + "\_" + Tag + "_RGB.png"
   v.snapshot(path, width=5000, height=5000)

def exportGroundtruths(directory, v, Tag=""):
   path = directory + "\_" + Tag + "_GT.png"
   v.snapshot(path)

def load_rule_file(rule_file_path, objs):
    all_shapes = ce.getObjectsFrom(ce.scene, objs)
    ce.setRuleFile(all_shapes, rule_file_path)
    ce.generateModels(all_shapes)
    ce.waitForUIIdle()
    
def dynamic_attributes(adjust_list, camera_angle, light_angle, light_intensity, dynamic_range):
    '''
    adjust_list: a list of strings
    camera_angle: number between 0~90
    light_angle: number between 0~90
    light_instensity: number between 0~1
    dynamic_range: a dictionary has the form
        {'ca': int, 'la': int, 'li': int}
        The value  will vary in range of [sv-dv, sv+dv]
    '''
    lightSettings = ce.getLighting()
    assert ('la' in adjust_list) or ('ca' in adjust_list) or ('li' in adjust_list), "Please select an attribute to augment"
    if 'la' in adjust_list:
        light_angle = light_angle + random.randint(-dynamic_range['la'], dynamic_range['la'])
        lightSettings.setSolarElevationAngle(light_angle)
    if 'ca' in adjust_list:
        camera_angle = camera_angle + random.randint(-dynamic_range['ca'], dynamic_range['ca'])
        camera_angle = '-' + str(camera_angle)
    if 'li' in adjust_list:
        light_intensity = min(1, light_intensity + 0.1 * random.randint(-int(10*dynamic_range['li']), int(10*dynamic_range['li'])))
        lightSettings.setSolarIntensity(light_intensity)    
    ce.setLighting(lightSettings)
    print("New attribute triple bracket is ", (light_angle, camera_angle, light_intensity))
    return camera_angle

if __name__ == '__main__':
    
    dynamic_range={'ca': 0, 'la': 0, 'li': 0}
    
    camfile = ce.toFSPath("data/camera.fbx")
    view = importFbxCamera(camfile)
    
    ########################
        #default adjust
    adjust_list = ['la', 'ca', 'li']
    camera_angle = -90
    light_angle = 50 
    light_intensity=1 
    ###########################
    dynamic_attributes(adjust_list, camera_angle, light_angle, light_intensity, dynamic_range)
    #load_rule_file('paris.cga', ce.isBlock)
    exportImages(ce.toFSPath('images'), view, Tag='random_city_2')
    
    ########################
        #default adjust
    adjust_list = ['la', 'ca', 'li']
    camera_angle = -90
    light_angle = 90 
    light_intensity=1 
    ###########################
    dynamic_attributes(adjust_list, camera_angle, light_angle, light_intensity, dynamic_range)
    load_rule_file('Synthinel_rules/international_city_3_cold_city_labelling.cga', ce.isBlock)
    exportGroundtruths(ce.toFSPath('images'), view, Tag='random_city_2')
    # exportGroundtruths(ce.toFSPath('images'), view, Tag='Vienna_5')