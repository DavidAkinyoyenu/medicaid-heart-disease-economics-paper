# The Effect of Medicaid Expansion on Ischaemic Heart Disease Mortality (1999 - 2019)

## 1. Project Overview
This repository documents an econometric analysis investigating the relationship between Medicaid Expansion and the mortatility rate from heart disease in the US. The study pulls data from five primary sources to create a state-year panel from 1999 to 2019 for difference-in-difference testing. This documentation serves as a supplement to the full paper, which can be found as [Full Paper](./Full_Paper.pdf).

### A. Key Insights
- Methodology: The regression was run with state and time fixed effects, along with controls for unemployment, poverty, and cigarette taxes
- Findings: While the results did not produce statistically significant effects that were distinct from zero, we were able to rule out large effects and emphasize the impact of cigarette taxes
- Limitations: Given a US population of over 300 million, the impact for the only 20 million people that recieved insurance through Expansion may not be visible at the state level.

## 2. Technical Workflow and Reproducability
This project was built for all results to be reproducable. Section A outlines the naming convention for each file, and the following sections explain the 3 core steps of this project: Data Preparation, Statistical Analysis, and Results. Each step has its respective folder as [build ](./build), [analysis ](./analysis), or [output ](./output).

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
├── Full_Paper.pdf
│  
├── /Build
│   ├── 00-cdc-wonder.py
│   ├── ...    
│   └── 10-merge_adults.py
│
├── /Analysis
│   ├── 10-event-study.do
│   ├── ...
│   ├── 20-reg_men_55_64.do
│   ├── ... 
│   └── 30-table_men_55_64.do
│  
└── /Output
    ├── event_study_adults_45_64.png
    ├── ...
    └── table_11_summary_adults_45_64

```

### B. Data Preparation - [build ](./build)
The build folder is the first folder of our analysis and details how to gather data from our five primary sources to build a state-year panel dataset from 1999 to 2019 for all 50 US states. 
- Tools: Python, DuckDB, SQL
- Process: Pull data at the state level from [CDC Wonder](https://wonder.cdc.gov/mcd.html) for crude mortatility rate, [Kaiser Family Foundation](https://www.kff.org/affordable-care-act/state-indicator/state-activity-around-expanding-medicaid-under-the-affordable-care-act/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D) for Expansion year, [Bureau of Labor Statistics](https://www.bls.gov/lau/rdscnp16.htm) for unemployment rate, [US census](https://www.census.gov/data/datasets/2024/demo/saipe/2024-state-and-county.html) for poverty rate, and the [CDC](https://healthdata.gov/CDC/The-Tax-Burden-on-Tobacco-1970-2019/etts-u9ii/about_data) for cigarette taxes. Use DuckDB within a Python file to run SQL queries for cleaning and merging the data.
- Data Sections:
    - Section 0: Python files for data extraction into state-year format, starting with 00-cdc-wonder.py
    - Section 1: Python files that merge data files into complete state-year panels, starting with 10-merges_US_MEN_55_64.py 
    - Sub folders: Raw files are in [raw](./build/raw), files in the process of being modified are in [intermediate](./build/intermediate), and final analysis-ready panel sets are in [output](./build/output)

### C. Statistical Analysis - [analysis ](./analysis)
The analysis folder is the second folder of our analysis and details how use the completed panel data to run difference-in-difference regressions. 
- Tools: Stata
- Process: Use the completed panel data sets from the build file to run difference-in-difference regressions. Use several subgroups of adults and include/remove control variables such as unemployment and cigarette taxes. Add an event study, summary statistics, and regression tables to clearly present findings.
- Data Sections:
    - Section 1: Do files to create exproloratory event studies and summary statistics, starting with 10-event-study.do
    - Section 2: Do files to run core regression models for various demographic subgroups, starting with 20-reg_men_55_64.do
    - Section 3: Do files to generate publication-ready regression tables for each respective subset of adults in section 2, starting with 30-table_men_55_64.do

### D. Results - [output ](./output).
This final section contains the output of all regression analysis in the form of pictures for event studies and text files for summary statistics and regression tables. 


### About the Author
- Name: *David Akinyoyenu*
- University: *MIT, class of 2027*
- Major: *6-14, Computer Science, Data Science, and Economics*
