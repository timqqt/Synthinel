'''
Created on 2019-9-6

@author: Dell
'''
from scripting import *
import pickle

# get a CityEngine instance
ce = CE()

def load_rule_file(rule_file_path, objs):
    print('load rule file')
    #all_shapes = ce.getObjectsFrom(ce.scene, objs)
    ce.setRuleFile(objs, rule_file_path)
    ce.generateModels(objs)
    ce.waitForUIIdle()
    
#all_objects = ce.getObjectsFrom(ce.scene, ce.isShape)
#oid = '5f2dde5d-26e4-11b2-aa5b-0081d75d416c'
##oid = '68e10e5e-26e4-11b2-aa5b-0081d75d416c:53'
#object = ce.findByOID(oid)
#ce.setSelection(object)
#object2 = ce.getObjectsFrom(ce.selection)
#print(object)
#print(object2)
#
#load_rule_file('Synthinel_rules/international_city_1_vienna_labelling.cga', object2)
mapLayers = ce.getObjectsFrom(ce.scene, ce.isMapLayer)
print(mapLayers)
mapLayers[0].setVisible(True) # Set visibility of map layer -> integrate Venice into our pipeline.

#print(object)
#oid_list = []
#for each_obj in all_objects:
#    oid = ce.getOID(each_obj)
#    oid_list.append(oid)

#file = open('D:/CityEngine Workspace/Dynamic_shooting/data/list_of_oids.txt', 'wb')
#pickle.dump(oid_list, file)
#for oid_item in oid_list:
#    file.write('%s\n' % oid_item)
#print('I write it !')
#for each_oid in oid_list:
#    object = ce.findByOID(oid)
#    ce.setSelection(object)
#    print(object)

