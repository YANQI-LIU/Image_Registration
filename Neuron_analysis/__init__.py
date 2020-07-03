'''Package for dealing with single neuron annotated points in corresponding atlases

'''

import os
import re

import numpy as np
import pandas as pd


import tkinter as tk
import tkinter.filedialog as fdialog
from tkinter import simpledialog

__all__ = ["atlas", "points", "analysis_tools"]

global atlas_labels
atlas_labels=atlas_labels=pd.read_csv('D:\Allenbrainatlas\ARA_25_micron_mhd_ccf2017\labels.csv')

global fullatlas_name
fullatlas_name='D:\Allenbrainatlas\ARA_25_micron_mhd_ccf2017\\annotation_25.mhd'

def find_mousename(dir):
    '''find the mouse name from out dir.
    example D:/AL142 will return AL142'''
    m=re.search('\D{2}[0-9]{3}', dir)
    return m[0]

def find_crop(name):
    ''' takes in atlas or tempalte name that has xxx-xxx in its name.
    finds the missing section in z coronal plane to transform back to original full span(1-528)
    For exmaple, for atlas_104-400.mhd, will output 103,128'''
    m= re.search("[0-9]{2,3}.[0-9]{3}",name)[0]
    to_add= m.split('-')
    lead= int(to_add[0])-1
    trail= 528 - int(to_add[1])+1-1
    return lead, trail

def get_pt_natlas(dspoint_name,outdir, full=False):
    '''Read the downsampled points and get the corresponding atlas name
    '''
    with open(dspoint_name,'r') as output:
        outputpoint= output.readlines()
    
    all_points=[]
    if 'outputpoints' in dspoint_name:
        files=os.listdir(outdir)
        atlas=[i for i in files if re.search("atlas.+\.mhd",i)][0]
        atlas_name=os.path.join(outdir, atlas)

        for lines in outputpoint:
            m=re.search("(?:OutputIndexFixed = \[ )([0-9]+ [0-9]+ [0-9]+)", lines).groups(0)
            this_line= str(m[0]).split(' ')
            mypoints= [int(stuff) for stuff in this_line]
            all_points.append(mypoints)
    else:
        atlas_name=outdir+'/ara2sample_atlas/result.mhd'
        for lines in outputpoint[2:]:
            this_line= lines.split (' ')
            mypoints= [int(stuff) for stuff in this_line]
            all_points.append(mypoints)
    
    if full== True:
        atlas_name=fullatlas_name
    else: 
        pass
    return all_points, atlas_name

def whatis ():
    '''input the ID of a brain region and returns full name and other details'''
    x=input('what is it that you look for?')
    index=atlas_labels.id==int(x)
    print (f'Atlas id= {atlas_labels.id[index]}\n' 
           f'Name= {atlas_labels.safe_name[index]}\n'
           f'Hemisphere= {atlas_labels.hemisphere_id[index]}')
    return