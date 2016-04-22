#Created by Tania Sanchez (2014-2016) tania.sanchezmonroy@manchester.ac.uk
#This code is submits the ABAQUS job and call the data extraction codes
cores=16

#print time submitted
timenow= datetime.datetime.now()
track=open('simulations_status.txt', 'a')
out= '****************\n'+jobName + ' '+ 'Submitted at '+ str(timenow)+'\n'
track.write(out)
track.close()

#execute
mdb.JobFromInputFile(explicitPrecision=SINGLE,memory=70, memoryUnits=PERCENTAGE, name=jobName, 
	inputFileName=InputFile, numCpus=cores, numDomains=cores, parallelizationMethodExplicit=DOMAIN,  
	type=ANALYSIS,  nodalOutputPrecision=SINGLE, numGPUs=1, userSubroutine='slsbis.for')
try:
	mdb.jobs[jobName].submit()
	mdb.jobs[jobName].waitForCompletion()
except:
	pass

execfile('All-output.py')
execfile('All-figures.py')




