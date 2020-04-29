# Mesh generation for simple geometries in OpenCMISS
 
This program aims to generate 2D simple geometric meshes in OpenCMISS for the open-source finite element software OpenCMISS, both for test cases and physical simulations. Currently implemented options involve circle, cell (adhered cell), ellipse, square, stadium (2D capsule). First, the shapes are defined by their boundaries in .poly files. Second, a mesh is generated in the form of .node (nodes) and .ele (element) files. Finally, the mesh is converted into OpenCMISS in the form of .exnode (node) and .exelem (element) files, which store both mesh and numerical solutions to the finite element methods. 


## Usage

### Requirements
This program is written in [Python 3.7](https://www.python.org/downloads/release/python-370/). It uses [Triangle](https://www.cs.cmu.edu/~quake/triangle.html), a two-dimensional quality mesh generator and delaunay trianguator. It relies on the Iron library from the OpenCMISS mathematical modelling environment to create, constrain, and solve the finite element model. See the [OpenCMISS website](https://www.opencmiss.org) and [GitHub repository](https://github.com/OpenCMISS/iron) for details on installation, usage, and source code. Visualization is done using [cmgui](https://www.cmiss.org/cmgui).

Python 3.7 using the following modules:

* [OpenCMISS-Iron](https://www.opencmiss.org/)
* [NumPy](https://www.numpy.org/)
* [os](https://docs.python.org/3/library/os.html)
* [argparse](https://docs.python.org/3/library/argparse.html)


### Step 1: define boundaries
Chose which mesh to generate, and enter the corresponding directory

```
cd circle_mesh
cd cell_mesh
cd ellipse_mesh
cd square_mesh
cd stadium_mesh
```

Using flags, chose the desired geometric parameters

```
python createCircle.py  --radius 0.5              --nodes 100
python createCell.py    --length 0.5              --nodes 100
python createEllipse.py --width 1.0  --height 2.0 --nodes 100
python createSquare.py  --length 1.0              --nodes 100
python createStadium.py --width 2.0  --height 0.5 --nodes 100
```


### Step 2: generate mesh
Use triangles to generate a mesh. Use the flags to specify mesh properties. For more information, run 'triangle' in the command prompt to view available options

```
triangle -jo2a0.002 circle.poly
triangle -jo2a0.002 cell.poly
triangle -jo2a0.002 ellipse.poly
triangle -jo2a0.002 square.poly
triangle -jo2a0.002 stadium.poly
```


### Step 3: running OpenCMISS script

Go back in the main directory and run python with OpenCMISS from there. To note, no input file will default to circle.

```
cd ..
python src/mesh.py circle
python src/mesh.py cell
python src/mesh.py ellipse
python src/mesh.py square
python src/mesh.py stadium
```


### Step 3: visualizaiton

The visulization is automated with the visualise.com script.

```
cd output
cmgui visualise.com
```


## Author

* **Jared Collette** - [jaredmcollette](https://github.com/jaredmcollette)


## Contributor

* **Vijay Rajagopal** - [vraj004](https://github.com/vraj004)


## License

This project is licensed under the GNU GPL v3 - See License.txt for details


## Acknowledgements

* [**Cell Structure and Mechanobiology Group**](https://cellularsmb.org/) at the University of Melbourne - [cellsmb](https://github.com/cellsmb)