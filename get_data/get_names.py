# This script serves two purposes:
#   1 - To get back into using Python after many many years of not.
#   2 - To generate a dataset of names to be used for creating a sample HR
#       dataset that I can use to try and build some interesting Power BI
#       visualisations.

# I am using the Queensland Government Open Data Top 100 Baby Names by year
# dataset to get first names. The easiest way to get these names would be to go
# go through the portal and download all of the files by hand but this would
# not help me achieve purpose 1 so here we are.


### Setup ###
from enum import unique
from bs4            import BeautifulSoup
from urllib.request import urlopen
from os             import listdir
from os.path        import isfile, join
import pandas       as pd
import numpy        as np

dir_project_root         = 'C:\Projects\Python\DatasetGenerator'
dir_dataset_raw          = dir_project_root + '\datasets\\raw'
dir_dataset_transformed  = dir_project_root + '\datasets\\transformed'
dir_dataset_modelled     = dir_project_root + '\datasets\modelled'

dir_dataset_raw_given_names = dir_dataset_raw + '\given_names'


### Save Raw Given Names Data To Raw ###
# Load HTML of the Top 100 Baby Names dataset. This page links to each of the
# by year dataset pages. Each of these specific by year dataset pages has a
# link to a csv version of the dataset which will download into our transformed
# directory.
url_root        = 'https://data.qld.gov.au'
url_names_root  = url_root + '/dataset/top-100-baby-names'
html_names_root = BeautifulSoup(urlopen(url_names_root).read(), 'html.parser')

# For all anchor tags that sit directly under a list item with class
# resource-item extract the href attribute of the anchor tag. For this page as
# at 2022-08-10 these represent the relative paths to each linked name dataset.
relative_urls_names_datasets = [a.attrs['href'] for a in html_names_root.select('li.resource-item a')]

for url_current_dataset in relative_urls_names_datasets:  
  html_names_current_page = BeautifulSoup(urlopen(url_root + url_current_dataset).read(), 'html.parser')
  url_names_current_csv   = html_names_current_page.select('a.resource-url-analytics')[0].attrs['href']
  fn_names_current_csv    = str.rsplit(url_names_current_csv, '/')[-1]
  dataset_current_csv     = urlopen(url_names_current_csv).read()

  with open(join(dir_dataset_raw_given_names, fn_names_current_csv), mode='wb') as f:
    f.write(dataset_current_csv)


### Create transformed Dataset of Given Names With Sex ###
# Open all raw given names datasets and create a list of unique names with sex.
all_given_names_list = []
def collect_given_names(list, name, sex, source):
  name_cleaned = str(name).strip().lower().capitalize()

  if len(name_cleaned) >= 0:
    list.append([name_cleaned, sex, source])


for f in listdir(dir_dataset_raw_given_names):
  current_raw_file = join(dir_dataset_raw_given_names, f)
  print(current_raw_file)

  if isfile(current_raw_file):
    current_dataset = pd.read_csv(current_raw_file)

    # Input files either have a single Name and Sex column or a column each for
    # Boy Names and Girl Names. Refactoring required if this changes at the
    # moment I'd rather not get bogged down into a smarter solution but
    # something to think about.
    if 'Name' in current_dataset.columns:
      current_dataset.apply(lambda row: collect_given_names(all_given_names_list, row['Name'], row['Sex'], current_raw_file), axis='columns')
    else:
      current_dataset.apply(lambda row: collect_given_names(all_given_names_list, row['Girl Names'], 'Female', current_raw_file), axis='columns')
      current_dataset.apply(lambda row: collect_given_names(all_given_names_list, row['Boy Names'], 'Male', current_raw_file), axis='columns')

# Uniquefy list of names and then set a subset of sexes to non-binary.
# Pending release of the ABS Article on non-binary sex based on Census 2021 data
# which is due in September 2022 I will set a random 20% of th enames to non-binary.
# https://www.abs.gov.au/articles/non-binary-sex-2021-census
unique_given_names = pd.DataFrame(all_given_names_list, columns=['name', 'sex', 'source']).drop_duplicates(subset=['name'])
unique_given_names.reset_index(drop = True, inplace = True)
unique_given_names['id'] = unique_given_names.index
mask = unique_given_names['id'] % 5 == 0
unique_given_names.loc[mask, 'sex'] = 'Non-Binary'
unique_given_names.to_csv(
    path_or_buf = join(dir_dataset_transformed, 'given_names.csv')
  , sep         = ','
  , columns     = ('id', 'name', 'sex')
  , header      = True
  , index       = False
)