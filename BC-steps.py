#Created by Tania Sanchez 2015-2016

#Indentation step
mdb.models[model].ViscoStep(amplitude=RAMP, cetol=5e-07, 
    description='Indenter is pressed onto the sample at a constant rate', 
    initialInc=0.001, maxInc=0.01, maxNumInc=2000, minInc=1e-10, name=
    'Indentation_visco', nlgeom=ON, previous='Initial', timePeriod=tr)

#Holding step		
mdb.models[model].ViscoStep(cetol=5e-07, description=
    'The load on the indenter is held for thold', 
    initialInc=0.001, maxInc=0.1, maxNumInc=10000, minInc=1e-10, name=
    'Holding_visco', previous='Indentation_visco', timePeriod=thold)

#BC base constrained in all directions/rotations
mdb.models[model].EncastreBC(createStepName='Initial', 
    localCsys=None, name='Base', region=
    mdb.models[model].rootAssembly.instances['Substrate-1'].sets['Substrate_bottom'])

#BC roller on the sample (not allowed to move in the x direction or to rotate)
mdb.models[model].XsymmBC(createStepName='Initial', 
    localCsys=None, name='Roller', region=
    mdb.models[model].rootAssembly.instances['Sample-1'].sets['Sample_roller'])
	
#BC indenter displacement
ass = mdb.models[model].rootAssembly
v1 = ass.instances['Indenter-1'].vertices
verts1 = v1.findAt(((R,0.0, 0.0),) )
ass.Set(vertices=verts1, name='Indenter_RP')

mdb.models[model].rootAssembly.regenerate()
mdb.models[model].DisplacementBC(amplitude=UNSET, 
    createStepName='Initial', distributionType=UNIFORM, fieldName='', 
    localCsys=None, name='Indenter_mov', region=
    mdb.models[model].rootAssembly.sets['Indenter_RP'], u1=
    SET, u2=UNSET, ur3=SET)
	
#Load
mdb.models[model].ConcentratedForce(cf2=-load, 
    createStepName='Indentation_visco', distributionType=UNIFORM, field='', 
    localCsys=None, name='Indenter_load', region=
    mdb.models[model].rootAssembly.sets['Indenter_RP'])
	
mdb.models[model].historyOutputRequests['H-Output-1'].setValues(
    variables=('CAREA', 'CFN1', 'CFN2', 'CFN3', 'CFNM'))

#Create set for the top left vertex of the sample
p = mdb.models[model].parts[specimen]
v=p.vertices
verts=[]
for i in v:
	a= i.pointOn[0]
	if a[0]==0.0:
		if a[1]==-R:
			verts=verts+[v.findAt(((a[0], a[1], 0.0),))] 
			p.Set(vertices=verts, name= specimen+'BT_vert')
ass.regenerate()
	
#Create job/write input
j1= int(thickness*1000)
jobName=str(j1)+'um-final'

mdb.Job(contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=
	    SINGLE, historyPrint=OFF, memory=70, memoryUnits=PERCENTAGE, model=
	    model, modelPrint=OFF, multiprocessingMode=DEFAULT, name=jobName, 
	    nodalOutputPrecision=SINGLE, numCpus=4, numDomains=4, 
	    parallelizationMethodExplicit=DOMAIN, type=ANALYSIS, 
	    userSubroutine='slsbis.for')
mdb.jobs[jobName].writeInput()