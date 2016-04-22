#Created by Tania Sanchez (2014-2016) tania.sanchezmonroy@manchester.ac.uk
#Main code for spherical indentation FEA (parametric studies)

#Import relevant modules 
from job import *
from visualization import *
from connectorBehavior import *
from abaqus import *
from abaqusConstants import *
import visualization
import os
import datetime
import shutil
from odbAccess import *
import sys

execfile('variables.py')
PP=load*1000000
#Make save and work directories
wDr=os.getcwd()
sDr1=wDr+'/'+'ViscoelasticOutputFiles_'+str(PP)+'uN'

#Make directories for the output data
if os.path.isdir(sDr1)==False:
	os.mkdir(sDr1)
os.mkdir(sDr1+'/Output')
os.mkdir(sDr1+'/Figures')

#Path to the directories 
outdir= sDr1+'/Output'
figdir=sDr1+'/Figures'
  
listBack=['Output-displacement.dat','Output-contactarea.txt']
for i in listBack:
	if os.path.exists(i)==True:
		os.remove(i)

#names variables
step1='Indentation_visco'
step2='Holding_visco'
nodeOut='BT_vert'


#Input files and associated name variables
#filename=['5','8','15','25','100','200','500','750','1000','1500','2000','2500','3000']
filename=['1500','2000','2500','3000']
for ix in range(len(filename)):
	if int(filename[ix]) <100:
		samp= filename[ix]
		jobName= samp+'um-final'
		partName='SAMPLE-1'
		sample = 'SAMPLE-'+ samp
		odbname = samp+'um-final.odb'
		varprin= '_U:Magnitude PI: '+partName+ ' N: 3'
		InputFile= jobName+'.inp'
		#nodeOut= '3'
		
		#Run
		execfile('All-run.py')
	
	elif 100<=int(filename[ix]) <1500:
		samp= filename[ix]
		jobName= samp+'um-final'
		partName='SAMPLE-1'
		sample = 'SAMPLE-'+ samp
		odbname = samp+'um-final.odb'
		varprin= '_U:Magnitude PI: '+partName+ ' N: 7'
		InputFile= jobName+'.inp'
		#nodeOut= '7'	

		#Run
		execfile('All-run.py')
		
	elif 1500<=int(filename[ix]) <3000:
		samp= filename[ix]
		jobName= samp+'um-final'
		partName='SAMPLE-1'
		sample = 'SAMPLE-'+ samp
		odbname = samp+'um-final.odb'
		varprin= '_U:Magnitude PI: '+partName+ ' N: 8'
		InputFile= jobName+'.inp'
		#nodeOut= '8'	

		#Run
		execfile('All-run.py')
	
	else:
		samp= filename[ix]
		jobName= samp+'um-final'
		partName='SAMPLE-'+ '3000UM' +'-MED-1'
		odbname = samp+'um-final.odb'
		#varprin= 'U:Magnitude PI: SAMPLE-3000UM-MED-1 N: 6805'
		varprin='_U:Magnitude PI: SAMPLE-3000UM-MED-1 N: 6805'
		InputFile= jobName+'.inp'
		nodeOut= '6805'
		
		#Run
		execfile('All-run.py')
		
		#delete record files
listBack=['abaqus.rpy','abaqus.rec','abaqus_acis.log','save_abaqus.rec']
for i in range(1,100):
	listBack=listBack+['abaqus.rpy.'+str(i),'abaqus'+str(i)+'.rec','save_abaqus'+str(i)+'.rec']
for i in listBack:
	if os.path.exists(i)==True:
		os.remove(i)

execfile('finish.py')
		