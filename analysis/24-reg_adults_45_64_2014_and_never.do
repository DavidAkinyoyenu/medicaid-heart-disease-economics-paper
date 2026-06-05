use "/Users/davidakinyoyenu/Downloads/00 26 Spring/14.33 - Adv Econometrics/Data/Master_Build_Analysis/build/output/panel_adults_45_64_2014_and_never_unemployment_poverty_cigarette.dta", clear

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
