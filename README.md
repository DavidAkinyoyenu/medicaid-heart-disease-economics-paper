# medicaid-heart-disease-economics-paper
This repository documents how to reproduce the results from my economics paper on the effect of Medicaid Expansion on Ischemic Heart Disease

# file naming mechanism 
Each file starts with a two-digit number. The first digit represents the section in the file, and the second digit is the file number within that section. For example, in the analysis folder, 23-reg_adults_45_56 is the 2nd section for regression files and is the 3rd file in there. The full breakdown is below:

Build - Contains the Python and SQL used to scrap data from data sets or online and get them into a panel format
Note: I used DuckDB to write SQL within the python file
  01 - 010 - Python files to get state year data for 1999 to 2019 for Expansion date, unemployment, poverty, cigarette tax, and crude mortality for multiple subgroups
  10-17 - Python files that merged the data together into one panel set from all sources for a particular subgroup, such as adults 45-64
Subfiles
Raw - raw data files
Intermediate - intermediate csv and parquet files, such as poverty rate for all state year combinations
Output - csv and parquet files of full panel sets for all subgroups
Analysis - Contains .do files that were run in Stata
10-12 - Event studies and summary tables
20-27 - Regression files for all groups
30-37 - Files to create regression tables for each corresponding regression
Output - png and text files of Event studies and regression tables
Table names provide full description of which group they correspond to
