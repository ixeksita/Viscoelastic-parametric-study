#Created by Tania Sanchez (2014-2016) tania.sanchezmonroy@manchester.ac.uk
#This code is used to obtain the time vs displacement and contact area data files from ABAQUS

rep=0
while os.path.exists(wDr+'/'+odbname)==False:
    time.sleep(10)
    rep=rep+1
    if rep>30:
        break
rep=0
while os.path.exists(wDr+'/'+jobName+'.lck')==True:
    time.sleep(10)
    rep=rep+1
    if rep>100:
        break
while os.path.exists(wDr+jobName+'.023')==True:
    time.sleep(10)
    rep=rep+1
    if rep>100:
        break
saveFig=0;

#Create a new viewport
myViewport=session.Viewport(name='MakePlot', origin=(0.0, 0.0), width=100, 
    height=100)
session.viewports['MakePlot'].makeCurrent()
session.viewports['MakePlot'].maximize()
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
odbdir='./'+odbname
o2 = session.openOdb(name=odbdir)

session.viewports['MakePlot'].setValues(displayedObject=o2)
odb = session.odbs[odbdir]
if int(filename[ix])<1500:
	xyDataListFromField(odb=odb, outputPosition=NODAL, variable=((
		'U', NODAL, ((INVARIANT, 'Magnitude'), )), ), nodeSets=(
		'SAMPLE-1.SAMPLEBT_VERT', ))
else:
	xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('U', 
		NODAL), ), nodeLabels=(('SAMPLE-3000UM-MED-1', ('6805', )), ))
Displacement= 'displ'+samp
session.xyDataObjects.changeKey(
    fromName=varprin, toName=Displacement)
x0 = session.xyDataObjects[Displacement]
session.writeXYReport(fileName=outdir+'/'+'Output-displacement'+samp+'.txt', appendMode=ON, xyData=(x0, ))

#nosteps=[0,1]
#for i in nosteps:
	#Steps= odb.steps[odb.steps.keys()[i]]
	#region= Steps.historyRegions[Steps.historyRegions.keys()[1]]
	#carea=region.historyOutputs[region.historyOutputs.keys()[0]].data
	#fd=open(outdir+'/Output-contactarea'+samp+'.txt', 'a')
	#for time, data in carea [1 :]:
		#fd.write('%1.14f ' % (data))
		#fd.write('\n')
	#fd.close()
	
#session.Path(name='Top_face', type=POINT_LIST, expression=((0.0, -R, 0.0), 
   #(width, -R, 0.0)))
if int(filename[ix])<1500:
	xy_result = session.XYDataFromHistory(name='area', odb=odb, 
		outputVariableName='Total area in contact: CAREA    ASSEMBLY_SAMPLE-1_CONTACT_SAMPLE/ASSEMBLY_INDENTER-1_CONTACT_INDENTER', 
		steps=('Indentation_visco', 'Holding_visco', ), )
	x0 = session.xyDataObjects['area']
	session.writeXYReport(fileName=outdir+'/'+'Output-contactarea'+samp+'.txt', xyData=(x0, ))

else:
	xy_result = session.XYDataFromHistory(name='area', odb=odb, 
		outputVariableName='Total area in contact: CAREA    ASSEMBLY_SAMPLE-3000UM-MED-1_TOP-2500UM/ASSEMBLY_FINE_INDENTER', 
		steps=('Indentation_visco', 'Holding_visco', ), )
	x0 = session.xyDataObjects['area']
	session.writeXYReport(fileName=outdir+'/'+'Output-contactarea'+samp+'.txt', xyData=(x0, ))

odb.close()

