'''
Created on 2019-9-12

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
    #assert ('la' in adjust_list) or ('ca' in adjust_list) or ('li' in adjust_list), "Please select an attribute to augment"
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
   v.snapshot(path, width=572, height=572)

def exportGroundtruths(directory, v, Tag=""):
    path = directory + "/_" + Tag + "_GT.jpg"
    v.snapshot(path, width=572, height=572)
   
def exportGroundtruths2(directory, v, Tag=""):
   path = directory + "/_" + Tag + "_GT2.jpg"
   v.snapshot(path, width=572, height=572)

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
                exportImages(ce.toFSPath('images/syn_data'), view, Tag=tag+'_'+str(counter))
            elif mode == 'GT':
                lightSettings = ce.getLighting()
                lightSettings.setSolarElevationAngle(90)
                lightSettings.setSolarIntensity(1)    
                ce.setLighting(lightSettings)
                ce.waitForUIIdle() 
                exportGroundtruths(ce.toFSPath('images/syn_data'), view, Tag=tag+'_'+str(counter))
            elif mode == 'GT2':
                lightSettings = ce.getLighting()
                lightSettings.setSolarElevationAngle(90)
                lightSettings.setSolarIntensity(1)    
                ce.setLighting(lightSettings)
                exportGroundtruths2(ce.toFSPath('images/syn_data'), view, Tag=tag+'_'+str(counter)) #break

    
def load_rule_file(rule_file_path, objs):
    print('load rule file ' + rule_file_path)
    #all_shapes = ce.getObjectsFrom(ce.scene, objs)
    ce.setRuleFile(objs, rule_file_path)
    ce.generateModels(objs)
    ce.waitForUIIdle()
    
if __name__ == '__main__':
    start_time = time.time()
    # Close the basemap of Venice
    mapLayers = ce.getObjectsFrom(ce.scene, ce.isMapLayer)
    mapLayers[0].setVisible(False) 
    ############################
    # Syn 1 vienna style
    oid = 'a8127ace-7f7c-11b2-9897-0081d75d416c'
    object = ce.findByOID(oid)
    ce.setSelection(object)
    object = ce.getObjectsFrom(ce.selection)
    load_rule_file('Synthinel_rules/international_city_1_vienna.cga', object)
    random.seed(1)
    loop_capturer_dynamic_attributes(start_axis=(-1500, -1200), 
                                     step=245, end_axis=(500,900), 
                                     tag='syn1_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=60,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='RGB')
    random.seed(1)
    load_rule_file('Synthinel_rules/international_city_1_vienna_labelling.cga', object)
    loop_capturer_dynamic_attributes(start_axis=(-1500, -1200), 
                                     step=245, end_axis=(500,900), 
                                     tag='syn1_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=90,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='GT')
    
    load_rule_file('__', object)
    # Syn 2 Paris style
    oid = '3cb6ef91-7fc1-11b2-9897-0081d75d416c'
    object = ce.findByOID(oid)
    ce.setSelection(object)
    object = ce.getObjectsFrom(ce.selection)
    load_rule_file('paris.cga', object)
    random.seed(1)
    loop_capturer_dynamic_attributes(start_axis=(-1200, -900), 
                                     step=245, end_axis=(1200, 900), 
                                     tag='syn2_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=60,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='RGB')
    random.seed(1)
    load_rule_file('paris_label.cga', object)
    loop_capturer_dynamic_attributes(start_axis=(-1200, -900), 
                                     step=245, end_axis=(1200, 900), 
                                     tag='syn2_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=90,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='GT')
    load_rule_file('__', object)
    # Syn 3 cold style
    oid = '8c0f498c-8050-11b2-9897-0081d75d416c'
    object = ce.findByOID(oid)
    ce.setSelection(object)
    object = ce.getObjectsFrom(ce.selection)
    load_rule_file('Synthinel_rules/international_city_3_cold_city.cga', object)
    random.seed(1)
    loop_capturer_dynamic_attributes(start_axis=(-1500, -1150), 
                                     step=245, end_axis=(1200,1500), 
                                     tag='syn3_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=60,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='RGB')
    random.seed(1)
    load_rule_file('Synthinel_rules/international_city_3_cold_city_labelling.cga', object)
    loop_capturer_dynamic_attributes(start_axis=(-1500, -1150), 
                                     step=245, end_axis=(1200,1500),  
                                     tag='syn3_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=90,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='GT')
    load_rule_file('__', object)
    # Syn 4 medieval style
    oid = '19af8e5b-806a-11b2-9897-0081d75d416c'
    object = ce.findByOID(oid)
    ce.setSelection(object)
    object = ce.getObjectsFrom(ce.selection)
    load_rule_file('medievalCity.cga', object) 
    random.seed(1)
    loop_capturer_dynamic_attributes(start_axis=(-1400, -1400), 
                                     step=245, end_axis=(1150,1200), 
                                     tag='syn4_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=60,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='RGB')
    random.seed(1)
    load_rule_file('medieval_label.cga', object)
    loop_capturer_dynamic_attributes(start_axis=(-1400, -1400), 
                                     step=245, end_axis=(1150,1200), 
                                     tag='syn4_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=90,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='GT')
    load_rule_file('__', object)   
    # Syn 5 damage style
    oid = '5e28cf3f-809f-11b2-9897-0081d75d416c'
    object = ce.findByOID(oid)
    ce.setSelection(object)
    object = ce.getObjectsFrom(ce.selection)   
    load_rule_file('buildings.cga', object)
    random.seed(1)
    loop_capturer_dynamic_attributes(start_axis=(-1150, -1500), 
                                     step=245, end_axis=(1100,800), 
                                     tag='syn5_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=60,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='RGB')
    random.seed(1)
    load_rule_file('buildings_labels.cga', object)
    loop_capturer_dynamic_attributes(start_axis=(-1150, -1500), 
                                     step=245, end_axis=(1100,800),  
                                     tag='syn5_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=90,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='GT')
    load_rule_file('__', object)    
    # Syn 6 Venice style
    # Invoke map layer first
    mapLayers = ce.getObjectsFrom(ce.scene, ce.isMapLayer)
    mapLayers[0].setVisible(True) 
    ########################
    oid = 'a8f109d9-81eb-11b2-9897-0081d75d416c'
    object = ce.findByOID(oid)
    ce.setSelection(object)
    object = ce.getObjectsFrom(ce.selection)
    load_rule_file('Venice Lots.cga', object) 
    random.seed(1)
    loop_capturer_dynamic_attributes(start_axis=(1200, 100), 
                                     step=245, end_axis=(5300,2850), 
                                     tag='syn6_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=60,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='RGB')
    random.seed(1)
    load_rule_file('Venice Lots_label.cga', object)
    loop_capturer_dynamic_attributes(start_axis=(1200, 100), 
                                     step=245, end_axis=(5300,2850),
                                     tag='syn6_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=90,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='GT')
    load_rule_file('__', object)  
    # Close map layer
    mapLayers = ce.getObjectsFrom(ce.scene, ce.isMapLayer)
    mapLayers[0].setVisible(False) 
    #################
    # Syn 7 desert style
    oid = 'bc04fba9-80d3-11b2-9897-0081d75d416c'
    object = ce.findByOID(oid)
    ce.setSelection(object)
    object = ce.getObjectsFrom(ce.selection) 
    load_rule_file('Synthinel_rules/international_city_1_vienna_labelling.cga', object)
    random.seed(1)
    loop_capturer_dynamic_attributes(start_axis=(-650, -1350), 
                                     step=245, end_axis=(1700,1550), 
                                     tag='syn7_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=60,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='RGB')
    random.seed(1)
    load_rule_file('Synthinel_rules/international_city_labelling_desert_city_7.cga', object)
    loop_capturer_dynamic_attributes(start_axis=(-650, -1350), 
                                     step=245, end_axis=(1700,1550), 
                                     tag='syn7_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=90,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='GT')
    load_rule_file('__', object)
  
    # Syn 8 scifi style
    oid = 'fb21bb82-80fc-11b2-9897-0081d75d416c'
    object = ce.findByOID(oid)
    ce.setSelection(object)
    object = ce.getObjectsFrom(ce.selection)   
    load_rule_file('instance_city_on_ground.cga', object)
    random.seed(1)
    loop_capturer_dynamic_attributes(start_axis=(-2200, -2000), 
                                     step=245, end_axis=(2300,2200), 
                                     tag='syn8_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=60,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='RGB')
    random.seed(1)
    load_rule_file('instance_city_building_label.cga', object)
    loop_capturer_dynamic_attributes(start_axis=(-2200, -2000), 
                                     step=245, end_axis=(2300,2200), 
                                     tag='syn8_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=90,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='GT')
    load_rule_file('__', object)
    # Syn 9 ancient China style
    oid = 'a6384d5b-815a-11b2-9897-0081d75d416c'
    object = ce.findByOID(oid)
    ce.setSelection(object)
    object = ce.getObjectsFrom(ce.selection)
    load_rule_file('pompeii.cga', object)
    random.seed(1)
    loop_capturer_dynamic_attributes(start_axis=(-3000, -3000), 
                                     step=245, end_axis=(1500,400), 
                                     tag='syn9_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=60,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='RGB')
    random.seed(1)
    load_rule_file('pompeii_label.cga', object)
    loop_capturer_dynamic_attributes(start_axis=(-3000, -3000), 
                                     step=245, end_axis=(1500,400), 
                                     tag='syn9_la60_ca90_li1_1', adjust_list = [],
                                     light_angle=90,  camera_angle=-90, light_intensity=1, 
                                     dynamic_range={},
                                     height='652', mode='GT')
    load_rule_file('__', object)
