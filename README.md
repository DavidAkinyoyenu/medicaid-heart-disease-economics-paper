# The Effect of Medicaid Expansion on Ischaemic Heart Disease Mortality (1999 - 2019)

## 1. Project Overview
This repository documents an econometric analysis investigating the relationship between Medicaid Expansion and deaths from heart disease among US states. The study pulls data from five primary sources to create a state-year panel from 1999 to 2019 for difference-in-difference testing. 

### A. Key Insights
- Methodology: The regression was run with state and time fixed effects, along with controls for unemployment, poverty, and cigarette taxes
- Findings: While the results did not produce statistically significant effects that were distinct from zero, we were able to rule out large effects and emphasize the impact of cigarette taxes
- Limitations: Given a US population of over 300 million, the impact for the only 20 million people that recieved insurance through Expansion may not be visible at the state level.

## 2. Technical Workflow and Reproducability
This project was built for all results to be reproducable. The workflow is split into 3 overall folders for Data Preparation, Statistical Analysis, and Results respectively: Data Preparation [build folder](./build), Statistical Analysis, and Results. Before explaining each folder, section A briefly explains the naming convention for each file.

### A. File Naming Convention
To maintain a structured research trail, each file starts with a two-digit number, followed by a short description. The first digit represents the section within a file, and the second digit is the file number within that section. A small example in the Analysis folder is below.
- Example: file 23-reg_adults_45_65
    - First digit: 2 refers to section 2 within the Analysis folder, regression files
    - Second digit: 3 implies this the third file in the section
    - Description: This file is a regression for adults aged 45 to 64

### B. Data Preparation
The build file is the first folder of our analysis and details how to gather data from our five primary sources to build a state-year panel dataset from 1999 to 2019 for all 50 US states. 
- Tools: Python, DuckDB, SQL
- Process: Pull data from public health and economic databases
    - 



### D. File Tree Diagram
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



### About the Author
- Name: *David Akinyoyenu*
- University: *MIT, class of 2027*
- Major: *6-14, Computer Science, Data Science, and Economics*
