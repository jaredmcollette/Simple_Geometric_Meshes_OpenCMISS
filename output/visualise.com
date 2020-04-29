##########################
# CMGUI VISUALIZATION FILE
##########################

#Author: Jared Collette

##########################


#Variable definitions
$name = "Region";


#Read in Mesh
gfx read node "mesh_output.part0.exnode" 
gfx read elem "mesh_output.part0.exelem" 


#Define element group
gfx define faces egroup $name;


#Create window and set camera
gfx create window 1;
gfx modify window 1 image rotate 1 0 0 -90;
gfx modify window 1 bac colour 0, 0, 0;


#Scale
gfx define field annotation string_constant "Scale: 0.5"
gfx modify g_element "/" point glyph line general size "0.5*0.5*0.5" line_width "2.0" label annotation centre 0.6, 0.8, 0.0, label_offset 0.0, 0.05, 0.0, select_on material default selected_material default;


#Axis
#gfx modify g_element "/" point glyph axes general size "0.2*0.2*0.2" line_width "6.0" centre 0.0, 0.0, 0.0, select_on material red selected_material default;


#Display Mesh
gfx modify g_element $name lines select_on coordinate Coordinate material black selected_material default_selected
gfx modify g_element $name surfaces as tc select_on coordinate Coordinate material grey75 selected_material default_selected render_shaded


#Background
gfx modify g_element "/" point glyph sheet general size "4.0*4.0*1.0" centre 0.0, 0.0, 0.0, select_on material black selected_material default;


#Open scene and spectrum windows
#gfx edit scene;
#gfx edit spectrum;

#Print
#gfx print png file mesh.png width 1200 height 1200;