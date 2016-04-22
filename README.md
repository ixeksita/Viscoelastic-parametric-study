#Created by Tania Sanchez (2014-2016) tania.sanchezmonroy@manchester.ac.uk


This set of codes can be used to perform parametric studies on spherical indentation models. 
The main program can be either called from MATLAB or directly called from ABAQUS either using
the command line or usign the CAE (run script).

The order of the program is as follows:
Shall you need to create a spherical indentation model you need to declare the pertinent
variables in 'variables.py. The units are specified according to ABAQUS units handling rules.
A. Part-mesh.py creates the indentation model using the variables declared in variables.py, then it
calls 'BC-steps.py'
B. BC-steps.py create the boundary conditions and steps for the analysis


Automated FEA and data extraction:
1. 'Main.py': The main program creates the directories needed and creates specific variables for the rest of the programs. Then it calls  ALL-run.py
2. All-run.py calls indentation.py which submits the job and waits for completion. 
3. Once completed, All-output.py and All-figures.py obtain the output data and figures needed and saved them in the output directories. 
(NOTE: the extracted figures and data can be modified depending on the desired data/analysis)
4. Once all this is completed the record and auxiliary files are deleted. The inp and odb files are kept.

If needed be, the replace-inp.py can be used to modify experimental parameters (loading time, substrate material, load, etc.) from the
previous input file to run a separate parametric study using the same configuration used for the previous nanoindentation studies. 
