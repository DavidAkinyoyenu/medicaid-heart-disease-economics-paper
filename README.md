# The Effect of Medicaid Expansion on Ischaemic Heart Disease Mortality (1999 - 2019)

## 1. Project Overview
This repository documents an econometric analysis investigating the relationship between Medicaid Expansion and the mortatility rate from heart disease among US states. The study pulls data from five primary sources to create a state-year panel from 1999 to 2019 for difference-in-difference testing. 

### A. Key Insights
- Methodology: The regression was run with state and time fixed effects, along with controls for unemployment, poverty, and cigarette taxes
- Findings: While the results did not produce statistically significant effects that were distinct from zero, we were able to rule out large effects and emphasize the impact of cigarette taxes
- Limitations: Given a US population of over 300 million, the impact for the only 20 million people that recieved insurance through Expansion may not be visible at the state level.

## 2. Technical Workflow and Reproducability
This project was built for all results to be reproducable. Section A outlines the naming convention for each file, and the following sections explain the 3 core steps of this project: Data Preparation, Statistical Analysis, and Results. Each step has its respective folder as [build ](./build), blank, or blank.

### A. File Naming Convention
To maintain a structured research trail, each file starts with a two-digit number, followed by a short description. The first digit represents the section within a folder, and the second digit is the file number within that section. A small example in the Analysis folder is below.
- Example: file 23-reg_adults_45_65
    - First digit: 2 refers to section 2 within the Analysis folder, regression files
    - Second digit: 3 implies this the third file in the section
    - Description: This file is a regression for adults aged 45 to 64
- File Tree Diagram
```Plaintext
/Project_Root
├── README.md
├── Paper.pdf
│  
├── /Build
│   ├── 01-data_scrape.py
│   ├── ...    
│   └── 10-merge_adults.py
│
├── /Analysis
│   ├── 01-data_scrape.py
│   ├── ...    
│   └── 10-merge_adults.py
│  
└── /Output
    ├── 10-event_study.do
    ├── ...    
    └── 20-regression_main.do

```

### B. Data Preparation
The build file is the first folder of our analysis and details how to gather data from our five primary sources to build a state-year panel dataset from 1999 to 2019 for all 50 US states. 
- Tools: Python, DuckDB, SQL
- Process: Pull data at the state level from [CDC Wonder](https://wonder.cdc.gov/mcd.html) for crude mortatility rate, [Kaiser Family Foundation](https://www.kff.org/affordable-care-act/state-indicator/state-activity-around-expanding-medicaid-under-the-affordable-care-act/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D) for Expansion year, [Bureau of Labor Statistics](https://www.bls.gov/lau/rdscnp16.htm) for unemployment rate, [US census](https://www.census.gov/data/datasets/2024/demo/saipe/2024-state-and-county.html) for poverty rate, and the [CDC](https://healthdata.gov/CDC/The-Tax-Burden-on-Tobacco-1970-2019/etts-u9ii/about_data) for cigarette taxes.
- Data Sections:
    - Section 0: Files 00-cdc-wonder.py to 010-cdc-wonder-adults-45-64-all-cause.py are data extraction scripts
    - Section 1: Files 10-merges_US_MEN_55_64 to 17-merges_US_ADULTS_45_64_ALL_CAUSE are merge files that pull from extracted data
    - Sub folders: Raw files are in [raw](./build/raw), files in the process of being modified are in [intermediate](./build/intermediate), and final analysis-ready panel sets are in [output](./build/output)





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

in [build folder](./build)


### About the Author
- Name: *David Akinyoyenu*
- University: *MIT, class of 2027*
- Major: *6-14, Computer Science, Data Science, and Economics*
