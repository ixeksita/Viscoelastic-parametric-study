#Created by Tania Sanchez (2014-2016) tania.sanchezmonroy@manchester.ac.uk
# This code can be used to modify experimental parameters on the indentation file
# to run a wide range of parameteric studies


import os
os.getcwd()
os.chdir('C:\Work\Scripting')
tr=4.47
load= -19.5e-06
hold=2.1075
id='-22'
material='VISHAY'

#filename=['5','8', '15', '25', '100', '200', '500', '750', '1000','1500', '2000', '2500', '3000']
filename=['1500', '2000', '2500', '3000']
for i in filename:
	listBack= i+'um-final.inp'
	if os.path.exists(listBack)==True:
		text_file = open('22uN_v/'+i+'um-final.inp', "w")
		count=0
		for line in open (i+'um-final.inp') :
			count+=1
			if  line.startswith('0.001, 4.'):text_file.write('0.001, '+str(tr)+', 1e-10, 0.01 \n')
       
			elif line.startswith('_PickedSet26, 2,'):
				text_file.write('_PickedSet26, 2, '+str(load)+'\n')
    
			elif line.startswith('0.001, 2.'):
				text_file.write('0.001, '+str(hold)+', 1e-10, 0.1 \n')
    
			elif line.startswith('*Solid Section, elset=__PickedSet26,'):
				text_file.write('*Solid Section, elset=_PickedSet26, material='+material+'\n')

			else:
				text_file.write(line)
		print ("******************** \n File created: %s \n********************\n " %(listBack))
	else:
		print ('Could not find: %s' %(listBack))

#print count
text_file.close()

#('Indenter_RP, 2,'):
#text_file.write('Indenter_RP, 2, '+str(load)+'\n')
#line.startswith('*Solid Section, elset=_PickedSet7,'):


#text_file.write('_PickedSet26, 2, '+str(load)+'\n')
#line.startswith('*Solid Section, elset=_PickedSet26,'):

