'''
Created on 06.26.2019

@author: Fanjie Kong



'''
from scripting import *
import time
import random
# get a CityEngine instance
ce = CE()


def dynamic_attributes(adjust_list, camera_angle, light_angle, light_intensity, dynamic_range, mode):
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
    if mode == 'GT':
        return camera_angle
    ce.setLighting(lightSettings)
    print("New attribute triple bracket is ", (light_angle, camera_angle, light_intensity))
    return camera_angle

'''
parse lines and look for id
prepare cam data in array
non-generic, works for specific fbx part only
'''
def drange(x, y, jump):
      while x < y:
        yield x
        x += jump

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
def importFbxCamera(fbxfile, axis, angle, height):
    
    data = parseFbxCam(fbxfile)
    if(data[0] and data[1]) :
        data[0][0]=str(axis[0])
        data[0][1] = height 
        data[0][2]= str(axis[1])
        data[1][0] = data[1][1] = angle
        v = setCamData(data)
        #print "Camera set to "+str(data)
        return v
    else:
        print "No camera data found in file "+file

def exportImages(directory, v, Tag=""):
   path = directory + "/_" + Tag + "_RGB.jpg"
   v.snapshot(path)

def exportGroundtruths(directory, v, Tag=""):
    path = directory + "/_" + Tag + "_GT.jpg"
    v.snapshot(path)
   
def exportGroundtruths2(directory, v, Tag=""):
   path = directory + "/_" + Tag + "_GT2.jpg"
   v.snapshot(path)

def loop_capturer_dynamic_attributes(start_axis, step, end_axis, tag,
                                     adjust_list = ['la', 'ca', 'li'],
                                     light_angle = 90, light_intensity=1, 
                                     dynamic_range={'ca': 10, 'la': 10, 'li': 0.2},
                                     camera_angle=90, height='340',mode='RGB'):
    counter = 0
    print('Start Shooting!')
    print(start_axis[0], end_axis[0], step)
    for i in drange(start_axis[0], end_axis[0], step):
        for j in drange(start_axis[1], end_axis[1], step):
            camfile = ce.toFSPath("data/camera.fbx")
            
            angle = dynamic_attributes(adjust_list, camera_angle, light_angle, light_intensity, dynamic_range, mode)
            view = importFbxCamera(camfile, (i, j), angle, height)
            counter += 1
            print(counter)
            time.sleep(0.02)
            if mode == 'RGB':
                exportImages(ce.toFSPath('images'), view, Tag=tag+'_'+str(counter))
            elif mode == 'GT':
                lightSettings = ce.getLighting()
                lightSettings.setSolarElevationAngle(90)
                lightSettings.setSolarIntensity(1)    
                ce.setLighting(lightSettings)
                ce.waitForUIIdle() 
                exportGroundtruths(ce.toFSPath('images'), view, Tag=tag+'_'+str(counter))
            elif mode == 'GT2':
                lightSettings = ce.getLighting()
                lightSettings.setSolarElevationAngle(90)
                lightSettings.setSolarIntensity(1)    
                ce.setLighting(lightSettings)
                exportGroundtruths2(ce.toFSPath('images'), view, Tag=tag+'_'+str(counter)) #break

def load_rule_file(rule_file_path, objs):
    all_shapes = ce.getObjectsFrom(ce.scene, objs)
    ce.setRuleFile(all_shapes, rule_file_path)
    ce.generateModels(all_shapes)
    ce.waitForUIIdle() 
                    
if __name__ == '__main__':
    '''
    shoot each location with a combination of randomized parameters in a range
    eg: 
    adjust_list = ['la', 'ca', 'li'], # list of parameters to be randomized
    light_angle=45,  camera_angle=80, light_intensity=0.8,  # centers of the range
    dynamic_range={'ca': 10, 'la': 15, 'li': 0.3} # the width of the range
    
    This set of parameters means shoot an image
     where camera angle is a random number in [70, 90],
     light angle is a random number in [30, 60],
     light intensity is a random number in [0.5, 1] 
    
    '''
    random.seed(1)
    start_time = time.time()
    load_rule_file('full_diver_syn_again/international_city_1_colorful.cga', ce.isShape)
    loop_capturer_dynamic_attributes(start_axis=(-2800, -550), step=245, end_axis=(2200,2000), 
                                     tag='dynamic2_syn_la45_ca70_li6_1', adjust_list = ['la', 'ca', 'li'],
                                     light_angle=45,  camera_angle=80, light_intensity=0.8, 
                                     dynamic_range={'ca': 10, 'la': 15, 'li': 0.3},
                                     height='930', mode='RGB')
    load_rule_file('full_diver_syn_again/International_city_labeling.cga', ce.isBlock)
    random.seed(1)
    loop_capturer_dynamic_attributes(start_axis=(-2800, -550), step=245, end_axis=(2200,2000), 
                                     tag='dynamic2_syn_la45_ca70_li6_1', adjust_list = ['la', 'ca', 'li'],
                                     light_angle=45,  camera_angle=80, light_intensity=0.8, 
                                     dynamic_range={'ca': 10, 'la': 15, 'li': 0.3},
                                     height='930', mode='GT')
    print('Duration: {}'.format(time.time()-start_time))
