# -*- coding: utf-8 -*-

"""
Created on Mon Nov 16 16:07:24 2015
@author: vrajagopal and maxmillian bode

Modified on Sat Dec 16 13:41:50 2017
@author: jcollette

"""

import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--length",nargs='?', type=float, default=1.0)
parser.add_argument("--nodes",nargs='?', type=int, default=100)
args = parser.parse_args()


length = args.length
nodes = args.nodes


polyfile = 'square.poly'


#create array of x-y coordinates from equally-space x coordinates
x_cords_right = np.full(int(nodes/4),length/2.0)
y_cords_right = np.linspace(-length/2.0,length/2.0,num=nodes/4, endpoint=False)

x_cords_top = np.linspace(length/2.0,-length/2.0,num=nodes/4, endpoint=False)
y_cords_top = np.full(int(nodes/4),length/2.0)

x_cords_left = np.full(int(nodes/4),-length/2.0)
y_cords_left = np.linspace(length/2.0,-length/2.0,num=nodes/4, endpoint=False)

x_cords_bottom = np.linspace(-length/2.0,length/2.0,num=nodes/4, endpoint=False)
y_cords_bottom = np.full(int(nodes/4),-length/2.0)

#combining all x-y coordinates into one array. The coordinates on the curve come before the flat section
x_cords = np.concatenate((x_cords_right, x_cords_top, x_cords_left, x_cords_bottom))
y_cords = np.concatenate((y_cords_right, y_cords_top, y_cords_left, y_cords_bottom))

numbering = range(1,(nodes+1))
numbering = np.array(numbering)
zeros = [0]*nodes


#write to file 
f = open(polyfile, 'w')
nodesheader_line = [(nodes), 2, 0, 0]
nodesheader_line = '   '.join(map(str,nodesheader_line))
f.write(nodesheader_line)
f.write('\n')

list_nodes = np.matrix((numbering, x_cords, y_cords, zeros))
list_nodes = list_nodes.transpose()
templist = []
for row in range(0,len(list_nodes)):
    temp = [str(int(list_nodes[row, 0])), str(list_nodes[row, 1]), str(list_nodes[row, 2]), str(int(list_nodes[row, 3]))]
    templist.append(temp)
    f.write('   '.join(temp))
    f.write('\n')

facetheader_line = [nodes, 0]
facetheader_line = '   '.join(map(str, facetheader_line))
f.write(facetheader_line)
f.write('\n')
facet_numbers = np.array(range(1,(nodes+1)))
facetnodei = np.array(range(1,(nodes+1)))
facetnodej = np.array(range(2, (nodes+1)))
facetnodej = np.append(facetnodej,1)
facetbdmarker = [0]*(nodes)
facetlist = np.matrix((facet_numbers, facetnodei, facetnodej, facetbdmarker))
facetlist = facetlist.transpose()
templist = []
for row in range(0,len(facetlist)):
    temp = [str(int(facetlist[row, 0])), str(int(facetlist[row, 1])), str(int(facetlist[row, 2])), str(int(facetlist[row, 3]))]
    templist.append(temp)
    f.write('   '.join(temp))
    f.write('\n')

f.write('0')
f.close()
