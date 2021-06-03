'''
Create a downsampled image stack from already downsmapled MaSIV stack
user inputs: 
MaSIV downsampled stack, goal resolution (10 or 25 um allen atlas), output directory

'''

import os

import tkinter as tk
import tkinter.filedialog as fdialog
from tkinter import simpledialog
# this is the gui for finding directory and files

import skimage
from skimage import io
from skimage import transform as tf

import numpy as np
import matplotlib.pyplot as plt

# Select the directory containing already stitched planes from stitchit (Rob code)
stack=fdialog.askopenfile(initialdir='Z:\\', title='select the MaSIVed stack to be further downsampled').name                               

# User input required for raw xyz resolution and goal dimension

xy = simpledialog.askfloat("Input", "What is the xy resolution '(in um)' ?",
                               minvalue=0, maxvalue=100)
# xy = 0.6
z = 5
goal_xyz = simpledialog.askfloat("Input", "What do you want to downsample the resolution to '(in um)' ?",
                               minvalue=10, maxvalue=100)

outdir = fdialog.askdirectory(title='Please select the output directory')

masiv_ds=stack[stack.find('_DS')+len('_DS'):stack.rfind('.tif')]
masiv_ds=float(masiv_ds)
masiv_xy= round (xy*masiv_ds,2)
print (f'MASIV stack is downsampled : {masiv_ds}, The masiv stack is : {masiv_xy} um/pixels') 
# note that this gives a float and have many decimal places which the end digit is non-zero
# for avoiding confusion we keep the 2 decimal places

ratioxy= round (goal_xyz/masiv_xy, 3)
ratioz=goal_xyz/z

message = (f"Sample resolution is {xy, xy, z} um in x y z. "
f"downsampling to {goal_xyz} um. "
f"dowmsample ratio is xy = {ratioxy} and z = {ratioz}.")

print(message)

im = io.imread(stack)

z,y,x= im.shape
print (im.shape) 

new_rows=int(y/ratioxy)
new_col=int(x/ratioxy)
new_z=int(z/ratioz)
tifarray = np.zeros([new_rows, new_col, z])

print( f'new shape of the data is  x y z= {new_rows, new_col, new_z}')

for i in range (z):
    new_xyplane=tf.resize(im[i,:,:],[new_rows, new_col], order=1, anti_aliasing=1)
    tifarray[:,:,i]= new_xyplane

del im

tifarray2 = np.zeros([new_rows, new_col, new_z])

if ratioz==1:
    print('z axis is not downsampled')
    tifarray2=tifarray
else:
    tifarray2 = np.zeros([new_rows, new_col, new_z])
    for i in range (new_rows):
        new_xyplane=tf.resize(tifarray[i,:,:], [new_col, new_z], order=0, anti_aliasing=0)
        tifarray2[i,:,:,]= new_xyplane

del tifarray

imguint16=skimage.img_as_uint(tifarray2)

coronal_planetmp= np.swapaxes(imguint16,0,2)
coronal_plane= np.swapaxes(coronal_planetmp,1,2)

out_name= outdir[3:8]+f'_{goal_xyz}um.tiff'

os.chdir(outdir)
io.imsave(out_name, coronal_plane)
