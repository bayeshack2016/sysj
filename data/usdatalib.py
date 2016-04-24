import pandas as pd

# either (county, state, year) or (state, year)
# if no year, will opportunistically find previous year

# valid years: 2010-2015
def get_pop_from_county(county, state, year): 
  county = '%s County' % county
  year_col = 'POPESTIMATE%s' % str(year)
  df = pd.read_csv('us_counties_pop_april2010_july2015.csv', encoding='utf-8')
  df = df[df.SUMLEV == 50]
  pop_cols = [c for c in df.columns if 'POPESTIMATE' in c]
  county_df = df[(df.STNAME == state) & (df.CTYNAME == county)][pop_cols]
  pop = county_df.iloc[0][year_col]
  return pop.item()

# valid years: 2012-2014
def get_income_from_county(county, state, year): 
  county = '%s County' % county
  year_col = 'pcpi_%s' % str(year)
  df = pd.read_csv('us_counties_per_capita_personal_income_2012_2014_subset.csv', encoding='utf-8')
  income = df[(df.state == state) & (df.county == county)].iloc[0][year_col]
  return income.item()

def get_gdp_from_state(state, year):
  # TODO: pre-merge before finishing this
  df2015 = pd.read_csv('us_states_gdp_in_millions_of_dollars_2015_q2.csv', encoding='utf-8')
  df = pd.read_csv('us_states_real_gdp_2011_2014.csv', encoding='utf-8')

print '\nTesting...'
county = 'San Francisco'
state = 'California'
year = 2014
print get_pop_from_county(county, state, year)
print get_income_from_county(county, state, year)

