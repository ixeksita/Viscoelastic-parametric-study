#Created by Tania Sanchez (2014-2016) tania.sanchezmonroy@manchester.ac.uk
#Parameters used for parametric study (viscoelastic materials indentation)

#Note the units correspond to SI (s, mm, N)


#R: indenter radius,  thickness: sample thickness, width:radial length of the sample
# cawidth: length of contact area (the minimun is cawidth=R)
#small_mesh: mesh size of the elements under the indenter
#substrate material: 'glass_section', 'vishay_section' or anhy other material 
# tr: rising (loading) time, thold: holding time
#load: indentation load (in N)

R=0.015
thickness =1.5
width=0.2

cawidth=0.02
#small_mesh= R/125
small_mesh= R/200

#max_meshv= thickness/120
max_meshv=thickness/100
max_mesh=thickness/60
max_meshh=0.015

tr= 4.26
thold= 2.1066
load= 12.5E-06

model= 'Spherical_indentation'
indenter = 'Indenter'
specimen= 'Sample'
substrate_material='glass-section'