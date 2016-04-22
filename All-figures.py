#Created by Tania Sanchez (2014-2016) tania.sanchezmonroy@manchester.ac.uk
#This code is used to generate Figures from ABAQUS

#Create a new viewport
myViewport=session.Viewport(name='Makefig', origin=(0.0, 0.0), width=100, 
    height=100)
session.viewports['Makefig'].makeCurrent()
session.viewports['Makefig'].maximize()

odbdir='./'+odbname
o2 = session.openOdb(name=odbdir)
session.viewports['Makefig'].setValues(displayedObject=o2)
odb = session.odbs[odbdir]

#display contour output
session.viewports['Makefig'].odbDisplay.display.setValues(plotState=(DEFORMED,))

#Do not print the viewport decorations or Black background.
session.printOptions.setValues(rendition=COLOR,
vpDecorations=OFF, vpBackground=OFF)

#Plotting preferences 
session.viewports['Makefig'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Makefig'].odbDisplay.commonOptions.setValues(
    deformationScaling=UNIFORM)
session.Spectrum(name="tania",  colors =('#00FFE3', '#008FFF', '#0004FF', 
    '#8600FF', '#6510A8', '#8B69A8', '#FF00EC', '#FF2900', '#FFB400', 
    '#BEFF00', ))
session.viewports['Makefig'].viewportAnnotationOptions.setValues(
    legendFont='-*-lucida sans-medium-r-normal-*-*-140-*-*-p-*-*-*')
session.viewports['Makefig'].odbDisplay.commonOptions.setValues(
    visibleEdges=FEATURE)
session.viewports['Makefig'].odbDisplay.contourOptions.setValues(
    spectrum='tania', maxAutoCompute=ON, minAutoCompute=ON)
session.viewports['Makefig'].viewportAnnotationOptions.setValues(triad=OFF, 
    title=OFF, state=OFF, annotations=OFF, compass=OFF)

#Fit assembly
session.viewports['Makefig'].view.fitView()

#close up
#session.viewports['Makefig'].view.setValues(nearPlane=0.786654, 
    #farPlane=1.1469, width=0.130959, height=0.0491659, viewOffsetX=-0.0350669, 
    #viewOffsetY=0.0806321)
session.viewports['Makefig'].view.setValues(nearPlane=0.769894, 
    farPlane=1.10969, width=0.120479, height=0.0454668, viewOffsetX=-0.073618, 
    viewOffsetY=0.0499722)

#figures for the last frame of the loading and holding portion	
frame=[0,-1]
cont=0
for i in frame:
	cont=cont+1
	#LE
	session.viewports['Makefig'].odbDisplay.setPrimaryVariable(variableLabel='LE', 
	outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 'Max. In-Plane Principal'), )
	session.viewports['Makefig'].odbDisplay.setFrame(step=1, frame=i)
	
	#Print to a PNG file
	session.printToFile( fileName=figdir+'/LEhold'+str(cont)+'_'+samp, format=PNG)	
	
	#Displacement
	myViewport.odbDisplay.setPrimaryVariable(variableLabel='U', 
	outputPosition=NODAL, refinement=(INVARIANT, 'Magnitude'), )
	session.viewports['Makefig'].odbDisplay.setFrame(step=1, frame=i)
	
	#Print to a PNG file
	session.printToFile( fileName=figdir+'/Uhold'+str(cont)+'_'+samp,format=PNG)
	
	#Displacement:U2 only
	session.viewports['Makefig'].odbDisplay.contourOptions.setValues(
		spectrum='tania', maxValue=8.5E-05, minValue=-2.5E-03)
	myViewport.odbDisplay.setPrimaryVariable(variableLabel='U', 
	outputPosition=NODAL, refinement=(COMPONENT, 'U2'), )
	session.viewports['Makefig'].odbDisplay.setFrame(step=1, frame=i)
	
	#Print to a PNG file
	session.printToFile( fileName=figdir+'/U2hold'+str(cont)+'_'+samp,format=PNG)
	
	#Mises
	session.viewports['Makefig'].odbDisplay.setPrimaryVariable(variableLabel='S', 
	outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 'Mises'), )
	session.viewports['Makefig'].odbDisplay.contourOptions.setValues(
		spectrum='tania', maxValue=1.35E-01, minValue=0)
	session.viewports['Makefig'].odbDisplay.setFrame(step=1, frame=i)
	
	#Print to a PNG file
	session.printToFile( fileName=figdir+'/Shold'+str(cont)+'_'+samp, format=PNG)	

#Print out time of completion and status
timenow= datetime.datetime.now()
track=open('simulations_status.txt', 'a')
out= jobName + ' '+ 'Completed at '+ str(timenow)+ '\n****************\n'
track.write(out)
track.close()
	
odb.close()