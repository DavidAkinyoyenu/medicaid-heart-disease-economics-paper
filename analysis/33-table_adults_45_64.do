* DiD build-up table: Heart Disease Mortality, Adults 45-64 (Men + Women)
* Requires: reghdfe, estout (ssc install reghdfe estout)

use "/Users/davidakinyoyenu/Downloads/00 26 Spring/14.33 - Adv Econometrics/Data/Master_Build_Analysis/build/output/panel_adults_45_64_unemployment_poverty_cigarette.dta", clear
encode state, gen(state_id)

eststo clear

* (1) No FE, no controls
eststo m1: reghdfe crude_rate treat_post, noabsorb vce(cluster state_id)
estadd local state_fe "No"
estadd local year_fe  "No"

* (2) State + year FE
eststo m2: reghdfe crude_rate treat_post, absorb(state_id year) vce(cluster state_id)
estadd local state_fe "Yes"
estadd local year_fe  "Yes"

* (3) Add economic controls
eststo m3: reghdfe crude_rate treat_post unemployment_rate poverty_rate, absorb(state_id year) vce(cluster state_id)
estadd local state_fe "Yes"
estadd local year_fe  "Yes"

* (4) Add policy control
eststo m4: reghdfe crude_rate treat_post unemployment_rate poverty_rate cigarette_tax_per_pack, absorb(state_id year) vce(cluster state_id)
estadd local state_fe "Yes"
estadd local year_fe  "Yes"

* --- Console preview ---
esttab m1 m2 m3 m4, ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    label ///
    mtitles("No FE" "State+Year FE" "+Econ Controls" "+Cigarette Tax") ///
    keep(treat_post unemployment_rate poverty_rate cigarette_tax_per_pack) ///
    stats(state_fe year_fe N r2, labels("State FE" "Year FE" "Observations" "R-squared")) ///
    title("DiD: Heart Disease Mortality, Adults 45-64")

* --- LaTeX export ---
esttab m1 m2 m3 m4 using "/Users/davidakinyoyenu/Downloads/00 26 Spring/14.33 - Adv Econometrics/Data/Master_Build_Analysis/output/table_23_adults_45_64.tex", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    label booktabs ///
    mtitles("No FE" "State+Year FE" "+Econ Controls" "+Cigarette Tax") ///
    keep(treat_post unemployment_rate poverty_rate cigarette_tax_per_pack) ///
    stats(state_fe year_fe N r2, fmt(0 0 %9.0f %9.3f) labels("State FE" "Year FE" "Observations" "R-squared")) ///
    title("DiD: Heart Disease Mortality, Adults 45--64") ///
    nonotes addnotes("Standard errors clustered at the state level.")

* --- RTF export (Word-compatible) ---
esttab m1 m2 m3 m4 using "/Users/davidakinyoyenu/Downloads/00 26 Spring/14.33 - Adv Econometrics/Data/Master_Build_Analysis/output/table_23_adults_45_64.rtf", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    label ///
    mtitles("No FE" "State+Year FE" "+Econ Controls" "+Cigarette Tax") ///
    keep(treat_post unemployment_rate poverty_rate cigarette_tax_per_pack) ///
    stats(state_fe year_fe N r2, fmt(0 0 %9.0f %9.3f) labels("State FE" "Year FE" "Observations" "R-squared")) ///
    title("DiD: Heart Disease Mortality, Adults 45-64") ///
    nonotes addnotes("Standard errors clustered at the state level.")
