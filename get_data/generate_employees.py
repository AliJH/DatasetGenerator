### Setup ###
from os.path  import join
from random   import randint, shuffle
from datetime import date
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
for key in given_names_by_sex.items():
  given_names_by_sex[key].reset_index(drop = True, inplace = True)

def validate_mix_percentages(mix):
  # To do: offer suggestions for fixes
  outcome = {
      'validation_result' : False
    , 'validation_message': ''
    , 'mix_total'         : 0.00
    , 'mix_variance'      : 0.00
    , 'values_over_one'   : []
    , 'values_under_zero' : []
  }

  # Begin Loop
  for key, value in mix.items():
    if value > 1.00:
      outcome['values_over_one'].append(key)
    elif value < 0.00:
      outcome['values_under_zero'].append(key)
    
    outcome['mix_total'] += value
  # End Loop

  outcome['mix_total']    = round(outcome['mix_total']       , 2)
  outcome['mix_variance'] = round(outcome['mix_total'] - 1.00, 2)
  
  if outcome['mix_variance'] == 0.00:
    outcome['validation_result']  = True
    outcome['validation_message'] = 'Validation Passed'
  else:
    outcome['validation_result']  = False
    outcome['validation_message'] = 'Variance of ' + str(outcome['mix_variance']) + ' mix total should equal 1.'
  
  return outcome

days_in_month_by_month_number = {
      1 : 31
    , 2 : 28 # Yes I know but this is good enough.
    , 3 : 31
    , 4 : 30
    , 5 : 31
    , 6 : 30
    , 7 : 31
    , 8 : 31
    , 9 : 30
    , 10: 31
    , 11: 30
    , 12: 31
}



### Configure employee demographic variables ###
# Very rough starting point much refactoring needed.
# Will eventually need to shift this into a GUI of
# some sort.
organisation_size = 1000


# Start: Generate Employee Type #
default_employee_type_mix = {
    'permanent full time': .50
  , 'permanent part time': .10
  , 'temporary full time': .20
  , 'temporary part time': .05
  , 'casual'             : .05
  , 'contractor'         : .10
  , 'volunteer'          : .00
}
default_employee_type_mix_validation_result = validate_mix_percentages(default_employee_type_mix)

employee_type_list = list([])
for key, value in default_employee_type_mix.items():
  employee_type_list.extend(key for i in range(int(organisation_size * value)))
# End: Generate Employee Type #

# Start: Generate Employee Name and Sex #
default_sex_mix = {
      'male'      : .40
    , 'female'    : .40
    , 'non-binary': .20
}
default_sex_mix_validation_result = validate_mix_percentages(default_sex_mix)

employee_name_and_sex_list = list([])
for key, value in default_sex_mix.items():
  for i in range(int(organisation_size * value)):
    employee_name_and_sex_list.append([
        family_names           .iloc[[randint(0, len(family_names)            - 1)]]['family_name'].values[0]
      , given_names_by_sex[key].iloc[[randint(0, len(given_names_by_sex[key]) - 1)]]['given_name'].values[0]
      , key
    ])
# End: Generate Employee Name and Sex #

# Start: Generate Employee Age #
default_age_mix = {
      'high': {'mix': .25, 'lower_age': 55, 'upper_age': 65}
    , 'mid' : {'mix': .50, 'lower_age': 30, 'upper_age': 54}
    , 'low' : {'mix': .25, 'lower_age': 20, 'upper_age': 29}
}

employee_age_list = list([])
current_year      = date.today().year
for key, value in default_age_mix.items():
  year_lower_bound = current_year - value['upper_age']
  year_upper_bound = current_year - value['lower_age']

  for i in range(int(organisation_size * value['mix'])):
    month        = randint(1, 12)
    day_of_month = randint(1, days_in_month_by_month_number[month])
    year         = randint(year_lower_bound, year_upper_bound)
    employee_age_list.append(date(year, month, day_of_month))
# End: Generate Employee Age #

# Merge Lists.
# Start: Prepare lists for merging.
# Shuffling is required otherwise final output will be skewed towards position
# of mix types across the different mixes.
shuffle(employee_type_list)
shuffle(employee_name_and_sex_list)
shuffle(employee_age_list)

# Lengths may differ between lists due to rounding of the mix type values when
# applied to the organisation size.
min_employee_list_length = min(
    len(employee_type_list)
  , len(employee_name_and_sex_list)
  , len(employee_age_list)
) + 1


employee_demographics_list = list([])
for i in range(0, min_employee_list_length):
  employee_demographics_list.append([
      employee_type_list[i]
    , employee_name_and_sex_list[i][0]
    , employee_name_and_sex_list[i][1]
    , employee_name_and_sex_list[i][2]
    , employee_age_list[i]
  ])

employees = pd.DataFrame(
    employee_demographics_list
  , columns=['employee_type', 'family_name', 'given_name', 'sex', 'date_of_birth']
)

### Configure team demogrpahic variables ###
# Will be implemented as part of the employee title generation
# default_level_mix = {
#     'level 0': .25
#   , 'level 1': .50
#   , 'level 2': .25 
# }


