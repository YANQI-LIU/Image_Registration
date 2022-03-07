''' Transform grey scale image using Transformix based on transform parameter files from a previous registration

ie. transform another channel based on registration between autofluorescent channel and allen brain template

User input: output directory, transformParameters, and file to be transformed

NOTE: This py file needs to be under the same directory as elastix to work
'''

import os

import subprocess

import tkinter.filedialog as fdialog

tempdir = fdialog.askdirectory(title='Please select a output directory')
transparam1=fdialog.askopenfile(initialdir=tempdir, title='select the transformparameter1 file').name
atlasname=fdialog.askopenfile(initialdir=tempdir, title='select the file to be transformed').name


command=['transformix', 
         '-out', tempdir,
         '-tp',transparam1, 
         '-in', atlasname
        ]

subprocess.run(command, cwd= 'C:/Users/liu')