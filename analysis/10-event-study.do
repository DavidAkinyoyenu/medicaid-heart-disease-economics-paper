* Event study / pre-trends test: Heart Disease Mortality, Men 55-64
* Tests parallel pre-trends and estimates dynamic treatment effects
* Requires: reghdfe, coefplot (ssc install reghdfe coefplot)

use "/Users/davidakinyoyenu/Downloads/00 26 Spring/14.33 - Adv Econometrics/Data/Master_Build_Analysis/build/output/panel_men_55_64_unemployment_poverty_cigarette.dta", clear

encode state, gen(state_id)

* --- Build relative time variable ---
* Never-expanding states have expansion_year = 3000; leave time_to_treat missing
gen time_to_treat = year - expansion_year if expansion_year < 3000

* Bin endpoints: all t <= -5 grouped as -5, all t >= 5 grouped as 5
replace time_to_treat = -5 if time_to_treat < -5 & !missing(time_to_treat)
replace time_to_treat =  5 if time_to_treat >  5 & !missing(time_to_treat)

* --- Create relative time dummies ---
* Reference period: t = -1 (year before expansion, omitted)
* Never-treated states: dummies set to 0 (they act as pure controls)
foreach k in 5 4 3 2 {
    gen rel_neg`k' = (time_to_treat == -`k')
    replace rel_neg`k' = 0 if missing(time_to_treat)
}
foreach k in 0 1 2 3 4 5 {
    gen rel_pos`k' = (time_to_treat == `k')
    replace rel_pos`k' = 0 if missing(time_to_treat)
}

* --- Event study regression ---
* Omits t = -1 (reference); includes economic + policy controls
reghdfe crude_rate ///
    rel_neg5 rel_neg4 rel_neg3 rel_neg2 ///
    rel_pos0 rel_pos1 rel_pos2 rel_pos3 rel_pos4 rel_pos5 ///
    unemployment_rate poverty_rate cigarette_tax_per_pack, ///
    absorb(state_id year) vce(cluster state_id)

* --- Coefficient plot ---
coefplot, keep(rel_neg5 rel_neg4 rel_neg3 rel_neg2 rel_pos0 rel_pos1 rel_pos2 rel_pos3 rel_pos4 rel_pos5) ///
    vertical recast(connected) ciopts(recast(rarea) fcolor(%30)) ///
    order(rel_neg5 rel_neg4 rel_neg3 rel_neg2 rel_pos0 rel_pos1 rel_pos2 rel_pos3 rel_pos4 rel_pos5) ///
    coeflabels(rel_neg5="-5" rel_neg4="-4" rel_neg3="-3" rel_neg2="-2" ///
               rel_pos0="0"  rel_pos1="1"  rel_pos2="2"  rel_pos3="3" ///
               rel_pos4="4"  rel_pos5="5") ///
    yline(0, lcolor(gray) lpattern(dash)) ///
    xline(4.5, lcolor(red) lpattern(dash)) ///
    title("Event Study: Heart Disease Mortality, Men 55-64") ///
    ytitle("Effect on crude rate (per 100k)") ///
    xtitle("Years relative to Medicaid expansion") ///
    note("Reference period: t = -1. Never-expanding states included as controls." ///
         "Endpoints binned at t = -5 and t = 5. SE clustered at state level.")

graph export "/Users/davidakinyoyenu/Downloads/00 26 Spring/14.33 - Adv Econometrics/Data/Master_Build_Analysis/output/event_study_men_55_64.png", replace width(1200)
