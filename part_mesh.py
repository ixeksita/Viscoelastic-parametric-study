#Created by Tania Sanchez (2014-2016) tania.sanchezmonroy@manchester.ac.uk
#This code generates the ABAQUS model using the variables contained in variables.py

# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

execfile('variables.py')

##########################
#Create the indenter
mdb.models.changeKey(fromName='Model-1', toName=model)
mdb.models[model].ConstrainedSketch(name='__profile__', 
    sheetSize=0.03)
mdb.models[model].sketches['__profile__'].sketchOptions.setValues(
    decimalPlaces=4, viewStyle=AXISYM)
mdb.models[model].sketches['__profile__'].ConstructionLine(
    point1=(0.0, -0.015), point2=(0.0, 0.015))
mdb.models[model].sketches['__profile__'].FixedConstraint(
    entity=
    mdb.models[model].sketches['__profile__'].geometry[2])
mdb.models[model].sketches['__profile__'].ArcByCenterEnds(
    center=(0.0, 0.0), direction=CLOCKWISE, point1=(0.015, 0.0), point2=(0.0, 
    -0.015))
mdb.models[model].Part(dimensionality=AXISYMMETRIC, name=
	indenter, type=DISCRETE_RIGID_SURFACE)
mdb.models[model].parts[indenter].BaseWire(sketch=
    mdb.models[model].sketches['__profile__'])
del mdb.models[model].sketches['__profile__']


#Create the sample
mdb.models[model].ConstrainedSketch(name='__profile__', 
    sheetSize=3.0)
mdb.models[model].sketches['__profile__'].sketchOptions.setValues(
    viewStyle=AXISYM)
mdb.models[model].sketches['__profile__'].ConstructionLine(
    point1=(0.0, -1.5), point2=(0.0, 1.5))
mdb.models[model].sketches['__profile__'].FixedConstraint(
    entity=
    mdb.models[model].sketches['__profile__'].geometry[2])
mdb.models[model].sketches['__profile__'].rectangle(point1=(
    0.0, -R), point2=(width, -(R+thickness)))
mdb.models[model].Part(dimensionality=AXISYMMETRIC, name=
    specimen, type=DEFORMABLE_BODY)
mdb.models[model].parts[specimen].BaseShell(sketch=
    mdb.models[model].sketches['__profile__'])
del mdb.models[model].sketches['__profile__']

#Create set for the bottom left vertex of the sample
#p = mdb.models[model].parts[specimen]
#v=p.vertices
#verts=[]
#for i in v:
	#a= i.pointOn[0]
	#if a[0]==0.0:
		#if a[1]==(-R-thickness):
			#verts=verts+[v.findAt(((a[0], a[1], 0.0),))] 
#mdb.models[model].parts[specimen].Set(vertices=verts, name= specimen+'BL_vert')


#Assigning sets for the edges
#p = mdb.models[model].parts[specimen]
#e = p.edges
#LEdges=[]; REdges=[]; TEdges=[]; BEdges=[]
#for i in e:
	#a=i.pointOn[0]
	#if a[0]==0:
		#LEdges=LEdges+[e.findAt(((a[0],a[1],a[2]),))]
	#elif a[0]==200E-03:
		#REdges=REdges+[e.findAt(((a[0],a[1],a[2]),))]
	#elif a[0]==0.05:
		#BEdges=BEdges+[e.findAt(((a[0],a[1],a[2]),))]	
	#else:
		#TEdges=TEdges+[e.findAt(((a[0],a[1],a[2]),))]
#p.Set(edges=LEdges, name='SL')
#p.Set(edges=REdges, name='SR')
#p.Set(edges=TEdges, name='TOP')
#p.Set(edges=BEdges, name='BOTTOM')	

#Create the substrate
mdb.models[model].ConstrainedSketch(name='__profile__', 
    sheetSize=3.0)
mdb.models[model].sketches['__profile__'].sketchOptions.setValues(
    viewStyle=AXISYM)
mdb.models[model].sketches['__profile__'].ConstructionLine(
    point1=(0.0, -1.5), point2=(0.0, 1.5))
mdb.models[model].sketches['__profile__'].FixedConstraint(
    entity=
    mdb.models[model].sketches['__profile__'].geometry[2])
mdb.models[model].sketches['__profile__'].rectangle(point1=(
    0.0, -(R+thickness)), point2=(width+0.005, -(R+thickness+0.15)))
mdb.models[model].Part(dimensionality=AXISYMMETRIC, name=
    'Substrate', type=DEFORMABLE_BODY)
mdb.models[model].parts['Substrate'].BaseShell(sketch=
    mdb.models[model].sketches['__profile__'])
del mdb.models[model].sketches['__profile__']

###########################
#Meshing the parts

#Partition the sample
if thickness>0.025:
	p = mdb.models[model].parts[specimen]
	f1, e1 = p.faces, p.edges
	p.DatumPointByOnFace(face=f1[0], edge1=e1[1], edge2=e1[0], offset1=cawidth, 
		offset2=thickness)
	p.DatumPointByOnFace(face=f1[0], edge1=e1[1], edge2=e1[0], offset1=cawidth, 
		offset2=0.0)
	p.DatumPointByOnFace(face=f1[0], edge1=e1[1], edge2=e1[0], offset1=0.0, 
		offset2=0.005)
	p.DatumPointByOnFace(face=f1[0], edge1=e1[1], edge2=e1[0], offset1=width, 
		offset2=0.005)
	d1=p.datums
	p.PartitionFaceByShortestPath(point1=d1[d1.keys()[1]], point2=d1[d1.keys()[2]], faces=f1)
	p.PartitionFaceByShortestPath(point1=d1[d1.keys()[3]], point2=d1[d1.keys()[4]], faces=f1)
elif thickness<=0.025:
	p = mdb.models[model].parts[specimen]
	p = mdb.models[model].parts[specimen]
	f1, e1 = p.faces, p.edges
	p.DatumPointByOnFace(face=f1[0], edge1=e1[1], edge2=e1[0], offset1=cawidth, 
		offset2=thickness)
	p.DatumPointByOnFace(face=f1[0], edge1=e1[1], edge2=e1[0], offset1=cawidth, 
		offset2=0.0)
	d1=p.datums
	p.PartitionFaceByShortestPath(point1=d1[d1.keys()[1]], point2=d1[d1.keys()[2]], faces=f1)

	
#Assign mesh elements and control	(sample)
if thickness>0.025:
	p = mdb.models[model].parts[specimen]
	f1, e1 = p.faces, p.edges
	mdb.models[model].parts[specimen].setElementType(elemTypes=
		(ElemType(elemCode=CAX4H, elemLibrary=STANDARD), ElemType(elemCode=CAX3, 
		elemLibrary=STANDARD)), regions=(
		mdb.models[model].parts[specimen].faces.getSequenceFromMask(
		('[#f 1]', ), ), ))
	f1 = p.faces
	pickedRegions = f1.getSequenceFromMask(mask=('[#f 1]', ), )
	p.setMeshControls(regions=pickedRegions, elemShape=QUAD, technique=STRUCTURED)
	
elif thickness<=0.025:
	p = mdb.models[model].parts[specimen]
	f1, e1 = p.faces, p.edges
	mdb.models[model].parts[specimen].setElementType(elemTypes=
		(ElemType(elemCode=CAX4H, elemLibrary=STANDARD), ElemType(elemCode=CAX3, 
		elemLibrary=STANDARD)), regions=(
		mdb.models[model].parts[specimen].faces.getSequenceFromMask(
		('[#3 ]', ), ), ))
	mdb.models[model].parts[specimen].setMeshControls(elemShape=
		QUAD, regions=
		mdb.models[model].parts[specimen].faces.getSequenceFromMask(
		('[#3 ]', ), ), technique=STRUCTURED)

#Asign seeding size (sample)

#under the indenter (constant mesh size R/100) (sample)
e=p.edges
pickedEdges = e.findAt(((cawidth/2.0,-R,0.0),))
p.seedEdgeBySize(edges=pickedEdges, size=small_mesh, deviationFactor=0.1, 
    constraint=FINER)
y1=-R-(0.005/2.0)
pickedEdges=e.findAt(((cawidth, y1, 0.0),)) 
p.seedEdgeBySize(edges=pickedEdges, size=small_mesh, deviationFactor=0.1, 
    constraint=FINER)
pickedEdges=e.findAt(((0.0, y1, 0.0),))
p.seedEdgeBySize(edges=pickedEdges, size=small_mesh, deviationFactor=0.1, 
    constraint=FINER)
pickedEdges=e.findAt(((width, y1, 0.0),))
p.seedEdgeBySize(edges=pickedEdges, size=small_mesh, deviationFactor=0.1, 
    constraint=FINER)

if thickness>0.025:
	pickedEdges=e.findAt(((cawidth/2.0, (-R-0.005), 0.0),))
	p.seedEdgeBySize(edges=pickedEdges, size=small_mesh, deviationFactor=0.1, 
		constraint=FINER)
	pickedEdges=e.findAt(((cawidth/2.0, (-R-0.005), 0.0),))
	p.seedEdgeBySize(edges=pickedEdges, size=small_mesh, deviationFactor=0.1, 
		constraint=FINER)
	pickedEdges=e.findAt(((cawidth/2.0, (-R-thickness), 0.0),))
	p.seedEdgeBySize(edges=pickedEdges, size=small_mesh, deviationFactor=0.1, 
		constraint=FINER)

elif thickness<=0.025:
	pickedEdges=e.findAt(((cawidth/2.0, (-R-thickness), 0.0),))
	p.seedEdgeBySize(edges=pickedEdges, size=small_mesh, deviationFactor=0.1, constraint=FINER)

	
#Vertical (increasing meshing size)	(sample)
x1= cawidth+(width/2.0)
y2= y1- (thickness/2.0)
if  thickness>0.25:
	pickedEdges = e.findAt(((0.0, y2, 0.0 ),))
	p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges, minSize=small_mesh, 
		maxSize=max_meshv, constraint=FINER)
	pickedEdges= e.findAt(((cawidth, y2, 0.0),))
	p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges, minSize=small_mesh, 
		maxSize=max_meshv, constraint=FINER)
	pickedEdges =e.findAt(((width, y2,0.0),))
	p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges, minSize=small_mesh, 
		maxSize=max_meshv, constraint=FINER)
#

#Horizontal (increasing meshing size)
pickedEdges=e.findAt(((x1, -R, 0.0),))
p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges, minSize=small_mesh, 
    maxSize=max_meshh, constraint=FINER)	
pickedEdges=e.findAt(((x1, (-R-thickness), 0.0),))
p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges, minSize=small_mesh, 
    maxSize=max_meshh, constraint=FINER)
if thickness>0.025:
	pickedEdges=e.findAt(((x1, -R-0.005, 0.0),))
	p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges, minSize=small_mesh, 
		maxSize=max_meshh, constraint=FINER)
#
#Mesh the sample	
f1 = p.faces
pickedRegions = f1.getSequenceFromMask(mask=('[#f 1]', ), )
p.generateMesh(regions=pickedRegions)


#Meshing controls for the substrate
sub=mdb.models[model].parts['Substrate']
mdb.models[model].parts['Substrate'].setElementType(elemTypes=
    (ElemType(elemCode=CAX4R, elemLibrary=STANDARD), ElemType(elemCode=CAX3, 
    elemLibrary=STANDARD)), regions=(
    mdb.models[model].parts[specimen].faces.getSequenceFromMask(
    ('[#f 1]', ), ), ))
sub.seedPart(size=0.025, deviationFactor=0.1, minSizeFactor=0.1)
pickedRegions = sub.faces.getSequenceFromMask(mask=('[#1 ]', ), )
sub.setMeshControls(regions=pickedRegions, elemShape=QUAD, technique=STRUCTURED)
sub.generateMesh()

#Mesh controls for the indenter
indentermesh= small_mesh*20.0
sp=mdb.models[model].parts[indenter]
sp.seedPart(size=indentermesh, deviationFactor=0.1, minSizeFactor=0.1)
sp.generateMesh()

#Creating the assembly 
ass = mdb.models[model].rootAssembly
mdb.models[model].rootAssembly.DatumCsysByDefault(CARTESIAN)
ass.Instance(name=indenter+'-1', part=sp, dependent=ON)
ass.Instance(name=specimen+'-1', part=p, dependent=ON)
ass.Instance(name='Substrate-1', part=mdb.models[model].parts['Substrate'], dependent=ON)

#Create contact surface for the indenter
side1Edges = sp.edges.getSequenceFromMask(mask=('[#1 ]', ), )
sp.Surface(side1Edges=side1Edges, name='Contact_indenter')

#Create contact surface for the sample
contactedge=[]
contactedge=contactedge+[e.findAt(((cawidth/2.0, -R, 0.0),))]
#p.Set(edges=contactedge, name='Contact_sample')
p.Surface(side1Edges=contactedge, name='Contact_sample')

#Create BC sets/surface on the sample
if thickness>0.025:
	roller=[]
	roller= roller +[e.findAt(((0.0, y1, 0.0),))]
	roller= roller +[e.findAt(((0.0, y2, 0.0),))]
	p.Set(edges=roller, name='Sample_roller')
elif thickness<=0.025:
	roller=[]
	roller= roller +[e.findAt(((0.0, y1, 0.0),))]
	p.Set(edges=roller, name='Sample_roller')
ass.regenerate()

ties=[]
ties= ties+[e.findAt(((cawidth/2.0, -R-thickness, 0.0),))]
ties= ties+[e.findAt(((x1, -R-thickness, 0.0),))]
p.Surface(side1Edges=ties, name='Sample_tie')

#Create BC sets/surfaces on the substrate
top=[]
top= top+[sub.edges.findAt(((width/2.0, -R-thickness, 0.0),))]
sub.Surface(side1Edges=top, name='Substrate_tie')

bottom=[]
bottom= sub.edges.getSequenceFromMask(mask=('[#4 ]', ), )
sub.Set(edges=bottom, name='Substrate_bottom')

#Contact control & behaviour
ass = mdb.models[model].rootAssembly
ass.regenerate()
mdb.models[model].ContactProperty('CONTACT')
mdb.models[model].interactionProperties['CONTACT'].TangentialBehavior(
    formulation=FRICTIONLESS)
mdb.models[model].StdContactControl(name='contact_control', 
    stabilizeChoice=AUTOMATIC, dampFactor=0.0001)
region1=ass.instances['Indenter-1'].surfaces['Contact_indenter']
region2=ass.instances['Sample-1'].surfaces['Contact_sample']
mdb.models['Spherical_indentation'].SurfaceToSurfaceContactStd(name='CSS', 
    createStepName='Initial', master=region1, slave=region2, sliding=FINITE, 
    thickness=ON, interactionProperty='CONTACT', 
    contactControls='contact_control', adjustMethod=NONE, 
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)	

#Materials and sections 
mdb.models[model].Material(name='GLASS')
mdb.models[model].materials['GLASS'].Density(table=((2.5e-09, 
    ), ))
mdb.models[model].materials['GLASS'].Elastic(table=((70000.0, 
    0.2), ))
mdb.models[model].Material(description='SLS BASED ON UMAT\n', 
    name='TANIA')
mdb.models[model].materials['TANIA'].Density(table=((9.7e-13, 
    ), ))
mdb.models[model].materials['TANIA'].UserMaterial(
    mechanicalConstants=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
mdb.models[model].Material(name='VISHAY')
mdb.models[model].materials['VISHAY'].Density(table=((
    1.2e-09, ), ))
mdb.models[model].materials['VISHAY'].Elastic(table=((4.0, 
    0.4995), ))
mdb.models[model].HomogeneousSolidSection(material='TANIA', 
    name='UMAT-section', thickness=None)
mdb.models[model].HomogeneousSolidSection(material='GLASS', 
    name='glass-section', thickness=None)
mdb.models[model].HomogeneousSolidSection(material='VISHAY', 
    name='vishay-section', thickness=None)
	
#Assign sections
p.SectionAssignment(offset=
    0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    faces=p.faces.getSequenceFromMask(
    mask=('[#f ]', ), )), sectionName='UMAT-section', thicknessAssignment=
    FROM_SECTION)

sub = mdb.models[model].parts['Substrate']
f = sub.faces
sub.SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    faces=p.faces.getSequenceFromMask(
    mask=('[#1 ]', ), )), sectionName='glass-section',  
    thicknessAssignment=FROM_SECTION )
	
#Rigid body indenter
ass =  mdb.models[model].rootAssembly
ass.ReferencePoint(point=(R, 0.0, 0.0))
ass.features.changeKey(fromName='RP-1', toName='Indenter_RP')
mdb.models[model].RigidBody(bodyRegion=Region(
    edges=mdb.models[model].rootAssembly.instances['Indenter-1'].edges.getSequenceFromMask(
    mask=('[#1 ]', ), )), name='RB', refPointRegion=Region(referencePoints=(
    mdb.models[model].rootAssembly.referencePoints[8], )))

#Tie sample to substrate
region1=ass.instances['Substrate-1'].surfaces['Substrate_tie']
region2=ass.instances['Sample-1'].surfaces['Sample_tie']
mdb.models[model].Tie(adjust=ON, master= region1, 
    name='Sample_substrate', positionToleranceMethod=COMPUTED, slave=region2, 
    thickness=ON, tieRotations=ON)
ass.regenerate()

execfile('BC-steps.py')