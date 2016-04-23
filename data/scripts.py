from __future__ import division
import pandas as pd

df = pd.read_csv('us_counties_pop_april2010_july2015.csv', encoding='UTF-8')
df = df[df.SUMLEV == 50]
pop_cols = [c for c in df.columns if 'POPESTIMATE' in c]
print pop_cols
def merge_popestimate(row):
  pops = row[pop_cols].tolist()
  return ','.join([str(p) for p in pops])
df['popestimate'] = df.apply(merge_popestimate, axis=1)
print df['popestimate'].head(5)
#def rate_dmig(row):
#  diff = row['DOMESTICMIG2015'] - row['DOMESTICMIG2014']
#  if row['DOMESTICMIG2014'] > 0:
#    return diff / row['DOMESTICMIG2014'] 
#  else:
#    return diff  # hack if 0
#df['rate_dmig_1415'] = df.apply(rate_dmig, axis=1)
#df_by_dmig = df.sort_values('rate_dmig_1415', ascending=False)
def rate_pop(row):
  diff = row['POPESTIMATE2015'] - row['POPESTIMATE2014']
  return diff / row['POPESTIMATE2014']
df['rate_pop_1415'] = df.apply(rate_pop, axis=1)
df_by_pop = df.sort_values('rate_pop_1415', ascending=False)
df_by_nmig = df.sort_values('RNETMIG2015', ascending=False)
print df_by_pop.head(10)  # dominated by North Dakota and Texas
print df_by_nmig.head(10) # ditto

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
