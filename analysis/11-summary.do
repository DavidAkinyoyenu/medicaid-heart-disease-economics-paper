* Summary statistics: Heart Disease Mortality, Adults 45-64
* Requires: estout (ssc install estout)

use "/Users/davidakinyoyenu/Downloads/00 26 Spring/14.33 - Adv Econometrics/Data/Master_Build_Analysis/build/output/panel_adults_45_64_unemployment_poverty_cigarette.dta", clear

eststo clear

estpost summarize crude_rate treat_post unemployment_rate poverty_rate cigarette_tax_per_pack, detail

* --- Console preview ---
esttab, cells("mean(fmt(%9.2f)) sd(fmt(%9.2f)) min(fmt(%9.2f)) max(fmt(%9.2f))") ///
    label noobs nostar nonote ///
    collabels("Mean" "SD" "Min" "Max") ///
    title("Summary Statistics: Heart Disease Mortality, Adults 45-64")

* --- LaTeX export ---
esttab using "/Users/davidakinyoyenu/Downloads/00 26 Spring/14.33 - Adv Econometrics/Data/Master_Build_Analysis/output/table_11_summary_adults_45_64.tex", replace ///
    cells("mean(fmt(%9.2f)) sd(fmt(%9.2f)) min(fmt(%9.2f)) max(fmt(%9.2f))") ///
    label noobs nostar nonote booktabs ///
    collabels("Mean" "SD" "Min" "Max") ///
    title("Summary Statistics: Heart Disease Mortality, Adults 45--64") ///
    addnotes("Observations at the state-year level.")

* --- RTF export (Word-compatible) ---
esttab using "/Users/davidakinyoyenu/Downloads/00 26 Spring/14.33 - Adv Econometrics/Data/Master_Build_Analysis/output/table_11_summary_adults_45_64.rtf", replace ///
    cells("mean(fmt(%9.2f)) sd(fmt(%9.2f)) min(fmt(%9.2f)) max(fmt(%9.2f))") ///
    label noobs nostar nonote ///
    collabels("Mean" "SD" "Min" "Max") ///
    title("Summary Statistics: Heart Disease Mortality, Adults 45-64") ///
    addnotes("Observations at the state-year level.")
