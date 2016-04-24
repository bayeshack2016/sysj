import numpy as np
import pandas as pd
import argparse
import os

# relative import
import data


def get_county_data(counties, month):
    percents = np.linspace(0, 100, 101)
    for n in counties:
        print n
        _, _, unmasked, masked, _ = dao.get_county(n, month, 'raster')
        county_name, state_name = tuple(n.split(',').strip())
        # import pudb; pudb.set_trace()
        flat = np.array(masked[~masked.mask])
        percentiles = np.percentile(flat, percents)
        county_data = {
            'name': n,
            'county_name': county_name,
            'state_name': state_name,
        }
        for p, v in zip(percents, percentiles):
            county_data['percentile_%03d' % p] = v
        yield county_data


def dataframe_from_record_iter(data, length):
    first = data.next()
    df = pd.DataFrame({
        k: np.repeat(v, length) for k, v in first.iteritems()
    })
    i = 0
    for record in data:
        i += 1
        for k, v in record.iteritems():
            df.set_value(i, k, v)
    return df


def create_dataframe(counties, month):
    iter_ = get_county_data(counties, month)
    n_county = len(counties)
    return dataframe_from_record_iter(iter_, n_county)


def add_fractions(df):
    "adds columns for fraction of pixels above percentile threshold"
    # calculate light intensity thresholds across counties

    percent_cols = filter(lambda c: c.startswith('percentile'), df.columns)
    vals = df[percent_cols].values

    percents = np.linspace(65,95,4)
    thresholds = {}
    fraction_above = {}

    for percent in percents:
        cutoff_value = np.percentile(vals, percent)
        thresholds['average_percentile_%d' % percent] = cutoff_value
        fraction_above['average_percentile_%d' % percent] = np.zeros(len(vals))

        for i in xrange(len(df)):
            county_percentiles = vals[i]
            frac_below = .01 * county_percentiles.searchsorted(cutoff_value)
            frac_above = 1.0 - frac_below
            fraction_above['average_percentile_%d' % percent][i] = frac_above

        df['fraction_above_%d' % percent] = \
            fraction_above['average_percentile_%d' % percent]
    
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
    df = create_dataframe(counties, month).set_index('name')
    add_fractions(df)
    
    df.to_csv(args.output, index=True)
