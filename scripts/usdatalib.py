import pandas as pd
import os

# library with functions to get county level statistics from processed
# data files

# either (county, state, year) or (state, year)
# if no year, will opportunistically find previous year

# dict of {state_name: state_code}, e.g. {'California': 'CA'}


def get_state_codes_map():
    try:
        df = pd.read_csv('%s/us_state_code_mapping.csv' %
                         data_folder, index_col='state_name', encoding='utf-8')
        df['state_code'] = df['state_code'].apply(lambda x: x.strip())
        return df.to_dict()['state_code']
    except:
        return None

# valid years: 2014 - 2016


def get_fraction_from_county(county, state, year, fraction=85):
    try:
        county_col = '%s, %s' % (county, state)
        fraction_col = '%s_fraction_above_%d' % (year, fraction)
        df = pd.read_csv(
            '%s/us_counties_fraction_above_2014_2016.csv' % data_folder)
        fraction = df[df.name == county_col].iloc[0][fraction_col]
        return float(fraction.item())
    except:
        return None

# valid years: 2010-2015


def get_pop_from_county(county, state, year):
    try:
        county = '%s County' % county
        year_col = 'POPESTIMATE%s' % str(year)
        df = pd.read_csv('%s/us_counties_pop_april2010_july2015.csv' %
                         data_folder, encoding='utf-8')
        df = df[df.SUMLEV == 50]
        pop_cols = [c for c in df.columns if 'POPESTIMATE' in c]
        county_df = df[(df.STNAME == state) & (df.CTYNAME == county)][pop_cols]
        pop = county_df.iloc[0][year_col]
        return pop.item()
    except:
        return None

# valid years: 2012-2014
# only valid for a small subset of counties and states!


def get_income_from_county(county, state, year):
    try:
        county = '%s County' % county
        year_col = 'pcpi_%s' % str(year)
        df = pd.read_csv('%s/us_counties_per_capita_personal_income_2012_2014_subset.csv' %
                         data_folder, encoding='utf-8')
        income = df[(df.state == state) & (
            df.county == county)].iloc[0][year_col]
        return income.item()
    except:
        return None

# valid years: 2011-2015


def get_gdp_from_state(state, year):
    try:
        year_col = 'gdp_%s' % str(year)
        df = pd.read_csv('%s/us_states_real_gdp_2011_2015.csv' %
                         data_folder, encoding='utf-8')
        gdp = df[df.state == state].iloc[0][year_col]
        return gdp.item()
    except:
        return None

# valid years: 2012-2014


def get_pce_from_state(state, year):
    try:
        year_col = 'pce_%s' % str(year)
        df = pd.read_csv('%s/us_states_personal_consumption_expenditures_2012_2014.csv' %
                         data_folder, encoding='utf-8')
        pce = df[df.state == state].iloc[0][year_col]
        return pce.item()
    except:
        return None

# Uncomment for testing:
# print '\nTesting...'
#county = 'San Francisco'
#state = 'California'
#year = 2014
# print 'Data for %s, %s in year %s:' % (county, state, year)
# print 'pop: %d' % get_pop_from_county(county, state, year)
# print 'income: %d' % get_income_from_county(county, state, year)
# print 'gdp: %d' % get_gdp_from_state(state, year)
# print 'pce: %d' % get_pce_from_state(state, year)
# print 'state codes: '
# print get_state_codes_map()
# print 'light: %0.2f' % get_fraction_from_county(county, state, year)
