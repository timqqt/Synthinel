import numpy as np

oid_list = np.loadtxt('list_of_oids.txt', dtype=str, delimiter='\n')
print(oid_list.shape)