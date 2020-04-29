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
parser.add_argument("--width",nargs='?', type=float, default=3.0*np.sqrt(np.pi)/4.0)
parser.add_argument("--height",nargs='?', type=float, default=1/np.sqrt(np.pi))
parser.add_argument("--nodes",nargs='?', type=int, default=100)
args = parser.parse_args()

polyfile = 'stadium.poly'

#TODO - Numbers are not generalizable. Do not change without more modifications
height = args.height
width = args.width
total = width + height



nodes_curve = int(round((height/total)*args.nodes/2)) #number of nodes to make one half of the ellipse
nodes_flat = int(round((width/total)*args.nodes/2))
nodes = 2*nodes_curve + 2*nodes_flat

#create array of x-y coordinates from equally-spaced theta increments
theta_right = np.linspace(-np.pi/2, np.pi/2, num=nodes_curve, endpoint=False)
x_cords_rightcurve = height/2.0*np.cos(theta_right)+width/2.0
y_cords_rightcurve = height/2.0*np.sin(theta_right)

theta_left = np.linspace(-np.pi/2, np.pi/2, num=nodes_curve, endpoint=False)
x_cords_leftcurve = -height/2.0*np.cos(theta_left)-width/2.0
y_cords_leftcurve = -height/2.0*np.sin(theta_left)

x_cords_topflat = np.linspace(width/2.0,-width/2.0,num=nodes_flat, endpoint=False)
y_cords_topflat = np.full(nodes_flat,height/2.0)

x_cords_bottomflat = np.linspace(-width/2.0,width/2.0,num=nodes_flat, endpoint=False)
y_cords_bottomflat = np.full(nodes_flat,-height/2.0)

x_cords = np.concatenate((x_cords_rightcurve, x_cords_topflat, x_cords_leftcurve, x_cords_bottomflat))
y_cords = np.concatenate((y_cords_rightcurve, y_cords_topflat, y_cords_leftcurve, y_cords_bottomflat))

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
