import os

import pandas as pd

import numpy as np

import tkinter as tk
import tkinter.filedialog as fdialog
from tkinter import simpledialog

xy = 0.8
z = 5
outdir = fdialog.askdirectory(title='Please select the output directory')
anno_file=fdialog.askopenfile(initialdir=outdir, title='Select the eswc file containing the annotations').name 


print('Converting pixels to ums....')

anno=open(anno_file,'r')
anno_data=anno.readlines()
# heading is stored in anno_data[2], 1st line basically useless

headings=anno_data[2].rstrip('\n').split(' ')
annotations=[lines.rstrip('\n').split(' ') for lines in anno_data[3:]]

annotation_df=pd.DataFrame(annotations, columns=headings)

annotation_df['x']=pd.to_numeric(annotation_df['x'])*xy
annotation_df['y']=pd.to_numeric(annotation_df['y'])*xy
annotation_df['z']=pd.to_numeric(annotation_df['z'])*z

tfile = open(anno_file+'converted.eswc', 'a')
tfile.write(anno_data[0])
tfile.write(anno_data[1])
tfile.write(anno_data[2])
tfile.write(annotation_df.to_string(header=False, index=False))
tfile.close()

print('Done!')
