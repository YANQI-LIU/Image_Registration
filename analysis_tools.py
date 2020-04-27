'''Contains tools for analysis such as make_pd and findID_origional'''

import os
import re

import numpy as np
import pandas as pd
import SimpleITK as sitk
import warnings

import skimage
from skimage import io

global atlas_labels
atlas_labels=atlas_labels=pd.read_csv('D:\Allenbrainatlas\ARA_25_micron_mhd_ccf2017\labels.csv')

def make_pd(allpoints, ending_indices,dir):
    ''' 
    Reads in all points as well as ending indices and formulates a pd structure.
    Input: all downsampled points (in transformix compatible format), corresponding indicies of endings 
    ouputs: a pandas dataframe with anatomical regions and their corresponding total points count and ending points count, list of atlas ID for each point
    
    '''
        
    ending_indices = np.genfromtxt(ending_indices, delimiter=',', dtype='int')
            
    with open(allpoints,'r') as output:
        outputpoint= output.readlines()
    
    all_points=[]
    
    if 'outputpoints' in allpoints:
        files=os.listdir(dir)
        atlas=[i for i in files if re.search("atlas.+\.mhd",i)][0]
        atlas_name=os.path.join(dir, atlas)

        for lines in outputpoint:
            m=re.search("(?:OutputIndexFixed = \[ )([0-9]+ [0-9]+ [0-9]+)", lines).groups(0)
            this_line= str(m[0]).split(' ')
            mypoints= [int(stuff) for stuff in this_line]
            all_points.append(mypoints)
    else:
        atlas_name=dir+'/ara2sample_atlas/result.mhd'
        for lines in outputpoint[2:]:
            this_line= lines.split (' ')
            mypoints= [int(stuff) for stuff in this_line]
            all_points.append(mypoints)

    atlas= sitk.ReadImage(atlas_name)
        
    points_in_atlas=[int(atlas[i]) for i in all_points ]
    #find an ID for all points
    endings_in_atlas=[points_in_atlas[i] for i in ending_indices]
    # find the IDs associated with endings

    unique_id=set(points_in_atlas)

    our_regions=atlas_labels.loc[atlas_labels['id'].isin (unique_id)]

    id_withcounts=[]
    for i in unique_id:
        id_withcounts.append([i, points_in_atlas.count(i), endings_in_atlas.count(i)])

    new_df= pd.DataFrame(id_withcounts, columns=['id', 'Total_counts','Endings_counts'])
    our_regionWcounts=pd.merge(atlas_labels, new_df)
    return our_regionWcounts.sort_values(by=['Total_counts']), points_in_atlas

def check_points(points_in_atlas):
    '''Checks whether all your points' ID is within the atlas labels
    Input: matching ID of the points (this is the second output from analysis_tools.make_pd)
    '''
    id_inatlas=[]
    for x in atlas_labels['id']:
        intID = int(x)
        id_inatlas.append(intID)

    # need to format this first ourselves,otherwise problematic for 0 and very large numbers (idk why)    

    num_of_zeros = [i for i, x in enumerate(points_in_atlas) if x == 0]
    # find the indices for which carries an id =0
    
    unique_id=set(points_in_atlas)
    
    for id_inbrain in unique_id:
        if id_inbrain not in id_inatlas:
            if id_inbrain==0:
                print(f'There are {len(num_of_zeros)} points with ID= {id_inbrain}, this index is outside of the brain, consider possible suboptimal image registration')
            else: 
                print(id_inbrain,'this index does not exist in allen reference atlas, see https://github.com/ChristophKirst/ClearMap/issues/37')
            warnings.warn('Some points do not have corresponding labels')
    return 


def findID_origional(origional_points, points_in_atlas,dir,axon=True):
    '''
    Associate origional points with atlas ID and name, default is axon
    Inputs: origional onverted resampled points and matching atlas ID (this is the second output from analysis_tools.make_pd)
    Ouputs a pd dataframe with x, y, z, atlas ID, region name, colour
    '''
    #Load the origional points
    with open(origional_points,'r') as anno:
        anno_data=anno.readlines()
    # heading is stored in anno_data[2], 1st line basically useless

    headings=anno_data[2].rstrip('\n').replace(' ', '').split(',')
    annotations=[lines.rstrip('0 1\n').split(' ') for lines in anno_data[3:]]
    #slight modification on replacing and stripping due to the format of the resampled swc
    annotation_df=pd.DataFrame(annotations, columns=headings)

    points_with_id= pd.DataFrame (zip(annotation_df['x'],annotation_df['y'], annotation_df['z'],points_in_atlas ), columns=['x', 'y','z', 'atlasID'])
    if axon==True:
        out_name=dir+'/resamp_oripoints_withID.csv'
    else:
        out_name=dir+'/D_resamp_oripoints_withID.csv'
    points_with_id.to_csv (out_name, index = None, header=True) #Don't forget to add '.csv' at the end of the path
    
    #Creates colour for each region
    uniqueID=np.unique(points_with_id['atlasID'])
    colour= np.linspace(1,np.size(uniqueID)+1, num=np.size(uniqueID),dtype='int')
    colourdict=dict(zip(uniqueID,colour))
    
    # find region name based on ID
    namedict=dict(zip(atlas_labels['id'],atlas_labels['name']))
    points_with_id['name'] = points_with_id['atlasID'].map(namedict)
    points_with_id['colour'] = points_with_id['atlasID'].map(colourdict)
    return points_with_id

def make_tif(all_points,dir, axon=True):
    ''' Project downsampled points on to a tiff stack, useful for overlaping with brain or template (ie, in imageJ)
    input: downsampled points, directory containing it (this is also the output directory) and whether annotation is axon or not (default True)
    output: a tiff stack with the same dimensions of the brain/template/atlas mhd files with downsampled points only
    each point has a value of the number of occurences (since downsampling combines multiple points as one)
    '''
    
    print('saving tif files..')

    atlas_name=dir+'/ara2sample_atlas/result.mhd'
    atlas= sitk.ReadImage(atlas_name)
    svolume=np.zeros(atlas.GetSize())
    #columns, rows, planes
    
    with open(all_points,'r') as output:
        outputpoint= output.readlines()
    
    all_points=[]
    for lines in outputpoint[2:]:
        this_line= lines.split (' ')
        mypoints= [int(stuff) for stuff in this_line]
        all_points.append(mypoints)

    zplanes=[]
    for i in all_points:
        zplanes.append( i[2])
    zplanes=np.unique(zplanes)
    temp=np.zeros(atlas.GetSize()[0:2])
    thepoints=np.asarray(all_points)

    for i in zplanes:
        index= thepoints[:,2]==i
        uindex,counts=np.unique(thepoints[index],return_counts=True, axis=0)
        for j, lines in enumerate(uindex):
            coord1,coord2=lines[0:2]
            temp[coord1][coord2]= counts[j]
        svolume[:,:,i]=temp #write this in 
        temp=np.zeros(atlas.GetSize()[0:2]) #reset the empty plane after each z
        
    
    coronal_planetmp= np.swapaxes(np.int16(svolume),0,2)
    #for some reason, if just save stuff as tiff, it will save x planes of yz view
    #here we shift the 3rd dimension with the first dimension to obtain xy view
    if axon==True:
        out_name=dir+'/DSpoints.tif'
    else:
        out_name=dir+'/D_Dspoints.tif'

    io.imsave(out_name,coronal_planetmp)
    return 