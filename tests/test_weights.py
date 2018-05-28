import pytest
import numpy as np


@pytest.mark.parametrize('kind', ['cps', 'puf'])
def test_weights(kind, cps_weights, puf_weights,
                 growfactors, cps_count, puf_count,
                 cps_start_year, puf_start_year):
    # specify weights dataframe and related parameters
    if kind == 'cps':
        weights = cps_weights
        count = cps_count
        first_year = cps_start_year
    elif kind == 'puf':
        weights = puf_weights
        count = puf_count
        first_year = puf_start_year
    else:
        raise ValueError('illegal kind={}'.format(kind))
    # test count of records in weights
    if weights.shape[0] != count:
        msg = '{} weights.shape[0]={} < {}'
        raise ValueError(msg.format(kind, weights.shape[0], count))
    # test range of years in weights file
    sorted_weights_columns = sorted([col for col in weights])
    first_weights_column = sorted_weights_columns[0]
    assert first_weights_column == 'WT{}'.format(first_year)
    last_weights_column = sorted_weights_columns[-1]
    assert last_weights_column == 'WT{}'.format(growfactors.index.max())
    # test range of weight values for each year
    min_weight = 0  # weight must be non-negative,
    max_weight = 2000000  # but can be quite large
    for col in weights:
        if weights[col].min() < min_weight:
            msg = '{} weights[{}].min()={} < {}'
            raise ValueError(msg.format(kind, col,
                                        weights[col].min(), min_weight))
        if weights[col].max() > max_weight:
            msg = '{} weights[{}].max()={} > {}'
            raise ValueError(msg.format(kind, col,
                                        weights[col].max(), max_weight))
    # test sum of weights (in millions) for each year
    min_weight_sum = 150
    max_weight_sum = 200
    for col in weights:
        weight_sum = weights[col].sum() * 1e-2 * 1e-6  # in millions
        if weight_sum < min_weight_sum:
            msg = '{} weights[{}].sum()={:.1f} < {:.1f}'
            raise ValueError(msg.format(kind, col, weight_sum, max_weight_sum))
        if weight_sum > max_weight_sum:
            msg = '{} weights[{}].max()={:.1f} > {:.1f}'
            raise ValueError(msg.format(kind, col, weight_sum, max_weight_sum))
    # test that there are no weights records with a zero weight in every year
    num_nonzero_years = np.count_nonzero(weights, axis=1)
    num_total_years = num_nonzero_years.copy()
    num_total_years.fill(growfactors.index.max() - first_year + 1)
    num_allzero_years = num_total_years - num_nonzero_years
    if np.any(num_allzero_years):
        num_allzero_records = np.count_nonzero(num_allzero_years)
        txt = 'number {} records with zero weight in every year = {}'
        msg = txt.format(kind, num_allzero_records)
        if kind == 'puf' and num_allzero_records == 1:
            print('WARNING: ' + msg)
        else:
            raise ValueError(msg)