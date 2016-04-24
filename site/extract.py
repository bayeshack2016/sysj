import rasterio
import numpy as np
import pandas as pd

# relative import
import data

dao = data.Data()

counties = dao.counties[:5]

def get_county_data(counties, month):
    percents = np.linspace(0, 100, 101)
    for n in counties:
        _, _, unmasked, masked, _ = dao.get_county(n, month, 'raster')
        county_name, state_name = tuple(n.split(','))
        # import pudb; pudb.set_trace()
        flat = np.array(masked[~masked.mask])
        percentiles = np.percentile(flat, percents)
        county_data = {
            'name': n,
            'county_name': county_name,
            'state_name': state_name,
        }
        for p, v in zip(percents, percentiles):
            county_data['percentile_%d' %p] = v
        yield county_data

