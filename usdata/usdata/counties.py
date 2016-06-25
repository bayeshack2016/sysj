import pandas as pd

data_folder = 'data'

"""
Library with functions to get county level statistics from processed data files
Functions generally take (county, state, year) as arguments
With no year, will opportunistically find previous year
"""

def get_income(county, state, year):
    """
    Given a county, state and year, returns the per-capita income in dollars
    Valid years: 2012-2014
    Only valid for a small subset of counties and states!
    """
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


def get_population(county, state, year):
    """
    Given a county, state and year, returns the population
    Valid years: 2010-2015
    """
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

def get_fraction_above_coverage_percentile(county, state, year, percentile=85):
    """
    Given a county, state, year, and nation-wide percentile,
    returns the fraction of that county with light coverage at least that percentile
    Valid years: 2014-2016
    """
    try:
        county_col = '%s, %s' % (county, state)
        fraction_col = '%s_fraction_above_%d' % (year, percentile)
        df = pd.read_csv(
            '%s/us_counties_fraction_above_2014_2016.csv' % data_folder)
        fraction = df[df.name == county_col].iloc[0][fraction_col]
        return float(fraction.item())
    except:
        return None
