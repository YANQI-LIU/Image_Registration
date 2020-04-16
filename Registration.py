'''Registration to Allen mouse ccf
Works for both sample2ara and ara2sample, just switch the 2 image file accordingly

Requirements: mhd formats of your image stack and allen brain template in the correct z orientation (can be done in imageJ to flip the Y order. Image->transform->flipz)

User inputs: define output directory, moving image, fixed image, elastix parameter file (in order)

NOTE: This py file needs to be under the same directory as elastix to work
'''

import os

import subprocess

import tkinter.filedialog as fdialog

# this is the gui for finding directory and files

import shutil

tempdir = fdialog.askdirectory(title='Please select a output directory')
fixed_img=fdialog.askopenfile(initialdir=tempdir, title='select the fixed image').name
# need the .name part because askopenfile returns an io.textiowrapper not the full str name
moving_img=fdialog.askopenfile(initialdir=tempdir, title='select the moving image').name

param1=fdialog.askopenfile(title='select the first parameter file', initialdir = "D:/elastix_params").name
param2=fdialog.askopenfile(title='select the second parameter file',initialdir = "D:/elastix_params").name

shutil.copy(param1, tempdir)
shutil.copy(param2, tempdir)

command_line= ['elastix -f '+ fixed_img+ ' -m ' + moving_img+ 
               ' -out '+ tempdir+ ' -p '+ param1+
              ' -p ' + param2]
print('formulated commandline: ' , command_line)

input("Press Enter to continue...")

command=['elastix', 
         '-f', fixed_img, 
         '-m', moving_img,
         '-out', tempdir,
         '-p', param1, 
         '-p', param2
        ]

subprocess.run(command, cwd= 'C:/Users/liu')

print('The elastix command was: ' + command_line)

answer=None
exit_this=0
while answer not in ('y','n') and exit_this!=0:
	answer= input('Rerun the previous elastix command?[y/n]')
	if answer =='y':
		subprocess.run(command, cwd= 'C:/Users/liu')
	elif answer=='n':
        exit_this=1
		pass
	else:
		print('Please enter y or n, case sensitive')

