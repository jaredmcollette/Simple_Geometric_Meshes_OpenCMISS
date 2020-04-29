#!/usr/bin/env python


# Intialise OpenCMISS-Iron
from opencmiss.iron import iron
import numpy as np
import os
import argparse


#------------------------------------------------------------------------------------------------
# INPUTS
#------------------------------------------------------------------------------------------------

#User Input
parser = argparse.ArgumentParser()
parser.add_argument("input_mesh", nargs='?', default="circle")
args = parser.parse_args()

#Geometric Inputs
node_input = "./" + args.input_mesh + "_mesh/" + args.input_mesh + ".1.node"
elem_input = "./" + args.input_mesh + "_mesh/" + args.input_mesh + ".1.ele"


#------------------------------------------------------------------------------------------------
# USER NUMBERS
#------------------------------------------------------------------------------------------------

#Defining User Numbers
coordinateSystemUserNumber              = 10
regionUserNumber                        = 20
basisUserNumber                         = 30
meshUserNumber                          = 50
decompositionUserNumber                 = 60
geometricFieldUserNumber                = 70


#------------------------------------------------------------------------------------------------
# DIAGNOSTICS AND COMPUTATIONAL NODE INFORMATION
#------------------------------------------------------------------------------------------------

#iron.DiagnosticsSetOn(iron.DiagnosticTypes.IN,[1,2,3,4,5],"Diagnostics",["DOMAIN_MAPPINGS_LOCAL_FROM_GLOBAL_CALCULATE"])

# Get the computational nodes information
numberOfComputationalNodes = iron.ComputationalNumberOfNodesGet()
computationalNodeNumber = iron.ComputationalNodeNumberGet()


#------------------------------------------------------------------------------------------------
# COORDINATE SYSTEM
#------------------------------------------------------------------------------------------------

#Two Dimensional Coordinate System
coordinateSystem = iron.CoordinateSystem()
coordinateSystem.CreateStart(coordinateSystemUserNumber)
coordinateSystem.label = "Coordinates"
coordinateSystem.dimension = 2
coordinateSystem.CreateFinish()


#------------------------------------------------------------------------------------------------
# REGION
#------------------------------------------------------------------------------------------------

#Start Region
region = iron.Region()
region.CreateStart(regionUserNumber,iron.WorldRegion)
region.label = "Region"
region.coordinateSystem = coordinateSystem
region.CreateFinish()


#------------------------------------------------------------------------------------------------
# BASIS
#------------------------------------------------------------------------------------------------

#Simplex Basis Reaction Diffusion
basis = iron.Basis()
basis.CreateStart(basisUserNumber)
basis.type = iron.BasisTypes.SIMPLEX
basis.numberOfXi = 2
basis.interpolationXi = [iron.BasisInterpolationSpecifications.QUADRATIC_SIMPLEX]*2
basis.quadratureOrder = 3
basis.CreateFinish()


#------------------------------------------------------------------------------------------------
# MESH
#------------------------------------------------------------------------------------------------

num_nodes_boundary = 0

#Inputing node file
try:
    with open(node_input,'r') as node_file:
    
        #Reading the values of the first line
        num_nodes, num_coords, num_attributes, boundary_markers = map(int,node_file.readline().split())

        #Creating variables to store node number & boundary marker
        NodeNums = np.zeros((num_nodes,2),dtype=int)

        #Creating variable to store x and y coordinates
        NodeCoords = np.zeros((num_nodes,num_coords), dtype=float)

        #Reading data from nodefile
        for i in range(num_nodes):
            NodeNums[i,0], NodeCoords[i,0], NodeCoords[i,1], NodeNums[i,1] = node_file.readline().split()
            if NodeNums[i,1] == 1:
                num_nodes_boundary += 1

except IOError:
    print('Could not open file: ' + node_input)



#Inputing element file
try:
    with open(elem_input,'r') as elem_file:

        #Reading the values of the first line
        num_elements, nodes_per_ele, ele_attributes = map(int,elem_file.readline().split())

        #Creating variable to store element map
        ElemMap = np.zeros((num_elements,nodes_per_ele+1),dtype=int)

        #Reading data from elemfile
        for i in range(num_elements):
            #5,6,4 are switched to map triangles to opencmiss
            ElemMap[i,0],ElemMap[i,1],ElemMap[i,2],ElemMap[i,3],ElemMap[i,5],ElemMap[i,6],ElemMap[i,4] = elem_file.readline().split()
#except EnvironmentError:
except IOError:
    print('Could not open file: ' + elem_input)
    

#Initialise Nodes
nodes = iron.Nodes()
nodes.CreateStart(region,num_nodes)
nodes.CreateFinish()

#Initialise Mesh
mesh = iron.Mesh()
mesh.CreateStart(meshUserNumber,region,num_coords)
mesh.NumberOfElementsSet(num_elements)
mesh.NumberOfComponentsSet(1)

#Initialise Elements
meshElements = iron.MeshElements()
meshElements.CreateStart(mesh,1,basis)
for i in range(num_elements):
    element = int(ElemMap[i,0])
    meshElements.NodesSet(element,[ElemMap[i,1],ElemMap[i,2],ElemMap[i,3],ElemMap[i,4],ElemMap[i,5],ElemMap[i,6]])
meshElements.CreateFinish()

#Finilise Mesh
mesh.CreateFinish()


#------------------------------------------------------------------------------------------------
# MESH DECOMPOSITION
#------------------------------------------------------------------------------------------------

#Parallelization
decomposition = iron.Decomposition()
decomposition.CreateStart(decompositionUserNumber,mesh)
decomposition.type = iron.DecompositionTypes.CALCULATED
decomposition.numberOfDomains = numberOfComputationalNodes
decomposition.CreateFinish()


#------------------------------------------------------------------------------------------------
# GEOMETRIC FIELD
#------------------------------------------------------------------------------------------------

#Geometric Field 
geometricField = iron.Field()
geometricField.CreateStart(geometricFieldUserNumber,region)
geometricField.MeshDecompositionSet(decomposition)
geometricField.TypeSet(iron.FieldTypes.GEOMETRIC)
geometricField.VariableLabelSet(iron.FieldVariableTypes.U,"Coordinate")
geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U,1,1)
geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U,2,1)
#geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U,3,1)
geometricField.CreateFinish()

#Update Geometric Field from customized mesh
for i in range(num_nodes):
    node = int(NodeNums[i,0])
    nodeDomain = decomposition.NodeDomainGet(node,1)
    if nodeDomain == computationalNodeNumber:
        nodex = NodeCoords[i,0]
        nodey = NodeCoords[i,1]
        geometricField.ParameterSetUpdateNodeDP(iron.FieldVariableTypes.U,
                                                iron.FieldParameterSetTypes.VALUES,
                                                1,1,node,1,nodex)
        geometricField.ParameterSetUpdateNodeDP(iron.FieldVariableTypes.U,
                                                iron.FieldParameterSetTypes.VALUES,
                                                1,1,node,2,nodey)

#Update Geometric Field
geometricField.ParameterSetUpdateStart(iron.FieldVariableTypes.U,
                                       iron.FieldParameterSetTypes.VALUES)
geometricField.ParameterSetUpdateFinish(iron.FieldVariableTypes.U,
                                        iron.FieldParameterSetTypes.VALUES)

        
#Exporting Node and Element Files
#name = "output/mesh"
name = "output/mesh_output"

fields = iron.Fields()
fields.CreateRegion(region)
fields.ElementsExport(name,"FORTRAN")
# fields.ElementsExport("output/ActinWaves_0000","FORTRAN")
# fields.ElementsExport(name,"FORTRAN")
fields.NodesExport(name,"FORTRAN")            
fields.Finalise()

# Finalise OpenCMISS-Iron
iron.Finalise()