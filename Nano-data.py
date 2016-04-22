#Created by Tania Sanchez Monroy (April 2016) tania.sanchezmonroy@manchester.ac.uk
#Customized code for FEA obtained indentation data (can be easily adapted for 
#any othe plots)
#This code opens the FEA obtained data sets, creates plots and store all the data in
#one single text file shall it need to be imported
import re
import os
import glob 
import pandas as pd
import matplotlib.pyplot  as plt
import brewer2mpl 
import matplotlib.ticker as ticker

#Get working directory and set path and type of files to read (data files)
os.getcwd()
path="C:/Work/scripting/16uN/output"
os.chdir(path)
data = path+'\*.txt'
lista= glob.glob(data)

#Remove any pre-exixsting sets of data
filename='alldata.txt'
if os.path.exists(filename)==True:
    os.remove(filename)

#sort files by name (which is related to the sample thickness)
digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))

lista.sort(key=tokenize)

#Get colormap
#set2 = brewer2mpl.get_map('BuPu', 'sequential', 9).mpl_colors #if less than 9 plots brewer can be used
#more than 9 
execfile('colorpal.py')
set2=y

#Font={'fontname': 'Arial'}
Font={'fontname': 'computer modern sans serif'}
plt.rc('font', family='computer modern sans serif')


#Creating figure 
fig, ax =plt.subplots(figsize=(8,8))
figure, ax1 =plt.subplots(figsize=(8,8))
figg, ax2=plt.subplots(figsize=(8,8))
#size= marker size
size=30
counter=-1

#create data frame for all data
alldata=pd.DataFrame()

#To calculate compliance
F= (16*(0.015**(0.5)))/(3*12.5E-06)

#open the files, create data frame
for i in lista:
    counter+=1
    df=pd.read_csv(i,sep='\s+')
    df.columns=['Time', 'displacement']
    lab= i[len(path)+20:-4]
    creept=df.Time[432:]
    #creep=df.displacement[432:]/df.displacement[432]
    creep=df.displacement[432:]
    J= (creep**(1.5))*F
    
    ####Creating the scatter plot of the data
    color=set2[counter]
    
    ax.scatter(df.Time,df.displacement, color=color, marker='o',alpha=1.0, 
             s=size, linewidth=0.2, edgecolor='White', label=lab+'um')
             
    ax1.scatter(creept,creep, color=color, marker='o',alpha=1.0, 
             s=size, linewidth=0.2, edgecolor='White', label=lab+'um')
    
    
    ax2.scatter(creept,J, color=color, marker='o',alpha=1.0, 
             s=size, linewidth=0.2, edgecolor='White', label=lab+'um')             
             
    #plt.colorbar()
    #more customization    
    plt.xlabel('Time (s)', **Font)
    ax.set_ylabel('Displacement (mm)', **Font)
    ax.set_ylim(0.0, 0.003)
    ax.set_xlim(0.0, 7.0)
    ax1.set_ylim(0.001, 0.003)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels), loc='upper left', 
              frameon=False, fontsize=9, scatterpoints=1)  # reverse to keep order consistent
    ax1.legend(reversed(handles), reversed(labels), loc='upper right', 
              frameon=False, fontsize=9, scatterpoints=1)  # reverse to keep order consistent          
    #ax.legend(frameon=False, loc='upper left', fontsize=9, scatterpoints=1)
    tick_sp=0.5
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_sp))
    
   #Save all the data sets in a separate file (cleaned data)
    Displcol= 'Displacement'+str(counter)
    Timecol= 'Time'+str(counter)
    alldata[Timecol] = df.Time
    alldata[Displcol] = df.displacement
    
    
alldata.to_csv('alldata.txt',sep='\t' , na_rep='', line_terminator='\n', index=None)
#plt.close('all')
