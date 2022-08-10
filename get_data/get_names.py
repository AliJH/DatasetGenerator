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
from bs4 import BeautifulSoup
from urllib.request import urlopen

dir_project_root     = 'C:\Projects\Python\DatasetGenerator'
dir_dataset_raw      = dir_project_root + '\datasets\\raw'
dir_dataset_staging  = dir_project_root + '\datasets\staging'
dir_dataset_modelled = dir_project_root + '\datasets\modelled'


### Save Raw Given Names Data To Raw ###
# Load HTML of the Top 100 Baby Names dataset. This page links to each of the
# by year dataset pages. Each of these specific by year dataset pages has a
# link to a csv version of the dataset which will download into our staging
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

  with open(dir_dataset_raw + '\given_names\\' + fn_names_current_csv, 'wb') as f:
    f.write(dataset_current_csv)


### Create Staging Dataset of Given Names With Sex ###



### Create Modelled Dataset of Popular Names ###