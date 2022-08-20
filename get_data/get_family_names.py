# Couldn't find any reasonable only datasets to hook into for this
# so have just manually grabbed this list
# https://gist.github.com/craigh411/19a4479b289ae6c3f6edb95152214efc

### Setup ###
from os.path  import join
import pandas as pd

dir_project_root         = 'C:\Projects\Python\DatasetGenerator'
dir_dataset_raw          = dir_project_root + '\datasets\\raw'
dir_dataset_transformed  = dir_project_root + '\datasets\\transformed'
dir_dataset_modelled     = dir_project_root + '\datasets\modelled'

family_names        = pd.read_csv(join(dir_dataset_raw, 'family_names\\family_names_raw.csv'))
unique_family_names = family_names.drop_duplicates(subset=['family_name'])
unique_family_names.to_csv(join(dir_dataset_transformed, 'family_names.csv'), index = False)