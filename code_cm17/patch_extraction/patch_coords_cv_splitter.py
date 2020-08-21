import pandas as pd
import os,sys
from os.path import join
import itertools

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

data_dir = join('..','..','data','raw-data')
patch_coords_dir = join(data_dir,'patch_coords_200k')
cv_dir = join(data_dir, 'cross_val_splits_5_whole')
splits = int(splitall(cv_dir)[-1].split('_')[-2])

#Ignoring the valid generated by patch extraction
for i in range(splits):
    print('Making fold %d/%d' %(i+1,splits))
    for (mode, t_type, coord_type) in itertools.product(['training','validation'],['whole','viable'],['normal','tumor']):
        print(mode,t_type,coord_type)

        fold = pd.read_csv(join(cv_dir,'%s_fold_%d.csv'%(mode,i)))
        list_of_samples = [splitall(x)[-2] for x in list(fold['Image_Path'])]

        
        df = pd.read_csv(join(patch_coords_dir,'train_%s_%s.txt'%(t_type,coord_type)),names=['pid', 'mask', 'x', 'y', 'tf'])

        filtered_df =  df[df.apply(lambda x: splitall(x['pid'])[-2] in list_of_samples, axis=1)]

        
        out_dir = join(patch_coords_dir,'%dfold_%d'%(splits,i))
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)
        filtered_df.to_csv(join(out_dir,'%s_%s_%s.txt'%(mode,t_type,coord_type)), header=False,index=False)


