import usdata

county = 'San Francisco'
state = 'California'
year = 2014
print 'Data for %s, %s in year %s:' % (county, state, year)
print 'population:  %d'    % usdata.counties.get_population(county, state, year)
print 'income:      %d'    % usdata.counties.get_income(county, state, year)
print 'light:       %0.2f' % usdata.counties.get_fraction_above_coverage_percentile(county, state, year)
print 'gdp:         %d'    % usdata.states.get_gdp(state, year)
print 'pce:         %d'    % usdata.states.get_pce(state, year)
print 'state codes: %s'    % usdata.states.get_codes_map()
