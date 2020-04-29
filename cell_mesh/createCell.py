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
parser.add_argument("--length",nargs='?', type=float, default=np.sqrt(0.5))
parser.add_argument("--nodes",nargs='?', type=int, default=100)
args = parser.parse_args()


cell_length = args.length
nodes = args.nodes

polyfile = 'cell.poly'

nodes_curve = int(round(nodes*(8/13))) #number of free nodes
nodes_flat = int(round(nodes*(5/13))) #number of fixed nodes adhered to the substrate
nodes = nodes_curve + nodes_flat #total number of nodes

#create array of x-y coordinates from equally-spaced theta increments
theta = np.linspace(0, np.pi, num=nodes_curve, endpoint=False)
radius = cell_length*(np.sin(theta) + np.cos(theta)**2)
x_cords_curve = radius*np.cos(theta)
y_cords_curve = radius*np.sin(theta)

#create array of x-y coordinates from equally-space x coordinates
x_cords_flat = np.linspace(-cell_length,cell_length,num=nodes_flat, endpoint=False)
y_cords_flat = np.zeros(nodes_flat)

#combining all x-y coordinates into one array. The coordinates on the curve come before the flat section
x_cords = np.concatenate((x_cords_curve, x_cords_flat))
y_cords = np.concatenate((y_cords_curve, y_cords_flat))

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
