import os

import numpy as np
import pandas as pd

import tkinter as tk
import tkinter.filedialog as fdialog
from tkinter import simpledialog

outdir = fdialog.askdirectory(initialdir='D:/', title='Please select the output directory')
resample_file=fdialog.askopenfile(initialdir='M:/analysis/Yanqi_Liu/Annotations/', title='Select the eswc file containing the converted and recampled annotations').name 

resampled_xyz = simpledialog.askfloat("Input", "What is the x, y and z resolution in um after converting and resampling?",
                               minvalue=0.0, maxvalue=100)
goal_xyz = simpledialog.askfloat("Input", "What do you want to downsample the resolution to '(in um)' ?",
                               minvalue=10, maxvalue=100)

ratioxyz=goal_xyz/resampled_xyz

message = (f"Resampled annotation step size is {resampled_xyz} um in x y z. "
f"downsampling to {goal_xyz} um. "
f"dowmsample ratio is {ratioxyz}.")

print(message)

input("Press Enter to continue...")

resampled_anno=open(resample_file,'r')
resampled_anno_data=resampled_anno.readlines()
# heading is stored in anno_data[2], 1st line basically useless

headings=resampled_anno_data[2].rstrip('\n').replace(' ', '').split(',')
resampled_annotations=[lines.rstrip('0 1\n').split(' ') for lines in resampled_anno_data[3:]]
#slight modification on replacing and stripping due to the format of the resampled swc

resampled_annotation_df=pd.DataFrame(resampled_annotations, columns=headings)

ds_x= pd.to_numeric(resampled_annotation_df['x'])
ds_x=ds_x/ratioxyz
ds_xround=ds_x.astype(int).astype(str)
ds_y= pd.to_numeric(resampled_annotation_df['y'])
ds_y=ds_y/ratioxyz
ds_yround=ds_y.astype(int).astype(str)

ds_z= pd.to_numeric(resampled_annotation_df['z'])
ds_z=ds_z/ratioxyz
ds_zround=ds_z.astype(int).astype(str)

ds_coordinates= pd.DataFrame(columns=['x','y','z'])
ds_coordinates['x']=ds_xround
ds_coordinates['y']=ds_yround
ds_coordinates['z']=ds_zround

q = [' '.join(x) for x in zip(ds_xround,ds_yround,ds_zround)]

if 'D' in resample_file:
    out_name= outdir[3:]+ f'D_{goal_xyz}voxel_trace_1umStepsize.txt'
else:
    out_name= outdir[3:]+ f'_{goal_xyz}voxel_trace_1umStepsize.txt'
print(out_name)
input("Check the output name carefully! Press Enter to continue...")

num_row=len(resampled_annotation_df.index)
f=open(outdir+'/'+out_name,'w+')
f.write('point'+'\n')
f.write(str(num_row)+'\n')

for lines in q:
    f.write(lines+'\n')

f.close()

print('Downsampling annotation done.')

print('Finding endings of the annotations...')
list_parent= resampled_annotation_df['pid'].to_numpy()

parent_index=np.argwhere(list_parent=='-1')
ending_index=parent_index[:-1]+1
ending_index=np.insert(ending_index, 0, 0)
print(f'There are {len(ending_index)} endings')

endings_df=resampled_annotation_df.iloc[ending_index]

if 'D' in resample_file:
    out_name_endings= outdir[3:]+ f'D_endings.csv'
else:
    out_name_endings= outdir[3:]+ f'_endings.csv'
print(outdir+'/'+out_name_endings)

np.savetxt(outdir+'/'+out_name_endings, ending_index, delimiter=",", fmt='%i')
print('File saved in the output directory.')