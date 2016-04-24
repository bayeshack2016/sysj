from __future__ import division
import pandas as pd

df = pd.read_csv('us_counties_pop_april2010_july2015.csv', encoding='utf-8')
df = df[df.SUMLEV == 50]
pop_cols = [c for c in df.columns if 'POPESTIMATE' in c]
def merge_popestimate(row):
  pops = row[pop_cols].tolist()
  return ','.join([str(p) for p in pops])
df['popestimate'] = df.apply(merge_popestimate, axis=1)
def rate_pop(row):
  diff = row['POPESTIMATE2015'] - row['POPESTIMATE2014']
  return diff / row['POPESTIMATE2014']
df['rate_pop_1415'] = df.apply(rate_pop, axis=1)
df_by_pop = df.sort_values('rate_pop_1415', ascending=False)
df_by_nmig = df.sort_values('RNETMIG2015', ascending=False)
#print df_by_pop.head(10)  # dominated by North Dakota and Texas
#print df_by_nmig.head(10) # ditto

cols = ['CTYNAME', 'STNAME', 'popestimate', 'rate_pop_1415', 'RNETMIG2015']
top_pop = df_by_pop.head(10)
print '\n=== Top 10 counties by rate of population increase from July 2014 to July 2015: ==='
print top_pop[cols]
top_nmig = df_by_nmig.head(10)
print '\n=== Top 10 counties by rate of net migration increase from July 2014 to July 2015: ==='
print top_nmig[cols]

'''
df_by_pop

SUMLEV  REGION  DIVISION  STATE  COUNTY     STNAME           CTYNAME  
50       3         7      48     301         Texas     Loving County
50       2         4      38      53  North Dakota   McKenzie County
50       2         4      38     105  North Dakota   Williams County
50       3         7      48     269         Texas       King County
50       2         4      38      61  North Dakota  Mountrail County
50       2         4      38      89  North Dakota      Stark County
50       3         7      48     461         Texas      Upton County
50       2         4      31       7      Nebraska     Banner County
50       3         7      48     229         Texas   Hudspeth County
50       3         7      48     209         Texas       Hays County
                              popestimate   rate_pop_1415
                      83,95,81,103,87,112   0.287356
          6399,7015,7969,9269,10995,12826   0.166530
      22587,24401,26710,29561,32129,35294   0.098509
                  288,258,270,272,262,282   0.076336
           7720,8105,8741,9338,9749,10331   0.059698
      24352,25165,26931,28399,30490,32154   0.054575
            3343,3286,3259,3365,3465,3651   0.053680
                  697,737,765,768,748,788   0.053476
            3464,3411,3337,3312,3211,3379   0.052320
158275,163291,168571,176114,185096,194739   0.052097

df_by_nmig

SUMLEV  REGION  DIVISION  STATE  COUNTY    STNAME  \
50       3         7     48     301         Texas
50       2         4     38      53  North Dakota
50       2         4     38     105  North Dakota
50       3         7     48     269         Texas
50       3         5     12     119       Florida
50       2         4     31       7      Nebraska
50       2         4     38      61  North Dakota
50       3         7     48     229         Texas
50       4         8      8      79      Colorado
50       4         8      8      14      Colorado

CTYNAME             CENSUS2010POP  ESTIMATESBASE2010  POPESTIMATE2010  \
    Loving County             82                 82               83
  McKenzie County           6360               6360             6399
  Williams County          22398              22398            22587
      King County            286                286              288
    Sumter County          93420              93420            94279
    Banner County            690                690              697
 Mountrail County           7673               7673             7720
  Hudspeth County           3476               3476             3464
   Mineral County            712                712              704
Broomfield County          55889              55866            56271
                            popestimate  rate_pop_1415
                    83,95,81,103,87,112       0.287356
        6399,7015,7969,9269,10995,12826       0.166530
    22587,24401,26710,29561,32129,35294       0.098509
                288,258,270,272,262,282       0.076336
94279,98581,102781,108253,114000,118891       0.042904
                697,737,765,768,748,788       0.053476
         7720,8105,8741,9338,9749,10331       0.059698
          3464,3411,3337,3312,3211,3379       0.052320
                704,711,710,721,695,726       0.044604
    56271,57445,58949,60163,61875,65065       0.051556
'''

'''
Let's focus on these counties for now:
  Loving County, TX
  McKenzie County, ND
  Williams County, ND
  King County, TX
  San Francisco, CA
They are the top 4 counties by both pop rate and net domestic migration rate from 2014 to 2015, plus SF for comparison.
'''

# Temp code to calculate percent change in pcpi from 2012 to 2014 and add that to the csv
#pcpi['perc_change_2012_2014'] = pcpi.apply(lambda r: round((r['pcpi_2014'] - r['pcpi_2012'])/r['pcpi_2012'] * 100, 1), axis=1)
#pcpi.to_csv('us_counties_per_capita_personal_income_2012_2014_subset.csv', index=False)

print '\n=== Per capita personal income in the 5 counties of interest from 2012 to 2014: ==='
pcpi = pd.read_csv('us_counties_per_capita_personal_income_2012_2014_subset.csv', encoding='utf-8')
print pcpi

# Temp code to data munge pce data
#pce = pd.read_csv('us_states_personal_consumption_expenditures_2012_2014.csv', sep='  ', engine='python')
#pce.to_csv('us_states_personal_consumption_expenditures_2012_2014.csv', sep=',', index=False)

print '\n=== Top 10 states by percent increase in personal consumption expenditures from 2013 to 2014: ==='
pce = pd.read_csv('us_states_personal_consumption_expenditures_2012_2014.csv', encoding='utf-8')
pce_by_perc_change = pce.sort_values('perc_change_2013_2014', ascending=False)
print pce_by_perc_change.head(10)

# Temp code to data munge gdp data
#gdp = pd.read_csv('us_states_percent_change_gdp_2014_2015.csv', sep='  ', engine='python')
#gdp.to_csv('us_states_percent_change_gdp_2014_2015.csv', sep=',', index=False)

print '\n=== Top 10 states by percent increase in GDP from 2014 to 2015: ==='
gdp = pd.read_csv('us_states_percent_change_gdp_2014_2015.csv', encoding='utf-8')
#gdp['gdp_2014_2015_q3'] = gdp.apply(lambda r: round((r['gdp_2015_q3'] - r['gdp_2014_q3'])/r['gdp_2014_q3'], 1), axis=1)
gdp_by_perc_change = gdp.sort_values('gdp_2015_q3', ascending=False)  # gdp_2014_2015_q3
print gdp_by_perc_change.head(10)

