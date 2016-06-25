import pandas as pd

data_folder = 'data'

"""
Library with functions to get state level statistics from processed data files
Functions generally take (state, year) as arguments
With no year, will opportunistically find previous year
"""

def get_codes_map():
    """
    Returns a mapping from the name of a state to its 2 letter state code,
    e.g. 'California' -> 'CA'
    """
    try:
        df = pd.read_csv('%s/us_state_code_mapping.csv' %
                         data_folder, index_col='state_name', encoding='utf-8')
        df['state_code'] = df['state_code'].apply(lambda x: x.strip())
        print df.to_dict()['state_code']
        return df.to_dict()['state_code']
    except:
        import traceback
        print traceback.format_exc()
        return None

def get_gdp(state, year):
    """
    Given a state and year, returns the GDP in millions of USD
    Valid years: 2011-2015
    """
    try:
        year_col = 'gdp_%s' % str(year)
        df = pd.read_csv('%s/us_states_real_gdp_2011_2015.csv' %
                         data_folder, encoding='utf-8')
        gdp = df[df.state == state].iloc[0][year_col]
        return gdp.item()
    except:
        return None

def get_pce(state, year):
    """
    Given a state and year, returns the personal consumption expenditures in dollars
    Valid years: 2012-2014
    """
    try:
        year_col = 'pce_%s' % str(year)
        df = pd.read_csv('%s/us_states_personal_consumption_expenditures_2012_2014.csv' %
                         data_folder, encoding='utf-8')
        pce = df[df.state == state].iloc[0][year_col]
        return pce.item()
    except:
        return None
