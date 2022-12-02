# Major to do, 2022-09-03 was the day I realised that Python for loops
# do not have their own scope. Need to either abstract away via functions
# or re-name variables to reduce chance of incorrect re-use.

# More general to do, refactor this code so that it is somewhat readable.


### Setup ###
from os.path  import join
from random   import randint, shuffle
from datetime import date
import pandas as pd
import numpy  as np

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
for key in given_names_by_sex.keys():
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
)


employee_demographics_list = list([])
for i in range(0, min_employee_list_length):
  employee_demographics_list.append([
      employee_type_list[i]
    , employee_name_and_sex_list[i][0]
    , employee_name_and_sex_list[i][1]
    , employee_name_and_sex_list[i][2]
    , employee_age_list[i]
    , '' # Placeholder for division
    , '' # Placeholder for department
    , '' # Placeholder for team
    , '' # Placeholder for position
    , '' # Placeholder for level
    , '' # Placeholder for employee id
    , '' # Placeholder for reports to
  ])

employees = pd.DataFrame(
    employee_demographics_list
  , columns=[
      'employee_type'
    , 'family_name'
    , 'given_name'
    , 'sex'
    , 'date_of_birth'
    , 'division'
    , 'department'
    , 'team'
    , 'position'
    , 'level'
    , 'employee_id'
    , 'reports_to'
  ]
)


### Associate Employees with Teams and Positions ###
company_executive_leadership_team = pd.read_csv(join(dir_dataset_transformed, 'company_executive_leadership_team.csv'))
company_teams                     = pd.read_csv(join(dir_dataset_transformed, 'company_teams.csv')).replace(np.nan, '', regex=True)
company_departments               = company_teams.filter(['department', 'division']).drop_duplicates().replace(r'^\s*$', np.nan, regex=True).dropna().reset_index(drop = True)

company_position_modifiers        = pd.read_csv(join(dir_dataset_transformed, 'company_position_modifiers.csv'))
company_department_head_positions = company_position_modifiers.query('level_name == "Department Head"').reset_index(drop = True)

employees_processed  = 0
employees_to_process = len(employees)


# lets try iterating through the teams and assigning them a start and end employee list offset
# then maybe we can apply a map against that range of the employee list rather than iterating
# through it
company_teams.insert(1, 'employee_offset_start', -1)
company_teams.insert(2, 'employee_offset_end'  , -1)

company_elt_team_offset_start             = 0
company_elt_team_offset_end               = len(company_executive_leadership_team)
company_department_head_team_offset_start = company_elt_team_offset_end
company_department_head_team_offset_end   = company_department_head_team_offset_start + len(company_departments)

next_team_offset_start = company_department_head_team_offset_end + 1
for i in range(0, len(company_teams)):
  current_team_size = round(organisation_size * company_teams.loc[i, 'company_size_mix'])

  company_teams.loc[i, 'employee_offset_start'] = next_team_offset_start 
  # Once we get to the final team there is a chance that the offset end will be greater
  # than the organisation size, simple guard against that.
  company_teams.loc[i, 'employee_offset_end']   = min(next_team_offset_start + current_team_size, organisation_size - 1)

  next_team_offset_start += current_team_size + 1


# Pick out ELT and Department Heads first, they should all be over 30 (sorry young people).
minimum_age_for_leaders = 30

# We'll use the index of the employee record as an employee id.
# Need to record the employee id of the CEO so that we can have them report to nobody
# and have the rest of the ELT report to them.
ceo_employee_id = company_executive_leadership_team.index[company_executive_leadership_team['executive'] == 'Chief Executive Officer'].tolist()[0]

for i in range(company_elt_team_offset_start, company_elt_team_offset_end):
  employees.loc[i, 'employee_type'] = 'executive leader'
  employees.loc[i, 'division'     ] = company_executive_leadership_team.loc[i, 'division']
  employees.loc[i, 'department'   ] = ''
  employees.loc[i, 'team'         ] = 'Executive Leadership Team'
  employees.loc[i, 'position'     ] = company_executive_leadership_team.loc[i, 'executive']
  employees.loc[i, 'level'        ] = 5 # should be made to dynamically get the level for the ELT positions but I am tired
  employees.loc[i, 'employee_id'  ] = i
  employees.loc[i, 'reports_to'   ] = ceo_employee_id

  # Set the CEO to report to nobody.
  if i == ceo_employee_id:
    employees.loc[i, 'reports_to'] = -1

  current_employee_age_years = current_year - employees.loc[i, 'date_of_birth'].year
  if current_employee_age_years < minimum_age_for_leaders:
    employees.loc[i, 'date_of_birth'] = date(
        employees.loc[i, 'date_of_birth'].year - minimum_age_for_leaders + current_employee_age_years
      , employees.loc[i, 'date_of_birth'].month
      , employees.loc[i, 'date_of_birth'].day
    )

  employees_processed  += 1
  employees_to_process -= 1

# To Do find a neater way to describe via logic/variable names that we are piggy backing off
# of the employee iteration to iterate through the departments list.
company_executive_leadership_team_length = len(company_executive_leadership_team)
company_departments_length = len(company_departments)
for i in range(company_department_head_team_offset_start, company_department_head_team_offset_end):
  current_slt_department_index = i - company_executive_leadership_team_length
  current_slt_position_index   = randint(0, len(company_department_head_positions) - 1)
  current_slt_head_query       = 'team == "Executive Leadership Team" and division == "' + company_departments.loc[current_slt_department_index, 'division'] + '"'

  employees.loc[i, 'employee_type'] = 'senior leader'
  employees.loc[i, 'division'     ] = company_departments.loc[current_slt_department_index, 'division']
  employees.loc[i, 'department'   ] = company_departments.loc[current_slt_department_index, 'department']
  employees.loc[i, 'team'         ] = 'Senior Leadership Team'
  employees.loc[i, 'position'     ] = company_department_head_positions.loc[current_slt_position_index, 'modifier']
  employees.loc[i, 'level'        ] = company_department_head_positions.loc[current_slt_position_index, 'level']
  employees.loc[i, 'employee_id'  ] = i
  employees.loc[i, 'reports_to'   ] = employees.query(current_slt_head_query).reset_index().loc[0, 'employee_id']

  current_employee_age_years = current_year - employees.loc[i, 'date_of_birth'].year
  if current_employee_age_years < minimum_age_for_leaders:
    employees.loc[i, 'date_of_birth'] = date(
        employees.loc[i, 'date_of_birth'].year - minimum_age_for_leaders + current_employee_age_years
      , employees.loc[i, 'date_of_birth'].month
      , employees.loc[i, 'date_of_birth'].day
    )

  employees_processed  += 1
  employees_to_process -= 1


organisation_size_minus_leaders      = organisation_size - employees_processed
company_teams_length                 = len(company_teams)
employees_processed_at_current_team  = employees_processed
employees_to_process_at_current_team = employees_to_process


level_0_title_modifiers = ['Graduate', 'Junior', 'Associate']

for team_index in range(0, company_teams_length):
  division    = company_teams.loc[team_index, 'division']
  department  = company_teams.loc[team_index, 'department']
  team        = company_teams.loc[team_index, 'team']

  current_department_head_query = 'team == "Senior Leadership Team" and department == "' + department + '" and division == "' + division + '"'
  department_head_id = employees.query(current_slt_head_query).reset_index().loc[0, 'employee_id']

  titles        = company_teams.loc[team_index, 'titles'].split('|')
  titles_length = len(titles) - 1
  level_mix     = {
      'level_2_mix': company_teams.loc[team_index, 'level_2_mix']
    , 'level_1_mix': company_teams.loc[team_index, 'level_1_mix']
    , 'level_0_mix': company_teams.loc[team_index, 'level_0_mix']
  }

  # Round team sizes natually and once we get to the final team cap numbers to remaining employees.
  size = round(organisation_size_minus_leaders * company_teams.loc[team_index, 'company_size_mix'])

  # I should try and write some abstraction for iterating through the team mixes, for now just
  # so that I can see some output we'll generate random titles.
  for employee_index in range(employees_processed_at_current_team, min(employees_processed_at_current_team + size, organisation_size)):
    # Make the first employee the team leader.
    if employee_index == employees_processed_at_current_team:
      team_leader_id = employee_index
      employees.loc[employee_index, 'position'  ] = 'Team Leader'
      employees.loc[employee_index, 'level'     ] = 3
      employees.loc[employee_index, 'reports_to'] = department_head_id

      if employees.loc[employee_index, 'employee_type'] == 'casual':
        employees.loc[employee_index, 'employee_type'] = 'permanent full time'
    else:
      # To do remove this randomisation of levels and change it to use the defined team mixes.
      level = randint(0, 3)

      if level == 0:
        employees.loc[employee_index, 'position'  ] = level_0_title_modifiers[randint(0, len(level_0_title_modifiers) - 1)] + ' ' + titles[randint(0, titles_length)]
      elif level == 1:
        employees.loc[employee_index, 'position'  ] = titles[randint(0, titles_length)]
      else:
        employees.loc[employee_index, 'position'  ] = 'Senior ' + titles[randint(0, titles_length)]

      employees.loc[employee_index, 'level'     ] = level
      employees.loc[employee_index, 'reports_to'] = team_leader_id

    employees.loc[employee_index, 'division'   ] = division
    employees.loc[employee_index, 'department' ] = department
    employees.loc[employee_index, 'team'       ] = team
    employees.loc[employee_index, 'employee_id'] = employee_index

    employees_processed  += 1
    employees_to_process -= 1

  employees_processed_at_current_team  = employees_processed
  employees_to_process_at_current_team = employees_to_process

employees.to_csv(join(dir_dataset_modelled, 'test_employees.csv'), index = False)