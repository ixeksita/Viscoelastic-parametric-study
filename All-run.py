#Created by Tania Sanchez (2014-2016) tania.sanchezmonroy@manchester.ac.uk
# This code is used to run the FEsimulations and upon completion it deletes the record files

Mdb()
#execute routines
execfile('indentation.py')

#Delete auxiliary data 
execfile('All-DelFile.py')
	
#Move odb into Output directory
if os.path.exists(odbdir)==True:
	shutil.move(odbdir, outdir)

