import pandas as pd

data_folder = 'data'

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

# valid years: 2011-2015
def get_gdp(state, year):
    """
    Given a state and year, returns the GDP in millions of USD
    """
    try:
        year_col = 'gdp_%s' % str(year)
        df = pd.read_csv('%s/us_states_real_gdp_2011_2015.csv' %
                         data_folder, encoding='utf-8')
        gdp = df[df.state == state].iloc[0][year_col]
        return gdp.item()
    except:
        return None

# valid years: 2012-2014
def get_pce(state, year):
    try:
        year_col = 'pce_%s' % str(year)
        df = pd.read_csv('%s/us_states_personal_consumption_expenditures_2012_2014.csv' %
                         data_folder, encoding='utf-8')
        pce = df[df.state == state].iloc[0][year_col]
        return pce.item()
    except:
        return None

# valid years: 2012-2014
# only valid for a small subset of counties and states!
def get_income(county, state, year):
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

