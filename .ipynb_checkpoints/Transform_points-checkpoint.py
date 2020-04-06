'''For sample2ara: calculate inverse transform and transform annotation points
'''

import os
import subprocess
import tkinter.filedialog as fdialog


tempdir = fdialog.askdirectory(title='Please select a output directory')
param1=fdialog.askopenfile(initialdir=tempdir, title='select the first parameter file', initialdir = "D:/elastix_params_backup").name
param2=fdialog.askopenfile(initialdir=tempdir, title='select the second parameter file',initialdir = "D:/elastix_params_backup").name
points_name=fdialog.askopenfile(initialdir=tempdir, title='select the corresponding downsampled organized points').name

fixed_img=fdialog.askopenfile(initialdir=tempdir, title='select the fixed image').name
coefparam=fdialog.askopenfile(initialdir=tempdir, title='select the higherorder coeficcient file').name
#ie. here the higher order coefficient file is the transformparameters.1 (this is coupled with transformparameters.0 within the file) in the sample2ara folder

command=['elastix', 
         '-f', fixed_img,
         '-m', fixed_img,
         '-out', tempdir
         '-t0',coefparam,
         '-p',transparam0, 
         '-p',transparam1
        ]

subprocess.run(command, cwd= 'C:/Users/liu')


newparam=fdialog.askopenfile(initialdir=tempdir, title='select the newly generated transformparameter1 file').name
#This is the newly generated inverse transformation

command2=['transformix', 
         '-def', fixed_img,
         '-out', tempdir,
         '-tp',newparam
        ]

subprocess.run(command2, cwd= 'C:/Users/liu')
