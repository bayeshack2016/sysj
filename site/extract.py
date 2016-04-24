import rasterio
import numpy as np
import pandas as pd
import time
import argparse
import os

# relative import
import data

def get_county_data(counties, month):
    percents = np.linspace(0, 100, 101)
    for n in counties:
        start_time = time.time()
        print 'fetching'
        _, _, unmasked, masked = dao.get_county(n, month, 'raster')
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
        print 'fetched: ' + str(time.time() - start_time)
        yield county_data

def dataframe_from_record_iter(data, length):
    first = data.next()
    df = pd.DataFrame({
        k: np.repeat(v, length) for k, v in first.iteritems()
    })
    i = 0
    for record in data:
        i += 1
        for k,v in record.iteritems():
            df.set_value(i, k, v)
    return df

def create_dataframe(counties, month):
    iter_ = get_county_data(counties, month)
    n_county = len(counties)
    return dataframe_from_record_iter(iter_, n_county)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--month", "-m", type=str,
        help="Month for which to load light data (yyyy/mm)",
        required=True
    )
    parser.add_argument(
        "--output", "-o", type=str,
        help="Path to write .csv file",
        required=True
    )
    args = parser.parse_args()
    if os.path.exists(args.output):
        raise ValueError

    dao = data.Data()
    month = args.month
    counties = dao.counties
    df = create_dataframe(counties, month)

    df.to_csv(args.output, index=False)
