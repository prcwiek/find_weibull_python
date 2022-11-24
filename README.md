# Find Weibull

Simple program for finding the Weibull distribution parameters
k shape factor and c scale factor. Usage:<br><br>
python find_weibull.py <i>filename</i> -p<br><br>
where:<br>
<i>filename</i> is a text file from which program loads the first column with the header.<br>
<i>-p</i> parameter if plot should be preparded and saved<br><br>
python find_weibull.py data_example/WS125.txt -p<br>
python find_weibull.py -p<br>

The file <i>WS125.txt</i> with the example wind measurement data set comes
from the measurement mast US Virgin Islands St. Thomas Bovoni and
was downloaded from the site<br>
<https://midcdmz.nrel.gov/apps/sitehome.pl?site=USVILONA>.

## Information about the data set used
### Any publication based in whole or in part on these data sets should cite the data source as:
Roberts, O.; Andreas, A.; (1997). United States Virgin Islands:<br>
St. Thomas & St. Croix (Data); NREL Report No. DA-5500-64451.<br>
<http://dx.doi.org/10.7799/1183464><br>
<https://midcdmz.nrel.gov/><br><br>
Sorting function from<br>
<https://fortran-lang.discourse.group/t/modern-fortran-sample-code/2019/4>



