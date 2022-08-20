### Setup ###
from os.path  import join
from random   import randint
import pandas as pd

dir_project_root         = 'C:\Projects\Python\DatasetGenerator'
dir_dataset_raw          = dir_project_root + '\datasets\\raw'
dir_dataset_transformed  = dir_project_root + '\datasets\\transformed'
dir_dataset_modelled     = dir_project_root + '\datasets\modelled'

family_names             = pd.read_csv(join(dir_dataset_transformed, 'family_names.csv'))
given_names              = pd.read_csv(join(dir_dataset_transformed, 'given_names.csv'))

given_names_by_sex = {
    'non-binary': given_names[given_names['sex'] == 'non-binary']
  , 'female'    : given_names[given_names['sex'] == 'female']
  , 'male'      : given_names[given_names['sex'] == 'male']
}
given_names_by_sex['non-binary'].reset_index(drop = True, inplace = True)
given_names_by_sex['female']    .reset_index(drop = True, inplace = True)
given_names_by_sex['male']      .reset_index(drop = True, inplace = True)


### Configure employee demographic variables ###
# Very rough starting point much refactoring needed.
# Will eventually need to shift this into a GUI of
# some sort.
organisation_size = 1000

default_employee_type_mix = {
    'permanent full time': .50
  , 'permanent part time': .10
  , 'temporary full time': .20
  , 'temporary part time': .05
  , 'casual'             : .05
  , 'contractor'         : .10
  , 'volunteer'          : .00
}
employee_type_list = []
for key, value in default_employee_type_mix.items():
  employee_type_list.extend(key for i in range(int(value * organisation_size)))

default_sex_mix = {
      'male'      : .40
    , 'female'    : .40
    , 'non-binary': .20
}
employee_name_and_sex_list = []
for key, value in default_sex_mix.items():
  for i in range(int(organisation_size * value)):
    employee_name_and_sex_list.append([
        family_names           .iloc[[randint(0, len(family_names) - 1)]]           ['family_name'].values[0]
      , given_names_by_sex[key].iloc[[randint(0, len(given_names_by_sex[key]) - 1)]]['given_name'].values[0]
      , key
    ])

default_age_mix = {
      'high': .25
    , 'mid' : .50
    , 'low' : .25
}



### Configure team demogrpahic cariables ###
# Will be implemented as part of the employee title generation
# default_level_mix = {
#     'level 0': .25
#   , 'level 1': .50
#   , 'level 2': .25 
# }

