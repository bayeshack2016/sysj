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
# only valid for a small subset of counties and states!
def get_income_from_county(county, state, year): 
  county = '%s County' % county
  year_col = 'pcpi_%s' % str(year)
  df = pd.read_csv('us_counties_per_capita_personal_income_2012_2014_subset.csv', encoding='utf-8')
  income = df[(df.state == state) & (df.county == county)].iloc[0][year_col]
  return income.item()

# valid years: 2011-2015
def get_gdp_from_state(state, year):
  year_col = 'gdp_%s' % str(year)
  df = pd.read_csv('us_states_real_gdp_2011_2015.csv', encoding='utf-8')
  gdp = df[df.state == state].iloc[0][year_col]
  return gdp.item()

# valid years: 2012-2014
def get_pce_from_state(state, year):
  year_col = 'pce_%s' % str(year)
  df = pd.read_csv('us_states_personal_consumption_expenditures_2012_2014.csv', encoding='utf-8')
  pce = df[df.state == state].iloc[0][year_col]
  return pce.item()


print '\nTesting...'
county = 'San Francisco'
state = 'California'
year = 2014
print 'Data for %s, %s in year %s:' % (county, state, year)
print 'pop: %d' % get_pop_from_county(county, state, year)
print 'income: %d' % get_income_from_county(county, state, year)
print 'gdp: %d' % get_gdp_from_state(state, year)
print 'pce: %d' % get_pce_from_state(state, year)
