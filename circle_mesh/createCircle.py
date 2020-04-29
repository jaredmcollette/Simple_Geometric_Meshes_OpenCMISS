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
parser.add_argument("--radius",nargs='?', type=float, default=1/np.sqrt(np.pi))
parser.add_argument("--nodes",nargs='?', type=int, default=100)
args = parser.parse_args()

polyfile = 'circle.poly'

radius = args.radius

nodes = args.nodes #number of nodes to make one half of the ellipse

#create array of x-y coordinates from equally-spaced theta increments
theta = np.linspace(0, 2*np.pi, num=nodes, endpoint=False)

x_cords = radius*np.cos(theta)
y_cords = radius*np.sin(theta)

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
