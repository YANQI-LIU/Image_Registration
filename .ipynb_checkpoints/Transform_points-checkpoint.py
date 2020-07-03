'''For sample2ara: calculate inverse transform and transform annotation points

NOTE: This py file needs to be under the same directory as elastix to work
'''

import os
import subprocess
import tkinter.filedialog as fdialog


tempdir = fdialog.askdirectory(title='Please select a output directory')
param1=fdialog.askopenfile(title='select the first parameter file', initialdir = tempdir).name
param2=fdialog.askopenfile(title='select the second parameter file',initialdir = tempdir).name

fixed_img=fdialog.askopenfile(initialdir=tempdir, title='select the fixed image').name
coefparam=fdialog.askopenfile(initialdir=tempdir, title='select the higherorder coeficcient file').name
#ie. here the higher order coefficient file is the transformparameters.1 (this is coupled with transformparameters.0 within the file) in the sample2ara folder

command=['elastix', 
         '-f', fixed_img,
         '-m', fixed_img,
         '-out', tempdir,
         '-t0',coefparam,
         '-p',param1, 
         '-p',param2
        ]

subprocess.run(command, cwd= 'C:/Users/liu')


print('Inverse transform generated!')

points_name=fdialog.askopenfile(initialdir=tempdir, title='select the corresponding downsampled points').name
newparam=fdialog.askopenfile(initialdir=tempdir, title='select the newly generated transformparameter1 file').name
#This is the newly generated inverse transformation
tempdir_new = fdialog.askdirectory(title='Please select a output directory for your transformed points')

command_line= ['transformix',
               '-def',
               points_name,
               '-out',
               tempdir_new,
               '-tp',
               newparam]
subprocess.run(command_line,cwd= 'C:/Users/liu')

anwser=None
while anwser not in ('y' , 'n'):
    anwser= input('Transform another point file using the same inverse transform? y/n: ')
    if anwser=='y':
        points_name2=fdialog.askopenfile(initialdir=tempdir, title='select the corresponding downsampled points').name
        tempdir_new2 = fdialog.askdirectory(title='Please select a output directory for your transformed points')
        command_line2= ['transformix',
                        '-def',
                       points_name2,
                       '-out',
                       tempdir_new2,
                       '-tp',
                       newparam ]
        subprocess.run(command_line2,cwd= 'C:/Users/liu')
    elif anwser=='n':
        pass
    else:
        print('Please enter y or n, case sensitive')